# -*- coding: utf-8 -*-
"""Okul Öncesi Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm A: 1-5)."""


def _build_prek_sci_renk_karistirma_html():
    """Renk Karıştırma Labı — İki ana rengi karıştırarak hedef rengi bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
canvas.width=W;canvas.height=H;
const ctx=canvas.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',round=1,maxRound=10,score=0,particles=[];
let selected=[],mixResult=null,shakeTimer=0,pourAnim=null,bubbles=[];
let correctFlash=0,wrongFlash=0,hintAlpha=1;
const PRIMARY={red:'#ef4444',blue:'#3b82f6',yellow:'#fbbf24'};
const MIXES=[
{a:'red',b:'blue',result:'purple',color:'#8b5cf6',name:'Mor'},
{a:'red',b:'yellow',result:'orange',color:'#f97316',name:'Turuncu'},
{a:'blue',b:'yellow',result:'green',color:'#22c55e',name:'Yeşil'},
{a:'red',b:'blue',result:'purple',color:'#a855f7',name:'Mor'},
{a:'red',b:'yellow',result:'orange',color:'#fb923c',name:'Turuncu'},
{a:'blue',b:'yellow',result:'green',color:'#4ade80',name:'Yeşil'},
{a:'red',b:'red',result:'darkred',color:'#dc2626',name:'Koyu Kırmızı'},
{a:'blue',b:'blue',result:'darkblue',color:'#2563eb',name:'Koyu Mavi'},
{a:'red',b:'yellow',result:'orange',color:'#f97316',name:'Turuncu'},
{a:'blue',b:'yellow',result:'green',color:'#16a34a',name:'Yeşil'}
];
let currentMix=null;
const beakers=[
{x:120,y:160,color:PRIMARY.red,label:'Kırmızı',key:'red',level:0.7,bubT:0},
{x:350,y:160,color:PRIMARY.blue,label:'Mavi',key:'blue',level:0.7,bubT:0},
{x:580,y:160,color:PRIMARY.yellow,label:'Sarı',key:'yellow',level:0.7,bubT:0}
];
let mixBeaker={x:350,y:450,color:'#666',level:0,bubT:0};
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addParticles(x,y,clr){for(let i=0;i<15;i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr,r:3+Math.random()*4})}
function startRound(){selected=[];mixResult=null;mixBeaker.level=0;mixBeaker.color='#666';
currentMix=MIXES[(round-1)%MIXES.length];hintAlpha=1;pourAnim=null;
bubbles=[];for(let i=0;i<8;i++)bubbles.push({x:Math.random()*60-30,y:Math.random()*60,s:2+Math.random()*4,sp:0.3+Math.random()*0.5})}
function drawBeaker(bk,sel,idx){
ctx.save();ctx.translate(bk.x,bk.y);
if(shakeTimer>0&&sel){ctx.translate(Math.sin(shakeTimer*20)*5,0)}
const bw=80,bh=120;
ctx.strokeStyle=sel?'#fbbf24':'#94a3b8';ctx.lineWidth=sel?4:2;
ctx.beginPath();ctx.moveTo(-bw/2,0);ctx.lineTo(-bw/2-5,bh);ctx.lineTo(bw/2+5,bh);ctx.lineTo(bw/2,0);ctx.stroke();
ctx.beginPath();ctx.moveTo(-bw/2+2,bh*(1-bk.level));ctx.lineTo(-bw/2-3,bh);ctx.lineTo(bw/2+3,bh);ctx.lineTo(bw/2-2,bh*(1-bk.level));ctx.closePath();
ctx.fillStyle=bk.color;ctx.globalAlpha=0.85;ctx.fill();ctx.globalAlpha=1;
bubbles.forEach(b=>{if(idx!==undefined){
let by=bh-b.y*bk.level;b.y+=b.sp*0.3;if(b.y>60)b.y=0;
ctx.beginPath();ctx.arc(b.x*0.4,by,b.s,0,Math.PI*2);ctx.fillStyle='#ffffff30';ctx.fill()}});
ctx.fillStyle='#e2e8f0';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText(bk.label||'',0,bh+20);ctx.restore()}
function drawTargetArea(){
const tx=600,ty=350;
ctx.save();ctx.translate(tx,ty);
ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;ctx.setLineDash([5,5]);
ctx.strokeRect(-55,-55,110,110);ctx.setLineDash([]);
ctx.beginPath();ctx.arc(0,0,40,0,Math.PI*2);
ctx.fillStyle=currentMix.color;ctx.fill();
ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.globalAlpha=round<4?1:Math.max(0.2,hintAlpha);
ctx.fillText(currentMix.name,0,65);
ctx.globalAlpha=1;
ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';
ctx.fillText('Hedef Renk',0,-65);
ctx.restore()}
function drawMixArea(){
ctx.save();ctx.translate(mixBeaker.x,mixBeaker.y);
const bw=100,bh=140;
ctx.strokeStyle='#c084fc';ctx.lineWidth=3;
ctx.beginPath();ctx.moveTo(-bw/2,0);ctx.lineTo(-bw/2-8,bh);ctx.lineTo(bw/2+8,bh);ctx.lineTo(bw/2,0);ctx.stroke();
if(mixBeaker.level>0){
ctx.beginPath();ctx.moveTo(-bw/2+3,bh*(1-mixBeaker.level));
ctx.lineTo(-bw/2-5,bh);ctx.lineTo(bw/2+5,bh);ctx.lineTo(bw/2-3,bh*(1-mixBeaker.level));ctx.closePath();
ctx.fillStyle=mixBeaker.color;ctx.globalAlpha=0.9;ctx.fill();ctx.globalAlpha=1;
for(let i=0;i<5;i++){let bub=bubbles[i];
let by=bh-bub.y*mixBeaker.level;bub.y+=bub.sp*0.2;if(bub.y>60)bub.y=0;
ctx.beginPath();ctx.arc(bub.x*0.5,by,bub.s,0,Math.PI*2);ctx.fillStyle='#ffffff30';ctx.fill()}}
ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Karışım',0,bh+22);
ctx.restore()}
function drawPour(){if(!pourAnim)return;
let pa=pourAnim;ctx.strokeStyle=pa.color;ctx.lineWidth=6;ctx.globalAlpha=0.7;
ctx.beginPath();ctx.moveTo(pa.sx,pa.sy);
let cy=pa.sy+(mixBeaker.y-pa.sy)*pa.progress;
ctx.lineTo(pa.sx+(mixBeaker.x-pa.sx)*pa.progress,cy);ctx.stroke();ctx.globalAlpha=1;
for(let i=0;i<3;i++){let dx=(Math.random()-0.5)*10;
let dy=cy+Math.random()*10;
ctx.beginPath();ctx.arc(pa.sx+(mixBeaker.x-pa.sx)*pa.progress+dx,dy,3,0,Math.PI*2);
ctx.fillStyle=pa.color;ctx.fill()}}
function hexToRgb(h){let r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);return{r,g,b}}
function rgbToHex(r,g,b){return '#'+[r,g,b].map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('')}
function mixColors(c1,c2){let a=hexToRgb(c1),b=hexToRgb(c2);return rgbToHex((a.r+b.r)/2,(a.g+b.g)/2,(a.b+b.b)/2)}
function checkMix(){
let s=selected.map(i=>beakers[i].key).sort().join('+');
let need=[currentMix.a,currentMix.b].sort().join('+');
return s===need}
function draw(){ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🧪 Renk Karıştırma Labı 🧪',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('İki rengi karıştırarak hedef rengi bul!',W/2,230);
ctx.fillText('Üstteki şişelerden ikisine tıkla',W/2,260);
ctx.fillStyle='#a78bfa';roundRect(W/2-80,300,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Harika Kimyager! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';roundRect(W/2-80,310,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';
ctx.fillText('Puan: '+score,W-20,35);
ctx.textAlign='center';ctx.fillStyle='#c084fc';ctx.font='bold 18px Segoe UI';
ctx.fillText('İki şişeye tıklayarak renkleri karıştır!',W/2,75);
beakers.forEach((b,i)=>{let sel=selected.includes(i);drawBeaker(b,sel,i)});
drawTargetArea();drawMixArea();drawPour();
if(correctFlash>0){ctx.globalAlpha=correctFlash;ctx.fillStyle='#22c55e';ctx.font='bold 40px Segoe UI';
ctx.textAlign='center';ctx.fillText('✓ Doğru!',W/2,400);ctx.globalAlpha=1}
if(wrongFlash>0){ctx.globalAlpha=wrongFlash;ctx.fillStyle='#ef4444';ctx.font='bold 40px Segoe UI';
ctx.textAlign='center';ctx.fillText('✗ Tekrar Dene!',W/2,400);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);
ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);
ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);
ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();ctx.fill()}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
if(shakeTimer>0)shakeTimer-=0.05;
if(correctFlash>0)correctFlash-=0.02;
if(wrongFlash>0)wrongFlash-=0.02;
if(round>3)hintAlpha=Math.max(0,hintAlpha-0.003);
if(pourAnim){pourAnim.progress+=0.03;
if(pourAnim.progress>=1){
mixBeaker.level=Math.min(0.7,mixBeaker.level+0.35);
if(selected.length===1){mixBeaker.color=beakers[selected[0]].color}
else if(selected.length===2){mixBeaker.color=mixColors(beakers[selected[0]].color,beakers[selected[1]].color)}
pourAnim=null;
if(selected.length===2){
setTimeout(()=>{
if(checkMix()){score+=10;playSound(true);correctFlash=1;
addParticles(mixBeaker.x,mixBeaker.y,currentMix.color);
addParticles(mixBeaker.x-30,mixBeaker.y-20,currentMix.color);
setTimeout(()=>{round++;if(round>maxRound){state='win'}else{startRound()}},1200)}
else{playSound(false);wrongFlash=1;shakeTimer=1;
setTimeout(()=>{selected=[];mixBeaker.level=0;mixBeaker.color='#666'},800)}
},300)}}}
bubbles.forEach(b=>{b.y+=b.sp*0.1;if(b.y>60)b.y=0});
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';startRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;state='play';startRound()}return}
if(pourAnim||correctFlash>0.5||wrongFlash>0.5)return;
beakers.forEach((b,i)=>{
let dx=mx-b.x,dy=my-b.y;
if(Math.abs(dx)<50&&dy>-10&&dy<140&&!selected.includes(i)&&selected.length<2){
selected.push(i);playSound(true);
pourAnim={sx:b.x,sy:b.y+120,color:b.color,progress:0}}})});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_prek_sci_miknatis_topla_html():
    """Mıknatıs Topla — Mıknatısla nesneleri çekiyor/çekmiyor olarak ayır."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
