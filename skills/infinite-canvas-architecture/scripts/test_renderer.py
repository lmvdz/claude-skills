"""Focused invariants for the renderer/whitelist; no architecture correctness claims."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from canvas_model import normalize
from render_canvas import ASSETS,render
from serve_canvas import make_server

class CanvasTests(unittest.TestCase):
    def setUp(self):self.raw=json.loads((ASSETS/'example-scene.json').read_text(encoding='utf-8'))
    def test_references_and_sources(self):
        for mutation in [lambda s:s['nodes'].append(deepcopy(s['nodes'][0])),
                         lambda s:s['edges'][0].update(target='missing'),
                         lambda s:s['edges'][0].update(target='scope'),
                         lambda s:s['sources'][0].update(href='javascript:alert(1)'),
                         lambda s:s.update(schemaVersion=2),
                         lambda s:s['nodes'][0].update(x=float('inf'))]:
            scene=deepcopy(self.raw);mutation(scene)
            with self.assertRaises(ValueError):normalize(scene)
    def test_sequence_and_route(self):
        self.raw['boards'][0]['sequence']={'participants':[{'id':'a','label':'A'},{'id':'b','label':'B'}],'messages':[[0,1,'Call','request'],[1,0,'Receipt','return']]}
        self.raw['edges'][0]['route']={'sourceSide':'right','targetSide':'left'}
        scene,_=normalize(self.raw);self.assertEqual(scene['edges'][0]['route']['via'],[])
        self.raw['boards'][0]['sequence']['messages'][0][0]=2
        with self.assertRaises(ValueError):normalize(self.raw)
    def test_cross_board_node_references(self):
        # Existing version-1 scenes need no new fields; explicit references preserve identity.
        old,_=normalize(self.raw)
        self.assertTrue(all(n['references']==[] for n in old['nodes']))
        self.raw['nodes'][0]['references']=[{'target':'scope','label':'Decision governing retries'}]
        scene,_=normalize(self.raw)
        self.assertEqual(scene['nodes'][0]['references'],self.raw['nodes'][0]['references'])
        self.assertNotEqual(scene['nodes'][0]['concept'],scene['nodes'][5]['concept'])
        with tempfile.TemporaryDirectory() as tmp:
            render(self.raw,tmp)
            exported=json.loads((Path(tmp)/'atlas.json').read_text(encoding='utf-8'))
            self.assertEqual(exported['nodes'][0]['references'],self.raw['nodes'][0]['references'])
        for refs in [None,{},['scope'],[{}],[{'target':'missing'}],
                     [{'target':'customer'}],[{'target':'scope'},{'target':'scope'}],
                     [{'target':'scope','label':42}]]:
            with self.subTest(refs=refs):
                raw=deepcopy(self.raw);raw['nodes'][0]['references']=refs
                with self.assertRaises(ValueError):normalize(raw)
    @unittest.skipUnless(shutil.which('node'),'Node.js is needed for the inspector/controller check')
    def test_reference_navigation_controller(self):
        subprocess.run(['node',str(Path(__file__).with_name('test_viewer_references.js'))],check=True)
    def test_artifact_escape_and_collision(self):
        self.raw['title']='Example </title><script>alert(1)</script>'
        self.raw['nodes'][0]['lines']=['</script><script>alert(1)</script> & value']
        with tempfile.TemporaryDirectory() as tmp:
            result=render(self.raw,tmp,penpot_file_id='authorized-file')
            self.assertFalse(result['warnings'])
            html=(Path(tmp)/'index.html').read_text(encoding='utf-8')
            self.assertNotIn('</title><script>alert',html)
            self.assertNotIn('</script><script>alert',html)
            for svg in Path(tmp).glob('*.svg'):ET.fromstring(svg.read_text(encoding='utf-8'))
            self.assertIn('authorized-file',(Path(tmp)/'penpot-import.js').read_text(encoding='utf-8'))
            (Path(tmp)/'keep.txt').write_text('unrelated')
            render(self.raw,tmp)
            self.assertEqual((Path(tmp)/'keep.txt').read_text(),'unrelated')
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp)/'index.html').write_text('existing')
            with self.assertRaises(ValueError):render(self.raw,tmp)
            self.assertEqual((Path(tmp)/'index.html').read_text(),'existing')
    def test_loopback_whitelist(self):
        with tempfile.TemporaryDirectory() as tmp:
            render(self.raw,tmp);(Path(tmp)/'secret.txt').write_text('private')
            server=make_server(tmp);worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            base=f'http://127.0.0.1:{server.server_port}/'
            try:
                with urllib.request.urlopen(base) as response:self.assertEqual(response.status,200)
                for path in ['secret.txt','canvas-manifest.json','../secret.txt','%2e%2e/secret.txt']:
                    with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(base+path)
                    self.assertEqual(error.exception.code,404)
                with urllib.request.urlopen(urllib.request.Request(base+'atlas.svg',method='HEAD')) as response:self.assertEqual(response.read(),b'')
            finally:server.shutdown();server.server_close();worker.join()

if __name__=='__main__':unittest.main()
