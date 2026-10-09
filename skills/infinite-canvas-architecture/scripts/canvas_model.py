"""Normalize and validate an architecture scene without inferring its design."""
from copy import deepcopy
import hashlib
import json
import math
import re
import textwrap
from urllib.parse import urlsplit

KINDS={'component','authority','store','tool','entity','interface','activity','decision','state','boundary'}
SIDES={'top','bottom','left','right'}
IDENTIFIER=re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$')

def fail(message):
    raise ValueError(message)

def ident(value, label):
    if not isinstance(value,str) or not IDENTIFIER.fullmatch(value):
        fail(f'{label} must be a safe stable ID of 1–100 letters/digits/dot/underscore/hyphen')
    return value

def number(value,label,positive=False):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        fail(f'{label} must be finite')
    if abs(value)>1_000_000 or (positive and value<=0):
        fail(f'{label} is outside the supported range')
    return value

def text(value,label,limit=20_000):
    if not isinstance(value,str) or len(value)>limit or '\0' in value:
        fail(f'{label} must be bounded text')
    return value

def source(ref,known):
    if ref is None:return None
    if isinstance(ref,str):
        if ref not in known:fail(f'Unknown source reference: {ref}')
        return ref
    if not isinstance(ref,dict):fail('Source must be a declared source ID or object')
    result=deepcopy(ref)
    result['label']=text(result.get('label',result.get('id','Supplied context')),'source label',500)
    if result.get('href'):
        href=text(result['href'],'source href',4000)
        parsed=urlsplit(href)
        if parsed.scheme and parsed.scheme not in {'https','http','file'}:
            fail('Source links may not use executable/data URL schemes')
        if any(ord(c)<32 for c in href):fail('Source URL contains control characters')
    if 'note' in result:text(result['note'],'source note')
    return result