canvas.width=W;canvas.height=H;
const ctx=canvas.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',round=1,maxRound=10,score=0,particles=[];
let magnet={x:W/2,y:H/2,dragging:false,attached:[]};
let objects=[],sorted=0,totalInRound=0;
let correctFlash=0,wrongFlash=0,fieldLines=[];
const MAGNETIC_ITEMS=[
{name:'Çivi',emoji:'🔩',magnetic:true},{name:'Anahtar',emoji:'🔑',magnetic:true},
{name:'Ataş',emoji:'📎',magnetic:true},{name:'Bozuk Para',emoji:'🪙',magnetic:true},
{name:'Kaşık',emoji:'🥄',magnetic:true},{name:'Makas',emoji:'✂️',magnetic:true},
{name:'İğne',emoji:'🪡',magnetic:true},{name:'Çekiç',emoji:'🔨',magnetic:true}
];
const NON_MAGNETIC_ITEMS=[
{name:'Tahta',emoji:'🪵',magnetic:false},{name:'Silgi',emoji:'🧽',magnetic:false},
{name:'Cam',emoji:'🥛',magnetic:false},{name:'Kâğıt',emoji:'📄',magnetic:false},
{name:'Yaprak',emoji:'🍃',magnetic:false},{name:'Top',emoji:'🏀',magnetic:false},
{name:'Kumaş',emoji:'🧶',magnetic:false},{name:'Plastik',emoji:'🧴',magnetic:false}
];
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addParticles(x,y,clr){for(let i=0;i<15;i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr,r:3+Math.random()*4})}
function shuffle(arr){for(let i=arr.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}return arr}
function startRound(){
let count=Math.min(3+Math.floor(round/3),5);
totalInRound=count;sorted=0;
let pool=[];
let mCount=1+Math.floor(Math.random()*Math.min(count-1,3));
let nmCount=count-mCount;
let mItems=shuffle([...MAGNETIC_ITEMS]).slice(0,mCount);
let nmItems=shuffle([...NON_MAGNETIC_ITEMS]).slice(0,nmCount);
pool=[...mItems,...nmItems];
shuffle(pool);
objects=pool.map((item,i)=>{
let angle=(i/(count))*Math.PI*1.5+0.5;
let cx=W/2+Math.cos(angle)*180;
let cy=H/2+Math.sin(angle)*120;
return{...item,x:cx,y:cy,ox:cx,oy:cy,r:30,attracted:false,sorted:false,attractSpeed:0}});
magnet={x:W/2,y:200,dragging:false,attached:[]}}
function drawMagnet(mx,my){
ctx.save();ctx.translate(mx,my);
ctx.fillStyle='#ef4444';ctx.beginPath();
ctx.moveTo(-25,-30);ctx.lineTo(-25,10);ctx.arc(-12,10,13,Math.PI,0,true);ctx.lineTo(1,-30);ctx.closePath();ctx.fill();
ctx.fillStyle='#3b82f6';ctx.beginPath();
ctx.moveTo(1,-30);ctx.lineTo(1,10);ctx.arc(14,10,13,Math.PI,0,true);ctx.lineTo(27,-30);ctx.closePath();ctx.fill();
ctx.fillStyle='#9ca3af';ctx.fillRect(-25,-30,52,10);
ctx.fillStyle='#fff';ctx.font='bold 11px Segoe UI';ctx.textAlign='center';
ctx.fillText('N',-12,-5);ctx.fillText('S',14,-5);
let near=false;
objects.forEach(o=>{if(!o.sorted&&o.magnetic){
let d=Math.hypot(o.x-mx,o.y-my);if(d<120)near=true}});
if(near){ctx.strokeStyle='#60a5fa40';ctx.lineWidth=1;
for(let i=0;i<6;i++){let a=i*Math.PI/3;
ctx.beginPath();ctx.arc(0,0,40+i*15,a-0.3,a+0.3);ctx.stroke()}}
ctx.restore()}
function drawBaskets(){
ctx.fillStyle='#22c55e20';ctx.strokeStyle='#22c55e';ctx.lineWidth=2;
ctx.fillRect(10,H-130,140,120);ctx.strokeRect(10,H-130,140,120);
ctx.fillStyle='#22c55e';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Çekiyor ✓',80,H-140);
ctx.fillStyle='#ef444420';ctx.strokeStyle='#ef4444';ctx.lineWidth=2;
ctx.fillRect(W-150,H-130,140,120);ctx.strokeRect(W-150,H-130,140,120);
ctx.fillStyle='#ef4444';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Çekmiyor ✗',W-80,H-140)}
function drawObject(o){
if(o.sorted)return;
ctx.save();ctx.translate(o.x,o.y);
ctx.beginPath();ctx.arc(0,0,o.r+5,0,Math.PI*2);
ctx.fillStyle=o.magnetic?'#1e3a5f50':'#3f1d0550';ctx.fill();
ctx.strokeStyle=o.attracted?'#fbbf24':'#94a3b8';ctx.lineWidth=o.attracted?3:1;ctx.stroke();
ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(o.emoji,0,2);
ctx.fillStyle='#e2e8f0';ctx.font='bold 11px Segoe UI';
ctx.fillText(o.name,0,o.r+18);
ctx.restore()}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);
ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);
ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);
ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();ctx.fill()}
function draw(){ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🧲 Mıknatıs Topla 🧲',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Mıknatısı sürükle, nesneleri ayır!',W/2,230);
ctx.fillText('Çekiyorsa sola, çekmiyorsa sağa bırak',W/2,260);
ctx.fillStyle='#a78bfa';roundRect(W/2-80,300,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Süper Bilimci! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';roundRect(W/2-80,310,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';
ctx.fillText('Puan: '+score,W-20,35);
ctx.textAlign='center';ctx.fillStyle='#c084fc';ctx.font='bold 16px Segoe UI';
ctx.fillText('Mıknatısı sürükleyerek nesneleri doğru sepete bırak!',W/2,65);
drawBaskets();
objects.forEach(o=>drawObject(o));
drawMagnet(magnet.x,magnet.y);
if(correctFlash>0){ctx.globalAlpha=correctFlash;ctx.fillStyle='#22c55e';ctx.font='bold 36px Segoe UI';
ctx.textAlign='center';ctx.fillText('✓ Doğru!',W/2,H/2);ctx.globalAlpha=1}
if(wrongFlash>0){ctx.globalAlpha=wrongFlash;ctx.fillStyle='#ef4444';ctx.font='bold 36px Segoe UI';
ctx.textAlign='center';ctx.fillText('✗ Yanlış!',W/2,H/2);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
if(correctFlash>0)correctFlash-=0.02;
if(wrongFlash>0)wrongFlash-=0.02;
if(state==='play'){
objects.forEach(o=>{if(o.sorted)return;
let d=Math.hypot(o.x-magnet.x,o.y-magnet.y);
if(o.magnetic&&d<100&&magnet.dragging){
o.attracted=true;
let angle=Math.atan2(magnet.y-o.y,magnet.x-o.x);
o.attractSpeed=Math.min(o.attractSpeed+0.5,5);
if(d>45){o.x+=Math.cos(angle)*o.attractSpeed;o.y+=Math.sin(angle)*o.attractSpeed}
else{o.x+=(magnet.x+30-o.x)*0.2;o.y+=(magnet.y+30-o.y)*0.2}}
else{o.attracted=false;o.attractSpeed=0;
if(!magnet.dragging){o.x+=(o.ox-o.x)*0.05;o.y+=(o.oy-o.y)*0.05}}});
if(!magnet.dragging){
objects.forEach(o=>{if(o.sorted||!o.attracted)return;
let inLeft=o.x<150&&o.y>H-130;
let inRight=o.x>W-150&&o.y>H-130;
if(inLeft||inRight){
let correct=(inLeft&&o.magnetic)||(inRight&&!o.magnetic);
o.sorted=true;o.attracted=false;sorted++;
if(correct){score+=10;playSound(true);correctFlash=1;addParticles(o.x,o.y,'#22c55e')}
else{playSound(false);wrongFlash=1}
if(sorted>=totalInRound){setTimeout(()=>{round++;if(round>maxRound)state='win';else startRound()},1000)}}})}}
draw();requestAnimationFrame(update)}
function getPos(e){const rect=canvas.getBoundingClientRect();
return{x:(e.clientX-rect.left)*(W/rect.width),y:(e.clientY-rect.top)*(H/rect.height)}}
canvas.addEventListener('mousedown',e=>{const p=getPos(e);
if(state==='start'){if(p.x>W/2-80&&p.x<W/2+80&&p.y>300&&p.y<350){state='play';startRound()}return}
if(state==='win'){if(p.x>W/2-80&&p.x<W/2+80&&p.y>310&&p.y<360){round=1;score=0;state='play';startRound()}return}
if(Math.hypot(p.x-magnet.x,p.y-magnet.y)<50){magnet.dragging=true}});
canvas.addEventListener('mousemove',e=>{if(!magnet.dragging)return;
const p=getPos(e);magnet.x=p.x;magnet.y=p.y});
canvas.addEventListener('mouseup',()=>{magnet.dragging=false});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
const rect=canvas.getBoundingClientRect();
const p={x:(t.clientX-rect.left)*(W/rect.width),y:(t.clientY-rect.top)*(H/rect.height)};
if(state!=='play'){canvas.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));return}
if(Math.hypot(p.x-magnet.x,p.y-magnet.y)<60){magnet.dragging=true}});
canvas.addEventListener('touchmove',e=>{e.preventDefault();if(!magnet.dragging)return;
const t=e.touches[0];const p=getPos(t);magnet.x=p.x;magnet.y=p.y});
canvas.addEventListener('touchend',()=>{magnet.dragging=false});
update();
</script></body></html>"""


def _build_prek_sci_batiyor_mu_html():
    """Batıyor mu Yüzüyor mu? — Nesnelerin suda batıp yüzdüğünü tahmin et."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
