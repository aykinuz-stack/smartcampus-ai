# -*- coding: utf-8 -*-
"""Okul Öncesi Eğlenceli Matematik Oyunları — 20 Premium HTML5 Oyun."""


def _build_prek_math_sayi_bahcesi_html():
    """Sayı Bahçesi — Çiçeklere dokunarak 1-10 arası sayma."""
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
let flowers=[],round=1,maxRound=10,nextTap=1,maxNum=5,score=0,particles=[];
let state='start',correct=0;
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;
o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();
if(ok){setTimeout(()=>{o.frequency.value=659},100)}
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function spawnFlowers(){maxNum=Math.min(3+round*2,12);flowers=[];
for(let i=0;i<maxNum;i++){
let x,y,ok=false;
while(!ok){x=60+Math.random()*(W-120);y=200+Math.random()*(H-300);
ok=flowers.every(f=>Math.hypot(f.x-x,f.y-y)>70)}
flowers.push({x,y,num:i+1,tapped:false,scale:1,bloom:0,clr:COLORS[i%COLORS.length]})}}
function addParticles(x,y,clr){for(let i=0;i<15;i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr,r:3+Math.random()*4})}
function drawFlower(f){ctx.save();ctx.translate(f.x,f.y);ctx.scale(f.scale,f.scale);
const petals=6,pr=22+f.bloom*8;
for(let i=0;i<petals;i++){const a=i*Math.PI*2/petals;
ctx.beginPath();ctx.ellipse(Math.cos(a)*pr*0.6,Math.sin(a)*pr*0.6,pr*0.5,pr*0.3,a,0,Math.PI*2);
ctx.fillStyle=f.tapped?f.clr+'90':f.clr;ctx.fill();ctx.strokeStyle='#fff3';ctx.lineWidth=1;ctx.stroke()}
ctx.beginPath();ctx.arc(0,0,14,0,Math.PI*2);ctx.fillStyle=f.tapped?'#fbbf24':'#7c3aed';ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(f.num,0,1);ctx.restore()}
function draw(){ctx.clearRect(0,0,W,H);
// sky
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
// grass
ctx.fillStyle='#166534';ctx.fillRect(0,H-80,W,80);
ctx.fillStyle='#15803d';ctx.beginPath();
for(let i=0;i<W;i+=30){ctx.moveTo(i,H-80);ctx.quadraticCurveTo(i+15,H-110,i+30,H-80)}
ctx.fill();
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌸 Sayı Bahçesi 🌸',W/2,180);ctx.font='22px Segoe UI';
ctx.fillText('Çiçeklere sırayla dokun: 1, 2, 3...',W/2,240);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,300,160,50);ctx.borderRadius=12;
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Tebrikler! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
// HUD
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';
ctx.fillText('Puan: '+score,W-20,35);ctx.textAlign='center';
ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';
ctx.fillText('Sıradaki: '+nextTap,W/2,35);
flowers.forEach(f=>drawFlower(f));
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
flowers.forEach(f=>{if(f.tapped&&f.bloom<1)f.bloom+=0.05});
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';spawnFlowers()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;nextTap=1;state='play';spawnFlowers()}return}
flowers.forEach(f=>{if(!f.tapped&&Math.hypot(mx-f.x,my-f.y)<30){
if(f.num===nextTap){f.tapped=true;f.scale=1.3;setTimeout(()=>f.scale=1,200);
score+=10;addParticles(f.x,f.y,f.clr);playSound(true);nextTap++;
if(nextTap>maxNum){round++;nextTap=1;if(round>maxRound)state='win';else setTimeout(()=>spawnFlowers(),800)}}
else{playSound(false);f.scale=0.8;setTimeout(()=>f.scale=1,200)}}})});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_prek_math_balon_patlat_html():
    """Balon Patlat — Hedef sayıyı gösteren balonları patlat."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const COLORS=['#ef4444','#f59e0b','#10b981','#3b82f6','#8b5cf6','#ec4899','#06b6d4','#f97316'];
let balloons=[],target=0,lives=3,score=0,round=0,maxRounds=10,state='start',particles=[],popAnim=[];
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function nextRound(){round++;if(round>maxRounds){state='win';return}
target=1+Math.floor(Math.random()*9);balloons=[];
for(let i=0;i<8;i++){let n=Math.random()<0.4?target:1+Math.floor(Math.random()*9);
balloons.push({x:50+Math.random()*(W-100),y:H+40+Math.random()*200,
num:n,clr:COLORS[i%COLORS.length],r:32,spd:0.5+Math.random()*1.2+round*0.15,wobble:Math.random()*Math.PI*2,alive:true})}}
function addPop(x,y,clr){for(let i=0;i<12;i++)
particles.push({x,y,vx:(Math.random()-0.5)*8,vy:(Math.random()-0.5)*8,life:1,clr,r:3+Math.random()*3})}
function draw(){ctx.clearRect(0,0,W,H);
const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');
ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎈 Balon Patlat 🎈',W/2,200);ctx.font='20px Segoe UI';
ctx.fillText('Hedef sayıyı gösteren balonları patlat!',W/2,260);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Harika! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
if(state==='lose'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('😢 Canın Bitti!',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
// HUD
ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';
ctx.fillText('Hedef: '+target,W/2,40);ctx.fillStyle='#e9d5ff';ctx.font='18px Segoe UI';
ctx.textAlign='left';ctx.fillText('❤️'.repeat(lives),15,35);
ctx.textAlign='right';ctx.fillText('Puan: '+score+'  Tur: '+round+'/'+maxRounds,W-15,35);
balloons.forEach(b=>{if(!b.alive)return;ctx.save();
b.wobble+=0.03;const wx=Math.sin(b.wobble)*8;
ctx.translate(b.x+wx,b.y);
// string
ctx.strokeStyle='#fff5';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(0,b.r);ctx.lineTo(0,b.r+30);ctx.stroke();
// balloon
ctx.beginPath();ctx.ellipse(0,0,b.r,b.r*1.2,0,0,Math.PI*2);ctx.fillStyle=b.clr;ctx.fill();
ctx.strokeStyle='#fff3';ctx.lineWidth=2;ctx.stroke();
// shine
ctx.beginPath();ctx.ellipse(-8,-10,6,10,-.3,0,Math.PI*2);ctx.fillStyle='#fff3';ctx.fill();
// number
ctx.fillStyle='#fff';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(b.num,0,0);ctx.restore()});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){if(state==='play'){
balloons.forEach(b=>{if(b.alive){b.y-=b.spd;if(b.y<-50)b.alive=false}});
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.15});
particles=particles.filter(p=>p.life>0);
if(balloons.every(b=>!b.alive))nextRound()}
draw();requestAnimationFrame(update)}
cv.addEventListener('click',e=>{const rect=cv.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';lives=3;score=0;round=0;nextRound()}return}
if(state==='win'||state==='lose'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';lives=3;score=0;round=0;nextRound()}return}
balloons.forEach(b=>{if(!b.alive)return;const wx=Math.sin(b.wobble)*8;
if(Math.hypot(mx-(b.x+wx),my-b.y)<b.r*1.2){b.alive=false;addPop(b.x,b.y,b.clr);
if(b.num===target){score+=10;playSound(true)}else{lives--;playSound(false);if(lives<=0)state='lose'}}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_prek_math_sekil_avi_html():
    """Şekil Avı — Düşen şekilleri yakala."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const SHAPES=['daire','kare','ucgen','dikdortgen','yildiz','kalp'];
