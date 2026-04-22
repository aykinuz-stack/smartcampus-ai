# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm D: 16-20)."""


def _build_elem_sci_hava_olaylari_html():
    """Hava Olayları Fabrikası — Basınç/Nem/Sıcaklık ile hava durumu oluştur."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[];
let pressure=50,humidity=50,temperature=50;
let targetWeather='',resultWeather='',showRes=0,resTime=0,applied=false;
let rainDrops=[],snowFlakes=[],lightningT=0,sunAngle=0,cloudX=0;
const WEATHERS=[
  {name:'Güneşli ☀️',emoji:'☀️',check:function(p,h,t){return h<40&&t>60}},
  {name:'Bulutlu 🌥️',emoji:'🌥️',check:function(p,h,t){return h>=40&&h<70&&t>=30&&t<=70}},
  {name:'Yağmurlu 🌧️',emoji:'🌧️',check:function(p,h,t){return h>=60&&t>=20&&t<=60}},
  {name:'Karlı ❄️',emoji:'❄️',check:function(p,h,t){return h>=55&&t<25}},
  {name:'Fırtına ⛈️',emoji:'⛈️',check:function(p,h,t){return h>=70&&(p<30||p>75)}},
  {name:'Sisli 🌫️',emoji:'🌫️',check:function(p,h,t){return h>=50&&h<75&&t>=15&&t<=40&&p>=40&&p<=65}}
];
let dragSlider=-1;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function genTarget(){
  const pool=[0,1,2,3,4,5];
  const idx=pool[Math.floor(Math.random()*pool.length)];
  targetWeather=WEATHERS[idx].name;
  resultWeather='';applied=false;showRes=0;
  pressure=30+Math.floor(Math.random()*40);
  humidity=30+Math.floor(Math.random()*40);
  temperature=30+Math.floor(Math.random()*40);
  rainDrops=[];snowFlakes=[];
}
function determineWeather(p,h,t){
  for(let i=0;i<WEATHERS.length;i++){if(WEATHERS[i].check(p,h,t))return WEATHERS[i].name}
  return 'Bulutlu 🌥️';
}
function initWeatherFx(){
  rainDrops=[];snowFlakes=[];
  if(resultWeather.includes('Yağmur')||resultWeather.includes('Fırtına')){
    for(let i=0;i<60;i++)rainDrops.push({x:380+Math.random()*300,y:Math.random()*350,sp:3+Math.random()*4})
  }
  if(resultWeather.includes('Kar')){
    for(let i=0;i<40;i++)snowFlakes.push({x:380+Math.random()*300,y:Math.random()*350,sp:1+Math.random()*2,sw:Math.random()*2})
  }
}
function sliderY(val){return 160+val*3.2}
function sliderVal(my){return Math.max(0,Math.min(100,Math.round((my-160)/3.2)))}
function drawSlider(x,val,label,clr,idx){
  ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.fillText(label,x,145);
  ctx.strokeStyle='#a78bfa40';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,160);ctx.lineTo(x,480);ctx.stroke();
  for(let i=0;i<=10;i++){const yy=160+i*32;ctx.strokeStyle='#a78bfa20';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x-8,yy);ctx.lineTo(x+8,yy);ctx.stroke()}
  const hy=sliderY(val);
  ctx.fillStyle=clr;ctx.beginPath();ctx.arc(x,hy,12,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='#fff';ctx.font='bold 12px Segoe UI';ctx.fillText(val,x,hy+4);
  ctx.fillStyle='#e9d5ff80';ctx.font='11px Segoe UI';
  if(idx===0){ctx.fillText('Düşük',x,490);ctx.fillText('Yüksek',x,155)}
  if(idx===1){ctx.fillText('Kuru',x,490);ctx.fillText('Nemli',x,155)}
  if(idx===2){ctx.fillText('Soğuk',x,490);ctx.fillText('Sıcak',x,155)}
}
function drawWeatherScene(){
  const sx=370,sy=120,sw=310,sh=370;
  const skyG=ctx.createLinearGradient(sx,sy,sx,sy+sh);
  if(resultWeather.includes('Güneş')){skyG.addColorStop(0,'#38bdf8');skyG.addColorStop(1,'#7dd3fc')}
  else if(resultWeather.includes('Kar')){skyG.addColorStop(0,'#94a3b8');skyG.addColorStop(1,'#cbd5e1')}
  else if(resultWeather.includes('Fırtına')){skyG.addColorStop(0,'#94A3B8');skyG.addColorStop(1,'#475569')}
  else if(resultWeather.includes('Sis')){skyG.addColorStop(0,'#94a3b8');skyG.addColorStop(1,'#e2e8f0')}
  else{skyG.addColorStop(0,'#64748b');skyG.addColorStop(1,'#94a3b8')}
  ctx.fillStyle=skyG;ctx.beginPath();ctx.roundRect(sx,sy,sw,sh,12);ctx.fill();
  ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.stroke();
  // ground
  ctx.fillStyle='#22c55e30';ctx.fillRect(sx,sy+sh-40,sw,40);
  if(resultWeather.includes('Güneş')){
    sunAngle+=0.02;
    const scx=sx+sw/2,scy=sy+80;
    ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(scx,scy,35,0,Math.PI*2);ctx.fill();
    for(let i=0;i<12;i++){const a=sunAngle+i*Math.PI/6;
      ctx.strokeStyle='#fbbf2480';ctx.lineWidth=3;ctx.beginPath();
      ctx.moveTo(scx+Math.cos(a)*42,scy+Math.sin(a)*42);
      ctx.lineTo(scx+Math.cos(a)*58,scy+Math.sin(a)*58);ctx.stroke()}
  }
  if(resultWeather.includes('Bulut')||resultWeather.includes('Yağmur')||resultWeather.includes('Fırtına')){
    cloudX+=0.3;
    for(let i=0;i<3;i++){const cx=sx+60+i*100+(cloudX%20),cy=sy+50+i*30;
      ctx.fillStyle='#cbd5e1';ctx.beginPath();ctx.arc(cx,cy,25,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(cx+20,cy-8,20,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(cx+35,cy,22,0,Math.PI*2);ctx.fill()}
  }
  rainDrops.forEach(d=>{d.y+=d.sp;if(d.y>sy+sh-40){d.y=sy;d.x=380+Math.random()*290}
    ctx.strokeStyle='#60a5fa';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(d.x-1,d.y+10);ctx.stroke()});
  snowFlakes.forEach(s=>{s.y+=s.sp;s.x+=Math.sin(s.sw+=0.02)*0.5;
    if(s.y>sy+sh-40){s.y=sy;s.x=380+Math.random()*290}
    ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(s.x,s.y,3,0,Math.PI*2);ctx.fill()});
  if(resultWeather.includes('Fırtına')&&Math.random()<0.03){lightningT=10}
  if(lightningT>0){lightningT--;ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;ctx.beginPath();
    const lx=sx+80+Math.random()*150;ctx.moveTo(lx,sy+20);ctx.lineTo(lx+10,sy+80);ctx.lineTo(lx-5,sy+130);ctx.lineTo(lx+15,sy+200);ctx.stroke()}
  if(resultWeather.includes('Sis')){for(let i=0;i<5;i++){ctx.fillStyle='rgba(226,232,240,'+(0.15+i*0.05)+')';
    ctx.fillRect(sx,sy+100+i*50,sw,30)}}
  if(!applied){ctx.fillStyle='#e9d5ff60';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Kontrolleri ayarla',sx+sw/2,sy+sh/2);ctx.fillText('ve Uygula!',sx+sw/2,sy+sh/2+30)}
  else{ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(resultWeather,sx+sw/2,sy+sh-10)}
}
function draw(){
  ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🌦️ Hava Olayları Fabrikası',W/2,180);ctx.font='18px Segoe UI';
    ctx.fillText('Kontrolleri ayarlayarak hedef havayı oluştur!',W/2,220);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,280,160,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,312);return}
  if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🌦️ Hava Bilimci!',W/2,200);ctx.font='22px Segoe UI';
    ctx.fillText('Puan: '+score+'/'+maxR*10,W/2,250);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,300,180,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,332);return}
  // HUD
  ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,25);
  // Target
  ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Hedef: '+targetWeather,30,55);
  // Hint
  ctx.fillStyle='#e9d5ff80';ctx.font='13px Segoe UI';ctx.textAlign='left';
  const hints={'Güneşli ☀️':'Nem düşük, sıcaklık yüksek','Bulutlu 🌥️':'Nem orta, sıcaklık orta','Yağmurlu 🌧️':'Nem yüksek, sıcaklık orta',
    'Karlı ❄️':'Nem yüksek, sıcaklık çok düşük','Fırtına ⛈️':'Nem çok yüksek, basınç aşırı','Sisli 🌫️':'Nem orta-yüksek, sıcaklık düşük-orta'};
  ctx.fillText('İpucu: '+(hints[targetWeather]||''),30,80);
  // Sliders
  drawSlider(80,pressure,'Basınç','#ef4444',0);
  drawSlider(180,humidity,'Nem','#3b82f6',1);
  drawSlider(280,temperature,'Sıcaklık','#f59e0b',2);
  // Apply button
  ctx.fillStyle=applied?'#6b7280':'#10b981';ctx.beginPath();ctx.roundRect(50,520,260,45,10);ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
  ctx.fillText(applied?'Uygulandı!':'Uygula! 🌤️',180,550);
  // Weather scene
  drawWeatherScene();
  // Result feedback
  if(showRes>0){
    ctx.fillStyle=showRes===1?'#10b981':'#ef4444';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';
    ctx.fillText(showRes===1?'✓ Doğru! +10':'✗ Yanlış!',W/2,610)
  }
  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}
function upd(){
  if(showRes>0&&Date.now()-resTime>1200){showRes=0;round++;if(round>maxR){state='win'}else{genTarget()}}
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
  draw();requestAnimationFrame(upd);
}
function handleDown(mx,my){
  if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>280&&my<330){state='play';score=0;round=1;genTarget()}return}
  if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';score=0;round=1;genTarget()}return}
  if(showRes>0)return;
  // Check slider handles
  if(Math.abs(mx-80)<20&&my>150&&my<490)dragSlider=0;
  else if(Math.abs(mx-180)<20&&my>150&&my<490)dragSlider=1;
  else if(Math.abs(mx-280)<20&&my>150&&my<490)dragSlider=2;
  // Apply button
  else if(mx>50&&mx<310&&my>520&&my<565&&!applied){
    applied=true;
    resultWeather=determineWeather(pressure,humidity,temperature);
    initWeatherFx();
    if(resultWeather===targetWeather){score+=10;snd(true);addP(W/2,550,'#10b981');showRes=1}
    else{snd(false);addP(W/2,550,'#ef4444');showRes=2}
    resTime=Date.now();
  }
}
function handleMove(mx,my){
  if(dragSlider===0)pressure=sliderVal(my);
  else if(dragSlider===1)humidity=sliderVal(my);
  else if(dragSlider===2)temperature=sliderVal(my);
}
function handleUp(){dragSlider=-1}
cv.addEventListener('mousedown',e=>{const r=cv.getBoundingClientRect();handleDown((e.clientX-r.left)*(W/r.width),(e.clientY-r.top)*(H/r.height))});
cv.addEventListener('mousemove',e=>{if(dragSlider<0)return;const r=cv.getBoundingClientRect();handleMove((e.clientX-r.left)*(W/r.width),(e.clientY-r.top)*(H/r.height))});
cv.addEventListener('mouseup',handleUp);
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=cv.getBoundingClientRect();handleDown((t.clientX-r.left)*(W/r.width),(t.clientY-r.top)*(H/r.height))});
cv.addEventListener('touchmove',e=>{e.preventDefault();if(dragSlider<0)return;const t=e.touches[0];const r=cv.getBoundingClientRect();handleMove((t.clientX-r.left)*(W/r.width),(t.clientY-r.top)*(H/r.height))});
cv.addEventListener('touchend',e=>{e.preventDefault();handleUp()});
upd();
</script></body></html>"""