canvas.width=W;canvas.height=H;
const ctx=canvas.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',round=1,maxRound=10,score=0,particles=[];
let currentObj=null,phase='guess',dropY=0,dropSpeed=0,bobT=0;
let resultText='',resultAlpha=0,waveT=0,waterBubbles=[];
const OBJECTS=[
{name:'Taş',emoji:'🪨',sinks:true,color:'#78716c'},
{name:'Tahta',emoji:'🪵',sinks:false,color:'#a16207'},
{name:'Top',emoji:'🏐',sinks:false,color:'#f59e0b'},
{name:'Bozuk Para',emoji:'🪙',sinks:true,color:'#eab308'},
{name:'Yaprak',emoji:'🍃',sinks:false,color:'#22c55e'},
{name:'Elma',emoji:'🍎',sinks:false,color:'#ef4444'},
{name:'Anahtar',emoji:'🔑',sinks:true,color:'#f59e0b'},
{name:'Mantar',emoji:'🍄',sinks:false,color:'#a855f7'},
{name:'Tüy',emoji:'🪶',sinks:false,color:'#e2e8f0'},
{name:'Demir Bilye',emoji:'⚫',sinks:true,color:'#6b7280'}
];
let usedIndices=[];
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addParticles(x,y,clr){for(let i=0;i<15;i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr,r:3+Math.random()*4})}
function startRound(){phase='guess';resultText='';resultAlpha=0;
if(usedIndices.length>=OBJECTS.length)usedIndices=[];
let idx;do{idx=Math.floor(Math.random()*OBJECTS.length)}while(usedIndices.includes(idx));
usedIndices.push(idx);
currentObj={...OBJECTS[idx],x:W/2,y:120,targetY:0,settled:false};
dropY=120;dropSpeed=0;
waterBubbles=[];for(let i=0;i<20;i++)
waterBubbles.push({x:Math.random()*W,y:380+Math.random()*270,r:2+Math.random()*5,sp:0.3+Math.random()*0.8,a:Math.random()})}
const WATER_TOP=380;
function drawWater(){
ctx.fillStyle='#1e40af30';ctx.fillRect(0,WATER_TOP,W,H-WATER_TOP);
let wg=ctx.createLinearGradient(0,WATER_TOP,0,H);
wg.addColorStop(0,'#3b82f680');wg.addColorStop(0.5,'#1d4ed880');wg.addColorStop(1,'#1e3a8a90');
ctx.fillStyle=wg;ctx.fillRect(0,WATER_TOP,W,H-WATER_TOP);
ctx.strokeStyle='#60a5fa60';ctx.lineWidth=2;ctx.beginPath();
for(let x=0;x<W;x+=5){let wy=WATER_TOP+Math.sin(waveT+x*0.02)*8+Math.sin(waveT*1.5+x*0.03)*4;
if(x===0)ctx.moveTo(x,wy);else ctx.lineTo(x,wy)}
ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();
ctx.fillStyle='#3b82f640';ctx.fill();ctx.stroke();
waterBubbles.forEach(b=>{b.y-=b.sp;b.a+=0.02;if(b.y<WATER_TOP){b.y=H;b.x=Math.random()*W}
ctx.beginPath();ctx.arc(b.x+Math.sin(b.a)*5,b.y,b.r,0,Math.PI*2);
ctx.fillStyle='#93c5fd30';ctx.fill();ctx.strokeStyle='#93c5fd50';ctx.lineWidth=0.5;ctx.stroke()})}
function drawTank(){
ctx.strokeStyle='#60a5fa80';ctx.lineWidth=3;
ctx.beginPath();ctx.moveTo(30,WATER_TOP-50);ctx.lineTo(30,H-20);
ctx.lineTo(W-30,H-20);ctx.lineTo(W-30,WATER_TOP-50);ctx.stroke();
ctx.fillStyle='#60a5fa';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText('Su Tankı',W/2,H-5)}
function drawCurrentObject(){
if(!currentObj)return;
let dy=currentObj.y;
ctx.save();ctx.translate(currentObj.x,dy);
if(phase==='animate'&&dy>WATER_TOP){
let submerge=Math.min(1,(dy-WATER_TOP)/50);
ctx.globalAlpha=0.7+0.3*(1-submerge)}
ctx.font='50px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(currentObj.emoji,0,0);
ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';
if(phase==='guess')ctx.fillText(currentObj.name,0,40);
ctx.restore()}
function drawButtons(){
if(phase!=='guess')return;
ctx.fillStyle='#ef4444';roundRect(W/2-200,290,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Batıyor 🔽',W/2-120,320);
ctx.fillStyle='#3b82f6';roundRect(W/2+40,290,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';
ctx.fillText('Yüzüyor 🔼',W/2+120,320)}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);
ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);
ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);
ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();ctx.fill()}
function draw(){ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌊 Batıyor mu Yüzüyor mu? 🌊',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Nesne suda batar mı yüzer mi tahmin et!',W/2,230);
ctx.fillStyle='#a78bfa';roundRect(W/2-80,280,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,310);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Harika Deneyci! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';roundRect(W/2-80,310,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
drawWater();drawTank();
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';
ctx.fillText('Puan: '+score,W-20,35);
ctx.textAlign='center';ctx.fillStyle='#c084fc';ctx.font='bold 18px Segoe UI';
if(phase==='guess')ctx.fillText('Bu nesne batar mı yüzer mi?',W/2,75);
drawCurrentObject();drawButtons();
if(resultAlpha>0){ctx.globalAlpha=Math.min(1,resultAlpha);
ctx.fillStyle=resultText.includes('Doğru')?'#22c55e':'#ef4444';
ctx.font='bold 32px Segoe UI';ctx.textAlign='center';
ctx.fillText(resultText,W/2,260);ctx.globalAlpha=1;
let explain=currentObj.sinks?currentObj.name+' ağır, batar!':currentObj.name+' hafif, yüzer!';
ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';
ctx.fillText(explain,W/2,295)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
waveT+=0.03;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
if(resultAlpha>0&&phase==='result')resultAlpha-=0.005;
if(phase==='animate'&&currentObj){
if(currentObj.sinks){
let bottomY=H-60;
if(currentObj.y<bottomY){dropSpeed+=0.15;
if(currentObj.y>WATER_TOP)dropSpeed=Math.min(dropSpeed,2);
currentObj.y+=dropSpeed;
if(currentObj.y>WATER_TOP&&dropSpeed>1){
for(let i=0;i<5;i++)waterBubbles.push({x:currentObj.x-20+Math.random()*40,y:currentObj.y,r:3+Math.random()*4,sp:1+Math.random()*2,a:Math.random()})}}
else{currentObj.y=bottomY;if(!currentObj.settled){currentObj.settled=true;
setTimeout(()=>{phase='result';setTimeout(()=>{round++;if(round>maxRound)state='win';else startRound()},2000)},500)}}}
else{
let floatY=WATER_TOP-10+Math.sin(bobT)*8;
if(currentObj.y<WATER_TOP){dropSpeed+=0.3;currentObj.y+=dropSpeed}
else{bobT+=0.05;currentObj.y+=(floatY-currentObj.y)*0.08;
if(!currentObj.settled&&Math.abs(currentObj.y-floatY)<5){currentObj.settled=true;
addParticles(currentObj.x,WATER_TOP,'#60a5fa');
setTimeout(()=>{phase='result';setTimeout(()=>{round++;if(round>maxRound)state='win';else startRound()},2000)},500)}}}}
if(phase==='result'&&currentObj&&!currentObj.sinks){bobT+=0.04;
currentObj.y=WATER_TOP-10+Math.sin(bobT)*8}
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>280&&my<330){state='play';startRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;usedIndices=[];state='play';startRound()}return}
if(phase!=='guess')return;
let guessSink=false,guessFloat=false;
if(mx>W/2-200&&mx<W/2-40&&my>290&&my<340)guessSink=true;
if(mx>W/2+40&&mx<W/2+200&&my>290&&my<340)guessFloat=true;
if(!guessSink&&!guessFloat)return;
let correct=(guessSink&&currentObj.sinks)||(!guessSink&&!currentObj.sinks);
if(correct){score+=10;playSound(true);resultText='✓ Doğru!';resultAlpha=2;
addParticles(currentObj.x,currentObj.y,'#22c55e')}
else{playSound(false);resultText='✗ Hayır!';resultAlpha=2}
phase='animate';dropSpeed=0;bobT=0;currentObj.settled=false});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_prek_sci_golge_avi_html():
    """Gölge Avı — Işık kaynağını hareket ettirerek hedef gölgeyi yakala."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
canvas.width=W;canvas.height=H;
const ctx=canvas.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',round=1,maxRound=10,score=0,particles=[];
let lightX=350,lightY=60,draggingLight=false;
let currentScene=null,correctFlash=0,matchTimer=0,matched=false;
const GROUND_Y=520;
const SCENES=[
{name:'Ağaç',emoji:'🌳',w:60,h:100,objX:350,targetLightX:200,
drawObj:function(x,y){ctx.font='80px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🌳',x,y)}},
{name:'Ev',emoji:'🏠',w:70,h:80,objX:350,targetLightX:500,
drawObj:function(x,y){ctx.font='70px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🏠',x,y)}},
{name:'Kedi',emoji:'🐱',w:40,h:50,objX:320,targetLightX:180,
drawObj:function(x,y){ctx.font='50px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🐱',x,y)}},
{name:'Çiçek',emoji:'🌻',w:35,h:70,objX:380,targetLightX:550,
drawObj:function(x,y){ctx.font='60px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🌻',x,y)}},
{name:'Araba',emoji:'🚗',w:70,h:45,objX:340,targetLightX:150,
drawObj:function(x,y){ctx.font='55px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🚗',x,y)}},
{name:'Kuş',emoji:'🐦',w:35,h:35,objX:360,targetLightX:480,
drawObj:function(x,y){ctx.font='45px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🐦',x,y)}},
{name:'Mantar',emoji:'🍄',w:40,h:55,objX:330,targetLightX:220,
drawObj:function(x,y){ctx.font='50px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🍄',x,y)}},
{name:'Robot',emoji:'🤖',w:50,h:70,objX:370,targetLightX:530,
drawObj:function(x,y){ctx.font='60px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🤖',x,y)}},
{name:'Tavşan',emoji:'🐰',w:40,h:55,objX:310,targetLightX:160,
drawObj:function(x,y){ctx.font='50px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🐰',x,y)}},
{name:'Kale',emoji:'🏰',w:80,h:90,objX:350,targetLightX:500,
drawObj:function(x,y){ctx.font='75px Segoe UI';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText('🏰',x,y)}}
];
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addParticles(x,y,clr){for(let i=0;i<15;i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr,r:3+Math.random()*4})}
function startRound(){matched=false;matchTimer=0;correctFlash=0;
currentScene=SCENES[(round-1)%SCENES.length];
lightX=350;lightY=60}
function calcShadow(lx,objX,objW,objH){
let dx=objX-lx;
let shadowStretch=1.5+Math.abs(dx)/300;
let shadowX=objX+dx*0.6;
let shadowW=objW*shadowStretch;
if(lx<objX){shadowX=objX+objW*0.3*shadowStretch}
else{shadowX=objX-objW*0.3*shadowStretch}
return{x:shadowX,w:shadowW,h:objH*0.3}}
function drawSun(x,y){
ctx.save();ctx.translate(x,y);
let glow=ctx.createRadialGradient(0,0,15,0,0,60);
glow.addColorStop(0,'#fbbf2480');glow.addColorStop(1,'#fbbf2400');
ctx.fillStyle=glow;ctx.beginPath();ctx.arc(0,0,60,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(0,0,25,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;
for(let i=0;i<8;i++){let a=i*Math.PI/4+performance.now()*0.001;
ctx.beginPath();ctx.moveTo(Math.cos(a)*30,Math.sin(a)*30);
ctx.lineTo(Math.cos(a)*45,Math.sin(a)*45);ctx.stroke()}
ctx.fillStyle='#fff';ctx.font='20px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('☀️',0,0);
ctx.restore()}
function drawRays(lx,ly,objX){
ctx.save();ctx.strokeStyle='#fbbf2415';ctx.lineWidth=1;
for(let i=0;i<12;i++){let angle=Math.atan2(GROUND_Y-ly,objX-lx+i*10-60);
ctx.beginPath();ctx.moveTo(lx,ly);
ctx.lineTo(lx+Math.cos(angle)*600,ly+Math.sin(angle)*600);ctx.stroke()}
ctx.restore()}
function drawShadow(shadow,isTarget){
ctx.save();ctx.translate(shadow.x,GROUND_Y);
if(isTarget){ctx.setLineDash([6,4]);ctx.strokeStyle='#fbbf2480';ctx.lineWidth=2;
ctx.beginPath();ctx.ellipse(0,0,shadow.w,shadow.h,0,0,Math.PI*2);ctx.stroke();
ctx.setLineDash([]);
ctx.fillStyle='#fbbf2415';ctx.beginPath();ctx.ellipse(0,0,shadow.w,shadow.h,0,0,Math.PI*2);ctx.fill()}
else{ctx.fillStyle='#00000060';ctx.beginPath();ctx.ellipse(0,0,shadow.w,shadow.h,0,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='#00000030';ctx.lineWidth=1;
ctx.beginPath();ctx.ellipse(0,0,shadow.w,shadow.h,0,0,Math.PI*2);ctx.stroke()}
ctx.restore()}
function drawGround(){
ctx.fillStyle='#166534';ctx.fillRect(0,GROUND_Y+15,W,H-GROUND_Y-15);
ctx.strokeStyle='#15803d';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(0,GROUND_Y+15);ctx.lineTo(W,GROUND_Y+15);ctx.stroke();
for(let i=0;i<W;i+=40){ctx.beginPath();ctx.moveTo(i,GROUND_Y+15);
ctx.quadraticCurveTo(i+20,GROUND_Y,i+40,GROUND_Y+15);
ctx.fillStyle='#15803d';ctx.fill()}}
function drawSliderTrack(){
ctx.fillStyle='#ffffff15';ctx.fillRect(80,50,W-160,20);
ctx.strokeStyle='#ffffff30';ctx.lineWidth=1;
ctx.strokeRect(80,50,W-160,20);
ctx.fillStyle='#fbbf24';ctx.font='12px Segoe UI';ctx.textAlign='left';
ctx.fillText('← Güneşi sürükle →',90,45)}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);
ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);
ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);
ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();ctx.fill()}
function draw(){ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🔦 Gölge Avı 🔦',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Güneşi hareket ettirerek gölgeyi',W/2,230);
ctx.fillText('hedef gölgeyle eşleştir!',W/2,260);
ctx.fillStyle='#a78bfa';roundRect(W/2-80,300,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Gölge Ustası! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';roundRect(W/2-80,310,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
drawGround();drawSliderTrack();
let sc=currentScene;
let targetShadow=calcShadow(sc.targetLightX,sc.objX,sc.w,sc.h);
drawShadow(targetShadow,true);
let currentShadow=calcShadow(lightX,sc.objX,sc.w,sc.h);
drawShadow(currentShadow,false);
drawRays(lightX,lightY,sc.objX);
sc.drawObj(sc.objX,GROUND_Y);
drawSun(lightX,lightY);
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,100);ctx.textAlign='right';
ctx.fillText('Puan: '+score,W-20,100);
ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';
ctx.fillText(sc.name+' '+sc.emoji,W/2,120);
let overlap=Math.abs(currentShadow.x-targetShadow.x);
let maxDist=200;
let matchPct=Math.max(0,Math.round((1-overlap/maxDist)*100));
ctx.fillStyle=matchPct>80?'#22c55e':matchPct>50?'#fbbf24':'#ef4444';
ctx.font='bold 16px Segoe UI';
ctx.fillText('Eşleşme: %'+matchPct,W/2,GROUND_Y+50);
let barW=200;
ctx.fillStyle='#ffffff20';ctx.fillRect(W/2-barW/2,GROUND_Y+55,barW,12);
ctx.fillStyle=matchPct>80?'#22c55e':matchPct>50?'#fbbf24':'#ef4444';
ctx.fillRect(W/2-barW/2,GROUND_Y+55,barW*matchPct/100,12);
if(correctFlash>0){ctx.globalAlpha=correctFlash;ctx.fillStyle='#22c55e';ctx.font='bold 40px Segoe UI';
ctx.fillText('✓ Mükemmel!',W/2,300);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
if(correctFlash>0)correctFlash-=0.015;
if(state==='play'&&currentScene&&!matched){
let targetShadow=calcShadow(currentScene.targetLightX,currentScene.objX,currentScene.w,currentScene.h);
let currentShadow=calcShadow(lightX,currentScene.objX,currentScene.w,currentScene.h);
let overlap=Math.abs(currentShadow.x-targetShadow.x);
let tolerance=25+round*(-1);
if(tolerance<10)tolerance=10;
if(overlap<tolerance){matchTimer++;
if(matchTimer>30){matched=true;score+=10;playSound(true);correctFlash=1.5;
addParticles(currentScene.objX,GROUND_Y-50,'#fbbf24');
addParticles(lightX,lightY,'#fbbf24');
setTimeout(()=>{round++;if(round>maxRound)state='win';else startRound()},1500)}}
else{matchTimer=Math.max(0,matchTimer-1)}}
draw();requestAnimationFrame(update)}
function getPos(e){const rect=canvas.getBoundingClientRect();
return{x:(e.clientX-rect.left)*(W/rect.width),y:(e.clientY-rect.top)*(H/rect.height)}}
canvas.addEventListener('mousedown',e=>{const p=getPos(e);
if(state==='start'){if(p.x>W/2-80&&p.x<W/2+80&&p.y>300&&p.y<350){state='play';startRound()}return}
if(state==='win'){if(p.x>W/2-80&&p.x<W/2+80&&p.y>310&&p.y<360){round=1;score=0;state='play';startRound()}return}
if(Math.hypot(p.x-lightX,p.y-lightY)<50){draggingLight=true}});
canvas.addEventListener('mousemove',e=>{if(!draggingLight)return;
const p=getPos(e);lightX=Math.max(80,Math.min(W-80,p.x))});
canvas.addEventListener('mouseup',()=>{draggingLight=false});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
const p=getPos(t);
if(state!=='play'){canvas.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));return}
if(Math.hypot(p.x-lightX,p.y-lightY)<60){draggingLight=true}});
canvas.addEventListener('touchmove',e=>{e.preventDefault();if(!draggingLight)return;
const t=e.touches[0];const p=getPos(t);lightX=Math.max(80,Math.min(W-80,p.x))});
canvas.addEventListener('touchend',()=>{draggingLight=false});
update();
</script></body></html>"""


