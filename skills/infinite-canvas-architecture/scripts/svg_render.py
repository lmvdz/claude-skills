"""Standalone SVG rendering for normalized architecture scenes."""
from html import escape as esc
from canvas_model import geometry
PALETTE={'component':'#EEF2FF','authority':'#F3E8FF','store':'#F1F5F9','tool':'#ECFDF5','entity':'#FFFFFF','interface':'#EEF2FF','activity':'#FFFFFF','decision':'#FFF7ED','state':'#F1F5F9','boundary':'#FFF7ED'}
def render_svg(scene, selected_boards=None):
    boards=scene["boards"];nodes=scene["nodes"];edges=scene["edges"]
    byid={n["id"]:n for n in nodes}
    selected_boards=selected_boards or boards
    ids={b['id'] for b in selected_boards}
    minx=min(b['x'] for b in selected_boards)-30; miny=min(b['y'] for b in selected_boards)-30
    maxx=max(b['x']+b['w'] for b in selected_boards)+30; maxy=max(b['y']+b['h'] for b in selected_boards)+30
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{maxx-minx}" height="{maxy-miny}" viewBox="{minx} {miny} {maxx-minx} {maxy-miny}">',
      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B"/></marker><marker id="triangle" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto"><path d="M 1 1 L 11 6 L 1 11 z" fill="#FFFFFF" stroke="#64748B"/></marker></defs>',
      '<style>text{font-family:Inter,Segoe UI,Arial,sans-serif;fill:#172033} .code{font-family:Consolas,monospace} .edge{fill:none;stroke:#64748B;stroke-width:2} .muted{fill:#64748B}</style>',
      f'<rect x="{minx}" y="{miny}" width="{maxx-minx}" height="{maxy-miny}" fill="#E9EEF5"/>']
    for bb in selected_boards:
        x,y,w,h=bb['x'],bb['y'],bb['w'],bb['h']
        parts.extend([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#FFFFFF" stroke="#CBD5E1"/>',
                      f'<text x="{x+44}" y="{y+57}" font-size="32" font-weight="600">{esc(bb["title"])}</text>',
                      f'<text x="{x+44}" y="{y+94}" font-size="17" class="muted">{esc(bb["subtitle"])}</text>'])
    for e in edges:
        if e['board'] not in ids: continue
        g=geometry(byid[e['source']],byid[e['target']],e);d,s,t,m=g['d'],g['s'],g['t'],g['m']
        impl=e['relation']=='implements'
        hollow=e['relation'] in {'implements','generalization'}
        parts.append(f'<path d="{d}" class="edge" marker-end="url(#{"triangle" if hollow else "arrow"})"'+(' stroke-dasharray="8 5"' if impl else '')+'/>')
        if e['label']:
            width=min(510,max(70,len(e['label'])*9+18))
            angle=(e.get('route') or {}).get('labelAngle',0)
            parts.extend([f'<g transform="translate({m[0]} {m[1]}) rotate({angle})"><rect x="{-width/2}" y="-21" width="{width}" height="29" rx="5" fill="#FFFFFF"/>',f'<text x="0" y="0" text-anchor="middle" font-size="16">{esc(e["label"])}</text></g>'])
        for point,card,n in [(s,e['sourceCard'],byid[e['source']]),(t,e['targetCard'],byid[e['target']])]:
            if card:
                xx,yy,anchor=point[0]+10,point[1]-10,'start'
                if abs(point[0]-n['x'])<.1:xx=point[0]-10;anchor='end'
                elif abs(point[1]-n['y'])<.1:xx=point[0]+12;yy=point[1]-13
                elif abs(point[1]-(n['y']+n['h']))<.1:xx=point[0]+12;yy=point[1]+24
                parts.append(f'<text x="{xx}" y="{yy}" text-anchor="{anchor}" font-size="17" fill="#2563EB">{esc(card)}</text>')
    for n in nodes:
        if n['board'] not in ids: continue
        x,y,w,h=n['x'],n['y'],n['w'],n['h']
        fill=PALETTE[n['kind']]
        if n['kind']=='decision':
            parts.append(f'<path d="M {x+w/2} {y} L {x+w} {y+h/2} L {x+w/2} {y+h} L {x} {y+h/2} Z" fill="{fill}" stroke="#CBD5E1"/>')
            parts.append(f'<text x="{x+w/2}" y="{y+h/2-22}" text-anchor="middle" font-size="19" font-weight="600">{esc(n["title"])}</text>')
            for i,line in enumerate(n['lines']):
                parts.append(f'<text x="{x+w/2}" y="{y+h/2+5+i*21}" text-anchor="middle" font-size="14">{esc(line)}</text>')
            continue
        else: parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{2 if n["kind"] in ["entity","interface"] else 12}" fill="{fill}" stroke="#CBD5E1"/>')
        parts.append(f'<text x="{x+20}" y="{y+25}" font-size="12" class="muted">{esc(n["status"].upper())}</text>')
        parts.append(f'<text x="{x+20}" y="{y+52}" font-size="21" font-weight="600">{esc(n["title"])}</text>')
        parts.append(f'<path d="M {x+16} {y+66} H {x+w-16}" stroke="#CBD5E1"/>')
        for i,line in enumerate(n['lines']):
            parts.append(f'<text x="{x+20}" y="{y+91+i*21}" font-size="15"'+(' class="code"' if n['kind'] in ['entity','interface'] else '')+f'>{esc(line)}</text>')
    for bb in selected_boards:
        if 'sequence' not in bb: continue
        sq=bb['sequence']; xpos=[bb['x']+180+i*(bb['w']-360)/(len(sq['participants'])-1) for i in range(len(sq['participants']))]
        for i,p in enumerate(sq['participants']):
            parts.append(f'<rect x="{xpos[i]-155}" y="{bb["y"]+175}" width="310" height="70" rx="8" fill="#EEF2FF" stroke="#CBD5E1"/>')
            parts.append(f'<text x="{xpos[i]}" y="{bb["y"]+218}" font-size="20" text-anchor="middle">{esc(p["label"])}</text>')
            parts.append(f'<path d="M {xpos[i]} {bb["y"]+245} V {bb["y"]+bb["h"]-100}" class="edge" stroke-dasharray="8 8"/>')
        for i,(aa,zz,label,typ) in enumerate(sq['messages']):
            yy=bb['y']+310+i*sq['rowGap']
            parts.append(f'<path d="M {xpos[aa]} {yy} H {xpos[zz]}" class="edge" marker-end="url(#arrow)"'+(' stroke-dasharray="7 5"' if typ=='return' else '')+'/>')
            parts.append(f'<text x="{(xpos[aa]+xpos[zz])/2}" y="{yy-12}" text-anchor="middle" font-size="15">{i+1}. {esc(label)}</text>')
    parts.append('</svg>')
    return ''.join(parts)