def _build_elem_sci_besin_zinciri_html():
    """Besin Zinciri Kur — Organizmaları doğru sıraya yerleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[];
const CHAINS=[
  {eco:'Kara (Çayır)',bg:'#22c55e',items:[
    {emoji:'🌿',name:'Ot',role:0},{emoji:'🐇',name:'Tavşan',role:1},{emoji:'🦊',name:'Tilki',role:2},{emoji:'🍄',name:'Mantar',role:3}]},
  {eco:'Deniz',bg:'#0ea5e9',items:[
    {emoji:'🦠',name:'Plankton',role:0},{emoji:'🐟',name:'Küçük Balık',role:1},{emoji:'🦈',name:'Büyük Balık',role:2},{emoji:'🧫',name:'Bakteri',role:3}]},
  {eco:'Orman',bg:'#15803d',items:[
    {emoji:'🌱',name:'Bitki',role:0},{emoji:'🦗',name:'Çekirge',role:1},{emoji:'🐸',name:'Kurbağa',role:2},{emoji:'🐍',name:'Yılan',role:3}]},
  {eco:'Göl',bg:'#0284c7',items:[
    {emoji:'🌾',name:'Su Yosunu',role:0},{emoji:'🐛',name:'Larva',role:1},{emoji:'🐠',name:'Balık',role:2},{emoji:'🦅',name:'Balıkçıl',role:3}]},
  {eco:'Kutup',bg:'#94a3b8',items:[
    {emoji:'🌿',name:'Yosun',role:0},{emoji:'🐟',name:'Balık',role:1},{emoji:'🦭',name:'Fok',role:2},{emoji:'🐻‍❄️',name:'Kutup Ayısı',role:3}]},
  {eco:'Savan',bg:'#ca8a04',items:[
    {emoji:'🌾',name:'Çimen',role:0},{emoji:'🦌',name:'Geyik',role:1},{emoji:'🦁',name:'Aslan',role:2},{emoji:'🪱',name:'Solucan',role:3}]},
  {eco:'Çöl',bg:'#d97706',items:[
    {emoji:'🌵',name:'Kaktüs',role:0},{emoji:'🦎',name:'Kertenkele',role:1},{emoji:'🦅',name:'Kartal',role:2},{emoji:'🦠',name:'Bakteri',role:3}]},
  {eco:'Tropik Orman',bg:'#059669',items:[
    {emoji:'🌳',name:'Ağaç',role:0},{emoji:'🐒',name:'Maymun',role:1},{emoji:'🐆',name:'Jaguar',role:2},{emoji:'🍄',name:'Mantar',role:3}]},
  {eco:'Tatlı Su',bg:'#0891b2',items:[
    {emoji:'🌿',name:'Su Bitkisi',role:0},{emoji:'🐌',name:'Salyangoz',role:1},{emoji:'🐢',name:'Kaplumbağa',role:2},{emoji:'🧫',name:'Ayrıştırıcı',role:3}]},
  {eco:'Dağ',bg:'#4b5563',items:[
    {emoji:'🌱',name:'Ot',role:0},{emoji:'🐐',name:'Dağ Keçisi',role:1},{emoji:'🦅',name:'Kartal',role:2},{emoji:'🪱',name:'Solucan',role:3}]}
];
const ROLE_NAMES=['Üretici','1. Tüketici','2. Tüketici','Ayrıştırıcı'];
let curChain=null,cards=[],slots=[null,null,null,null],dragIdx=-1,dragOX=0,dragOY=0;
let showRes=0,resTime=0,arrowAnim=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function genRound(){
  curChain=CHAINS[round<=CHAINS.length?round-1:(round-1)%CHAINS.length];
  cards=[];slots=[null,null,null,null];showRes=0;
  const shuffled=[...curChain.items];
  for(let i=shuffled.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]]}
  const startX=80,gap=155;
  shuffled.forEach((it,i)=>{cards.push({emoji:it.emoji,name:it.name,role:it.role,x:startX+i*gap,y:80,w:130,h:70,placed:-1})});
}
function slotX(i){return 40+i*170}
function draw(){
  ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🔗 Besin Zinciri Kur',W/2,180);ctx.font='18px Segoe UI';
    ctx.fillText('Canlıları doğru sıraya yerleştir!',W/2,220);
    ctx.font='14px Segoe UI';ctx.fillStyle='#c084fc';
    ctx.fillText('Üretici → 1. Tüketici → 2. Tüketici → Ayrıştırıcı',W/2,260);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,290,160,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,322);return}
  if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🔗 Ekoloji Uzmanı!',W/2,200);ctx.font='22px Segoe UI';
    ctx.fillText('Puan: '+score+'/'+maxR*10,W/2,250);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,300,180,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,332);return}
  // HUD
  ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,25);
  // Ecosystem label
  ctx.fillStyle=curChain.bg;ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Ekosistem: '+curChain.eco,30,55);
  // Ecosystem background band
  ctx.fillStyle=curChain.bg+'20';ctx.fillRect(0,350,W,250);
  // Slot positions
  for(let i=0;i<4;i++){
    const sx=slotX(i),sy=420;
    ctx.fillStyle='#1e1b4b';ctx.strokeStyle=slots[i]!==null?'#10b981':'#a78bfa';ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(sx,sy,150,90,10);ctx.fill();ctx.stroke();
    ctx.fillStyle='#a78bfa';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';
    ctx.fillText(ROLE_NAMES[i],sx+75,sy-8);
    if(slots[i]!==null){
      const c=cards[slots[i]];
      ctx.fillStyle='#34d399';ctx.font='28px Segoe UI';ctx.fillText(c.emoji,sx+75,sy+40);
      ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.fillText(c.name,sx+75,sy+65);
    }
    // Arrows between slots
    if(i<3){
      arrowAnim+=0.001;
      const ax=sx+155,ay=sy+45;
      ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';
      ctx.fillText('→',ax,ay);
      if(slots[i]!==null&&slots[i+1]!==null){
        ctx.strokeStyle='#fbbf2460';ctx.lineWidth=2;ctx.beginPath();
        ctx.moveTo(ax-10,ay-15);ctx.lineTo(ax+10,ay-15);ctx.stroke();
      }
    }
  }
  // Cards (unplaced)
  cards.forEach((c,i)=>{
    if(c.placed>=0)return;
    if(i===dragIdx)return;
    ctx.fillStyle='#312e81';ctx.strokeStyle=COLORS[i%COLORS.length];ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(c.x,c.y,c.w,c.h,10);ctx.fill();ctx.stroke();
    ctx.fillStyle='#fff';ctx.font='26px Segoe UI';ctx.textAlign='center';ctx.fillText(c.emoji,c.x+c.w/2,c.y+32);
    ctx.fillStyle='#e9d5ff';ctx.font='bold 13px Segoe UI';ctx.fillText(c.name,c.x+c.w/2,c.y+55);
  });
  // Dragged card
  if(dragIdx>=0){
    const c=cards[dragIdx];
    ctx.globalAlpha=0.8;ctx.fillStyle='#4c1d95';ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;
    ctx.beginPath();ctx.roundRect(c.x,c.y,c.w,c.h,10);ctx.fill();ctx.stroke();
    ctx.globalAlpha=1;ctx.fillStyle='#fff';ctx.font='26px Segoe UI';ctx.textAlign='center';ctx.fillText(c.emoji,c.x+c.w/2,c.y+32);
    ctx.fillStyle='#fbbf24';ctx.font='bold 13px Segoe UI';ctx.fillText(c.name,c.x+c.w/2,c.y+55);
  }
  // Result
  if(showRes>0){ctx.fillStyle=showRes===1?'#10b981':'#ef4444';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';
    ctx.fillText(showRes===1?'✓ Doğru Zincir! +10':'✗ Yanlış sıra!',W/2,600)}
  // Check button
  const allPlaced=slots.every(s=>s!==null);
  if(allPlaced&&showRes===0){
    ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-80,555,160,40,10);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Kontrol Et ✓',W/2,582);
  }
  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}
function checkChain(){
  let correct=true;
  for(let i=0;i<4;i++){if(slots[i]===null||cards[slots[i]].role!==i){correct=false;break}}
  if(correct){score+=10;snd(true);addP(W/2,560,'#10b981');showRes=1}
  else{snd(false);addP(W/2,560,'#ef4444');showRes=2;
    // bounce back wrong ones
    for(let i=0;i<4;i++){if(slots[i]!==null&&cards[slots[i]].role!==i){
      const ci=slots[i];cards[ci].placed=-1;
      const idx2=cards.filter(c2=>c2.placed<0).length-1;
      cards[ci].x=80+idx2*155;cards[ci].y=80;slots[i]=null}}
  }
  resTime=Date.now();
}
function upd(){
  if(showRes===1&&Date.now()-resTime>1200){showRes=0;round++;if(round>maxR)state='win';else genRound()}
  if(showRes===2&&Date.now()-resTime>1200){showRes=0}
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
  draw();requestAnimationFrame(upd);
}
function getPos(e){const r=cv.getBoundingClientRect();
  const raw=e.touches?e.touches[0]:e;
  return{x:(raw.clientX-r.left)*(W/r.width),y:(raw.clientY-r.top)*(H/r.height)}}
function handleDown(mx,my){
  if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<340){state='play';score=0;round=1;genRound()}return}
  if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';score=0;round=1;genRound()}return}
  if(showRes>0)return;
  // Check button
  const allPlaced=slots.every(s=>s!==null);
  if(allPlaced&&mx>W/2-80&&mx<W/2+80&&my>555&&my<595){checkChain();return}
  // Pick up from slot
  for(let i=0;i<4;i++){const sx=slotX(i),sy=420;
    if(slots[i]!==null&&mx>sx&&mx<sx+150&&my>sy&&my<sy+90){
      dragIdx=slots[i];cards[dragIdx].placed=-1;slots[i]=null;
      dragOX=mx-cards[dragIdx].x;dragOY=my-cards[dragIdx].y;return}}
  // Pick up card
  for(let i=cards.length-1;i>=0;i--){const c=cards[i];
    if(c.placed>=0)continue;
    if(mx>c.x&&mx<c.x+c.w&&my>c.y&&my<c.y+c.h){dragIdx=i;dragOX=mx-c.x;dragOY=my-c.y;return}}
}
function handleMove(mx,my){if(dragIdx<0)return;cards[dragIdx].x=mx-dragOX;cards[dragIdx].y=my-dragOY}
function handleUp(mx,my){
  if(dragIdx<0)return;
  const c=cards[dragIdx];
  let placed=false;
  for(let i=0;i<4;i++){const sx=slotX(i),sy=420;
    if(c.x+c.w/2>sx&&c.x+c.w/2<sx+150&&c.y+c.h/2>sy&&c.y+c.h/2<sy+90&&slots[i]===null){
      slots[i]=dragIdx;c.placed=i;placed=true;snd(true);break}}
  if(!placed){
    const unplaced=cards.filter((cc,ii)=>cc.placed<0&&ii!==dragIdx).length;
    c.x=80+unplaced*155;c.y=80;c.placed=-1;
  }
  dragIdx=-1;
}
cv.addEventListener('mousedown',e=>{const p=getPos(e);handleDown(p.x,p.y)});
cv.addEventListener('mousemove',e=>{const p=getPos(e);handleMove(p.x,p.y)});
cv.addEventListener('mouseup',e=>{const p=getPos(e);handleUp(p.x,p.y)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const p=getPos(e);handleDown(p.x,p.y)});
cv.addEventListener('touchmove',e=>{e.preventDefault();const p=getPos(e);handleMove(p.x,p.y)});
cv.addEventListener('touchend',e=>{e.preventDefault();const r=cv.getBoundingClientRect();
  const lt=e.changedTouches[0];handleUp((lt.clientX-r.left)*(W/r.width),(lt.clientY-r.top)*(H/r.height))});
upd();
</script></body></html>"""