def _build_prek_sci_ruzgar_ufle_html():
    """Rüzgâr Üfle — Rüzgârla yelkenliyi engelleri aşarak hedefe ulaştır."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
canvas.width=W;canvas.height=H;
const ctx=canvas.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',round=1,maxRound=10,score=0,particles=[];
let blowing=false,boat={x:80,y:0,speed:0,angle:0},scrollX=0;
let obstacles=[],finishX=1200,windLines=[];
let clouds=[],waves=[{amp:4},{amp:5},{amp:3},{amp:6},{amp:4}],hitFlash=0,winAnim=0;
let levelTime=0,hits=0,boatBob=0;
const WATER_Y=420;
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addParticles(x,y,clr){for(let i=0;i<15;i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr,r:3+Math.random()*4})}
function startLevel(){
boat={x:80,y:WATER_Y-30,speed:0,angle:0};scrollX=0;blowing=false;
hits=0;levelTime=0;winAnim=0;hitFlash=0;
finishX=800+round*120;
obstacles=[];
let obsCount=2+round;
for(let i=0;i<obsCount;i++){
let ox=250+i*(finishX-300)/obsCount+Math.random()*60-30;
let type=Math.random()<0.5?'rock':'whirlpool';
obstacles.push({x:ox,y:WATER_Y-10-Math.random()*20,type:type,r:20+Math.random()*10,rot:0,active:true})}
clouds=[];for(let i=0;i<6;i++)
clouds.push({x:Math.random()*finishX*1.5,y:50+Math.random()*120,w:60+Math.random()*80,speed:0.2+Math.random()*0.3});
waves=[];for(let i=0;i<30;i++)
waves.push({x:i*50,phase:Math.random()*Math.PI*2,amp:3+Math.random()*5});
windLines=[]}
function drawSky(){
let g=ctx.createLinearGradient(0,0,0,WATER_Y);
g.addColorStop(0,'#1e1b4b');g.addColorStop(1,'#312e81');
ctx.fillStyle=g;ctx.fillRect(0,0,W,WATER_Y)}
function drawWaterBg(){
let g=ctx.createLinearGradient(0,WATER_Y,0,H);
g.addColorStop(0,'#1d4ed8');g.addColorStop(0.5,'#1e40af');g.addColorStop(1,'#1e3a8a');
ctx.fillStyle=g;ctx.fillRect(0,WATER_Y,W,H-WATER_Y);
ctx.strokeStyle='#60a5fa30';ctx.lineWidth=1;
let t=performance.now()*0.002;
for(let row=0;row<5;row++){ctx.beginPath();
for(let x=0;x<W;x+=3){let wy=WATER_Y+20+row*30+Math.sin(t+x*0.02+row)*waves[row%waves.length].amp;
if(x===0)ctx.moveTo(x,wy);else ctx.lineTo(x,wy)}
ctx.stroke()}}
function drawWaves(){
ctx.strokeStyle='#93c5fd50';ctx.lineWidth=2;
let t=performance.now()*0.003;
ctx.beginPath();
for(let x=0;x<W;x+=3){let wy=WATER_Y+Math.sin(t+x*0.015)*6+Math.sin(t*0.7+x*0.025)*4;
if(x===0)ctx.moveTo(x,wy);else ctx.lineTo(x,wy)}
ctx.stroke()}
function drawClouds(){
clouds.forEach(c=>{
let sx=c.x-scrollX*0.3;
if(sx<-c.w)sx+=finishX*1.5+c.w;
if(sx>W+c.w)return;
ctx.fillStyle='#ffffff15';
ctx.beginPath();ctx.ellipse(sx,c.y,c.w/2,20,0,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.ellipse(sx-15,c.y-10,c.w/3,15,0,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.ellipse(sx+15,c.y-8,c.w/3,18,0,0,Math.PI*2);ctx.fill()})}
function drawBoat(){
let bx=boat.x-scrollX;
let by=boat.y+Math.sin(boatBob)*5;
ctx.save();ctx.translate(bx,by);
ctx.fillStyle='#92400e';ctx.beginPath();
ctx.moveTo(-30,0);ctx.lineTo(-25,20);ctx.lineTo(35,20);ctx.lineTo(40,0);
ctx.quadraticCurveTo(40,-5,30,-5);ctx.lineTo(-25,-5);ctx.quadraticCurveTo(-30,-5,-30,0);
ctx.closePath();ctx.fill();
ctx.strokeStyle='#78350f';ctx.lineWidth=1;ctx.stroke();
ctx.strokeStyle='#a16207';ctx.lineWidth=3;
ctx.beginPath();ctx.moveTo(5,-5);ctx.lineTo(5,-60);ctx.stroke();
let sailPuff=blowing?15:5;
ctx.fillStyle='#111827';ctx.beginPath();
ctx.moveTo(5,-55);ctx.quadraticCurveTo(5+sailPuff+boat.speed*3,-35,5,-10);ctx.closePath();ctx.fill();
ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1;ctx.stroke();
ctx.fillStyle='#ef4444';ctx.beginPath();
ctx.moveTo(5,-60);ctx.lineTo(15,-55);ctx.lineTo(5,-50);ctx.closePath();ctx.fill();
ctx.restore()}
function drawObstacles(){
obstacles.forEach(o=>{
if(!o.active)return;
let ox=o.x-scrollX;
if(ox<-50||ox>W+50)return;
if(o.type==='rock'){
ctx.fillStyle='#6b7280';ctx.beginPath();
ctx.moveTo(ox-o.r,WATER_Y+5);ctx.lineTo(ox-o.r*0.7,WATER_Y-o.r);
ctx.lineTo(ox-o.r*0.2,WATER_Y-o.r*1.3);ctx.lineTo(ox+o.r*0.3,WATER_Y-o.r*0.9);
ctx.lineTo(ox+o.r*0.8,WATER_Y-o.r*0.4);ctx.lineTo(ox+o.r,WATER_Y+5);
ctx.closePath();ctx.fill();
ctx.strokeStyle='#9ca3af';ctx.lineWidth=1;ctx.stroke();
ctx.font='20px Segoe UI';ctx.textAlign='center';ctx.fillText('🪨',ox,WATER_Y-o.r*0.5)}
else{o.rot+=0.05;
ctx.save();ctx.translate(ox,WATER_Y+5);
ctx.strokeStyle='#7c3aed60';ctx.lineWidth=2;
for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(0,0,o.r-i*6,o.rot+i,o.rot+i+4);ctx.stroke()}
ctx.font='24px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('🌀',0,0);ctx.restore()}})}
function drawFinish(){
let fx=finishX-scrollX;
if(fx<0||fx>W+50)return;
ctx.strokeStyle='#22c55e';ctx.lineWidth=3;ctx.setLineDash([10,5]);
ctx.beginPath();ctx.moveTo(fx,WATER_Y-80);ctx.lineTo(fx,WATER_Y+30);ctx.stroke();
ctx.setLineDash([]);
ctx.fillStyle='#22c55e';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏁 Bitiş',fx,WATER_Y-90);
ctx.font='30px Segoe UI';ctx.fillText('🚩',fx,WATER_Y-60)}
function drawWindButton(){
let bx=60,by=H-80,br=45;
ctx.save();ctx.translate(bx,by);
let g=ctx.createRadialGradient(0,0,10,0,0,br);
g.addColorStop(0,blowing?'#60a5fa':'#475569');
g.addColorStop(1,blowing?'#3b82f6':'#334155');
ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,0,br,0,Math.PI*2);ctx.fill();
ctx.strokeStyle=blowing?'#93c5fd':'#64748b';ctx.lineWidth=3;
ctx.beginPath();ctx.arc(0,0,br,0,Math.PI*2);ctx.stroke();
ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('💨',0,-2);
ctx.fillStyle='#e2e8f0';ctx.font='bold 12px Segoe UI';
ctx.fillText(blowing?'Üflüyor!':'Bas & Üfle',0,br+15);
ctx.restore()}
function drawWindLines(){
if(!blowing)return;
let bx=boat.x-scrollX;
for(let i=windLines.length;i<8;i++){
windLines.push({x:bx-60-Math.random()*40,y:boat.y-30+Math.random()*50,len:20+Math.random()*30,life:1})}
windLines.forEach(wl=>{
ctx.strokeStyle='rgba(147,197,253,'+wl.life+')';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(wl.x,wl.y);ctx.lineTo(wl.x+wl.len,wl.y);
let arr=wl.x+wl.len;ctx.moveTo(arr,wl.y);ctx.lineTo(arr-6,wl.y-4);ctx.moveTo(arr,wl.y);ctx.lineTo(arr-6,wl.y+4);
ctx.stroke()})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);
ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);
ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);
ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();ctx.fill()}
function draw(){ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){
drawSky();drawWaterBg();drawWaves();
ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('⛵ Rüzgâr Üfle ⛵',W/2,160);ctx.font='20px Segoe UI';
ctx.fillText('Rüzgâr düğmesine basarak yelkenliyi',W/2,210);
ctx.fillText('engelleri aşarak hedefe ulaştır!',W/2,240);
ctx.fillStyle='#a78bfa';roundRect(W/2-80,280,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,310);return}
if(state==='win'){
drawSky();drawWaterBg();drawWaves();
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Kaptan Süper! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';roundRect(W/2-80,310,160,50,12);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
drawSky();drawClouds();drawWaterBg();drawWaves();
drawFinish();drawObstacles();drawBoat();drawWindLines();drawWindButton();
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
ctx.fillText('Seviye: '+round+'/'+maxRound,15,30);ctx.textAlign='right';
ctx.fillText('Puan: '+score,W-15,30);
ctx.textAlign='center';
let progress=Math.min(100,Math.round((boat.x/finishX)*100));
ctx.fillStyle='#ffffff20';ctx.fillRect(W/2-100,45,200,10);
ctx.fillStyle='#22c55e';ctx.fillRect(W/2-100,45,progress*2,10);
ctx.fillStyle='#e2e8f0';ctx.font='12px Segoe UI';
ctx.fillText(progress+'%',W/2,42);
if(hitFlash>0){ctx.globalAlpha=hitFlash;ctx.fillStyle='#ef4444';
ctx.fillRect(0,0,W,H);ctx.globalAlpha=1;
ctx.fillStyle='#fff';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';
ctx.fillText('💥 Engel!',W/2,H/2)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
if(hitFlash>0)hitFlash-=0.03;
boatBob+=0.04;
if(state==='play'){
levelTime++;
if(blowing){boat.speed=Math.min(boat.speed+0.15,3+round*0.2)}
else{boat.speed=Math.max(boat.speed-0.08,0)}
boat.x+=boat.speed;
scrollX=Math.max(0,boat.x-200);
windLines.forEach(wl=>{wl.x+=4;wl.life-=0.03});
windLines=windLines.filter(wl=>wl.life>0);
let bx=boat.x;
obstacles.forEach(o=>{if(!o.active)return;
let d=Math.hypot(bx-o.x,boat.y-(o.y));
if(d<o.r+25){o.active=false;hits++;hitFlash=1;playSound(false);
boat.speed=Math.max(0,boat.speed-2);
boat.x=Math.max(boat.x-30,80)}});
if(boat.x>=finishX){
let timeBonus=Math.max(0,100-Math.floor(levelTime/60)*10);
let hitPenalty=hits*5;
let roundScore=Math.max(0,10+Math.floor(timeBonus/10)-hitPenalty);
score+=roundScore;playSound(true);
addParticles(boat.x-scrollX,boat.y,'#22c55e');
addParticles(boat.x-scrollX+20,boat.y-20,'#fbbf24');
setTimeout(()=>{round++;if(round>maxRound)state='win';else startLevel()},1500);
state='levelclear'}
clouds.forEach(c=>{c.x+=c.speed})}
draw();requestAnimationFrame(update)}
function getPos(e){const rect=canvas.getBoundingClientRect();
return{x:(e.clientX-rect.left)*(W/rect.width),y:(e.clientY-rect.top)*(H/rect.height)}}
function checkStartWin(p){
if(state==='start'){if(p.x>W/2-80&&p.x<W/2+80&&p.y>280&&p.y<330){state='play';startLevel()}return true}
if(state==='win'){if(p.x>W/2-80&&p.x<W/2+80&&p.y>310&&p.y<360){round=1;score=0;state='play';startLevel()}return true}
return false}
function isWindBtn(p){return Math.hypot(p.x-60,p.y-(H-80))<50}
canvas.addEventListener('mousedown',e=>{const p=getPos(e);
if(checkStartWin(p))return;
if(state==='play'&&isWindBtn(p)){blowing=true}});
canvas.addEventListener('mouseup',()=>{blowing=false});
canvas.addEventListener('mouseleave',()=>{blowing=false});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const p=getPos(t);
if(checkStartWin(p))return;
if(state==='play'&&isWindBtn(p)){blowing=true}});
canvas.addEventListener('touchend',e=>{e.preventDefault();blowing=false});
canvas.addEventListener('touchcancel',()=>{blowing=false});
update();
</script></body></html>"""
