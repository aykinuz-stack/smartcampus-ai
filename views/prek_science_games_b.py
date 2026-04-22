# -*- coding: utf-8 -*-
"""Okul Öncesi Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm B: 6-10)."""


def _build_prek_sci_yagmur_bulutu_html():
    """Yağmur Bulutu Yap — Su döngüsü simülasyonu."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[];
let phase=0,steamParts=[],cloudFill=0,cloudMax=100,rainDrops=[],sunClicks=0,sunNeeded=8;
let waterWave=0,labelAlpha=0,labelText='',labelTimer=0;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<8;i++)particles.push({x,y,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*3})}
function showLabel(t){labelText=t;labelAlpha=1;labelTimer=120}

function setup(){phase=0;steamParts=[];cloudFill=0;rainDrops=[];sunClicks=0;
sunNeeded=Math.max(3,10-round);cloudMax=80+round*5}

function addSteam(){for(let i=0;i<3;i++){steamParts.push({x:150+Math.random()*400,y:490+Math.random()*20,vy:-1-Math.random()*1.5,vx:(Math.random()-.5)*.5,r:4+Math.random()*4,alpha:1})}}

function drawWater(){
waterWave+=0.03;
const wy=500;
const gw=ctx.createLinearGradient(0,wy,0,H);
gw.addColorStop(0,'#1e90ff');gw.addColorStop(0.5,'#1565c0');gw.addColorStop(1,'#0d47a1');
ctx.fillStyle=gw;
ctx.beginPath();ctx.moveTo(0,H);
for(let x=0;x<=W;x+=5){const y=wy+Math.sin(x*0.02+waterWave)*8+Math.sin(x*0.01+waterWave*1.3)*5;ctx.lineTo(x,y)}
ctx.lineTo(W,H);ctx.closePath();ctx.fill();
ctx.fillStyle='rgba(255,255,255,0.08)';
for(let i=0;i<5;i++){const sx=((i*160+waterWave*30)%W);ctx.beginPath();ctx.ellipse(sx,wy+20+i*10,40,3,0,0,Math.PI*2);ctx.fill()}}

function drawSun(hot){
const sx=580,sy=80,sr=hot?48:42;
ctx.save();
if(hot){for(let i=0;i<12;i++){const a=i*Math.PI/6+Date.now()*0.002;ctx.strokeStyle='rgba(255,200,0,0.3)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(sx+Math.cos(a)*(sr+5),sy+Math.sin(a)*(sr+5));ctx.lineTo(sx+Math.cos(a)*(sr+20),sy+Math.sin(a)*(sr+20));ctx.stroke()}}
const sg=ctx.createRadialGradient(sx,sy,0,sx,sy,sr);
sg.addColorStop(0,'#fff700');sg.addColorStop(0.5,'#ffb300');sg.addColorStop(1,'rgba(255,150,0,0.3)');
ctx.fillStyle=sg;ctx.beginPath();ctx.arc(sx,sy,sr,0,Math.PI*2);ctx.fill();
ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('☀️',sx,sy);
ctx.restore();
if(phase===0){ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.fillText('Tıkla! ('+sunClicks+'/'+sunNeeded+')',sx,sy+sr+20)}}

function drawCloud(){
const cx=W/2,cy=120;
const fill=Math.min(cloudFill/cloudMax,1);
const gray=Math.floor(200-fill*150);
const col='rgb('+gray+','+gray+','+(gray+20)+')';
ctx.fillStyle=col;
const s=0.6+fill*0.5;
ctx.beginPath();
ctx.arc(cx,cy,35*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx-35*s,cy+10,28*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx+35*s,cy+10,30*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx-18*s,cy-15*s,22*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx+18*s,cy-15*s,24*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx,cy+20*s,32*s,0,Math.PI*2);ctx.fill();
if(fill>0.3){ctx.fillStyle='rgba(255,255,255,0.1)';ctx.beginPath();ctx.arc(cx-10*s,cy-10*s,12*s,0,Math.PI*2);ctx.fill()}}

function drawRain(){
rainDrops.forEach(d=>{ctx.fillStyle='rgba(100,180,255,'+d.alpha+')';ctx.beginPath();
ctx.moveTo(d.x,d.y-6);ctx.quadraticCurveTo(d.x+4,d.y,d.x,d.y+6);ctx.quadraticCurveTo(d.x-4,d.y,d.x,d.y-6);ctx.fill()})}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌧️ Yağmur Bulutu Yap',W/2,180);
ctx.font='20px Segoe UI';ctx.fillText('Güneşe tıkla → Su buharlaşır →',W/2,240);
ctx.fillText('Bulut oluşur → Yağmur yağar!',W/2,270);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,350);return}

if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Harika Bilim İnsanı! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);
ctx.fillText(round-1+' su döngüsü tamamlandı!',W/2,300);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,340,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,370);return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);

drawWater();drawSun(phase===0);drawCloud();

steamParts.forEach(s=>{ctx.fillStyle='rgba(200,220,255,'+s.alpha*0.7+')';
ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill()});

drawRain();

if(phase===0){ctx.fillStyle='rgba(255,200,50,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Buharlaşma ☀️',W/2,470)}
if(phase===1){ctx.fillStyle='rgba(200,200,255,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Yoğunlaşma ☁️',W/2,200)}
if(phase===2){ctx.fillStyle='rgba(100,180,255,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Yağış 🌧️',W/2,200)}

if(labelAlpha>0){ctx.fillStyle='rgba(255,255,255,'+labelAlpha+')';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText(labelText,W/2,420)}

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);

if(labelTimer>0){labelTimer--;if(labelTimer<30)labelAlpha=labelTimer/30}

if(state==='play'){
if(phase===0&&sunClicks>=sunNeeded){phase=1;showLabel('Buhar yükseliyor!');addSteam();addSteam();addSteam()}

steamParts.forEach(s=>{s.y+=s.vy;s.x+=s.vx;
if(s.y<160){s.alpha-=0.02;cloudFill+=0.3}else{s.alpha-=0.002}});
steamParts=steamParts.filter(s=>s.alpha>0);

if(phase===1){
if(Math.random()<0.05)addSteam();
if(cloudFill>=cloudMax){phase=2;showLabel('Yağmur başlıyor!');
for(let i=0;i<20;i++){rainDrops.push({x:W/2-60+Math.random()*120,y:150+Math.random()*20,vy:2+Math.random()*3,alpha:0.8+Math.random()*0.2})}}}

if(phase===2){
rainDrops.forEach(d=>{d.y+=d.vy;d.vy+=0.05;
if(d.y>495){d.alpha-=0.1;addP(d.x,495,'#60a5fa')}});
rainDrops=rainDrops.filter(d=>d.alpha>0);
if(rainDrops.length===0){score+=10;snd(true);addP(W/2,300,'#fbbf24');round++;
if(round>maxR){state='win'}else{setup()}}}}

draw();requestAnimationFrame(upd)}

cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);

if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>340&&my<390){state='play';score=0;round=1;setup()}return}

if(state==='play'&&phase===0){
const sx=580,sy=80;
if(Math.hypot(mx-sx,my-sy)<55){sunClicks++;addSteam();addP(sx,sy,'#fbbf24');
if(sunClicks<sunNeeded)snd(true)}}});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_sci_tohumdan_cicege_html():
    """Tohumdan Çiçeğe — Tohumu sulayıp güneş vererek çiçek yetiştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