def _build_elem_sci_insan_vucudu_html():
    """İnsan Vücudu Görevleri — Dolaşım/Solunum/Sindirim mini oyunları."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[];
let mode='A',showRes=0,resTime=0;
// Mode A - Circulation
let heartBeat=0,heartPhase=0,heartTimer=0,heartTarget=0,heartClicks=0,heartScore=0;
let bloodCells=[{x:350,y:300,angle:0}];
let heartScale=1,lastBeatTime=0,beatInterval=0,targetBPM=0,rhythmBar=0;
// Mode B - Breathing
let breathPhase='in',breathTimer=0,lungScale=0.5,o2Particles=[],co2Particles=[];
let breathSequence=[],breathTarget=[],breathIdx=0;
// Mode C - Digestion
let foodEmoji='🍎',foodName='Elma',digestStage=0,digestHighlight=-1;
let digestOrgans=['Ağız','Yemek Borusu','Mide','İnce Bağırsak','Kalın Bağırsak'];
let digestInfo=['Yiyeceği çiğner ve parçalar','Yiyeceği mideye taşır','Asitle parçalar','Besinleri emer','Suyu emer, atıkları oluşturur'];
let digestClicked=[false,false,false,false,false];
let foodY=0,foodTargetY=0;
const FOODS=[{e:'🍎',n:'Elma'},{e:'🍞',n:'Ekmek'},{e:'🥕',n:'Havuç'},{e:'🍌',n:'Muz'},{e:'🧀',n:'Peynir'},{e:'🍚',n:'Pilav'}];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function getMode(r){if(r<=3)return'A';if(r<=6)return'B';if(r<=9)return'C';return['A','B','C'][Math.floor(Math.random()*3)]}
function initRound(){
  mode=getMode(round);showRes=0;
  if(mode==='A'){
    targetBPM=60+round*5;beatInterval=60000/targetBPM;heartClicks=0;heartScore=0;lastBeatTime=0;
    rhythmBar=50;heartScale=1;heartPhase=0;
    bloodCells=[];for(let i=0;i<8;i++)bloodCells.push({x:0,y:0,angle:i*Math.PI/4,speed:0.02+Math.random()*0.01});
  }
  if(mode==='B'){
    breathPhase='wait';breathTimer=0;lungScale=0.5;breathIdx=0;
    o2Particles=[];co2Particles=[];
    breathTarget=[];
    for(let i=0;i<6;i++)breathTarget.push(i%2===0?'in':'out');
    breathSequence=[];
  }
  if(mode==='C'){
    const f=FOODS[Math.floor(Math.random()*FOODS.length)];
    foodEmoji=f.e;foodName=f.n;digestStage=0;digestHighlight=-1;
    digestClicked=[false,false,false,false,false];foodY=120;foodTargetY=120;
  }
}
function drawBody(){
  // Simplified body outline
  ctx.strokeStyle='#a78bfa30';ctx.lineWidth=2;
  ctx.beginPath();ctx.ellipse(350,180,40,50,0,0,Math.PI*2);ctx.stroke(); // head
  ctx.beginPath();ctx.moveTo(310,230);ctx.lineTo(280,380);ctx.lineTo(310,380);ctx.lineTo(310,230);ctx.stroke(); // left body
  ctx.beginPath();ctx.moveTo(390,230);ctx.lineTo(420,380);ctx.lineTo(390,380);ctx.lineTo(390,230);ctx.stroke(); // right body
}
function drawModeA(){
  ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
  ctx.fillText('❤️ Dolaşım: Kalbi Ritimde Tut!',W/2,70);
  ctx.font='14px Segoe UI';ctx.fillStyle='#c084fc';
  ctx.fillText('Hedef: ~'+targetBPM+' BPM — Kalbe tıkla!',W/2,95);
  // Heart
  const hx=350,hy=280;
  const s=heartScale;
  ctx.fillStyle='#ef4444';ctx.beginPath();
  ctx.moveTo(hx,hy+15*s);
  ctx.bezierCurveTo(hx,hy-10*s,hx-40*s,hy-30*s,hx-40*s,hy);
  ctx.bezierCurveTo(hx-40*s,hy+20*s,hx,hy+45*s,hx,hy+55*s);
  ctx.moveTo(hx,hy+15*s);
  ctx.bezierCurveTo(hx,hy-10*s,hx+40*s,hy-30*s,hx+40*s,hy);
  ctx.bezierCurveTo(hx+40*s,hy+20*s,hx,hy+45*s,hx,hy+55*s);
  ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('💓',hx,hy+25);
  // Blood cells
  bloodCells.forEach(bc=>{
    bc.angle+=bc.speed;
    const r=120;
    bc.x=hx+Math.cos(bc.angle)*r;
    bc.y=hy+20+Math.sin(bc.angle)*r*0.6;
    ctx.fillStyle='#ef444480';ctx.beginPath();ctx.arc(bc.x,bc.y,5,0,Math.PI*2);ctx.fill();
  });
  // Rhythm bar
  ctx.fillStyle='#1e1b4b';ctx.fillRect(150,430,400,30);
  const barClr=rhythmBar>70?'#10b981':rhythmBar>40?'#fbbf24':'#ef4444';
  ctx.fillStyle=barClr;ctx.fillRect(150,430,rhythmBar*4,30);
  ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;ctx.strokeRect(150,430,400,30);
  ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.fillText('Ritim: '+Math.round(rhythmBar)+'%',350,450);
  // Click instruction
  ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';
  ctx.fillText('Kalbe ritmik tıkla!',350,500);
  // Time indicator
  heartTimer+=16;
  if(heartTimer>3000&&heartClicks>=3){
    // Evaluate rhythm
    if(rhythmBar>=60){score+=10;snd(true);addP(350,300,'#10b981');showRes=1}
    else{snd(false);addP(350,300,'#ef4444');showRes=2}
    resTime=Date.now();
  }
  // Heart animation
  if(heartScale>1)heartScale-=0.02;
  if(heartScale<1)heartScale=1;
}
function drawModeB(){
  ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
  ctx.fillText('🫁 Solunum: Doğru Sırada Nefes Al/Ver!',W/2,70);
  ctx.font='14px Segoe UI';ctx.fillStyle='#c084fc';
  const nextAction=breathIdx<breathTarget.length?
    (breathTarget[breathIdx]==='in'?'Nefes Al':'Nefes Ver'):'Tamamlandı';
  ctx.fillText('Sıradaki: '+nextAction+' ('+breathIdx+'/'+breathTarget.length+')',W/2,95);
  // Lungs
  const lx=300,ly=250,rx=400;
  const ls=0.5+lungScale*0.5;
  // Left lung
  ctx.fillStyle='#60a5fa50';ctx.beginPath();
  ctx.ellipse(lx,ly,35*ls,60*ls,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#60a5fa';ctx.lineWidth=2;ctx.stroke();
  // Right lung
  ctx.fillStyle='#60a5fa50';ctx.beginPath();
  ctx.ellipse(rx,ly,35*ls,60*ls,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#60a5fa';ctx.lineWidth=2;ctx.stroke();
  // Trachea
  ctx.strokeStyle='#a78bfa';ctx.lineWidth=4;ctx.beginPath();
  ctx.moveTo(350,160);ctx.lineTo(350,200);ctx.moveTo(350,200);ctx.lineTo(lx,220);
  ctx.moveTo(350,200);ctx.lineTo(rx,220);ctx.stroke();
  // O2 particles
  o2Particles.forEach(p=>{
    p.y+=p.vy;p.x+=Math.sin(p.t+=0.05)*0.5;
    ctx.fillStyle='#3b82f6';ctx.font='12px Segoe UI';ctx.fillText('O₂',p.x,p.y);
  });
  o2Particles=o2Particles.filter(p=>p.y<350&&p.y>100);
  // CO2 particles
  co2Particles.forEach(p=>{
    p.y+=p.vy;p.x+=Math.sin(p.t+=0.05)*0.5;
    ctx.fillStyle='#f87171';ctx.font='12px Segoe UI';ctx.fillText('CO₂',p.x,p.y);
  });
  co2Particles=co2Particles.filter(p=>p.y>100);
  // Buttons
  const btnY=420;
  ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.roundRect(150,btnY,160,50,10);ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Nefes Al 🌬️',230,btnY+32);
  ctx.fillStyle='#ef4444';ctx.beginPath();ctx.roundRect(390,btnY,160,50,10);ctx.fill();
  ctx.fillStyle='#fff';ctx.fillText('Nefes Ver 💨',470,btnY+32);
  // Lung animation
  if(breathPhase==='in'){lungScale=Math.min(1,lungScale+0.02);
    if(Math.random()<0.3)o2Particles.push({x:340+Math.random()*20,y:160,vy:2,t:Math.random()*6})}
  if(breathPhase==='out'){lungScale=Math.max(0.3,lungScale-0.02);
    if(Math.random()<0.3)co2Particles.push({x:340+Math.random()*20,y:250,vy:-2,t:Math.random()*6})}
  breathTimer++;
  if(breathTimer>40){breathPhase='wait';breathTimer=0}
}
function drawModeC(){
  ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
  ctx.fillText('🍽️ Sindirim: '+foodEmoji+' '+foodName+' Yolculuğu',W/2,70);
  ctx.font='14px Segoe UI';ctx.fillStyle='#c084fc';
  ctx.fillText('Organları sırayla tıkla!',W/2,95);
  // Body outline with digestive organs
  const organs=[
    {name:'Ağız',x:350,y:160,r:25,clr:'#f472b6'},
    {name:'Yemek Borusu',x:350,y:220,r:18,clr:'#fb923c'},
    {name:'Mide',x:340,y:290,r:30,clr:'#fbbf24'},
    {name:'İnce Bağırsak',x:350,y:370,r:28,clr:'#34d399'},
    {name:'Kalın Bağırsak',x:350,y:440,r:25,clr:'#60a5fa'}
  ];
  // Connections
  ctx.strokeStyle='#a78bfa30';ctx.lineWidth=3;
  for(let i=0;i<organs.length-1;i++){
    ctx.beginPath();ctx.moveTo(organs[i].x,organs[i].y+organs[i].r);
    ctx.lineTo(organs[i+1].x,organs[i+1].y-organs[i+1].r);ctx.stroke();
  }
  // Organs
  organs.forEach((o,i)=>{
    const done=digestClicked[i];
    const highlight=i===digestStage;
    ctx.fillStyle=done?o.clr+'40':highlight?o.clr:o.clr+'60';
    ctx.beginPath();ctx.ellipse(o.x,o.y,o.r,o.r*0.8,0,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle=highlight?'#fbbf24':done?'#10b981':'#a78bfa60';
    ctx.lineWidth=highlight?3:2;ctx.stroke();
    ctx.fillStyle=done?'#10b981':'#e9d5ff';ctx.font='bold 12px Segoe UI';
    ctx.fillText(o.name,o.x,o.y+4);
    if(done){ctx.fillStyle='#10b981';ctx.font='14px Segoe UI';ctx.fillText('✓',o.x+o.r+8,o.y)}
    if(highlight){ctx.fillStyle='#fbbf24';ctx.font='14px Segoe UI';ctx.fillText('👆',o.x+o.r+10,o.y)}
  });
  // Food position
  if(foodTargetY!==foodY){foodY+=(foodTargetY-foodY)*0.1}
  ctx.font='30px Segoe UI';ctx.fillText(foodEmoji,480,foodY);
  // Info panel
  if(digestStage>0&&digestStage<=5){
    const prevIdx=digestStage-1;
    ctx.fillStyle='#1e1b4b';ctx.beginPath();ctx.roundRect(480,250,200,80,8);ctx.fill();
    ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;ctx.stroke();
    ctx.fillStyle='#fbbf24';ctx.font='bold 13px Segoe UI';ctx.textAlign='left';
    ctx.fillText(digestOrgans[prevIdx]+':',490,275);
    ctx.fillStyle='#e9d5ff';ctx.font='12px Segoe UI';
    const words=digestInfo[prevIdx].split(' ');let line='',ly2=295;
    words.forEach(w=>{if((line+w).length>22){ctx.fillText(line,490,ly2);ly2+=16;line=w+' '}else{line+=w+' '}});
    if(line)ctx.fillText(line,490,ly2);
    ctx.textAlign='center';
  }
  // Progress
  ctx.fillStyle='#e9d5ff';ctx.font='13px Segoe UI';ctx.textAlign='center';
  ctx.fillText('İlerleme: '+digestStage+'/5',350,530);
}
function draw(){
  ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🫀 İnsan Vücudu Görevleri',W/2,170);ctx.font='18px Segoe UI';
    ctx.fillText('Dolaşım, Solunum ve Sindirim!',W/2,210);
    ctx.font='14px Segoe UI';ctx.fillStyle='#c084fc';
    ctx.fillText('Tur 1-3: Dolaşım ❤️  Tur 4-6: Solunum 🫁  Tur 7-9: Sindirim 🍽️',W/2,250);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,290,160,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,322);return}
  if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🫀 Vücut Uzmanı!',W/2,200);ctx.font='22px Segoe UI';
    ctx.fillText('Puan: '+score+'/'+maxR*10,W/2,250);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,300,180,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,332);return}
  // HUD
  ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score+'   Mod: '+(mode==='A'?'Dolaşım ❤️':mode==='B'?'Solunum 🫁':'Sindirim 🍽️'),W/2,25);
  if(mode==='A')drawModeA();
  else if(mode==='B')drawModeB();
  else drawModeC();
  if(showRes>0){ctx.fillStyle=showRes===1?'#10b981':'#ef4444';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
    ctx.fillText(showRes===1?'✓ Harika! +10':'✗ Tekrar dene!',W/2,590)}
  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}
function upd(){
  if(showRes>0&&Date.now()-resTime>1500){showRes=0;round++;if(round>maxR)state='win';else initRound()}
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
  draw();requestAnimationFrame(upd);
}
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
  if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<340){state='play';score=0;round=1;initRound()}return}
  if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';score=0;round=1;initRound()}return}
  if(showRes>0)return;
  if(mode==='A'){
    // Click on heart area
    const hx=350,hy=280;
    if(Math.abs(mx-hx)<50&&Math.abs(my-hy-20)<60){
      heartScale=1.3;heartClicks++;
      const now=Date.now();
      if(lastBeatTime>0){
        const interval=now-lastBeatTime;
        const diff=Math.abs(interval-beatInterval);
        const accuracy=Math.max(0,100-diff/5);
        rhythmBar=rhythmBar*0.6+accuracy*0.4;
      }
      lastBeatTime=now;
      addP(hx,hy,'#ef4444');
      // Add blood cells
      if(bloodCells.length<12)bloodCells.push({x:hx,y:hy,angle:Math.random()*Math.PI*2,speed:0.02+Math.random()*0.01});
    }
  }
  if(mode==='B'){
    if(breathIdx>=breathTarget.length)return;
    const btnY=420;
    if(mx>150&&mx<310&&my>btnY&&my<btnY+50){
      // Nefes Al
      if(breathTarget[breathIdx]==='in'){breathPhase='in';breathTimer=0;breathIdx++;snd(true);addP(230,btnY+25,'#3b82f6');
        if(breathIdx>=breathTarget.length){score+=10;showRes=1;resTime=Date.now()}}
      else{snd(false);addP(230,btnY+25,'#ef4444');showRes=2;resTime=Date.now()}
    }
    if(mx>390&&mx<550&&my>btnY&&my<btnY+50){
      // Nefes Ver
      if(breathTarget[breathIdx]==='out'){breathPhase='out';breathTimer=0;breathIdx++;snd(true);addP(470,btnY+25,'#ef4444');
        if(breathIdx>=breathTarget.length){score+=10;showRes=1;resTime=Date.now()}}
      else{snd(false);addP(470,btnY+25,'#ef4444');showRes=2;resTime=Date.now()}
    }
  }
  if(mode==='C'){
    const organs=[
      {x:350,y:160,r:25},{x:350,y:220,r:18},{x:340,y:290,r:30},{x:350,y:370,r:28},{x:350,y:440,r:25}
    ];
    organs.forEach((o,i)=>{
      if(Math.abs(mx-o.x)<o.r+10&&Math.abs(my-o.y)<o.r+10){
        if(i===digestStage){
          digestClicked[i]=true;digestStage++;
          foodTargetY=o.y;
          snd(true);addP(o.x,o.y,COLORS[i%COLORS.length]);
          if(digestStage>=5){score+=10;showRes=1;resTime=Date.now()}
        }else if(i!==digestStage){snd(false);addP(o.x,o.y,'#ef4444')}
      }
    });
  }
});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_sci_gunes_sistemi_html():
    """Güneş Sistemi Görevi — Gezegenleri doğru yörüngeye yerleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[];