def normalize(raw):
    if not isinstance(raw,dict):fail('Scene must be an object')
    if 'schemaVersion' in raw and (type(raw['schemaVersion']) is not int or raw['schemaVersion']!=1):fail('Unsupported schemaVersion; expected 1')
    s=deepcopy(raw)
    s['schemaVersion']=1
    s['title']=text(s.get('title','Architecture atlas'),'title',240)
    s['id']=ident(s.get('id',re.sub(r'[^a-z0-9]+','-',s['title'].lower()).strip('-')[:100] or 'architecture-atlas'),'scene ID')
    s['status']=text(s.get('status','Draft architecture — assumptions and proposals are labelled'),'status',500)
    s['layoutVersion']=s.get('layoutVersion',1)
    number(s['layoutVersion'],'layoutVersion',True)
    s['sourceRevision']=text(s.get('sourceRevision',hashlib.sha256(json.dumps(raw,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:12]),'sourceRevision',200)
    s['sources']=s.get('sources',[])
    if not isinstance(s['sources'],list):fail('sources must be an array')
    known=set()
    for ref in s['sources']:
        if not isinstance(ref,dict):fail('Declared source must be an object')
        rid=ident(ref.get('id'),'source ID')
        if rid in known:fail(f'Duplicate source ID: {rid}')
        known.add(rid)
    s['sources']=[source(ref,known) for ref in s['sources']]
    bs=s.get('boards',[]);ns=s.get('nodes',[]);es=s.get('edges',[])
    if not isinstance(bs,list) or not bs:fail('At least one board is required')
    if not isinstance(ns,list) or not ns:fail('At least one semantic node is required')
    if not isinstance(es,list):fail('edges must be an array')
    if len(ns)>10_000 or len(es)>30_000:fail('Split this scene into linked atlases before rendering')
    bid={};nid={};eid=set();warnings=[]
    for i,b in enumerate(bs):
        if not isinstance(b,dict):fail('Board must be an object')
        ident(b.get('id'),'board ID')
        if b['id'] in bid:fail(f'Duplicate board ID: {b["id"]}')
        b['title']=text(b.get('title',b['id']),'board title',300)
        b['subtitle']=text(b.get('subtitle',''),'board subtitle',600)
        b['x']=number(b.get('x',60+(i%3)*2500),'board x')
        b['y']=number(b.get('y',140+(i//3)*2100),'board y')
        b['w']=number(b.get('w',2300),'board width',True)
        b['h']=number(b.get('h',1900),'board height',True)
        b['source']=source(b.get('source'),known)
        b['doc']=b.get('doc','');b['anchor']=b.get('anchor','')
        bid[b['id']]=b
    grouped={id:[] for id in bid}
    for n in ns:
        if not isinstance(n,dict):fail('Node must be an object')
        ident(n.get('id'),'node ID')
        if n['id'] in nid:fail(f'Duplicate node ID: {n["id"]}')
        n['board']=n.get('board',bs[0]['id'])
        if n['board'] not in bid:fail(f'Unknown node board: {n["board"]}')
        n['title']=text(n.get('title',n['id']),'node title',300)
        n['kind']=n.get('kind','component')
        if n['kind'] not in KINDS:fail(f'Unsupported node kind: {n["kind"]}')
        n['status']=text(n.get('status','proposed'),'node status',200)
        n['concept']=text(n.get('concept',n['id']),'concept',200)
        n['detail']=text(n.get('detail',''),'node detail')
        n['invariants']=n.get('invariants',[])
        if not isinstance(n['invariants'],list):fail('invariants must be an array')
        n['invariants']=[text(v,'invariant') for v in n['invariants']]
        n['w']=number(n.get('w',620),'node width',True)
        lines=n.get('lines',[])
        if not isinstance(lines,list):fail('lines must be an array')
        wrapped=[]
        for value in lines:
            value=text(value,'node line')
            wrapped.extend(textwrap.wrap(value,width=max(20,int((n['w']-40)/7.6)),break_long_words=False,break_on_hyphens=False) or [''])
        n['lines']=wrapped
        n['h']=number(n.get('h',max(150,94+len(wrapped)*21)),'node height',True)
        if n['h']<94+len(wrapped)*21:warnings.append(f'{n["id"]}: contract text may overflow supplied height')
        n['source']=source(n.get('source',bid[n['board']].get('source')),known)
        n['doc']=n.get('doc','');n['anchor']=n.get('anchor','')
        nid[n['id']]=n;grouped[n['board']].append(n)
    for n in ns:
        refs=n.get('references',[])
        if not isinstance(refs,list):fail('Node references must be an array')
        seen=set()
        for ref in refs:
            if not isinstance(ref,dict):fail('Node reference must be an object')
            target=ident(ref.get('target'),'reference target')
            if target not in nid:fail(f'Unknown node reference target: {target}')
            if target==n['id']:fail('Node references must point to another node')
            if target in seen:fail(f'Duplicate node reference target: {target}')
            seen.add(target)
            if 'label' in ref:text(ref['label'],'reference label',500)
        n['references']=refs
    for b in bs:
        members=grouped[b['id']];row_height=max([n['h'] for n in members]or[180])+190
        columns=max(1,min(4,int(b.get('columns',3))))
        cell_width=max([n['w'] for n in members]or[620])+150
        for i,n in enumerate(members):
            n['x']=number(n.get('x',b['x']+100+(i%columns)*cell_width),'node x')
            n['y']=number(n.get('y',b['y']+180+(i//columns)*row_height),'node y')
            if n['x']<b['x'] or n['y']<b['y'] or n['x']+n['w']>b['x']+b['w'] or n['y']+n['h']>b['y']+b['h']:
                warnings.append(f'{n["id"]}: outside its board bounds; inspect or expand the board')
    for i,e in enumerate(es):
        if not isinstance(e,dict):fail('Edge must be an object')
        for key in ['source','target']:
            if e.get(key) not in nid:fail(f'Unknown relationship {key}: {e.get(key)}')
        if 'id' not in e:
            e['id']='edge-'+hashlib.sha256(json.dumps([e['source'],e['target'],e.get('label',''),e.get('relation','dependency')]).encode()).hexdigest()[:16]
        ident(e['id'],'edge ID')
        if e['id'] in eid:fail(f'Duplicate relationship ID: {e["id"]}')
        eid.add(e['id'])
        e['board']=e.get('board',nid[e['source']]['board'])
        if e['board'] not in bid or nid[e['source']]['board']!=e['board'] or nid[e['target']]['board']!=e['board']:
            fail('Draw within-view relationships; use node references or shared concepts for cross-view navigation')
        for key,default in [('label',''),('relation','dependency'),('sourceCard',''),('targetCard',''),('note','')]:e[key]=text(e.get(key,default),'edge '+key)
        r=e.get('route')
        if not r and e['label']:
            a,z=nid[e['source']],nid[e['target']]
            gap=abs((z['x']+z['w']/2)-(a['x']+a['w']/2))-(a['w']+z['w'])/2
            if abs(a['y']-z['y'])<1 and gap>=0 and gap<len(e['label'])*9+18:
                yy=min(a['y'],z['y'])-36
                sx=a['x']+a['w']/2;tx=z['x']+z['w']/2
                e['route']=r={'sourceSide':'top','targetSide':'top','via':[[sx,yy],[tx,yy]],'label':[(sx+tx)/2,yy]}
        if r:
            if not isinstance(r,dict) or r.get('sourceSide') not in SIDES or r.get('targetSide') not in SIDES:fail('Invalid route ports')
            r.setdefault('via',[])
            if not isinstance(r['via'],list):fail('Route via must be an array')
            for point in r.get('via',[])+([r['label']] if 'label' in r else []):
                if not isinstance(point,list) or len(point)!=2:fail('Route points must be [x,y]')
                for v in point:number(v,'route coordinate')
            for key in ['sourceOffset','targetOffset','labelAngle']:
                if key in r:number(r[key],'route '+key)
    for b in bs:
        sq=b.get('sequence')
        if not sq:continue
        if not isinstance(sq,dict):fail('Sequence must be an object')
        ps=sq.get('participants',[]);ms=sq.get('messages',[])
        if not isinstance(ps,list) or not isinstance(ms,list):fail('Sequence participants and messages must be arrays')
        if len(ps)<2:fail('A sequence needs at least two participants')
        participant_ids=set()
        for p in ps:
            if not isinstance(p,dict):fail('Participant must be an object')
            ident(p.get('id'),'participant ID');text(p.get('label'),'participant label',300)
            if p['id'] in participant_ids:fail('Duplicate sequence participant ID')
            participant_ids.add(p['id'])
        for m in ms:
            if not isinstance(m,list) or len(m)!=4:fail('Sequence message is [sourceIndex,targetIndex,label,request|return]')
            if any(isinstance(v,bool) or not isinstance(v,int) or v<0 or v>=len(ps) for v in m[:2]):fail('Sequence participant index is invalid')
            if m[0]==m[1]:fail('Use an activity node for a local self-call; sequence messages need distinct participants')
            text(m[2],'sequence message');
            if m[3] not in {'request','return'}:fail('Sequence message type is invalid')
        sq['notes']=[text(v,'sequence invariant') for v in sq.get('notes',[])]
        sq['rowGap']=number(sq.get('rowGap',min(78,max(36,(b['h']-520)/max(1,len(ms)-1)))),'sequence rowGap',True)
    s['boards']=bs;s['nodes']=ns;s['edges']=es
    all_rects=bs+ns
    minx=min(v['x'] for v in all_rects)-100;miny=min(v['y'] for v in all_rects)-100
    maxx=max(v['x']+v['w'] for v in all_rects)+160;maxy=max(v['y']+v['h'] for v in all_rects)+160
    s['world']={'x':minx,'y':miny,'width':maxx-minx,'height':maxy-miny}
    if len(ns)>2000:warnings.append('Large scene: consider linked subsystem atlases for semantic and rendering clarity')
    return s,warnings

def port(n,side,offset=0):
    return {'top':(n['x']+n['w']/2+offset,n['y']),'bottom':(n['x']+n['w']/2+offset,n['y']+n['h']),
            'left':(n['x'],n['y']+n['h']/2+offset),'right':(n['x']+n['w'],n['y']+n['h']/2+offset)}[side]

def geometry(a,z,e):
    r=e.get('route')
    if r:
        start=port(a,r['sourceSide'],r.get('sourceOffset',0));end=port(z,r['targetSide'],r.get('targetOffset',0))
        points=[start,*r.get('via',[]),end]
        return {'d':'M '+' L '.join(f'{p[0]} {p[1]}' for p in points),'s':start,'t':end,'m':r.get('label',((start[0]+end[0])/2,(start[1]+end[1])/2))}
    ax,ay=a['x']+a['w']/2,a['y']+a['h']/2;zx,zy=z['x']+z['w']/2,z['y']+z['h']/2
    if abs(zx-ax)>=abs(zy-ay)*.85:
        start=(a['x']+a['w'] if zx>=ax else a['x'],ay);end=(z['x'] if zx>=ax else z['x']+z['w'],zy)
        q=max(60,abs(end[0]-start[0])*.46);direction=1 if zx>=ax else -1
        d=f'M {start[0]} {start[1]} C {start[0]+q*direction} {start[1]}, {end[0]-q*direction} {end[1]}, {end[0]} {end[1]}'
    else:
        start=(ax,a['y']+a['h'] if zy>=ay else a['y']);end=(zx,z['y'] if zy>=ay else z['y']+z['h'])
        q=max(60,abs(end[1]-start[1])*.46);direction=1 if zy>=ay else -1
        d=f'M {start[0]} {start[1]} C {start[0]} {start[1]+q*direction}, {end[0]} {end[1]-q*direction}, {end[0]} {end[1]}'
    return {'d':d,'s':start,'t':end,'m':((start[0]+end[0])/2,(start[1]+end[1])/2)}