const FLOWERS=['🌸','🌺','🌻','🌹','🌷','💐','🌼','💮'];
let state='start',score=0,round=1,maxR=10,particles=[];
let stage=0,maxStage=6,nextNeed='water',wiltTimer=0,wiltAnim=0;
let growAnim=0,stepsNeeded=2,stepsDone=0;
let flowerEmoji='🌸',rootLen=0,stemH=0,leafAng=0,budSize=0,bloomSize=0;
let waterDrops=[],sunRays=[];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*4})}

function setup(){stage=0;nextNeed='water';wiltTimer=0;wiltAnim=0;growAnim=0;
stepsNeeded=Math.min(2+Math.floor(round/2),6);stepsDone=0;
flowerEmoji=FLOWERS[Math.floor(Math.random()*FLOWERS.length)];
rootLen=0;stemH=0;leafAng=0;budSize=0;bloomSize=0;waterDrops=[];sunRays=[]}

function drawSoil(){
const sy=420;
ctx.fillStyle='#5d4037';ctx.fillRect(0,sy,W,H-sy);
ctx.fillStyle='#4e342e';
for(let i=0;i<20;i++){const rx=Math.random()*W,ry=sy+10+Math.random()*(H-sy-20);
ctx.fillRect(rx,ry,8+Math.random()*12,2+Math.random()*3)}
ctx.fillStyle='#6d4c41';ctx.fillRect(0,sy,W,5);
const gg=ctx.createLinearGradient(0,sy-40,0,sy);
gg.addColorStop(0,'rgba(0,0,0,0)');gg.addColorStop(1,'rgba(93,64,55,0.5)');
ctx.fillStyle=gg;ctx.fillRect(0,sy-40,W,40)}