const PLANETS=[
  {name:'Merkür',emoji:'☿️',clr:'#94a3b8',r:6,orbit:1,speed:0.04},
  {name:'Venüs',emoji:'♀️',clr:'#fbbf24',r:8,orbit:2,speed:0.03},
  {name:'Dünya',emoji:'🌍',clr:'#3b82f6',r:9,orbit:3,speed:0.025},
  {name:'Mars',emoji:'♂️',clr:'#ef4444',r:7,orbit:4,speed:0.02},
  {name:'Jüpiter',emoji:'♃',clr:'#fb923c',r:14,orbit:5,speed:0.012},
  {name:'Satürn',emoji:'♄',clr:'#fbbf24',r:12,orbit:6,speed:0.009},
  {name:'Uranüs',emoji:'⛢',clr:'#67e8f9',r:10,orbit:7,speed:0.006},
  {name:'Neptün',emoji:'♆',clr:'#818cf8',r:10,orbit:8,speed:0.004}
];
const DWARFS=[
  {name:'Plüton',emoji:'⚫',clr:'#a78bfa',r:5,orbit:9,speed:0.003},
  {name:'Ceres',emoji:'⚪',clr:'#d4d4d8',r:4,orbit:4.5,speed:0.018}
];
let activePlanets=[],cards=[],placedPlanets=[],dragIdx=-1,dragOX=0,dragOY=0;
let showRes=0,resTime=0,starField=[],time=0;
let showHints=false,asteroidBelt=false;
// Init stars
for(let i=0;i<80;i++)starField.push({x:Math.random()*W,y:Math.random()*H,s:0.5+Math.random()*2,b:Math.random()});
const CX=280,CY=310,orbitBase=30,orbitGap=28;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function orbitRadius(orbitNum){return orbitBase+orbitNum*orbitGap}
function genRound(){
  showRes=0;placedPlanets=[];
  if(round<=3){
    activePlanets=PLANETS.slice(0,4);showHints=true;asteroidBelt=false;
  }else if(round<=7){
    activePlanets=[...PLANETS];showHints=false;asteroidBelt=false;
  }else{
    activePlanets=[...PLANETS,...DWARFS];showHints=false;asteroidBelt=true;
  }
  cards=[];
  const shuffled=[...activePlanets];
  for(let i=shuffled.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]]}
  const cardStartX=560,cardStartY=60;
  shuffled.forEach((p,i)=>{
    cards.push({...p,cx:cardStartX+((i%2)*70),cy:cardStartY+Math.floor(i/2)*60,w:60,h:50,placed:false,angle:Math.random()*Math.PI*2});
  });
}
function drawStars(){
  starField.forEach(s=>{s.b+=0.01;ctx.fillStyle='rgba(255,255,255,'+(0.3+Math.sin(s.b)*0.3)+')';
    ctx.beginPath();ctx.arc(s.x,s.y,s.s,0,Math.PI*2);ctx.fill()});
}
function drawSun(){
  const glow=ctx.createRadialGradient(CX,CY,5,CX,CY,35);
  glow.addColorStop(0,'#fbbf24');glow.addColorStop(0.5,'#f59e0b80');glow.addColorStop(1,'transparent');
  ctx.fillStyle=glow;ctx.beginPath();ctx.arc(CX,CY,35,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(CX,CY,18,0,Math.PI*2);ctx.fill();
  // Corona rays
  for(let i=0;i<8;i++){
    const a=time*0.5+i*Math.PI/4;
    ctx.strokeStyle='#fbbf2440';ctx.lineWidth=2;ctx.beginPath();
    ctx.moveTo(CX+Math.cos(a)*20,CY+Math.sin(a)*20);
    ctx.lineTo(CX+Math.cos(a)*32,CY+Math.sin(a)*32);ctx.stroke();
  }
}
function drawOrbits(){
  const maxOrbit=asteroidBelt?9:8;
  for(let i=1;i<=maxOrbit;i++){
    const r=orbitRadius(i);
    ctx.strokeStyle='#a78bfa15';ctx.lineWidth=1;ctx.beginPath();ctx.arc(CX,CY,r,0,Math.PI*2);ctx.stroke();
    if(showHints&&i<=4){ctx.fillStyle='#a78bfa40';ctx.font='10px Segoe UI';ctx.textAlign='center';ctx.fillText(i+'.',CX+r+5,CY-5)}
  }
  // Asteroid belt
  if(asteroidBelt){
    const abr=orbitRadius(4.5);
    for(let i=0;i<20;i++){
      const a=time*0.01+i*Math.PI/10;
      const rx=abr+Math.sin(i*3)*8;
      ctx.fillStyle='#6b728060';ctx.beginPath();ctx.arc(CX+Math.cos(a)*rx,CY+Math.sin(a)*rx,2,0,Math.PI*2);ctx.fill();
    }
  }
}
function drawPlacedPlanets(){
  placedPlanets.forEach(p=>{
    p.angle+=p.speed;
    const r=orbitRadius(p.orbit);
    const px=CX+Math.cos(p.angle)*r;
    const py=CY+Math.sin(p.angle)*r;
    // Planet body
    ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(px,py,p.r,0,Math.PI*2);ctx.fill();
    // Saturn ring
    if(p.name==='Satürn'){ctx.strokeStyle='#fbbf2480';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(px,py,p.r+6,3,0.3,0,Math.PI*2);ctx.stroke()}
    // Label
    ctx.fillStyle='#e9d5ff';ctx.font='9px Segoe UI';ctx.textAlign='center';ctx.fillText(p.name,px,py+p.r+12);
  });
}
function draw(){
  ctx.clearRect(0,0,W,H);ctx.fillStyle='#0a0118';ctx.fillRect(0,0,W,H);
  drawStars();
  if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🪐 Güneş Sistemi Görevi',W/2,180);ctx.font='18px Segoe UI';
    ctx.fillText('Gezegenleri doğru yörüngeye yerleştir!',W/2,220);
    ctx.font='14px Segoe UI';ctx.fillStyle='#c084fc';
    ctx.fillText('Güneşe en yakın: Merkür → En uzak: Neptün',W/2,260);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,290,160,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,322);return}
  if(state==='win'){
    drawSun();drawOrbits();drawPlacedPlanets();
    ctx.fillStyle='#e9d5ffd0';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🪐 Astronomi Uzmanı!',W/2,180);ctx.font='22px Segoe UI';
    ctx.fillText('Puan: '+score+'/'+maxR*10,W/2,220);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,260,180,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,292);return}
  time++;
  // HUD
  ctx.fillStyle='#e9d5ff';ctx.font='bold 15px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,20);
  drawSun();drawOrbits();drawPlacedPlanets();
  // Cards panel
  ctx.fillStyle='#1e1b4b40';ctx.beginPath();ctx.roundRect(545,40,145,H-80,10);ctx.fill();
  ctx.fillStyle='#e9d5ff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Gezegenler',617,58);
  cards.forEach((c,i)=>{
    if(c.placed)return;if(i===dragIdx)return;
    ctx.fillStyle='#312e81';ctx.strokeStyle=c.clr;ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(c.cx,c.cy,c.w,c.h,8);ctx.fill();ctx.stroke();
    ctx.fillStyle=c.clr;ctx.beginPath();ctx.arc(c.cx+20,c.cy+20,c.r*0.8,0,Math.PI*2);ctx.fill();
    if(c.name==='Satürn'){ctx.strokeStyle='#fbbf2480';ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(c.cx+20,c.cy+20,c.r+4,2,0.3,0,Math.PI*2);ctx.stroke()}
    ctx.fillStyle='#e9d5ff';ctx.font='10px Segoe UI';ctx.textAlign='left';ctx.fillText(c.name,c.cx+40,c.cy+24);
  });
  // Dragged card
  if(dragIdx>=0){
    const c=cards[dragIdx];
    ctx.globalAlpha=0.85;ctx.fillStyle='#4c1d95';ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;
    ctx.beginPath();ctx.roundRect(c.cx,c.cy,c.w,c.h,8);ctx.fill();ctx.stroke();
    ctx.globalAlpha=1;
    ctx.fillStyle=c.clr;ctx.beginPath();ctx.arc(c.cx+20,c.cy+20,c.r,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fbbf24';ctx.font='bold 10px Segoe UI';ctx.textAlign='left';ctx.fillText(c.name,c.cx+40,c.cy+24);
  }
  // Check if all placed
  const allDone=cards.every(c=>c.placed);
  if(allDone&&showRes===0){
    ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(200,590,160,40,10);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('Kontrol Et ✓',280,616);
  }
  if(showRes>0){ctx.fillStyle=showRes===1?'#10b981':'#ef4444';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
    ctx.fillText(showRes===1?'✓ Mükemmel! +10':'✗ Bazı gezegenler yanlış yörüngede!',350,620)}
  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}
