import * as THREE from './vendor/three.module.min.js';

const root = document.querySelector('#mouth-explorer');
const $ = selector => root.querySelector(selector);
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const treatments = {
  implant: { title: 'En ny tand, steg för steg.', description: 'Ett implantat kan ersätta en saknad tand. Följ hur implantat, distans och krona tillsammans bildar en ersättning.', link: 'tandimplantat', label: 'implantat', steps: [ ['En saknad tand', 'Ett tomrum visas där tanden saknas.'], ['Implantatet', 'En skruv av titan förankras i käkbenet. Modellen visar en förenklad genomskärning.'], ['Distansen', 'En distans kopplar samman implantatet och den kommande kronan.'], ['Kronan på plats', 'En individuellt utformad krona fästs ovanpå. Läkning och flera besök ingår vanligtvis i behandlingen.'] ] },
  crown: { title: 'Ett skydd runt din egen tand.', description: 'En krona täcker en förberedd tand. Lyft av den i modellen och se hur den omsluter tanden under.', link: 'kronor-och-broar', label: 'kronor', steps: [ ['Tanden och kronan', 'Den markerade tanden visar var en krona kan sitta.'], ['Se under kronan', 'Kronan lyfts för att visa principen: en förberedd tand finns kvar under.'], ['Kronan anpassas', 'En individuellt tillverkad krona provas och anpassas till tanden och bettet.'], ['Ett skyddande hölje', 'Kronan fästs och omsluter den förberedda tanden.'] ] },
  bridge: { title: 'En bro över mellanrummet.', description: 'En bro kan ersätta en saknad tand med stöd från intilliggande tänder. Följ hur delarna bildar en sammanhängande ersättning.', link: 'kronor-och-broar', label: 'broar', steps: [ ['En tand saknas', 'Den markerade platsen visar mellanrummet som ska ersättas.'], ['Stöd på båda sidor', 'I detta exempel förbereds granntänderna för att bära bron.'], ['Bron placeras', 'Den ersättande tanden sitter ihop med kronor på stödtänderna.'], ['En sammanhängande ersättning', 'Bron fästs. Konstruktion och antal stödtänder kan variera.'] ] },
  clean: { title: 'Kom närmare en renare tandrad.', description: 'Följ en förenklad rengöring längs tandköttskanten. De färgade beläggningarna är illustrativa, inte en analys av dina tänder.', link: 'tandhygienist', label: 'tandhygienistbehandling', steps: [ ['Beläggningar synliggörs', 'Färgade punkter visar exempel på beläggningar nära tandköttskanten.'], ['Rengöringen börjar', 'Området som bearbetas lyser upp. En tandhygienist väljer metod efter behov.'], ['Längs tandköttskanten', 'Rengöringen fortsätter runt tandraden, även där det kan vara svårt att komma åt själv.'], ['Fortsätt hemma', 'Daglig tandborstning och rengöring mellan tänderna hjälper till att förebygga nya beläggningar.'] ] },
  align: { title: 'Små förflyttningar. Ett nytt läge.', description: 'Se en illustrativ förflyttning av framtänder. I verkligheten sker tandreglering gradvis och under professionell uppföljning.', link: 'tandreglering', label: 'tandreglering', steps: [ ['Ett illustrativt utgångsläge', 'Några framtänder visas i olika positioner. Det här är ett exempel, inte en bedömning av ditt bett.'], ['Förflyttningen börjar', 'Lätta, kontrollerade krafter kan stegvis påverka tändernas position.'], ['Steg för steg', 'Tänderna närmar sig den illustrerade slutpositionen. Verklig behandling tar tid och kräver kontroller.'], ['En illustrerad slutposition', 'En retainer kan behövas för att behålla resultatet. Din tandläkare bedömer vad som är möjligt.'] ] }
};