function drawPlant(){
const cx=W/2,groundY=420;
const progress=stage/maxStage;
ctx.save();
if(wiltAnim>0){ctx.translate(cx,groundY);ctx.rotate(Math.sin(Date.now()*0.01)*wiltAnim*0.05);ctx.translate(-cx,-groundY)}

if(stage>=1){ctx.strokeStyle='#8d6e63';ctx.lineWidth=2;
const rl=20+progress*30;
ctx.beginPath();ctx.moveTo(cx,groundY+5);ctx.lineTo(cx-15,groundY+5+rl);ctx.stroke();
ctx.beginPath();ctx.moveTo(cx,groundY+5);ctx.lineTo(cx+12,groundY+5+rl*0.8);ctx.stroke();
ctx.beginPath();ctx.moveTo(cx,groundY+10);ctx.lineTo(cx,groundY+5+rl*0.6);ctx.stroke()}

if(stage>=2){const sh=Math.min(30+stage*35,200);
ctx.strokeStyle='#4caf50';ctx.lineWidth=3+stage*0.5;
ctx.beginPath();ctx.moveTo(cx,groundY);ctx.lineTo(cx,groundY-sh);ctx.stroke();
ctx.strokeStyle='#66bb6a';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(cx,groundY);ctx.quadraticCurveTo(cx+2,groundY-sh/2,cx,groundY-sh);ctx.stroke()}

if(stage>=3){const sh=Math.min(30+stage*35,200);
const ly=groundY-sh*0.5;
ctx.fillStyle='#66bb6a';
ctx.save();ctx.translate(cx-3,ly);ctx.rotate(-0.4-Math.sin(Date.now()*0.002)*0.05);
ctx.beginPath();ctx.ellipse(0,0,25,10,0,0,Math.PI*2);ctx.fill();ctx.restore();
ctx.save();ctx.translate(cx+3,ly-15);ctx.rotate(0.4+Math.sin(Date.now()*0.002)*0.05);
ctx.beginPath();ctx.ellipse(0,0,22,9,0,0,Math.PI*2);ctx.fill();ctx.restore();
if(stage>=4){const ly2=groundY-sh*0.7;
ctx.save();ctx.translate(cx-3,ly2);ctx.rotate(-0.5);
ctx.beginPath();ctx.ellipse(0,0,18,7,0,0,Math.PI*2);ctx.fill();ctx.restore();
ctx.save();ctx.translate(cx+3,ly2+10);ctx.rotate(0.5);
ctx.beginPath();ctx.ellipse(0,0,18,7,0,0,Math.PI*2);ctx.fill();ctx.restore()}}

if(stage>=4){const sh=Math.min(30+stage*35,200);
const by=groundY-sh-5;
ctx.fillStyle='#a5d6a7';ctx.beginPath();ctx.arc(cx,by,8+stage*2,0,Math.PI*2);ctx.fill()}

if(stage>=5){const sh=200;const fy=groundY-sh-10;
const fs=20+bloomSize;
ctx.font=fs+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(flowerEmoji,cx,fy)}

ctx.restore();

if(stage===0){ctx.fillStyle='#8d6e63';ctx.beginPath();ctx.ellipse(cx,groundY+15,8,5,0,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#6d4c41';ctx.beginPath();ctx.ellipse(cx,groundY+15,5,3,0,0,Math.PI*2);ctx.fill()}}

function drawButtons(){
const bw=140,bh=55,gap=30;
const bx1=W/2-bw-gap/2,bx2=W/2+gap/2,by=560;

const isWater=nextNeed==='water';
ctx.fillStyle=isWater?'#1e88e5':'#1565c080';
ctx.beginPath();ctx.roundRect(bx1,by,bw,bh,12);ctx.fill();
ctx.strokeStyle='#90caf9';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(bx1,by,bw,bh,12);ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('💧 Su Ver',bx1+bw/2,by+bh/2+7);

ctx.fillStyle=!isWater?'#f57f17':'#f57f1780';
ctx.beginPath();ctx.roundRect(bx2,by,bw,bh,12);ctx.fill();
ctx.strokeStyle='#ffcc02';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(bx2,by,bw,bh,12);ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('☀️ Güneş',bx2+bw/2,by+bh/2+7)}

function drawStageIndicator(){
const labels=['🌰 Tohum','🌱 Filiz','🌿 Gövde','🍃 Yaprak','🌷 Tomurcuk','🌸 Çiçek'];
const y=80;
for(let i=0;i<maxStage;i++){const x=W/(maxStage+1)*(i+1);
ctx.fillStyle=i<stage?'#4caf50':i===stage?'#fbbf24':'#555';
ctx.beginPath();ctx.arc(x,y,12,0,Math.PI*2);ctx.fill();
if(i<maxStage-1){ctx.strokeStyle=i<stage?'#4caf50':'#555';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(x+14,y);ctx.lineTo(W/(maxStage+1)*(i+2)-14,y);ctx.stroke()}
ctx.fillStyle=i<=stage?'#e9d5ff':'#777';ctx.font='10px Segoe UI';ctx.textAlign='center';ctx.fillText(labels[i],x,y+28)}}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌱 Tohumdan Çiçeğe',W/2,180);
ctx.font='20px Segoe UI';ctx.fillText('Su ve güneş vererek çiçek yetiştir!',W/2,230);
ctx.fillText('Sırayla: 💧 Su → ☀️ Güneş → 💧 Su ...',W/2,265);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}

if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌸 Muhteşem Bahçıvan! 🌸',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);
ctx.fillText(round-1+' çiçek yetiştirdin!',W/2,300);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,340,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,370);return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);

drawStageIndicator();drawSoil();drawPlant();

waterDrops.forEach(d=>{ctx.fillStyle='rgba(100,180,255,'+d.alpha+')';ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText('💧',d.x,d.y)});
sunRays.forEach(r=>{ctx.fillStyle='rgba(255,200,0,'+r.alpha+')';ctx.font='14px Segoe UI';ctx.textAlign='center';ctx.fillText('✨',r.x,r.y)});

if(wiltAnim>0){ctx.fillStyle='rgba(255,80,80,0.8)';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Yanlış sıra! Tekrar dene.',W/2,140)}

ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Sıradaki: '+(nextNeed==='water'?'💧 Su Ver':'☀️ Güneş Ver'),W/2,520);

drawButtons();

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function advanceStage(){
stepsDone++;
const stagesPerStep=maxStage/stepsNeeded;
const newStage=Math.min(Math.floor(stepsDone*stagesPerStep),maxStage);
if(newStage>stage){stage=newStage;snd(true);addP(W/2,400,'#4caf50');
if(stage>=maxStage){score+=10;addP(W/2,200,'#fbbf24');
setTimeout(()=>{round++;if(round>maxR)state='win';else setup()},1200)}}}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);