function findOrbit(mx,my){
  const dist=Math.sqrt((mx-CX)**2+(my-CY)**2);
  const maxOrbit=asteroidBelt?9:8;
  for(let i=1;i<=maxOrbit;i++){
    const r=orbitRadius(i);
    if(Math.abs(dist-r)<15)return i;
  }
  // Check for 4.5 (Ceres)
  if(asteroidBelt){const r45=orbitRadius(4.5);if(Math.abs(dist-r45)<15)return 4.5}
  return -1;
}
function checkAll(){
  let correct=true;
  cards.forEach(c=>{
    if(c.placedOrbit!==c.orbit)correct=false;
  });
  if(correct){score+=10;snd(true);addP(CX,CY,'#fbbf24');showRes=1;
    // Transfer to animated planets
    placedPlanets=[];cards.forEach(c=>{placedPlanets.push({...c,angle:Math.random()*Math.PI*2})})}
  else{snd(false);addP(CX,CY,'#ef4444');showRes=2;
    // Bounce back wrong ones
    cards.forEach(c=>{
      if(c.placedOrbit!==c.orbit){c.placed=false;c.placedOrbit=-1;
        const unpl=cards.filter(cc=>!cc.placed).length-1;
        c.cx=560+(unpl%2)*70;c.cy=70+Math.floor(unpl/2)*60}
    });
    // Remove wrong from placed
    placedPlanets=placedPlanets.filter(p=>{
      const card=cards.find(c=>c.name===p.name);return card&&card.placed;
    });
  }
  resTime=Date.now();
}
function upd(){
  if(showRes>0&&Date.now()-resTime>1500){
    if(showRes===1){showRes=0;round++;if(round>maxR)state='win';else genRound()}
    else{showRes=0}
  }
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
  draw();requestAnimationFrame(upd);
}
function getPos(e){const r=cv.getBoundingClientRect();const raw=e.touches?e.touches[0]:e;
  return{x:(raw.clientX-r.left)*(W/r.width),y:(raw.clientY-r.top)*(H/r.height)}}
