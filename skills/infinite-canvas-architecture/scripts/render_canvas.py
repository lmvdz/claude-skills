"""Build a portable atlas from caller-authored semantic JSON; stdlib only."""
import argparse
from html import escape
import json
import math
from pathlib import Path
from canvas_model import normalize, geometry, ident
from svg_render import render_svg

ASSETS=Path(__file__).resolve().parents[1]/'assets'

def render(raw,output,overwrite=False,penpot_file_id=None):
    scene,warnings=normalize(raw)
    output=Path(output).resolve()
    manifest=output/'canvas-manifest.json'
    managed=False
    if manifest.exists():
        try:managed=json.loads(manifest.read_text(encoding='utf-8')).get('generator')=='infinite-canvas-architecture-v1'
        except (ValueError,OSError):pass
    files={'atlas.json':json.dumps(scene,ensure_ascii=False,indent=2)+'\n',
           'atlas.svg':render_svg(scene)}
    for board in scene['boards']:
        files['view-'+board['id']+'.svg']=render_svg(scene,[board])
    payload=json.dumps(scene,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    files['index.html']=(ASSETS/'viewer.template.html').read_text(encoding='utf-8').replace('__TITLE__',escape(scene['title'])).replace('__SCENE__',payload)
    if penpot_file_id:
        ident(penpot_file_id,'Penpot file ID')
        byid={n['id']:n for n in scene['nodes']};edges=[]
        for e in scene['edges']:
            g=geometry(byid[e['source']],byid[e['target']],e);t=g['t'];target=byid[e['target']]
            g['angle']=0 if abs(t[0]-target['x'])<.1 else math.pi if abs(t[0]-(target['x']+target['w']))<.1 else math.pi/2 if abs(t[1]-target['y'])<.1 else -math.pi/2
            edges.append({**e,'geometry':g,'labelAngle':(e.get('route')or{}).get('labelAngle',0)})
        data=json.dumps({'fileId':penpot_file_id,'scene':scene,'edges':edges},ensure_ascii=False,separators=(',',':'))
        files['penpot-import.js']=(ASSETS/'penpot-import.template.js').read_text(encoding='utf-8').replace('__IMPORT_DATA__',data)
    if not managed and not overwrite and any((output/name).exists() for name in [*files,'canvas-manifest.json']):
        raise ValueError('Output contains unmanaged atlas filenames; choose a task-owned directory or use --overwrite deliberately')
    output.mkdir(parents=True,exist_ok=True)
    for name,value in files.items():
        (output/name).write_text(value,encoding='utf-8')
    # The server serves only portable artifact names, not the optional import script.
    public=[name for name in files if name.endswith(('.html','.json','.svg'))]
    manifest.write_text(json.dumps({'generator':'infinite-canvas-architecture-v1','sceneId':scene['id'],'files':public},indent=2)+'\n',encoding='utf-8')
    return {'output':str(output),'boards':len(scene['boards']),'nodes':len(scene['nodes']),'relationships':len(scene['edges']),'warnings':warnings}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene',type=Path);parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--overwrite',action='store_true');parser.add_argument('--penpot-file-id')
    args=parser.parse_args()
    try:result=render(json.loads(args.scene.read_text(encoding='utf-8-sig')),args.output,args.overwrite,args.penpot_file_id)
    except (ValueError,OSError) as error:parser.exit(1,f'ERROR: {error}\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