waterDrops.forEach(d=>{d.y+=d.vy;d.alpha-=0.015});
waterDrops=waterDrops.filter(d=>d.alpha>0);
sunRays.forEach(r=>{r.y+=r.vy;r.alpha-=0.015});
sunRays=sunRays.filter(r=>r.alpha>0);

if(wiltTimer>0){wiltTimer--;wiltAnim=wiltTimer/60;if(wiltTimer===0)wiltAnim=0}

if(stage>=5){bloomSize=Math.min(bloomSize+0.3,25)}

draw();requestAnimationFrame(upd)}

cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);

if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>340&&my<390){state='play';score=0;round=1;setup()}return}

if(state!=='play'||stage>=maxStage)return;

const bw=140,bh=55,gap=30;
const bx1=W/2-bw-gap/2,bx2=W/2+gap/2,by=560;

if(mx>bx1&&mx<bx1+bw&&my>by&&my<by+bh){
if(nextNeed==='water'){nextNeed='sun';
for(let i=0;i<5;i++)waterDrops.push({x:W/2-30+Math.random()*60,y:350,vy:1+Math.random()*2,alpha:1});
advanceStage()}else{snd(false);wiltTimer=60}}

if(mx>bx2&&mx<bx2+bw&&my>by&&my<by+bh){
if(nextNeed==='sun'){nextNeed='water';
for(let i=0;i<5;i++)sunRays.push({x:W/2-40+Math.random()*80,y:120,vy:1+Math.random()*1.5,alpha:1});
advanceStage()}else{snd(false);wiltTimer=60}}});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_sci_duyu_dedektifi_html():
    """Duyu Dedektifi — Nesnelerin hangi duyuyla algılandığını bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];

const SENSES=[
{emoji:'👁️',name:'Görme',color:'#60a5fa'},
{emoji:'👂',name:'Duyma',color:'#f472b6'},
{emoji:'👃',name:'Koklama',color:'#34d399'},
{emoji:'👅',name:'Tatma',color:'#fb923c'},
{emoji:'✋',name:'Dokunma',color:'#c084fc'}];

const OBJECTS=[
{emoji:'🎵',name:'Müzik Kutusu',hint:'Melodiler çalar',sense:1},
{emoji:'🌹',name:'Gül',hint:'Mis gibi kokar',sense:2},
{emoji:'🌈',name:'Gökkuşağı',hint:'Rengarenk görünür',sense:0},
{emoji:'🍦',name:'Dondurma',hint:'Tatlı ve soğuk',sense:3},
{emoji:'🧸',name:'Peluş Ayı',hint:'Yumuşacık hissedersin',sense:4},
{emoji:'🔔',name:'Çan',hint:'Çınnn diye ses çıkarır',sense:1},
{emoji:'🌸',name:'Çiçek',hint:'Güzel kokusu var',sense:2},
{emoji:'🎆',name:'Havai Fişek',hint:'Gökyüzünde parlar',sense:0},
{emoji:'🍫',name:'Çikolata',hint:'Ağzında erir',sense:3},
{emoji:'🧊',name:'Buz',hint:'Eline alınca soğuk',sense:4},
{emoji:'🥁',name:'Davul',hint:'Güm güm ses çıkarır',sense:1},
{emoji:'☕',name:'Kahve',hint:'Güzel kokusu yayılır',sense:2},
{emoji:'🌅',name:'Gün Batımı',hint:'Ufukta izlersin',sense:0},
{emoji:'🍋',name:'Limon',hint:'Ekşi ekşi',sense:3},
{emoji:'🪨',name:'Taş',hint:'Sert ve pürüzlü',sense:4},
{emoji:'🎸',name:'Gitar',hint:'Tıngır tıngır çalar',sense:1},
{emoji:'🧅',name:'Soğan',hint:'Kesince kokar',sense:2},
{emoji:'⭐',name:'Yıldız',hint:'Gökyüzünde parıldar',sense:0},
{emoji:'🍯',name:'Bal',hint:'Çok tatlı',sense:3},
{emoji:'🧤',name:'Eldiven',hint:'Elini sıcak tutar',sense:4}];

let state='start',score=0,round=1,maxR=10,particles=[];
let curObj=null,shakeIdx=-1,shakeTimer=0,usedIdx=[],objBounce=0,correctAnim=0;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*4})}

function pickObj(){if(usedIdx.length>=OBJECTS.length)usedIdx=[];
let idx;do{idx=Math.floor(Math.random()*OBJECTS.length)}while(usedIdx.includes(idx));
usedIdx.push(idx);curObj=OBJECTS[idx];correctAnim=0}

function drawSenseButtons(){
const bw=110,bh=80,gap=12;
const totalW=SENSES.length*(bw+gap)-gap;
const sx=(W-totalW)/2;
const by=80;
SENSES.forEach((s,i)=>{
const bx=sx+i*(bw+gap);
let offX=0;
if(shakeIdx===i&&shakeTimer>0){offX=Math.sin(Date.now()*0.05)*5*(shakeTimer/20)}
ctx.fillStyle=s.color+'30';ctx.strokeStyle=s.color;ctx.lineWidth=2;
ctx.beginPath();ctx.roundRect(bx+offX,by,bw,bh,10);ctx.fill();ctx.stroke();
ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.fillText(s.emoji,bx+bw/2+offX,by+35);
ctx.fillStyle=s.color;ctx.font='bold 13px Segoe UI';ctx.fillText(s.name,bx+bw/2+offX,by+62)})}

function drawObject(){
if(!curObj)return;
const cx=W/2,cy=310;
const bounce=Math.sin(Date.now()*0.003)*8;

ctx.fillStyle='#1e1b4b80';ctx.beginPath();ctx.roundRect(cx-120,cy-100,240,200,20);ctx.fill();
ctx.strokeStyle='#a78bfa40';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(cx-120,cy-100,240,200,20);ctx.stroke();

if(correctAnim>0){ctx.fillStyle='rgba(52,211,153,'+correctAnim+')';ctx.beginPath();ctx.arc(cx,cy-10,60+correctAnim*30,0,Math.PI*2);ctx.fill()}

ctx.font='64px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(curObj.emoji,cx,cy-10+bounce);

ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textBaseline='alphabetic';
ctx.fillText(curObj.name,cx,cy+65);

ctx.fillStyle='#e9d5ff99';ctx.font='16px Segoe UI';
ctx.fillText('"'+curObj.hint+'"',cx,cy+90)}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🔍 Duyu Dedektifi',W/2,180);
ctx.font='20px Segoe UI';ctx.fillText('Bu nesneyi hangi duyunla algılarsın?',W/2,230);
ctx.fillText('👁️ Görme  👂 Duyma  👃 Koklama  👅 Tatma  ✋ Dokunma',W/2,270);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}

if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏆 Süper Dedektif! 🏆',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);

ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Bu nesneyi hangi duyunla algılarsın?',W/2,55);

drawSenseButtons();drawObject();

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);
if(shakeTimer>0)shakeTimer--;
if(correctAnim>0)correctAnim-=0.02;
draw();requestAnimationFrame(upd)}

cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);

if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;usedIdx=[];pickObj()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){state='play';score=0;round=1;usedIdx=[];pickObj()}return}

if(state!=='play'||!curObj)return;

const bw=110,bh=80,gap=12;
const totalW=SENSES.length*(bw+gap)-gap;
const sx=(W-totalW)/2;
const by=80;
SENSES.forEach((s,i)=>{
const bx=sx+i*(bw+gap);
if(mx>bx&&mx<bx+bw&&my>by&&my<by+bh){
if(i===curObj.sense){score+=10;snd(true);correctAnim=1;
addP(bx+bw/2,by+bh/2,s.color);addP(W/2,300,'#fbbf24');
round++;if(round>maxR){setTimeout(()=>{state='win'},600)}
else{setTimeout(pickObj,700)}}
else{snd(false);shakeIdx=i;shakeTimer=20}}})});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_sci_sicak_soguk_html():
    """Sıcak mı Soğuk mu? — Nesneleri doğru sıcaklık bölgesine yerleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];