function handleDown(mx,my){
  if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<340){state='play';score=0;round=1;placedPlanets=[];genRound()}return}
  if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>260&&my<310){state='play';score=0;round=1;placedPlanets=[];genRound()}return}
  if(showRes>0)return;
  // Check button
  const allDone=cards.every(c=>c.placed);
  if(allDone&&mx>200&&mx<360&&my>590&&my<630){checkAll();return}
  // Pick from placed (on orbit)
  for(let i=placedPlanets.length-1;i>=0;i--){
    const p=placedPlanets[i];
    const r2=orbitRadius(p.orbit);
    const px=CX+Math.cos(p.angle)*r2;const py=CY+Math.sin(p.angle)*r2;
    if(Math.abs(mx-px)<20&&Math.abs(my-py)<20){
      const ci=cards.findIndex(c=>c.name===p.name);
      if(ci>=0){cards[ci].placed=false;cards[ci].placedOrbit=-1;cards[ci].cx=mx-30;cards[ci].cy=my-25;
        dragIdx=ci;dragOX=30;dragOY=25;placedPlanets.splice(i,1);return}
    }
  }
  // Pick card
  for(let i=cards.length-1;i>=0;i--){const c=cards[i];
    if(c.placed)continue;
    if(mx>c.cx&&mx<c.cx+c.w&&my>c.cy&&my<c.cy+c.h){dragIdx=i;dragOX=mx-c.cx;dragOY=my-c.cy;return}}
}
function handleMove(mx,my){if(dragIdx<0)return;cards[dragIdx].cx=mx-dragOX;cards[dragIdx].cy=my-dragOY}
function handleUp(mx,my){
  if(dragIdx<0)return;
  const c=cards[dragIdx];
  const orbit=findOrbit(mx,my);
  if(orbit>0){
    // Check if orbit already occupied
    const occupied=cards.some((cc,ii)=>ii!==dragIdx&&cc.placed&&cc.placedOrbit===orbit);
    if(!occupied){
      c.placed=true;c.placedOrbit=orbit;
      const angle=Math.atan2(my-CY,mx-CX);
      placedPlanets.push({...c,angle:angle});
      snd(true);
    }else{
      // Bounce back
      const unpl=cards.filter((cc,ii)=>!cc.placed&&ii!==dragIdx).length;
      c.cx=560+(unpl%2)*70;c.cy=70+Math.floor(unpl/2)*60;
    }
  }else{
    const unpl=cards.filter((cc,ii)=>!cc.placed&&ii!==dragIdx).length;
    c.cx=560+(unpl%2)*70;c.cy=70+Math.floor(unpl/2)*60;
  }
  dragIdx=-1;
}
cv.addEventListener('mousedown',e=>{const p=getPos(e);handleDown(p.x,p.y)});
cv.addEventListener('mousemove',e=>{const p=getPos(e);handleMove(p.x,p.y)});
cv.addEventListener('mouseup',e=>{const p=getPos(e);handleUp(p.x,p.y)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const p=getPos(e);handleDown(p.x,p.y)});
cv.addEventListener('touchmove',e=>{e.preventDefault();const p=getPos(e);handleMove(p.x,p.y)});
cv.addEventListener('touchend',e=>{e.preventDefault();const r=cv.getBoundingClientRect();
  const lt=e.changedTouches[0];handleUp((lt.clientX-r.left)*(W/r.width),(lt.clientY-r.top)*(H/r.height))});