let renderer, animationFrame;
try { initialize(); } catch (error) { showFallback('3D kunde inte starta på den här enheten. Läs om behandlingarna via länkarna nedan.'); console.warn('Dental model unavailable:', error.message); }
function showFallback(message) {
  if (animationFrame) cancelAnimationFrame(animationFrame);
  if (renderer) renderer.dispose();
  root.classList.remove('mouth-ready');
  $('#mouth-canvas').hidden = true;
  $('#mouth-fallback').hidden = false;
  $('#mouth-fallback-message').textContent = message;
  for (const selector of ['.mouth-tabs', '.mouth-toolbar', '.mouth-controls', '.mouth-drag-hint']) $(selector).hidden = true;
}
function initialize() {
  const canvas = $('#mouth-canvas');
  renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(37, 1, .1, 60);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x77877c, 2.7));
  for (const [color, intensity, position] of [[0xfff2de, 4, [4,6,7]], [0xd9f2ff, 2.5, [-5,2,3]], [0xffffff, 3, [0,4,-5]]]) {
    const light = new THREE.DirectionalLight(color, intensity); light.position.set(...position); scene.add(light);
  }
  const model = new THREE.Group(); scene.add(model);
  const records = [], picks = [], gums = [], plaques = [];
  const enamel = new THREE.MeshPhysicalMaterial({ color: 0xf5eee0, roughness: .24, metalness: 0, clearcoat: .7, clearcoatRoughness: .2 });
  const gumMaterial = new THREE.MeshPhysicalMaterial({ color: 0xb86f78, roughness: .48, clearcoat: .2, transparent: true, opacity: 1, side: THREE.DoubleSide });
  const metal = new THREE.MeshStandardMaterial({ color: 0xa8bac4, metalness: .82, roughness: .28 });
  const coreMaterial = new THREE.MeshStandardMaterial({ color: 0xd8bd83, roughness: .45 });
  const highlight = new THREE.Color(0x56ad90), hoverColor = new THREE.Color(0xd6af55), black = new THREE.Color(0x000000);
  const ivory = new THREE.Color(0xf5eee0), selectedEnamel = new THREE.Color(0x8fd9bc), hoveredEnamel = new THREE.Color(0xe5cb87);
  const sphereGeometry = new THREE.SphereGeometry(1, 20, 14);
  function toothGeometry(front) {
    const positions = [], indices = [], rings = 18, segments = 32;
    const width = front ? .205 : .25, depth = front ? .135 : .235, height = front ? .64 : .53;
    for (let j = 0; j <= rings; j++) {
      const t = j / rings;
      const profile = t < .22 ? .65 + t * 1.3 : t < .72 ? .94 + Math.sin((t-.22)*Math.PI)*.08 : Math.sqrt(Math.max(0,1-((t-.72)/.28)**2));
      for (let k = 0; k <= segments; k++) {
        const a = k / segments * Math.PI * 2;
        const superellipse = v => Math.sign(v)*Math.abs(v)**.68;
        const cusp = !front && t>.7 ? .025*Math.cos(a*4)*Math.sin((t-.7)/.3*Math.PI) : 0;
        positions.push(superellipse(Math.cos(a))*width*profile, t*height+cusp, superellipse(Math.sin(a))*depth*profile);
        if (j < rings && k < segments) { const n = j*(segments+1)+k; indices.push(n,n+segments+1,n+1,n+1,n+segments+1,n+segments+2); }
      }
    }
    const geometry = new THREE.BufferGeometry(); geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3)); geometry.setIndex(indices); geometry.computeVertexNormals(); return geometry;
  }
  const frontGeometry = toothGeometry(true), backGeometry = toothGeometry(false);
  for (const upper of [true,false]) {
    const gumPoints = [];
    for (let i = 0; i < 25; i++) { const a = (-105+i*210/24)*Math.PI/180; gumPoints.push(new THREE.Vector3(Math.sin(a)*2.05, upper ? .94 : -.94, Math.cos(a)*2.45)); }
    const gum = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(gumPoints), 80, .24, 16, false),gumMaterial.clone());model.add(gum);gums.push(gum);
    for (let i = 0; i < 16; i++) {
      const angle = (-100 + i*200/15)*Math.PI/180;
      const number = upper ? (i<8 ? 18-i : 21+i-8) : (i<8 ? 48-i : 31+i-8);
      const front = i>=5 && i<=10;
      const group = new THREE.Group(); group.position.set(Math.sin(angle)*2.05,upper ? .83 : -.83,Math.cos(angle)*2.45);group.rotation.set(0,angle,upper ? Math.PI : 0);model.add(group);
      const crown = new THREE.Mesh(front ? frontGeometry : backGeometry,enamel.clone());group.add(crown);picks.push(crown);
      const core = new THREE.Mesh(new THREE.CylinderGeometry(.12,.16,.35,20),coreMaterial);core.position.y=.17;core.visible=false;group.add(core);
      const collar = new THREE.Mesh(sphereGeometry,gum.material);collar.scale.set(.28,.14,.25);collar.position.y=-.06;group.add(collar);picks.push(collar);
      const screw = new THREE.Group();
      const shaft = new THREE.Mesh(new THREE.CylinderGeometry(.095,.065,.65,20),metal);shaft.position.y=-.23;screw.add(shaft);
      for(let j=0;j<9;j++){const thread=new THREE.Mesh(new THREE.TorusGeometry(.095,.022,6,20),metal);thread.rotation.x=Math.PI/2;thread.position.y=-.5+j*.066;screw.add(thread);}
      group.add(screw);screw.visible=false;
      const connector=new THREE.Mesh(new THREE.CylinderGeometry(.08,.11,.22,16),metal);connector.position.y=.17;connector.visible=false;group.add(connector);
      const plaqueGroup=new THREE.Group();group.add(plaqueGroup);
      for(let j=0;j<4;j++){const dot=new THREE.Mesh(sphereGeometry,new THREE.MeshStandardMaterial({color:0xc4a25c,roughness:.75,transparent:true}));dot.scale.set(.04,.03,.025);dot.position.set((j-1.5)*.075,.06,.21);plaqueGroup.add(dot);}
      plaqueGroup.visible=false;plaques.push(plaqueGroup);
      const ring=new THREE.Mesh(new THREE.TorusGeometry(.3,.018,8,40),new THREE.MeshBasicMaterial({color:0x58ac91}));ring.rotation.x=Math.PI/2;ring.position.y=.03;group.add(ring);
      const record={number,index:i,upper,front,group,crown,core,collar,screw,connector,ring,plaque:plaqueGroup,base:group.position.clone(),angle};
      crown.userData.record=record;collar.userData.record=record;records.push(record);
    }
  }
  const bridgeConnectors = new THREE.Group();model.add(bridgeConnectors);
  for(let i=0;i<2;i++){const mesh=new THREE.Mesh(new THREE.CylinderGeometry(.075,.075,1,16),enamel.clone());bridgeConnectors.add(mesh);}
  const brush=new THREE.Group();const brushHead=new THREE.Mesh(new THREE.BoxGeometry(.35,.12,.22),new THREE.MeshStandardMaterial({color:0xb9d9c9,roughness:.4}));brush.add(brushHead);
  for(let i=0;i<4;i++)for(let j=0;j<3;j++){const bristle=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,.14,5),new THREE.MeshStandardMaterial({color:0xf3f1df}));bristle.position.set((i-1.5)*.075,.11,(j-1)*.065);brush.add(bristle);}
  const handle=new THREE.Mesh(new THREE.CylinderGeometry(.04,.06,1.1,12),new THREE.MeshStandardMaterial({color:0x5c9e8a}));handle.rotation.z=Math.PI/2;handle.position.x=.65;brush.add(handle);model.add(brush);brush.visible=false;
  let selected=records.find(t=>t.number===44), hovered=null, treatment='implant', progress=0, playing=false, currentStep=-1, visible=false, animationVisible=false, contextLost=false;
  let yaw=.15,pitch=.16,radius=8.4,targetYaw=yaw,targetPitch=pitch,targetRadius=radius;
  const focus=new THREE.Vector3(0,0,.7),targetFocus=focus.clone(),raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();
  const clamp=THREE.MathUtils.clamp, smooth=t=>{t=clamp(t,0,1);return t*t*(3-2*t);};
  const stageSpan=(p,a,b)=>smooth((p-a)/(b-a));
  function setPlaying(value){playing=value;$('#mouth-play').replaceChildren(document.createTextNode(value?'Pausa animation Ⅱ':'Spela animation ▷'));$('#mouth-play').setAttribute('aria-pressed',String(value));const viewPlay=$('#mouth-view-play');viewPlay.textContent=value?'Ⅱ':'▷';viewPlay.setAttribute('aria-pressed',String(value));viewPlay.setAttribute('aria-label',value?'Pausa animation':'Spela animation');viewPlay.title=value?'Pausa animation':'Spela animation';}
  function updateCopy(){
    const data=treatments[treatment],step=Math.min(3,Math.floor(progress*4));
    if(step!==currentStep){currentStep=step;$('#mouth-step-number').textContent=`0${step+1} / 04`;$('#mouth-step-title').textContent=data.steps[step][0];$('#mouth-step-description').textContent=data.steps[step][1];}
    $('#mouth-progress').value=String(Math.floor(progress*100));$('#mouth-progress-value').textContent=`${Math.floor(progress*100)} %`;
    $('#mouth-progress').setAttribute('aria-valuetext',`${Math.floor(progress*100)} procent, ${data.steps[step][0]}`);
  }
  function bridgeNeighbours(){return records.filter(r=>r.upper===selected.upper&&Math.abs(r.index-selected.index)<=1);}
  function setSelected(record){
    // A bridge needs a supporting tooth on each side in this simplified example.
    if(treatment==='bridge'&&(record.index===0||record.index===15))record=records.find(r=>r.upper===record.upper&&r.index===(record.index===0?1:14));
    hovered=null;selected=record;$('#mouth-tooth').value=String(record.number);$('#mouth-tooth-label').textContent=`Tand ${record.number}`;
    targetFocus.copy(record.base).multiplyScalar(.28);targetFocus.y=0;targetFocus.z=Math.max(.6,targetFocus.z);
    targetYaw=clamp(record.base.x*.12,-.5,.5);targetPitch=.2;targetRadius=7.9;progress=0;currentStep=-1;setPlaying(!reducedMotion.matches);updateCopy();
  }
  function setTreatment(key){
    if(!treatments[key])return;
    treatment=key;root.dataset.treatment=key;currentStep=-1;
    for(const button of root.querySelectorAll('[data-treatment]'))button.setAttribute('aria-pressed',String(button.dataset.treatment===key));
    const data=treatments[key];$('#mouth-title').textContent=data.title;$('#mouth-description').textContent=data.description;$('#mouth-treatment-link').href=`/behandlingar/${data.link}/`;$('#mouth-treatment-link').firstChild.textContent=`Läs mer om ${data.label} `;
    for(const option of $('#mouth-tooth').options)option.disabled=key==='bridge'&&[18,28,48,38].includes(Number(option.value));
    setSelected(selected);$('#mouth-view-label').textContent=key==='implant'?'Implantat · förenklad genomskärning':'Interaktiv behandlingsmodell';
  }
  for(const button of root.querySelectorAll('.mouth-tabs button'))button.addEventListener('click',()=>setTreatment(button.dataset.treatment));
  $('#mouth-tooth').addEventListener('change',e=>setSelected(records.find(r=>r.number===Number(e.target.value))));
  for(const button of [$('#mouth-play'),$('#mouth-view-play')])button.addEventListener('click',()=>{if(progress>=1)progress=0;setPlaying(!playing);updateCopy();});
  $('#mouth-replay').addEventListener('click',()=>{progress=0;currentStep=-1;setPlaying(true);updateCopy();});
  $('#mouth-progress').addEventListener('input',e=>{progress=Number(e.target.value)/100;setPlaying(false);updateCopy();});
  function resetView(){targetYaw=.15;targetPitch=.16;targetRadius=8.4;targetFocus.set(0,0,.7);}
  for(const button of root.querySelectorAll('[data-view]'))button.addEventListener('click',()=>{const action=button.dataset.view;if(action==='left')targetYaw-=.3;if(action==='right')targetYaw+=.3;if(action==='in')targetRadius=clamp(targetRadius-.7,5,12);if(action==='out')targetRadius=clamp(targetRadius+.7,5,12);if(action==='reset')resetView();});
  function hit(event){const rect=canvas.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);raycaster.setFromCamera(pointer,camera);return raycaster.intersectObjects(picks,false).find(h=>h.object.visible&&h.object.parent.visible)?.object.userData.record||null;}
  let drag=null;
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,lastX:e.clientX,lastY:e.clientY,moved:false};});
  canvas.addEventListener('pointermove',e=>{
    if(drag){const dx=e.clientX-drag.x,dy=e.clientY-drag.y;
      if(!drag.moved&&Math.hypot(dx,dy)>7){if(e.pointerType==='touch'&&Math.abs(dy)>Math.abs(dx)){drag=null;return;}drag.moved=true;canvas.setPointerCapture(e.pointerId);}
      if(drag.moved){targetYaw-=(e.clientX-drag.lastX)*.008;targetPitch=clamp(targetPitch+(e.clientY-drag.lastY)*.006,-.55,.75);}
      drag.lastX=e.clientX;drag.lastY=e.clientY;
    }else{hovered=hit(e);canvas.style.cursor=hovered?'pointer':'grab';}
  });
  canvas.addEventListener('pointerup',e=>{if(drag&&!drag.moved){const tooth=hit(e);if(tooth)setSelected(tooth);}drag=null;if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);});
  canvas.addEventListener('pointercancel',()=>{drag=null;hovered=null;});canvas.addEventListener('pointerleave',()=>{hovered=null;if(drag&&!drag.moved)drag=null;});
  // Zoom buttons avoid trapping normal page scrolling, especially on phones.
  function resize(){const rect=$('#mouth-viewport').getBoundingClientRect();if(!rect.width||!rect.height)return;renderer.setSize(rect.width,rect.height,false);camera.aspect=rect.width/rect.height;camera.updateProjectionMatrix();}
  new ResizeObserver(resize).observe($('#mouth-viewport'));
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;},{rootMargin:'100px'}).observe(root);
  // Keep the full demonstration for when the model is actually on screen,
  // including after a selection made in the controls below it on mobile.
  new IntersectionObserver(entries=>{animationVisible=entries[0].isIntersecting&&entries[0].intersectionRatio>=.5;},{threshold:[0,.5]}).observe(canvas);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)setPlaying(false);});
  canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();contextLost=true;showFallback('3D-vyn avbröts. Ladda om sidan för att försöka igen, eller läs om behandlingarna nedan.');});
  reducedMotion.addEventListener('change',()=>setPlaying(false));
  function pose(dt){
    bridgeConnectors.visible=treatment==='bridge'&&progress>.5;
    brush.visible=treatment==='clean'&&progress>.04&&progress<.99;
    for(const gum of gums){gum.material.opacity=treatment==='implant'?.4:1;gum.material.depthWrite=treatment!=='implant';gum.material.emissive.set(treatment==='clean'?0x173e29:0x000000);gum.material.emissiveIntensity=treatment==='clean'?.15:0;}
    const neighbours=treatment==='bridge'?bridgeNeighbours():[];
    for(const r of records){
      r.group.position.copy(r.base);r.group.rotation.set(0,r.angle,r.upper?Math.PI:0);r.crown.visible=true;r.crown.position.set(0,0,0);r.crown.scale.setScalar(1);r.core.visible=false;r.screw.visible=false;r.connector.visible=false;r.plaque.visible=treatment==='clean';
      let active=r===selected;
      if(treatment==='align'){active=r.front;if(r.front){const offset=(1-stageSpan(progress,.08,.96));r.group.position.x+=Math.sin(r.index*2)*.12*offset;r.group.position.z+=Math.cos(r.index*2)*.16*offset;r.group.rotation.y+=Math.sin(r.index*3)*.3*offset;}}
      if(treatment==='implant'&&r===selected){const screwIn=stageSpan(progress,.12,.48),connectorIn=stageSpan(progress,.48,.7),crownIn=stageSpan(progress,.7,1);r.screw.visible=progress>.12;r.screw.scale.y=Math.max(.001,screwIn);r.screw.rotation.y=(1-screwIn)*Math.PI*3;r.connector.visible=progress>.48;r.connector.scale.y=Math.max(.001,connectorIn);r.crown.visible=progress>.7;r.crown.position.y=(1-crownIn)*.75+.08;r.crown.scale.setScalar(Math.max(.001,crownIn));}
      if(treatment==='crown'&&r===selected){r.core.visible=true;const lift=stageSpan(progress,.12,.4)-stageSpan(progress,.68,1);r.crown.position.y=lift*.85;r.crown.position.z=lift*.55;}
      if(treatment==='bridge'&&neighbours.includes(r)){active=true;if(r===selected){r.crown.visible=progress>.5;r.crown.position.y=(1-stageSpan(progress,.5,1))*.85;}else{r.core.visible=progress>.15;r.crown.position.y=(stageSpan(progress,.12,.4)-stageSpan(progress,.5,1))*.85;}}
      if(treatment==='clean'){
        const sweepIndex=progress*32;active=Math.abs(records.indexOf(r)-sweepIndex)<1.5;
        const remaining=1-stageSpan(progress,records.indexOf(r)/38+.04,records.indexOf(r)/38+.14);
        r.plaque.visible=remaining>.01;for(const dot of r.plaque.children)dot.material.opacity=remaining;
      }
      r.ring.visible=active||r===hovered;r.ring.material.color.copy(r===hovered?hoverColor:highlight);
      const color=r===hovered?hoverColor:active?highlight:black;
      r.crown.material.color.lerp(r===hovered?hoveredEnamel:active?selectedEnamel:ivory,reducedMotion.matches?1:Math.min(1,dt*9));
      r.crown.material.emissive.lerp(color,reducedMotion.matches?1:Math.min(1,dt*9));r.crown.material.emissiveIntensity=r===hovered?.35:.23;
      r.collar.material.emissive.lerp(treatment==='clean'?highlight:black,.12);
    }
    if(bridgeConnectors.visible){const ordered=neighbours.sort((a,b)=>a.index-b.index);for(let i=0;i<2;i++){const a=ordered[i],b=ordered[i+1],lift=(1-stageSpan(progress,.5,1))*.85,dir=selected.upper?-1:1;const start=a.group.position.clone().add(new THREE.Vector3(0,dir*(.28+lift),0)),end=b.group.position.clone().add(new THREE.Vector3(0,dir*(.28+lift),0));const connector=bridgeConnectors.children[i];connector.position.copy(start).lerp(end,.5);connector.scale.y=start.distanceTo(end);connector.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),end.sub(start).normalize());}}
    if(brush.visible){const index=clamp(Math.floor(progress*32),0,31),next=records[Math.min(31,index+1)],r=records[index];brush.position.copy(r.base).lerp(next.base,progress*32-index);brush.position.y+=r.upper?-.08:.08;brush.position.z+=.3;brush.rotation.set(0,r.angle,Math.sin(progress*180)*.1);}
  }
  let lastTime=0;
  function frame(time){
    if(contextLost)return;
    animationFrame=requestAnimationFrame(frame);const dt=Math.min(.05,(time-lastTime)/1000||.016);lastTime=time;
    if(!visible||document.hidden)return;
    if(playing&&animationVisible){progress=Math.min(1,progress+dt/14);if(progress===1)setPlaying(false);updateCopy();}
    const blend=reducedMotion.matches?1:1-Math.exp(-dt*8);yaw+=(targetYaw-yaw)*blend;pitch+=(targetPitch-pitch)*blend;radius+=(targetRadius-radius)*blend;focus.lerp(targetFocus,blend);
    const viewRadius=radius*Math.max(1,1.2/camera.aspect);
    camera.position.set(focus.x+Math.sin(yaw)*Math.cos(pitch)*viewRadius,focus.y+Math.sin(pitch)*viewRadius,focus.z+Math.cos(yaw)*Math.cos(pitch)*viewRadius);camera.lookAt(focus);pose(dt);renderer.render(scene,camera);
  }
  root.classList.add('mouth-ready');$('#mouth-fallback').hidden=true;canvas.hidden=false;
  for(const selector of ['.mouth-tabs','.mouth-toolbar','.mouth-controls','.mouth-drag-hint'])$(selector).hidden=false;
  setTreatment('implant');resize();animationFrame=requestAnimationFrame(frame);
}