const ITEMS=[
{emoji:'🍦',name:'Dondurma',zone:0,anim:'melt'},
{emoji:'🍲',name:'Sıcak Çorba',zone:2,anim:'steam'},
{emoji:'🧊',name:'Buz Küpü',zone:0,anim:'melt'},
{emoji:'🔥',name:'Kamp Ateşi',zone:2,anim:'fire'},
{emoji:'⛄',name:'Kardan Adam',zone:0,anim:'melt'},
{emoji:'🍵',name:'Sıcak Çay',zone:2,anim:'steam'},
{emoji:'☀️',name:'Güneş',zone:2,anim:'fire'},
{emoji:'🐧',name:'Penguen',zone:0,anim:'melt'},
{emoji:'🌋',name:'Yanardağ',zone:2,anim:'fire'},
{emoji:'🫕',name:'Sıcak Fırın',zone:2,anim:'steam'},
{emoji:'❄️',name:'Kar Tanesi',zone:0,anim:'melt'},
{emoji:'🌡️',name:'Ateşli Hasta',zone:1,anim:'steam'},
{emoji:'🌤️',name:'Ilık Hava',zone:1,anim:'none'},
{emoji:'🧣',name:'Kazak',zone:1,anim:'none'},
{emoji:'🌊',name:'Deniz Suyu',zone:1,anim:'none'},
{emoji:'🍞',name:'Taze Ekmek',zone:1,anim:'steam'},
{emoji:'🥶',name:'Buz Gibi El',zone:0,anim:'melt'},
{emoji:'♨️',name:'Kaplıca',zone:2,anim:'steam'},
{emoji:'🧃',name:'Meyve Suyu',zone:1,anim:'none'},
{emoji:'🏖️',name:'Sıcak Kum',zone:2,anim:'fire'}];

const ZONES=[
{name:'Soğuk ❄️',color:'#3b82f6',range:'0-30°C'},
{name:'Ilık 🌤️',color:'#eab308',range:'30-60°C'},
{name:'Sıcak 🔥',color:'#ef4444',range:'60-100°C'}];

let state='start',score=0,round=1,maxR=10,particles=[];
let curItem=null,usedIdx=[],markerY=0,dragging=false,answered=false;
let resultAnim=0,resultCorrect=false,itemAnimTimer=0;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*4})}

const thermX=80,thermTop=100,thermBot=550,thermW=40;
const thermH=thermBot-thermTop;