upd();
</script></body></html>"""


def _build_elem_sci_deprem_kopru_html():
    """Afet Bilinci: Deprem Dayanıklı Köprü — Malzeme seçerek köprü inşa et."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[];
const MATERIALS=[
  {name:'Taş',emoji:'🪨',cost:2,strength:40,weight:3,clr:'#6b7280',flex:0.1},
  {name:'Ahşap',emoji:'🪵',cost:1,strength:25,weight:1,clr:'#92400e',flex:0.8},
  {name:'Çelik',emoji:'🔩',cost:5,strength:90,weight:2,clr:'#60a5fa',flex:0.5},
  {name:'Tuğla',emoji:'🧱',cost:3,strength:55,weight:2.5,clr:'#dc2626',flex:0.2}
];
const GRID_W=5,GRID_H=3;
let grid=[];// 5x3, each cell: null or {matIdx, hp, shakeX, shakeY}
let budget=0,maxBudget=0,spent=0;
let magnitude=3,quakeActive=false,quakeTimer=0,quakeIntensity=0;
let selectedMat=-1,showRes=0,resTime=0;
let fallingBlocks=[],debris=[];
let bridgeIntegrity=100;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function initRound(){
  grid=[];for(let y=0;y<GRID_H;y++){grid[y]=[];for(let x=0;x<GRID_W;x++)grid[y][x]=null}
  magnitude=3+Math.floor((round-1)*0.5);if(magnitude>7)magnitude=7;
  maxBudget=15+round*3;budget=maxBudget;spent=0;
  quakeActive=false;quakeTimer=0;selectedMat=0;showRes=0;
  fallingBlocks=[];debris=[];bridgeIntegrity=100;
}
const bridgeX=175,bridgeY=340,cellW=70,cellH=50;
const cliffLeft=bridgeX-50,cliffRight=bridgeX+GRID_W*cellW;
function gridToXY(gx,gy){return{x:bridgeX+gx*cellW,y:bridgeY+gy*cellH}}
function drawCliffs(){
  // Left cliff
  ctx.fillStyle='#4b5563';
  ctx.beginPath();ctx.moveTo(0,bridgeY);ctx.lineTo(cliffLeft+50,bridgeY);
  ctx.lineTo(cliffLeft+50,bridgeY+GRID_H*cellH+30);ctx.lineTo(cliffLeft+30,H);ctx.lineTo(0,H);ctx.fill();
  // Rock texture
  ctx.fillStyle='#6b728020';
  for(let i=0;i<5;i++){ctx.beginPath();ctx.arc(30+i*25,bridgeY+50+i*20,8+i*3,0,Math.PI*2);ctx.fill()}
  // Right cliff
  ctx.fillStyle='#4b5563';
  ctx.beginPath();ctx.moveTo(cliffRight,bridgeY);ctx.lineTo(W,bridgeY);
  ctx.lineTo(W,H);ctx.lineTo(cliffRight+20,H);ctx.lineTo(cliffRight,bridgeY+GRID_H*cellH+30);ctx.fill();
  ctx.fillStyle='#6b728020';
  for(let i=0;i<5;i++){ctx.beginPath();ctx.arc(cliffRight+30+i*20,bridgeY+40+i*25,6+i*3,0,Math.PI*2);ctx.fill()}
  // Gap/chasm
  const cg=ctx.createLinearGradient(cliffLeft+50,bridgeY+GRID_H*cellH,cliffLeft+50,H);
  cg.addColorStop(0,'#1e1b4b');cg.addColorStop(1,'#0B0F19');
  ctx.fillStyle=cg;ctx.fillRect(cliffLeft+50,bridgeY+GRID_H*cellH,cliffRight-cliffLeft-50,H-bridgeY-GRID_H*cellH);
  // Water at bottom
  ctx.fillStyle='#0ea5e930';ctx.fillRect(cliffLeft+50,H-40,cliffRight-cliffLeft-50,40);
}
function drawBridge(){
  const shakeX=quakeActive?(Math.random()-0.5)*quakeIntensity*3:0;
  const shakeY=quakeActive?(Math.random()-0.5)*quakeIntensity*2:0;
  for(let gy=0;gy<GRID_H;gy++){for(let gx=0;gx<GRID_W;gx++){
    const pos=gridToXY(gx,gy);
    const cell=grid[gy][gx];
    // Grid outline
    ctx.strokeStyle=cell?'transparent':'#a78bfa30';ctx.lineWidth=1;
    if(!cell){ctx.setLineDash([4,4]);ctx.strokeRect(pos.x+shakeX,pos.y+shakeY,cellW-2,cellH-2);ctx.setLineDash([])}
    if(cell){
      const m=MATERIALS[cell.matIdx];
      const sx=quakeActive?(Math.random()-0.5)*quakeIntensity*(1-m.flex)*2:0;
      const sy=quakeActive?(Math.random()-0.5)*quakeIntensity*(1-m.flex):0;
      // Damage visual
      const hpRatio=cell.hp/m.strength;
      const alpha=0.3+hpRatio*0.7;
      ctx.globalAlpha=alpha;
      ctx.fillStyle=m.clr;ctx.beginPath();ctx.roundRect(pos.x+shakeX+sx,pos.y+shakeY+sy,cellW-2,cellH-2,4);ctx.fill();
      ctx.strokeStyle='#fff20';ctx.lineWidth=1;ctx.stroke();
      // Emoji
      ctx.globalAlpha=1;ctx.font='22px Segoe UI';ctx.textAlign='center';
      ctx.fillText(m.emoji,pos.x+cellW/2+shakeX+sx,pos.y+cellH/2+6+shakeY+sy);
      // Damage cracks
      if(hpRatio<0.5){ctx.strokeStyle='#ef444480';ctx.lineWidth=1;ctx.beginPath();
        ctx.moveTo(pos.x+10+shakeX,pos.y+10+shakeY);ctx.lineTo(pos.x+cellW-15+shakeX,pos.y+cellH-10+shakeY);ctx.stroke()}
    }
  }}
}
function drawMaterialPalette(){
  ctx.fillStyle='#1e1b4b80';ctx.beginPath();ctx.roundRect(50,550,600,85,10);ctx.fill();
  ctx.fillStyle='#e9d5ff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Malzeme Seç:',100,568);
  MATERIALS.forEach((m,i)=>{
    const mx2=160+i*130,my2=555;
    ctx.fillStyle=i===selectedMat?'#4c1d95':'#312e81';
    ctx.strokeStyle=i===selectedMat?'#fbbf24':'#a78bfa';ctx.lineWidth=i===selectedMat?3:1;
    ctx.beginPath();ctx.roundRect(mx2,my2,115,70,8);ctx.fill();ctx.stroke();
    ctx.font='20px Segoe UI';ctx.textAlign='center';ctx.fillText(m.emoji,mx2+25,my2+30);
    ctx.fillStyle='#e9d5ff';ctx.font='bold 11px Segoe UI';ctx.fillText(m.name,mx2+70,my2+22);
    ctx.fillStyle='#fbbf24';ctx.font='10px Segoe UI';
    ctx.fillText('💰'+m.cost+'  💪'+m.strength,mx2+70,my2+40);
    ctx.fillStyle='#c084fc';ctx.fillText('Esneklik: '+(m.flex>0.5?'Yüksek':'Düşük'),mx2+70,my2+55);
  });
}
function draw(){
  ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 30px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🌉 Deprem Dayanıklı Köprü',W/2,170);ctx.font='18px Segoe UI';
    ctx.fillText('Malzeme seçerek köprü inşa et,',W/2,210);
    ctx.fillText('depreme dayanıklı olsun!',W/2,240);
    ctx.font='14px Segoe UI';ctx.fillStyle='#c084fc';
    ctx.fillText('Çelik güçlü ama pahalı, Ahşap esnek ama zayıf',W/2,280);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,342);return}
  if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🌉 Mühendis Ustası!',W/2,200);ctx.font='22px Segoe UI';
    ctx.fillText('Puan: '+score+'/'+maxR*10,W/2,250);
    ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,300,180,50,12);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,332);return}
  // HUD
  ctx.fillStyle='#e9d5ff';ctx.font='bold 15px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,20);
  // Budget & Magnitude
  ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
  ctx.fillText('💰 Bütçe: '+budget+'/'+maxBudget,30,50);
  ctx.fillStyle='#ef4444';ctx.textAlign='right';
  ctx.fillText('Deprem: '+magnitude.toFixed(1)+' Büyüklük 🫨',W-30,50);
  // Budget bar
  ctx.fillStyle='#1e1b4b';ctx.fillRect(30,58,200,12);
  ctx.fillStyle=budget>maxBudget*0.3?'#10b981':'#ef4444';
  ctx.fillRect(30,58,200*(budget/maxBudget),12);
  // Integrity during quake
  if(quakeActive){
    ctx.fillStyle='#1e1b4b';ctx.fillRect(470,58,200,12);
    const intClr=bridgeIntegrity>60?'#10b981':bridgeIntegrity>30?'#fbbf24':'#ef4444';
    ctx.fillStyle=intClr;ctx.fillRect(470,58,200*(bridgeIntegrity/100),12);
    ctx.fillStyle='#e9d5ff';ctx.font='11px Segoe UI';ctx.textAlign='center';
    ctx.fillText('Dayanıklılık: '+Math.round(bridgeIntegrity)+'%',570,69);
  }
  drawCliffs();drawBridge();
  // Falling blocks
  fallingBlocks.forEach(fb=>{
    fb.y+=fb.vy;fb.vy+=0.3;fb.r+=fb.vr;
    ctx.save();ctx.translate(fb.x,fb.y);ctx.rotate(fb.r);
    ctx.fillStyle=fb.clr;ctx.globalAlpha=fb.alpha;
    ctx.fillRect(-15,-12,30,24);ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText(fb.emoji,0,6);
    ctx.restore();ctx.globalAlpha=1;
    fb.alpha-=0.01;
  });
  fallingBlocks=fallingBlocks.filter(fb=>fb.y<H&&fb.alpha>0);
  // Debris
  debris.forEach(d=>{d.x+=d.vx;d.y+=d.vy;d.vy+=0.2;d.life-=0.02;
    ctx.globalAlpha=d.life;ctx.fillStyle=d.clr;ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,Math.PI*2);ctx.fill()});
  debris=debris.filter(d=>d.life>0);ctx.globalAlpha=1;
  // Quake button or material palette
  if(!quakeActive&&showRes===0){
    drawMaterialPalette();
    // Quake test button
    const anyBlock=grid.some(row=>row.some(c=>c!==null));
    if(anyBlock){
      ctx.fillStyle='#ef4444';ctx.beginPath();ctx.roundRect(250,500,200,40,10);ctx.fill();
      ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
      ctx.fillText('Sarsıntı Testi! 🫨',350,526);
    }
  }
  // Result
  if(showRes>0){ctx.fillStyle=showRes===1?'#10b981':'#ef4444';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
    const msg=showRes===1?'✓ Köprü dayandı! +'+lastScore:'✗ Köprü çöktü!';
    ctx.fillText(msg,W/2,530)}
  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}
