// Native Penpot creation; execute through the existing connected MCP plugin.
// This script never removes or replaces another design page.
const spec=__IMPORT_DATA__;
if(penpot.currentFile?.id!==spec.fileId)throw new Error('Open the specified Penpot design file before importing the atlas.');
const font=penpot.fonts.findByName('Inter');
if(!font)throw new Error('Inter must be available before creating native atlas text.');
const page=penpot.createPage();page.name=spec.scene.title;
page.setPluginData('architecture-atlas-source',spec.scene.sourceRevision);
page.setPluginData('architecture-atlas-status','building');
await penpot.openPage(page);
function rect(parent,name,x,y,w,h,fill,r=10){const s=penpot.createRectangle();s.name=name;s.x=x;s.y=y;s.resize(w,h);s.borderRadius=r;s.fills=[{fillColor:fill,fillOpacity:1}];s.strokes=[{strokeColor:'#CBD5E1',strokeWidth:1,strokeAlignment:'center'}];parent.appendChild(s);return s;}
function text(parent,name,value,x,y,w,size=15,h=26,weight='400',color='#172033',align='left'){
  const s=penpot.createText(value);if(!s)throw new Error('Unable to create native text: '+name);
  s.name=name;const variant=font.variants.find(v=>String(v.fontWeight||v.weight)===weight);font.applyToText(s,variant);
  s.fontSize=String(size);s.fontWeight=weight;s.lineHeight='1.35';s.align=align;s.x=x;s.y=y;s.resize(w,h);s.growType='fixed';s.fills=[{fillColor:color,fillOpacity:1}];parent.appendChild(s);return s;
}
function path(parent,name,d,fill=null,dashed=false){const s=penpot.createPath();s.name=name;s.d=d;s.fills=fill?[{fillColor:fill,fillOpacity:1}]:[];s.strokes=[{strokeColor:'#64748B',strokeWidth:1.8,strokeStyle:dashed?'dashed':'solid',strokeAlignment:'center'}];parent.appendChild(s);return s;}
function arrow(parent,name,p,angle,hollow=false){const len=hollow?17:12,half=hollow?9:5;const base=[p[0]-Math.cos(angle)*len,p[1]-Math.sin(angle)*len];const q=[base[0]-Math.sin(angle)*half,base[1]+Math.cos(angle)*half],r=[base[0]+Math.sin(angle)*half,base[1]-Math.cos(angle)*half];return path(parent,name,`M ${p[0]} ${p[1]} L ${q[0]} ${q[1]} L ${r[0]} ${r[1]} Z`,hollow?'#FFFFFF':'#64748B');}
const fills={component:'#EEF2FF',authority:'#F3E8FF',store:'#F1F5F9',tool:'#ECFDF5',entity:'#FFFFFF',interface:'#EFF6FF',activity:'#FFFFFF',decision:'#FFF7ED',state:'#F8FAFC',boundary:'#FFF7ED'};
const boards=[];
for(const b of spec.scene.boards){
  const native=penpot.createBoard();native.name=b.title;native.x=b.x;native.y=b.y;native.resize(b.w,b.h);native.fills=[{fillColor:'#FFFFFF',fillOpacity:1}];native.borderRadius=18;native.setPluginData('architecture-diagram',b.id);
  text(native,b.title+'/Title',b.title,b.x+44,b.y+25,b.w-88,32,48,'600');text(native,b.title+'/Scope',b.subtitle,b.x+44,b.y+75,b.w-88,17,30,'400','#64748B');
  for(const e of spec.edges.filter(e=>e.board===b.id)){
    const wire=path(native,'Relationship / '+e.label,e.geometry.d,null,['implements','generalization'].includes(e.relation));wire.setPluginData('architecture-relationship',e.id);
    arrow(native,'Relationship arrow / '+e.id,e.geometry.t,e.geometry.angle,['implements','generalization'].includes(e.relation));
    if(e.label){const width=Math.max(70,Math.min(510,e.label.length*9+18));const back=rect(native,'Relationship label background',e.geometry.m[0]-width/2,e.geometry.m[1]-22,width,30,'#FFFFFF',4);const label=text(native,'Relationship label / '+e.id,e.label,e.geometry.m[0]-width/2,e.geometry.m[1]-19,width,16,29,'400','#172033','center');if(e.labelAngle){back.rotation=e.labelAngle;label.rotation=e.labelAngle;}}
    for(const [p,card,id]of [[e.geometry.s,e.sourceCard,e.source],[e.geometry.t,e.targetCard,e.target]]){
      if(!card)continue;const n=spec.scene.nodes.find(v=>v.id===id);let x=p[0]+10,y=p[1]-25;
      if(Math.abs(p[0]-n.x)<.1)x=p[0]-60;
      else if(Math.abs(p[1]-n.y)<.1){x=p[0]+12;y=p[1]-30;}
      else if(Math.abs(p[1]-(n.y+n.h))<.1){x=p[0]+12;y=p[1]+8;}
      text(native,'Multiplicity / '+e.id+'/'+id,card,x,y,75,17,26,'500','#245ADA');
    }
  }
  for(const n of spec.scene.nodes.filter(n=>n.board===b.id)){
    const parts=[];
    if(n.kind==='decision'){
      parts.push(path(native,n.title+'/Decision',`M ${n.x+n.w/2} ${n.y} L ${n.x+n.w} ${n.y+n.h/2} L ${n.x+n.w/2} ${n.y+n.h} L ${n.x} ${n.y+n.h/2} Z`,fills[n.kind]));
      parts.push(text(native,n.title+'/Title',n.title,n.x+30,n.y+n.h/2-45,n.w-60,19,28,'600','#172033','center'));
      n.lines.forEach((l,i)=>parts.push(text(native,n.title+'/Condition '+i,l,n.x+36,n.y+n.h/2-12+i*21,n.w-72,14,24,'400','#172033','center')));
    }else{
      parts.push(rect(native,n.title+'/Shape',n.x,n.y,n.w,n.h,fills[n.kind]||fills.component,['entity','interface'].includes(n.kind)?2:12));
      parts.push(text(native,n.title+'/Status',n.status.toUpperCase(),n.x+20,n.y+10,n.w-40,12,20,'400','#64748B'));
      parts.push(text(native,n.title+'/Title',n.title,n.x+20,n.y+32,n.w-40,21,31,'600'));
      parts.push(path(native,n.title+'/Divider',`M ${n.x+16} ${n.y+66} H ${n.x+n.w-16}`));
      n.lines.forEach((l,i)=>parts.push(text(native,n.title+'/Contract '+i,l,n.x+20,n.y+73+i*21,n.w-40,15,24)));
    }
    const group=penpot.group(parts);if(group){group.name=n.title;group.setPluginData('architecture-node',n.id);group.setPluginData('architecture-concept',n.concept);group.setPluginData('architecture-contract',JSON.stringify({status:n.status,source:n.source,anchor:n.anchor,invariants:n.invariants}));native.appendChild(group);}
  }
  if(b.sequence){const sq=b.sequence,xs=sq.participants.map((p,i)=>b.x+180+i*(b.w-360)/(sq.participants.length-1));sq.participants.forEach((p,i)=>{rect(native,p.label+'/Participant',xs[i]-155,b.y+175,310,70,'#EEF2FF',8);text(native,p.label+'/Title',p.label,xs[i]-145,b.y+194,290,20,34,'500','#172033','center');path(native,p.label+'/Lifeline',`M ${xs[i]} ${b.y+245} V ${b.y+b.h-100}`,null,true);});sq.messages.forEach(([a,z,l,type],i)=>{const y=b.y+310+i*(sq.rowGap||78);path(native,'Message '+(i+1),`M ${xs[a]} ${y} H ${xs[z]}`,null,type==='return');arrow(native,'Message arrow '+(i+1),[xs[z],y],z>a?0:Math.PI);text(native,'Message label '+(i+1),(i+1)+'. '+l,Math.min(xs[a],xs[z])+8,y-31,Math.abs(xs[z]-xs[a])-16,15,27,'400','#172033','center');});}
  boards.push({id:native.id,name:native.name});
}
page.setPluginData('architecture-atlas-status','complete');
return {fileId:penpot.currentFile.id,pageId:page.id,page:page.name,boards,nodeCount:spec.scene.nodes.length,relationshipCount:spec.edges.length};