function tempToY(t){return thermBot-(t/100)*thermH}
function yToTemp(y){return Math.max(0,Math.min(100,((thermBot-y)/thermH)*100))}
function getZone(y){const t=yToTemp(y);if(t<30)return 0;if(t<60)return 1;return 2}

function pickItem(){if(usedIdx.length>=ITEMS.length)usedIdx=[];
let idx;do{idx=Math.floor(Math.random()*ITEMS.length)}while(usedIdx.includes(idx));
usedIdx.push(idx);curItem=ITEMS[idx];
markerY=tempToY(50);answered=false;resultAnim=0;itemAnimTimer=0}

function drawThermometer(){
ctx.fillStyle='#1e1b4b';ctx.beginPath();ctx.roundRect(thermX-thermW/2-5,thermTop-20,thermW+10,thermH+55,15);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(thermX-thermW/2-5,thermTop-20,thermW+10,thermH+55,15);ctx.stroke();

const zoneH=thermH/3;
for(let i=2;i>=0;i--){
const zy=thermTop+(2-i)*zoneH;
ctx.fillStyle=ZONES[i].color+'40';ctx.fillRect(thermX-thermW/2,zy,thermW,zoneH);
ctx.strokeStyle=ZONES[i].color+'80';ctx.lineWidth=1;
ctx.beginPath();ctx.moveTo(thermX-thermW/2,zy);ctx.lineTo(thermX+thermW/2,zy);ctx.stroke()}

for(let t=0;t<=100;t+=10){
const y=tempToY(t);
ctx.strokeStyle='#a78bfa60';ctx.lineWidth=1;
ctx.beginPath();ctx.moveTo(thermX+thermW/2,y);ctx.lineTo(thermX+thermW/2+8,y);ctx.stroke();
if(t%20===0){ctx.fillStyle='#e9d5ff';ctx.font='11px Segoe UI';ctx.textAlign='left';ctx.fillText(t+'°',thermX+thermW/2+12,y+4)}}

const mercH=thermBot-markerY;
const mg=ctx.createLinearGradient(0,markerY,0,thermBot);
mg.addColorStop(0,'#ef4444');mg.addColorStop(1,'#dc2626');
ctx.fillStyle=mg;ctx.fillRect(thermX-8,markerY,16,mercH);

ctx.fillStyle='#ef4444';ctx.beginPath();ctx.arc(thermX,thermBot+15,18,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#fff';ctx.font='10px Segoe UI';ctx.textAlign='center';ctx.fillText(Math.round(yToTemp(markerY))+'°',thermX,thermBot+19);

ctx.fillStyle='#fbbf24';ctx.beginPath();
ctx.moveTo(thermX-thermW/2-15,markerY);
ctx.lineTo(thermX-thermW/2-5,markerY-8);
ctx.lineTo(thermX-thermW/2-5,markerY+8);
ctx.closePath();ctx.fill();

for(let i=0;i<3;i++){
const zy=thermTop+(2-i)*zoneH+zoneH/2;
ctx.fillStyle=ZONES[i].color;ctx.font='bold 11px Segoe UI';ctx.textAlign='right';
ctx.fillText(ZONES[i].name,thermX-thermW/2-10,zy+4)}}

function drawItem(){
if(!curItem)return;
const cx=420,cy=300;

ctx.fillStyle='#1e1b4b60';ctx.beginPath();ctx.roundRect(cx-130,cy-130,260,260,20);ctx.fill();
ctx.strokeStyle='#a78bfa30';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(cx-130,cy-130,260,260,20);ctx.stroke();

const bounce=Math.sin(Date.now()*0.003)*6;

if(answered&&resultAnim>0){
if(curItem.anim==='melt'){ctx.globalAlpha=0.3+resultAnim*0.7;const scale=0.7+resultAnim*0.3;ctx.save();ctx.translate(cx,cy+bounce);ctx.scale(scale,scale);ctx.font='80px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(curItem.emoji,0,0);ctx.restore();ctx.globalAlpha=1}
else if(curItem.anim==='steam'){ctx.font='80px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(curItem.emoji,cx,cy+bounce);
for(let i=0;i<3;i++){ctx.fillStyle='rgba(200,200,200,'+(0.3*resultAnim)+')';
ctx.font='20px Segoe UI';ctx.fillText('~',cx-20+i*20,cy-60-Math.sin(Date.now()*0.005+i)*15)}}
else if(curItem.anim==='fire'){ctx.font='80px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(curItem.emoji,cx,cy+bounce);
ctx.font='20px Segoe UI';for(let i=0;i<3;i++){ctx.fillText('🔥',cx-25+i*25,cy-55-Math.sin(Date.now()*0.006+i)*10)}}
else{ctx.font='80px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(curItem.emoji,cx,cy+bounce)}}
else{ctx.font='80px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(curItem.emoji,cx,cy+bounce)}

ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.textBaseline='alphabetic';
ctx.fillText(curItem.name,cx,cy+110);

if(answered){
const zn=ZONES[curItem.zone];
ctx.fillStyle=resultCorrect?'#34d399':'#ef4444';ctx.font='bold 20px Segoe UI';
ctx.fillText(resultCorrect?'Doğru! ✓':'Doğru bölge: '+zn.name,cx,cy+145)}}

function drawConfirmBtn(){
if(answered)return;
const bx=350,by=530,bw=160,bh=50;
ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(bx,by,bw,bh,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Onayla ✓',bx+bw/2,by+bh/2+7)}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌡️ Sıcak mı Soğuk mu?',W/2,180);
ctx.font='20px Segoe UI';ctx.fillText('Termometreyi doğru bölgeye ayarla!',W/2,230);
ctx.fillText('❄️ Soğuk(0-30) | 🌤️ Ilık(30-60) | 🔥 Sıcak(60-100)',W/2,265);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}

if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Sıcaklık Uzmanı! 🎉',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);

ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';
ctx.fillText('Termometreyi sürükle, doğru bölgeye ayarla!',W/2,60);

drawThermometer();drawItem();drawConfirmBtn();

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);
if(answered&&resultAnim>0)resultAnim-=0.005;
draw();requestAnimationFrame(upd)}

function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}

cv.addEventListener('mousedown',e=>{const m=gp(e);
if(state!=='play'||answered)return;
if(Math.abs(m.x-thermX)<35&&m.y>thermTop-20&&m.y<thermBot+35){dragging=true}});

cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);
markerY=Math.max(thermTop,Math.min(thermBot,m.y))});