let lastScore=0;
function startQuake(){
  quakeActive=true;quakeTimer=0;quakeIntensity=magnitude*1.5;bridgeIntegrity=100;
}
function updateQuake(){
  if(!quakeActive)return;
  quakeTimer++;
  // Shake for ~3 seconds (180 frames)
  const progress=quakeTimer/180;
  quakeIntensity=magnitude*1.5*Math.sin(progress*Math.PI);
  // Damage blocks
  for(let gy=0;gy<GRID_H;gy++){for(let gx=0;gx<GRID_W;gx++){
    const cell=grid[gy][gx];if(!cell)continue;
    const m=MATERIALS[cell.matIdx];
    // Damage based on magnitude, weight, and flexibility
    const dmg=(magnitude*0.8-m.flex*2)*(1+m.weight*0.1)*Math.random();
    if(dmg>0)cell.hp-=dmg;
    if(cell.hp<=0){
      // Block breaks
      const pos=gridToXY(gx,gy);
      fallingBlocks.push({x:pos.x+cellW/2,y:pos.y+cellH/2,vy:1,r:0,vr:(Math.random()-0.5)*0.1,
        clr:m.clr,emoji:m.emoji,alpha:1});
      for(let d=0;d<5;d++)debris.push({x:pos.x+cellW/2,y:pos.y+cellH/2,
        vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*3,life:1,clr:m.clr,r:2+Math.random()*3});
      grid[gy][gx]=null;
    }
  }}
  // Calculate integrity
  let total=0,alive=0;
  for(let gy=0;gy<GRID_H;gy++){for(let gx=0;gx<GRID_W;gx++){
    if(grid[gy][gx]!==null)alive++;total++}}
  const placed=GRID_W*GRID_H;
  const originalCount=grid.flat().filter(c=>c!==null).length+fallingBlocks.length;
  bridgeIntegrity=alive>0?(alive/(alive+fallingBlocks.length))*100:0;
  if(quakeTimer>=180){
    quakeActive=false;
    // Evaluate
    const surviving=grid.flat().filter(c=>c!==null).length;
    if(surviving>=Math.ceil(GRID_W*GRID_H*0.4)){
      // Bridge survived
      let pts=5;
      if(budget>maxBudget*0.2)pts+=3; // under budget bonus
      if(surviving===GRID_W*GRID_H)pts+=2; // all intact
      lastScore=pts;score+=pts;snd(true);addP(W/2,400,'#10b981');showRes=1;
    }else{
      lastScore=0;snd(false);addP(W/2,400,'#ef4444');showRes=2;
    }
    resTime=Date.now();
  }
}
function upd(){
  updateQuake();
  if(showRes>0&&!quakeActive&&Date.now()-resTime>2000){showRes=0;round++;if(round>maxR)state='win';else initRound()}
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
  draw();requestAnimationFrame(upd);
}
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
  if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;initRound()}return}
  if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';score=0;round=1;initRound()}return}
  if(quakeActive||showRes>0)return;
  // Material selection
  MATERIALS.forEach((m,i)=>{const mx2=160+i*130,my2=555;
    if(mx>mx2&&mx<mx2+115&&my>my2&&my<my2+70)selectedMat=i});
  // Place on grid
  for(let gy=0;gy<GRID_H;gy++){for(let gx=0;gx<GRID_W;gx++){
    const pos=gridToXY(gx,gy);
    if(mx>pos.x&&mx<pos.x+cellW&&my>pos.y&&my<pos.y+cellH){
      if(grid[gy][gx]===null&&selectedMat>=0){
        const m=MATERIALS[selectedMat];
        if(budget>=m.cost){
          grid[gy][gx]={matIdx:selectedMat,hp:m.strength,shakeX:0,shakeY:0};
          budget-=m.cost;spent+=m.cost;snd(true);addP(pos.x+cellW/2,pos.y+cellH/2,m.clr);
        }else{snd(false)}
      }else if(grid[gy][gx]!==null){
        // Remove block, refund
        const m=MATERIALS[grid[gy][gx].matIdx];
        budget+=m.cost;spent-=m.cost;
        grid[gy][gx]=null;
      }
      return;
    }
  }}
  // Quake button
  const anyBlock=grid.some(row=>row.some(c=>c!==null));
  if(anyBlock&&mx>250&&mx<450&&my>500&&my<540){startQuake()}
});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""
