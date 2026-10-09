// Execute the real inspector functions with a small DOM harness; no browser claim.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const template=fs.readFileSync(path.join(__dirname,'../assets/viewer.template.html'),'utf8');
new vm.Script(template.slice(template.lastIndexOf('<script>')+8,template.lastIndexOf('</script>')));
const controller=template.slice(template.indexOf('function relatedButton('),template.indexOf('function selectEdge('));
const node=(id,board,references)=>({id,board,title:id,concept:id,status:'proposed',kind:'interface',lines:[],invariants:[],references});
const nodes=[node('consumer','overview',[{target:'definition',label:'Defined by <contract>'}]),node('definition','detail',[{target:'decision'}]),node('decision','detail')];
const boxes=new Map();
function box(){return{children:[],textContent:'',append(...items){this.children.push(...items);},addEventListener(type,fn){this[type]=fn;}};}
const inspector=box();inspector.classList={add(){}};
Object.defineProperty(inspector,'innerHTML',{set(value){this.markup=value;for(const id of ['relations','concepts','references'])boxes.set(id,box());}});
let focused=null,hash=null;
const context={scene:{nodes,edges:[]},byId:new Map(nodes.map(n=>[n.id,n])),boardById:new Map([['overview',{title:'Overview'}],['detail',{title:'Detail'}]]),
  inspector,selected:null,selectedEdge:null,activeBoard:null,
  document:{createElement:box,getElementById(id){if(!boxes.has(id))boxes.set(id,box());return boxes.get(id);}},
  esc:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),sourceLink:()=>'',
  focusNode:id=>{focused=id;},updateSelection(){},updateNav(){},history:{replaceState(a,b,value){hash=value;}}};
vm.createContext(context);vm.runInContext(controller,context);
context.selectNode('consumer');
assert.equal(context.selected,'consumer');assert.equal(hash,'#node=consumer');
let links=boxes.get('references').children;
assert.equal(links.length,1);assert.ok(links[0].innerHTML.includes('Defined by &lt;contract&gt;'));
links[0].click();assert.equal(focused,'definition');
context.selectNode('definition');links=boxes.get('references').children;
assert.equal(links.length,2);assert.ok(links[0].innerHTML.includes('→ References'));
links[0].click();assert.equal(focused,'decision');
assert.ok(links[1].innerHTML.includes('← Defined by'));links[1].click();assert.equal(focused,'consumer');
context.selectNode('decision');links=boxes.get('references').children;
assert.equal(links.length,1);links[0].click();assert.equal(focused,'definition');
// Old schema-1 nodes without references still render and produce no explicit links.
delete nodes[0].references;context.selectNode('consumer');
assert.equal(boxes.get('references').children.length,0);assert.equal(boxes.get('references').textContent,'No explicit references.');
console.log('Inspector reference navigation passed (outgoing, incoming, escaped labels, legacy nodes).');