cv.addEventListener('mouseup',()=>{dragging=false});

cv.addEventListener('click',e=>{const m=gp(e);

if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;usedIdx=[];pickItem()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>320&&m.y<370){state='play';score=0;round=1;usedIdx=[];pickItem()}return}

if(state==='play'&&!answered){
const bx=350,by=530,bw=160,bh=50;
if(m.x>bx&&m.x<bx+bw&&m.y>by&&m.y<by+bh){
const chosen=getZone(markerY);
answered=true;resultAnim=1;
if(chosen===curItem.zone){resultCorrect=true;score+=10;snd(true);addP(420,300,'#34d399')}
else{resultCorrect=false;snd(false)}
setTimeout(()=>{round++;if(round>maxR)state='win';else pickItem()},1800)}}});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
const m=gp(t);
if(state!=='play'||answered){cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));return}
if(Math.abs(m.x-thermX)<35&&m.y>thermTop-20&&m.y<thermBot+35){dragging=true}
else{cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))}});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',e=>{e.preventDefault();dragging=false;
cv.dispatchEvent(new MouseEvent('mouseup',{}))});
upd();
</script></body></html>"""


def _build_prek_sci_kutle_kiyasla_html():
    """Kütle Kıyasla — Hangisinin daha ağır olduğunu tahmin et."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];

const PAIRS=[
{left:{emoji:'🐘',name:'Fil',w:5000},right:{emoji:'🐭',name:'Fare',w:0.02}},
{left:{emoji:'🍉',name:'Karpuz',w:8},right:{emoji:'🍇',name:'Üzüm',w:0.3}},
{left:{emoji:'🚗',name:'Araba',w:1500},right:{emoji:'🚲',name:'Bisiklet',w:12}},
{left:{emoji:'🪨',name:'Kaya',w:50},right:{emoji:'🪶',name:'Tüy',w:0.001}},
{left:{emoji:'🏀',name:'Basketbol',w:0.6},right:{emoji:'🎾',name:'Tenis Topu',w:0.06}},
{left:{emoji:'📚',name:'Kitap Yığını',w:5},right:{emoji:'📄',name:'Kağıt',w:0.005}},
{left:{emoji:'🐋',name:'Balina',w:100000},right:{emoji:'🐟',name:'Balık',w:2}},
{left:{emoji:'🏠',name:'Ev',w:50000},right:{emoji:'🏕️',name:'Çadır',w:5}},
{left:{emoji:'🎹',name:'Piyano',w:300},right:{emoji:'🎸',name:'Gitar',w:3}},
{left:{emoji:'🍎',name:'Elma',w:0.2},right:{emoji:'🍊',name:'Portakal',w:0.25}},
{left:{emoji:'🦁',name:'Aslan',w:190},right:{emoji:'🐈',name:'Kedi',w:4}},
{left:{emoji:'🚌',name:'Otobüs',w:12000},right:{emoji:'🛴',name:'Scooter',w:5}},
{left:{emoji:'🎃',name:'Balkabağı',w:5},right:{emoji:'🍓',name:'Çilek',w:0.02}},
{left:{emoji:'🥥',name:'Hindistan Cevizi',w:1.5},right:{emoji:'🥜',name:'Fıstık',w:0.01}},
{left:{emoji:'🐻',name:'Ayı',w:350},right:{emoji:'🐇',name:'Tavşan',w:2}}];

let state='start',score=0,round=1,maxR=10,particles=[];
let curPair=null,heavySide=-1,usedIdx=[],answered=false;
let beamAngle=0,targetAngle=0,animating=false;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*4})}

function pickPair(){if(usedIdx.length>=PAIRS.length)usedIdx=[];
let idx;do{idx=Math.floor(Math.random()*PAIRS.length)}while(usedIdx.includes(idx));
usedIdx.push(idx);
curPair=JSON.parse(JSON.stringify(PAIRS[idx]));
if(Math.random()>0.5){const tmp=curPair.left;curPair.left=curPair.right;curPair.right=tmp}
heavySide=curPair.left.w>=curPair.right.w?0:1;
answered=false;beamAngle=0;targetAngle=0;animating=false}