const SHAPE_TR={'daire':'Daire','kare':'Kare','ucgen':'Üçgen','dikdortgen':'Dikdörtgen','yildiz':'Yıldız','kalp':'Kalp'};
const SHAPE_EMO={'daire':'⭕','kare':'🟦','ucgen':'🔺','dikdortgen':'🟧','yildiz':'⭐','kalp':'❤️'};
const CLRS=['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#ec4899'];
let shapes=[],target='',score=0,misses=0,maxMiss=5,timer=60,state='start',particles=[],spawnT=0,spd=1.5,level=1,nextLvl=50,lvlFlash=0;
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function drawShape(x,y,type,sz,clr){ctx.fillStyle=clr;ctx.beginPath();
if(type==='daire'){ctx.arc(x,y,sz,0,Math.PI*2);ctx.fill()}
else if(type==='kare'){ctx.fillRect(x-sz,y-sz,sz*2,sz*2)}
else if(type==='ucgen'){ctx.moveTo(x,y-sz);ctx.lineTo(x+sz,y+sz);ctx.lineTo(x-sz,y+sz);ctx.closePath();ctx.fill()}
else if(type==='dikdortgen'){ctx.fillRect(x-sz*1.3,y-sz*0.7,sz*2.6,sz*1.4)}
else if(type==='yildiz'){for(let i=0;i<5;i++){const a=i*Math.PI*2/5-Math.PI/2;
const a2=a+Math.PI/5;ctx.lineTo(x+Math.cos(a)*sz,y+Math.sin(a)*sz);
ctx.lineTo(x+Math.cos(a2)*sz*0.4,y+Math.sin(a2)*sz*0.4)}ctx.closePath();ctx.fill()}
else if(type==='kalp'){const s=sz*0.6;ctx.moveTo(x,y+s);ctx.bezierCurveTo(x-s*2,y-s,x,y-s*2,x,y-s*0.5);
ctx.bezierCurveTo(x,y-s*2,x+s*2,y-s,x,y+s);ctx.fill()}}
function spawn(){const type=SHAPES[Math.floor(Math.random()*SHAPES.length)];
shapes.push({x:40+Math.random()*(W-80),y:-30,type,sz:20+Math.random()*8,
clr:CLRS[Math.floor(Math.random()*CLRS.length)],spd:spd+Math.random()*0.8,alive:true})}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c,r:3+Math.random()*3})}
function startGame(){state='play';score=0;misses=0;timer=60;shapes=[];spd=1.5;level=1;nextLvl=50;lvlFlash=0;
target=SHAPES[Math.floor(Math.random()*SHAPES.length)]}
function draw(){ctx.clearRect(0,0,W,H);
const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');
ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🔍 Şekil Avı 🔍',W/2,200);ctx.font='20px Segoe UI';
ctx.fillText('Hedef şekli yakala, diğerlerine dokunma!',W/2,260);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText(misses>=maxMiss?'⏰ Süre/Can Bitti!':'🎉 Süper!',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
// HUD
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
ctx.fillText('Hedef: '+SHAPE_EMO[target]+' '+SHAPE_TR[target],W/2,35);
ctx.fillStyle='#e9d5ff';ctx.font='18px Segoe UI';ctx.textAlign='left';
ctx.fillText('⏱️ '+Math.ceil(timer)+'s  Sv:'+level,15,35);ctx.textAlign='right';
ctx.fillText('Puan:'+score+'  ❌'+misses+'/'+maxMiss,W-15,35);
if(lvlFlash>0){ctx.fillStyle='#fbbf24';ctx.font='bold 30px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=lvlFlash/60;ctx.fillText('⬆️ Seviye '+level+'!',W/2,80);ctx.globalAlpha=1}
// deadline
ctx.strokeStyle='#ef444480';ctx.lineWidth=2;ctx.setLineDash([5,5]);
ctx.beginPath();ctx.moveTo(0,H-60);ctx.lineTo(W,H-60);ctx.stroke();ctx.setLineDash([]);
shapes.forEach(s=>{if(s.alive)drawShape(s.x,s.y,s.type,s.sz,s.clr)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function update(t){const dt=t-lastT;lastT=t;if(state==='play'){
timer-=dt/1000;if(lvlFlash>0)lvlFlash--;spawnT+=dt;if(spawnT>Math.max(400,800-level*50)){spawn();spawnT=0}
spd=1.5+level*0.5+score*0.01;
shapes.forEach(s=>{if(s.alive){s.y+=s.spd;if(s.y>H-40){s.alive=false;if(s.type===target)misses++}}});
shapes=shapes.filter(s=>s.alive||s.y<H+50);
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.03;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
if(timer<=0||misses>=maxMiss)state='end'}
draw();requestAnimationFrame(update)}
cv.addEventListener('click',e=>{const rect=cv.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360)startGame();return}
for(let i=shapes.length-1;i>=0;i--){const s=shapes[i];if(!s.alive)continue;
if(Math.hypot(mx-s.x,my-s.y)<s.sz+10){s.alive=false;addP(s.x,s.y,s.clr);
if(s.type===target){score+=10;playSound(true);if(score>=nextLvl){level++;nextLvl+=40+level*15;target=SHAPES[Math.floor(Math.random()*SHAPES.length)];spd+=0.4;maxMiss=Math.min(maxMiss+1,8);lvlFlash=60}}else{misses++;playSound(false)}break}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
requestAnimationFrame(update);
</script></body></html>"""


def _build_prek_math_renk_sekil_eslestir_html():
    """Renk-Şekil Eşleştir — Renkli şekilleri sürükle-bırak eşleştirme."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const CLRS=['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#ec4899'];
const SHAPES=['circle','square','triangle','star'];
let pieces=[],targets=[],dragging=null,dx=0,dy=0,score=0,level=1,maxLevel=8,matched=0,state='start',particles=[];
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function drawSh(x,y,type,sz,fill,stroke){ctx.beginPath();
if(type==='circle'){ctx.arc(x,y,sz,0,Math.PI*2)}
else if(type==='square'){ctx.rect(x-sz,y-sz,sz*2,sz*2)}
else if(type==='triangle'){ctx.moveTo(x,y-sz);ctx.lineTo(x+sz,y+sz);ctx.lineTo(x-sz,y+sz);ctx.closePath()}
else if(type==='star'){for(let i=0;i<5;i++){const a=i*Math.PI*2/5-Math.PI/2,a2=a+Math.PI/5;
ctx.lineTo(x+Math.cos(a)*sz,y+Math.sin(a)*sz);ctx.lineTo(x+Math.cos(a2)*sz*0.4,y+Math.sin(a2)*sz*0.4)}ctx.closePath()}
if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=3;ctx.setLineDash([6,4]);ctx.stroke();ctx.setLineDash([])}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c,r:3+Math.random()*3})}
function setupLevel(){pieces=[];targets=[];matched=0;
const cnt=Math.min(3+level,6);
const usedShapes=[...SHAPES].sort(()=>Math.random()-.5).slice(0,cnt);
const usedClrs=[...CLRS].sort(()=>Math.random()-.5).slice(0,cnt);
for(let i=0;i<cnt;i++){
targets.push({x:480+Math.random()*120,y:100+i*(H-150)/cnt+Math.random()*20,shape:usedShapes[i],clr:usedClrs[i],matched:false});
pieces.push({x:50+Math.random()*120,y:100+i*(H-150)/cnt+Math.random()*20,shape:usedShapes[i],clr:usedClrs[i],matched:false,ox:0,oy:0});}
pieces.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);
const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');
ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎨 Renk-Şekil Eşleştir 🎨',W/2,200);ctx.font='20px Segoe UI';
ctx.fillText('Şekilleri doğru yere sürükle!',W/2,260);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏆 Tebrikler! 🏆',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Seviye: '+level+'/'+maxLevel+'  Puan: '+score,W/2,35);
targets.forEach(t=>{if(!t.matched)drawSh(t.x,t.y,t.shape,25,null,t.clr+'80');
else drawSh(t.x,t.y,t.shape,25,t.clr+'60',t.clr)});
pieces.forEach(p=>{if(!p.matched)drawSh(p.x,p.y,p.shape,22,p.clr,null)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(update)}
function getPos(e){const r=cv.getBoundingClientRect();
return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=getPos(e);
if(state!=='play')return;
for(let i=pieces.length-1;i>=0;i--){const p=pieces[i];if(p.matched)continue;
if(Math.hypot(m.x-p.x,m.y-p.y)<30){dragging=p;dx=m.x-p.x;dy=m.y-p.y;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=getPos(e);dragging.x=m.x-dx;dragging.y=m.y-dy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;
targets.forEach(t=>{if(!t.matched&&t.shape===dragging.shape&&t.clr===dragging.clr&&Math.hypot(dragging.x-t.x,dragging.y-t.y)<50){
t.matched=true;dragging.matched=true;dragging.x=t.x;dragging.y=t.y;score+=15;matched++;
addP(t.x,t.y,t.clr);playSound(true);
if(matched>=targets.length){level++;if(level>maxLevel)state='win';else setTimeout(setupLevel,600)}}});dragging=null});
cv.addEventListener('click',e=>{const m=getPos(e);
if(state==='start'||state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){
state='play';score=0;level=1;setupLevel()}}});
// touch
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',e=>{cv.dispatchEvent(new MouseEvent('mouseup',{}))});
update();
</script></body></html>"""


def _build_prek_math_oruntu_treni_html():
    """Örüntü Treni — Deseni tamamla, tren ilerlesin."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const ITEMS=['🔴','🔵','🟡','🟢','🟣','🟠','⭐','💎','🌙','❤️'];
let pattern=[],shown=[],options=[],answer='',level=1,maxLevel=10,score=0,state='start';
let trainX=0,targetX=0,particles=[],smoke=[];
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function genLevel(){const pLen=Math.min(2+Math.floor(level/3),4);
const pool=ITEMS.sort(()=>Math.random()-.5).slice(0,pLen);
pattern=[];for(let i=0;i<pLen;i++)pattern.push(pool[i]);
shown=[];const reps=3+Math.floor(level/3);
for(let i=0;i<reps;i++)shown.push(pattern[i%pattern.length]);
answer=pattern[shown.length%pattern.length];shown.push('❓');
const opts=[answer];while(opts.length<4){const r=ITEMS[Math.floor(Math.random()*ITEMS.length)];
if(!opts.includes(r))opts.push(r)}options=opts.sort(()=>Math.random()-.5);
targetX=level*60}
function addSmoke(){smoke.push({x:trainX+20,y:340,r:5,life:1,vy:-1-Math.random(),vx:Math.random()*2})}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,r:3+Math.random()*3})}
function draw(){ctx.clearRect(0,0,W,H);
const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');
ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🚂 Örüntü Treni 🚂',W/2,200);ctx.font='20px Segoe UI';
ctx.fillText('Deseni tamamla, tren ilerlesin!',W/2,260);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Tren Hedefe Ulaştı! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
// HUD
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Seviye: '+level+'/'+maxLevel+'  Puan: '+score,W/2,35);
// rails
ctx.strokeStyle='#78716c';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(0,400);ctx.lineTo(W,400);ctx.stroke();
ctx.beginPath();ctx.moveTo(0,410);ctx.lineTo(W,410);ctx.stroke();
for(let x=0;x<W;x+=30){ctx.fillStyle='#57534e';ctx.fillRect(x,395,20,20)}
// train
ctx.fillStyle='#7c3aed';ctx.fillRect(trainX,355,60,40);ctx.fillStyle='#a78bfa';
ctx.fillRect(trainX+5,345,50,15);ctx.fillStyle='#fbbf24';
ctx.beginPath();ctx.arc(trainX+15,400,8,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(trainX+45,400,8,0,Math.PI*2);ctx.fill();
// smoke
smoke.forEach(s=>{ctx.globalAlpha=s.life*0.5;ctx.fillStyle='#d6d3d1';
ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
// wagons with pattern
const wagonStart=100;const wSize=55;
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Desen:',wagonStart-30,470);
shown.forEach((item,i)=>{const wx=wagonStart+i*wSize;
ctx.fillStyle=item==='❓'?'#7c3aed50':'#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
ctx.beginPath();ctx.roundRect(wx,455,48,48,8);ctx.fill();ctx.stroke();
ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.fillStyle='#fff';ctx.fillText(item,wx+24,488)});
// options
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Sıradaki ne?',W/2,550);
options.forEach((opt,i)=>{const ox=W/2-120+i*80;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
ctx.beginPath();ctx.roundRect(ox,560,65,65,10);ctx.fill();ctx.stroke();
ctx.font='36px Segoe UI';ctx.fillText(opt,ox+32,603)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle='#fbbf24';
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){if(state==='play'){
if(trainX<targetX)trainX+=2;
if(Math.random()<0.1)addSmoke();
smoke.forEach(s=>{s.y+=s.vy;s.x+=s.vx;s.r+=0.1;s.life-=0.015});
smoke=smoke.filter(s=>s.life>0)}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(update)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){
state='play';score=0;level=1;trainX=0;genLevel()}return}
if(state!=='play')return;
options.forEach((opt,i)=>{const ox=W/2-120+i*80;
if(mx>ox&&mx<ox+65&&my>560&&my<625){
if(opt===answer){score+=10*(level);playSound(true);addP(ox+32,590);level++;
if(level>maxLevel)state='win';else genLevel()}else{playSound(false)}}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""