function drawStand(){
const cx=W/2,baseY=480;
ctx.fillStyle='#8d6e63';ctx.fillRect(cx-8,300,16,baseY-300);
ctx.fillStyle='#a1887f';ctx.beginPath();ctx.moveTo(cx-50,baseY);ctx.lineTo(cx+50,baseY);ctx.lineTo(cx+40,baseY+15);ctx.lineTo(cx-40,baseY+15);ctx.closePath();ctx.fill();
ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(cx,300,10,0,Math.PI*2);ctx.fill()}

function drawBeam(){
const cx=W/2,pivotY=300,beamLen=220;
ctx.save();ctx.translate(cx,pivotY);ctx.rotate(beamAngle);

ctx.fillStyle='#d4a574';ctx.fillRect(-beamLen,-5,beamLen*2,10);
ctx.strokeStyle='#a1887f';ctx.lineWidth=2;ctx.strokeRect(-beamLen,-5,beamLen*2,10);

const chainLen=40+Math.abs(beamAngle)*20;

ctx.strokeStyle='#bbb';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(-beamLen+10,5);ctx.lineTo(-beamLen+10,5+chainLen);ctx.stroke();
ctx.beginPath();ctx.moveTo(-beamLen+50,5);ctx.lineTo(-beamLen+50,5+chainLen);ctx.stroke();

ctx.beginPath();ctx.moveTo(beamLen-10,5);ctx.lineTo(beamLen-10,5+chainLen);ctx.stroke();
ctx.beginPath();ctx.moveTo(beamLen-50,5);ctx.lineTo(beamLen-50,5+chainLen);ctx.stroke();

const panW=80,panH=15;
ctx.fillStyle='#cd9544';
ctx.beginPath();ctx.ellipse(-beamLen+30,5+chainLen+panH/2,panW/2,panH/2,0,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='#a67c3d';ctx.lineWidth=1.5;ctx.beginPath();ctx.ellipse(-beamLen+30,5+chainLen+panH/2,panW/2,panH/2,0,0,Math.PI*2);ctx.stroke();

ctx.fillStyle='#cd9544';
ctx.beginPath();ctx.ellipse(beamLen-30,5+chainLen+panH/2,panW/2,panH/2,0,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='#a67c3d';ctx.lineWidth=1.5;ctx.beginPath();ctx.ellipse(beamLen-30,5+chainLen+panH/2,panW/2,panH/2,0,0,Math.PI*2);ctx.stroke();

if(curPair){
ctx.font='44px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(curPair.left.emoji,-beamLen+30,5+chainLen-10);
ctx.fillText(curPair.right.emoji,beamLen-30,5+chainLen-10)}

ctx.restore()}

function drawLabels(){
if(!curPair)return;
const cx=W/2;

ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
ctx.fillText(curPair.left.name,cx-190,530);
ctx.fillText(curPair.right.name,cx+190,530);

if(!answered){
ctx.fillStyle='#fbbf2490';ctx.font='bold 16px Segoe UI';
ctx.fillText('⬇️ Tıkla',cx-190,555);ctx.fillText('⬇️ Tıkla',cx+190,555)}

if(answered){
const correctName=heavySide===0?curPair.left.name:curPair.right.name;
ctx.fillStyle='#34d399';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText(correctName+' daha ağır!',cx,570)}}

function drawClickAreas(){
if(answered)return;
const cx=W/2;
ctx.fillStyle='rgba(96,165,250,0.1)';ctx.strokeStyle='rgba(96,165,250,0.3)';ctx.lineWidth=2;
ctx.beginPath();ctx.roundRect(cx-280,250,170,200,15);ctx.fill();ctx.stroke();
ctx.beginPath();ctx.roundRect(cx+110,250,170,200,15);ctx.fill();ctx.stroke()}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('⚖️ Kütle Kıyasla',W/2,180);
ctx.font='20px Segoe UI';ctx.fillText('Hangisi daha ağır? Doğru tarafı seç!',W/2,230);
ctx.fillText('Terazi doğru tarafa eğilecek.',W/2,265);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}

if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏆 Fizik Dehası! 🏆',W/2,200);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);

ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';
ctx.fillText('Hangisi daha ağır? Ağır olanı tıkla!',W/2,60);

drawClickAreas();drawStand();drawBeam();drawLabels();

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);

if(animating){
const diff=targetAngle-beamAngle;
beamAngle+=diff*0.05;
if(Math.abs(diff)<0.005){beamAngle=targetAngle;animating=false}}

draw();requestAnimationFrame(upd)}

cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);

if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;usedIdx=[];pickPair()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){state='play';score=0;round=1;usedIdx=[];pickPair()}return}

if(state!=='play'||answered||!curPair)return;

const cx=W/2;
let chosen=-1;
if(mx>cx-280&&mx<cx-110&&my>250&&my<450)chosen=0;
if(mx>cx+110&&mx<cx+280&&my>250&&my<450)chosen=1;

if(chosen<0)return;

answered=true;animating=true;
targetAngle=heavySide===0?0.25:-0.25;

if(chosen===heavySide){score+=10;snd(true);
const px=heavySide===0?cx-190:cx+190;addP(px,350,'#34d399')}
else{snd(false)}

setTimeout(()=>{round++;if(round>maxR)state='win';else pickPair()},2000)});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""
