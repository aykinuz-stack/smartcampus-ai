# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm C: 11-15)."""


def _build_elem_sci_yogunluk_html():
    """Yoğunluk Dedektifi — Hangi cisim batar, hangisi yüzer?"""
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
let waveT=0,feedback='',feedbackTimer=0,feedbackOk=false;
let objA={name:'',density:0,emoji:'',color:''},objB={name:'',density:0,emoji:'',color:''};
let answered=false,animPhase=0,animT=0;
let objAY=0,objBY=0,objATargetY=0,objBTargetY=0;
const waterY=340,waterBottom=580;

const PAIRS=[
{a:{name:'Demir Top',density:7.9,emoji:'⚫',color:'#6b7280'},b:{name:'Tahta Top',density:0.6,emoji:'🟤',color:'#92400e'}},
{a:{name:'Altın Sikke',density:19.3,emoji:'🪙',color:'#fbbf24'},b:{name:'Alüminyum Sikke',density:2.7,emoji:'🪙',color:'#94a3b8'}},
{a:{name:'Taş',density:2.5,emoji:'🪨',color:'#78716c'},b:{name:'Mantar',density:0.2,emoji:'🟡',color:'#d4a373'}},
{a:{name:'Cam Bilye',density:2.5,emoji:'🔵',color:'#3b82f6'},b:{name:'Plastik Top',density:0.9,emoji:'🟢',color:'#22c55e'}},
{a:{name:'Kurşun',density:11.3,emoji:'⬛',color:'#94A3B8'},b:{name:'Buz',density:0.9,emoji:'🧊',color:'#a5f3fc'}},
{a:{name:'Bakır',density:8.9,emoji:'🟠',color:'#c2410c'},b:{name:'Sünger',density:0.03,emoji:'🟨',color:'#fde047'}},
{a:{name:'Mermer',density:2.7,emoji:'⚪',color:'#e2e8f0'},b:{name:'Mum',density:0.9,emoji:'🕯️',color:'#fef3c7'}},
{a:{name:'Çelik',density:7.8,emoji:'⬜',color:'#9ca3af'},b:{name:'Balsa Ağacı',density:0.15,emoji:'🪵',color:'#a3e635'}},
{a:{name:'Kum',density:1.6,emoji:'🟫',color:'#b45309'},b:{name:'Yağ',density:0.9,emoji:'🟡',color:'#facc15'}},
{a:{name:'Tuğla',density:2.0,emoji:'🧱',color:'#dc2626'},b:{name:'Strafor',density:0.03,emoji:'⬜',color:'#f0f9ff'}}
];
let pairOrder=[0,1,2,3,4,5,6,7,8,9];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<8;i++)particles.push({x,y,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*3})}

function shuffle(arr){for(let i=arr.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}return arr}

function setupRound(){
const idx=pairOrder[(round-1)%pairOrder.length];
const pair=PAIRS[idx];
if(Math.random()>0.5){objA={...pair.a};objB={...pair.b}}else{objA={...pair.b};objB={...pair.a}}
answered=false;animPhase=0;animT=0;
objAY=200;objBY=200;
objATargetY=objA.density>1.0?waterBottom-40:waterY-10;
objBTargetY=objB.density>1.0?waterBottom-40:waterY-10;
feedback='';feedbackTimer=0}

function startGame(){state='play';score=0;round=1;pairOrder=shuffle([...Array(10).keys()]);setupRound()}

function drawWater(){
waveT+=0.03;
const gw=ctx.createLinearGradient(0,waterY,0,waterBottom+30);
gw.addColorStop(0,'rgba(30,144,255,0.6)');gw.addColorStop(0.5,'rgba(21,101,192,0.7)');gw.addColorStop(1,'rgba(13,71,161,0.8)');
ctx.fillStyle=gw;ctx.beginPath();ctx.moveTo(100,waterBottom+30);
for(let x=100;x<=600;x+=3){const y=waterY+Math.sin(x*0.03+waveT)*6+Math.sin(x*0.015+waveT*1.5)*4;ctx.lineTo(x,y)}
ctx.lineTo(600,waterBottom+30);ctx.closePath();ctx.fill();
ctx.strokeStyle='rgba(255,255,255,0.15)';ctx.lineWidth=1;
for(let i=0;i<4;i++){ctx.beginPath();const yy=waterY+30+i*40;
for(let x=110;x<590;x+=3){ctx.lineTo(x,yy+Math.sin(x*0.02+waveT+i)*3)}ctx.stroke()}
ctx.fillStyle='rgba(255,255,255,0.12)';ctx.font='12px Segoe UI';ctx.textAlign='left';
ctx.fillText('Su yüzeyi (yoğunluk=1.0)',105,waterY-5);
ctx.strokeStyle='rgba(255,255,255,0.3)';ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(100,waterY);ctx.lineTo(600,waterY);ctx.stroke();ctx.setLineDash([])}

function drawTank(){
ctx.strokeStyle='#60a5fa';ctx.lineWidth=3;
ctx.strokeRect(98,waterY-60,504,waterBottom-waterY+92);
ctx.fillStyle='rgba(96,165,250,0.1)';ctx.fillRect(100,waterY-58,500,waterBottom-waterY+88);
ctx.fillStyle='#60a5fa';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText('Su Tankı',350,waterBottom+50)}

function drawObject(name,emoji,color,x,y,density){
ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,28,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='rgba(255,255,255,0.3)';ctx.lineWidth=2;ctx.stroke();
ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(emoji,x,y);
ctx.textBaseline='alphabetic';
ctx.fillStyle='#e9d5ff';ctx.font='bold 13px Segoe UI';ctx.fillText(name,x,y-38);
if(answered){ctx.fillStyle='#fbbf24';ctx.font='12px Segoe UI';ctx.fillText('d='+density,x,y+42)}}

function drawDensityScale(){
const sx=640,sy=waterY-50,sh=waterBottom-waterY+60;
ctx.fillStyle='rgba(30,30,80,0.6)';ctx.fillRect(sx,sy,50,sh);
ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;ctx.strokeRect(sx,sy,50,sh);
const maxD=12;
ctx.fillStyle='#e9d5ff';ctx.font='bold 11px Segoe UI';ctx.textAlign='center';
ctx.fillText('Yoğunluk',sx+25,sy-8);
for(let d=0;d<=maxD;d+=2){
const yy=sy+sh-(d/maxD)*sh;
ctx.fillStyle='rgba(255,255,255,0.4)';ctx.fillRect(sx,yy,50,1);
ctx.fillStyle='#e9d5ff';ctx.font='10px Segoe UI';ctx.fillText(d.toString(),sx+25,yy-3)}
const waterLine=sy+sh-(1.0/maxD)*sh;
ctx.strokeStyle='#60a5fa';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(sx,waterLine);ctx.lineTo(sx+50,waterLine);ctx.stroke();
ctx.fillStyle='#60a5fa';ctx.font='bold 10px Segoe UI';ctx.fillText('Su=1.0',sx+25,waterLine-4);
if(answered){
const aY=sy+sh-(Math.min(objA.density,maxD)/maxD)*sh;
const bY=sy+sh-(Math.min(objB.density,maxD)/maxD)*sh;
ctx.fillStyle=objA.color;ctx.beginPath();ctx.arc(sx+15,aY,6,0,Math.PI*2);ctx.fill();
ctx.fillStyle=objB.color;ctx.beginPath();ctx.arc(sx+35,bY,6,0,Math.PI*2);ctx.fill()}}

function drawSplash(x,y){
for(let i=0;i<5;i++){
const angle=-Math.PI+Math.random()*Math.PI;
const dist=10+Math.random()*20;
ctx.fillStyle='rgba(100,180,255,0.6)';
ctx.beginPath();ctx.arc(x+Math.cos(angle)*dist,y-Math.abs(Math.sin(angle)*dist),3,0,Math.PI*2);ctx.fill()}}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🔬 Yoğunluk Dedektifi',W/2,160);
ctx.font='20px Segoe UI';ctx.fillText('Hangi cisim batar, hangisi yüzer?',W/2,210);
ctx.font='16px Segoe UI';ctx.fillStyle='#a78bfa';
ctx.fillText('Yoğunluğu suyun yoğunluğundan (1.0) büyük olan batar!',W/2,250);
ctx.fillText('Küçük olan yüzer!',W/2,275);
drawWater();drawTank();
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);
return}

if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Süper Bilim İnsanı! 🎉',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxR*10,W/2,260);
ctx.font='18px Segoe UI';ctx.fillText('Yoğunluk konusunu öğrendin!',W/2,300);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,340,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,370);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);

if(!answered){
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
ctx.fillText('Hangisi BATAR? Tıkla!',W/2,65);
ctx.fillStyle='rgba(167,139,250,0.15)';ctx.beginPath();ctx.roundRect(130,140,200,120,15);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.stroke();
ctx.fillStyle='rgba(167,139,250,0.15)';ctx.beginPath();ctx.roundRect(370,140,200,120,15);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.stroke();
drawObject(objA.name,objA.emoji,objA.color,230,200,objA.density);
drawObject(objB.name,objB.emoji,objB.color,470,200,objB.density);
}else{
drawObject(objA.name,objA.emoji,objA.color,230,objAY,objA.density);
drawObject(objB.name,objB.emoji,objB.color,470,objBY,objB.density);
if(animPhase===1){
if(objAY>waterY-5)drawSplash(230,waterY);
if(objBY>waterY-5)drawSplash(470,waterY)}}

drawTank();drawWater();drawDensityScale();

if(feedbackTimer>0){
ctx.fillStyle=feedbackOk?'rgba(16,185,129,0.9)':'rgba(239,68,68,0.9)';
ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,100)}

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);

if(feedbackTimer>0)feedbackTimer--;

if(state==='play'&&answered&&animPhase===1){
animT++;
objAY+=(objATargetY-objAY)*0.06;
objBY+=(objBTargetY-objBY)*0.06;
if(animT>100){animPhase=2}
}
if(state==='play'&&animPhase===2){
animT++;
if(animT>160){round++;if(round>maxR){state='win';for(let i=0;i<30;i++)addP(W/2+Math.random()*200-100,300,'#fbbf24')}else setupRound()}}

draw();requestAnimationFrame(upd)}

cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);

if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){startGame()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>340&&my<390){startGame()}return}

if(state==='play'&&!answered){
let clickedA=mx>130&&mx<330&&my>140&&my<260;
let clickedB=mx>370&&mx<570&&my>140&&my<260;
if(clickedA||clickedB){
answered=true;animPhase=1;animT=0;
const clickedDenser=clickedA?objA.density>objB.density:objB.density>objA.density;
const denser=objA.density>objB.density?objA:objB;
if(clickedDenser){score+=10;snd(true);feedback='Doğru! '+denser.name+' (d='+denser.density+') batar!';feedbackOk=true;feedbackTimer=120;addP(W/2,100,'#34d399')}
else{snd(false);feedback='Yanlış! '+denser.name+' (d='+denser.density+') batardı!';feedbackOk=false;feedbackTimer=120;addP(W/2,100,'#ef4444')}
}}});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
setupRound();upd();
</script></body></html>"""


def _build_elem_sci_golge_isik_olcer_html():
    """Gölge & Işık Ölçer — Işık kaynağını hareket ettirerek gölge boyutunu ayarla."""
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
let lightX=150,lightY=320,dragging=false;
let objX=350,objY=320,objH=60,objW=20;
let wallX=600,targetShadowH=0,tolerance=0;
let feedback='',feedbackTimer=0,feedbackOk=false;
let objEmoji='🏠',objLabel='Ev';

const OBJECTS=[
{emoji:'🏠',label:'Ev',h:60,w:20},
{emoji:'🌳',label:'Ağaç',h:70,w:15},
{emoji:'🧍',label:'İnsan',h:55,w:12},
{emoji:'🐈',label:'Kedi',h:35,w:18},
{emoji:'🏗️',label:'Kule',h:80,w:12},
{emoji:'⛪',label:'Bina',h:65,w:25},
{emoji:'🗼',label:'Kule',h:75,w:14},
{emoji:'🌵',label:'Kaktüs',h:50,w:12},
{emoji:'🚗',label:'Araba',h:30,w:35},
{emoji:'🎄',label:'Çam',h:65,w:20}
];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<8;i++)particles.push({x,y,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*3})}

function calcShadowH(){
const distLightObj=objX-lightX;
const distObjWall=wallX-objX;
if(distLightObj<=0)return 999;
return Math.round(objH*(distLightObj+distObjWall)/distLightObj)}

function setupRound(){
const obj=OBJECTS[(round-1)%OBJECTS.length];
objEmoji=obj.emoji;objLabel=obj.label;objH=obj.h;objW=obj.w;
lightX=120+Math.random()*80;
tolerance=round<=3?25:round<=6?18:12;
const testPositions=[];
for(let lx=100;lx<=300;lx+=20){
const dLO=objX-lx;const dOW=wallX-objX;
if(dLO>0)testPositions.push(Math.round(objH*(dLO+dOW)/dLO))}
if(testPositions.length>0){targetShadowH=testPositions[Math.floor(Math.random()*testPositions.length)]}
else{targetShadowH=objH*2}
targetShadowH=Math.max(objH+10,Math.min(300,targetShadowH));
feedback='';feedbackTimer=0}

function startGame(){state='play';score=0;round=1;setupRound()}

function drawFloor(){
ctx.fillStyle='#1e1b4b';ctx.fillRect(0,450,W,200);
ctx.strokeStyle='rgba(167,139,250,0.2)';ctx.lineWidth=1;
for(let x=0;x<W;x+=40){ctx.beginPath();ctx.moveTo(x,450);ctx.lineTo(x,H);ctx.stroke()}
for(let y=450;y<H;y+=30){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}}

function drawWall(){
const g=ctx.createLinearGradient(wallX,0,W,0);
g.addColorStop(0,'#94A3B8');g.addColorStop(1,'#1f2937');
ctx.fillStyle=g;ctx.fillRect(wallX,50,100,400);
ctx.strokeStyle='#6b7280';ctx.lineWidth=2;ctx.strokeRect(wallX,50,100,400);
for(let y=50;y<450;y+=30){ctx.strokeStyle='rgba(107,114,128,0.3)';ctx.beginPath();ctx.moveTo(wallX,y);ctx.lineTo(W,y);ctx.stroke()}}

function drawLight(){
const glowR=30+Math.sin(Date.now()*0.005)*5;
const g=ctx.createRadialGradient(lightX,lightY,0,lightX,lightY,glowR);
g.addColorStop(0,'rgba(255,255,100,0.9)');g.addColorStop(0.5,'rgba(255,200,50,0.4)');g.addColorStop(1,'rgba(255,150,0,0)');
ctx.fillStyle=g;ctx.beginPath();ctx.arc(lightX,lightY,glowR,0,Math.PI*2);ctx.fill();
ctx.font='32px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🔦',lightX,lightY);
ctx.textBaseline='alphabetic';
ctx.fillStyle='#fbbf24';ctx.font='bold 12px Segoe UI';ctx.fillText('Işık',lightX,lightY+30);
if(!dragging&&state==='play'){
ctx.fillStyle='rgba(255,200,50,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';
ctx.font='11px Segoe UI';ctx.fillText('← Sürükle →',lightX,lightY+44)}}

function drawLightRays(){
ctx.save();ctx.globalAlpha=0.08;
const topEdge=objY-objH/2;const botEdge=objY+objH/2;
ctx.strokeStyle='#fbbf24';ctx.lineWidth=1;
for(let i=0;i<12;i++){
const angle=(i/12-0.5)*0.6;
const rayEndX=wallX;
const rayEndY=lightY+Math.tan(angle)*(wallX-lightX);
ctx.beginPath();ctx.moveTo(lightX,lightY);ctx.lineTo(rayEndX,rayEndY);ctx.stroke()}
ctx.globalAlpha=0.15;ctx.strokeStyle='#fbbf24';ctx.lineWidth=1;
ctx.beginPath();ctx.moveTo(lightX,lightY);ctx.lineTo(objX,topEdge);ctx.lineTo(wallX,topEdge-(wallX-objX)*(lightY-topEdge)/(objX-lightX));ctx.stroke();
ctx.beginPath();ctx.moveTo(lightX,lightY);ctx.lineTo(objX,botEdge);ctx.lineTo(wallX,botEdge+(wallX-objX)*(botEdge-lightY)/(objX-lightX));ctx.stroke();
ctx.restore()}

function drawObject(){
ctx.fillStyle='#4b5563';ctx.fillRect(objX-objW/2,objY-objH/2,objW,objH);
ctx.font=(objH*0.6)+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(objEmoji,objX,objY);ctx.textBaseline='alphabetic';
ctx.fillStyle='#e9d5ff';ctx.font='bold 12px Segoe UI';ctx.fillText(objLabel,objX,objY+objH/2+16)}

function drawShadow(){
const sh=calcShadowH();
const distLO=objX-lightX;const distOW=wallX-objX;
if(distLO<=0)return;
const shadowTopY=lightY-(lightY-(objY-objH/2))*(distLO+distOW)/distLO;
const shadowBotY=lightY-(lightY-(objY+objH/2))*(distLO+distOW)/distLO;
const actualSH=shadowBotY-shadowTopY;
const fuzziness=Math.min(15,distLO*0.03);
const g=ctx.createLinearGradient(wallX,shadowTopY,wallX+20,shadowTopY);
g.addColorStop(0,'rgba(0,0,0,0.7)');g.addColorStop(1,'rgba(0,0,0,0)');
ctx.fillStyle=g;
ctx.beginPath();
ctx.ellipse(wallX+2,(shadowTopY+shadowBotY)/2,8+fuzziness,Math.abs(actualSH)/2+fuzziness,0,0,Math.PI*2);
ctx.fill()}

function drawRuler(){
const sh=calcShadowH();
const distLO=objX-lightX;const distOW=wallX-objX;
if(distLO<=0)return;
const shadowTopY=lightY-(lightY-(objY-objH/2))*(distLO+distOW)/distLO;
const shadowBotY=lightY-(lightY-(objY+objH/2))*(distLO+distOW)/distLO;
const rX=wallX+40;
ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(rX,shadowTopY);ctx.lineTo(rX,shadowBotY);ctx.stroke();
ctx.beginPath();ctx.moveTo(rX-8,shadowTopY);ctx.lineTo(rX+8,shadowTopY);ctx.stroke();
ctx.beginPath();ctx.moveTo(rX-8,shadowBotY);ctx.lineTo(rX+8,shadowBotY);ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
ctx.fillText(Math.abs(Math.round(shadowBotY-shadowTopY))+' cm',rX+12,(shadowTopY+shadowBotY)/2+5)}

function drawDistLabel(){
const dist=Math.round(objX-lightX);
ctx.strokeStyle='rgba(251,191,36,0.4)';ctx.lineWidth=1;ctx.setLineDash([4,4]);
ctx.beginPath();ctx.moveTo(lightX,lightY+55);ctx.lineTo(objX,lightY+55);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#fbbf24';ctx.font='11px Segoe UI';ctx.textAlign='center';
ctx.fillText(dist+' cm',(lightX+objX)/2,lightY+52)}

function drawCheckButton(){
ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-60,580,120,45,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Ölç!',W/2,610)}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('💡 Gölge & Işık Ölçer',W/2,160);
ctx.font='20px Segoe UI';ctx.fillText('Işık kaynağını hareket ettir,',W/2,210);
ctx.fillText('gölgenin boyutunu ayarla!',W/2,240);
ctx.font='16px Segoe UI';ctx.fillStyle='#a78bfa';
ctx.fillText('Işık yakınsa → Gölge büyür!',W/2,280);
ctx.fillText('Işık uzaksa → Gölge küçülür!',W/2,305);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,340,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,370);
return}

if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Işık Ustası! 🎉',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxR*10,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';
ctx.fillText('Hedef Gölge: '+targetShadowH+' cm (±'+tolerance+')',W/2,60);

drawFloor();drawWall();drawLightRays();drawShadow();drawObject();drawLight();drawRuler();drawDistLabel();drawCheckButton();

if(feedbackTimer>0){
feedbackTimer--;
ctx.fillStyle=feedbackOk?'rgba(16,185,129,0.9)':'rgba(239,68,68,0.9)';
ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,540)}

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}

function checkAnswer(){
const sh=calcShadowH();
const distLO=objX-lightX;const distOW=wallX-objX;
if(distLO<=0)return;
const shadowTopY=lightY-(lightY-(objY-objH/2))*(distLO+distOW)/distLO;
const shadowBotY=lightY-(lightY-(objY+objH/2))*(distLO+distOW)/distLO;
const actualSize=Math.abs(Math.round(shadowBotY-shadowTopY));
if(Math.abs(actualSize-targetShadowH)<=tolerance){
score+=10;snd(true);feedback='Harika! Gölge: '+actualSize+' cm ✓';feedbackOk=true;feedbackTimer=80;addP(W/2,540,'#34d399')}
else{snd(false);feedback='Gölge: '+actualSize+' cm — Hedef: '+targetShadowH+' cm';feedbackOk=false;feedbackTimer=80;addP(W/2,540,'#ef4444')}
setTimeout(()=>{round++;if(round>maxR){state='win';for(let i=0;i<25;i++)addP(W/2+Math.random()*200-100,300)}else setupRound()},1200)}

cv.addEventListener('mousedown',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>340&&my<390){startGame()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){startGame()}return}
if(state==='play'){
if(mx>W/2-60&&mx<W/2+60&&my>580&&my<625){checkAnswer();return}
if(Math.hypot(mx-lightX,my-lightY)<40){dragging=true}}});

cv.addEventListener('mousemove',e=>{if(!dragging)return;const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width);
lightX=Math.max(80,Math.min(objX-30,mx))});

cv.addEventListener('mouseup',()=>{dragging=false});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
const r=cv.getBoundingClientRect();
const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){
cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));return}
if(state==='play'){
if(mx>W/2-60&&mx<W/2+60&&my>580&&my<625){checkAnswer();return}
if(Math.hypot(mx-lightX,my-lightY)<50){dragging=true}}});

cv.addEventListener('touchmove',e=>{e.preventDefault();if(!dragging)return;
const t=e.touches[0];const r=cv.getBoundingClientRect();
const mx=(t.clientX-r.left)*(W/r.width);
lightX=Math.max(80,Math.min(objX-30,mx))});

cv.addEventListener('touchend',()=>{dragging=false});

setupRound();upd();
</script></body></html>"""


def _build_elem_sci_ses_dalgasi_html():
    """Ses Dalgası Stüdyosu — Frekans ve genliği ayarlayarak ses dalgaları oluştur."""
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
let freq=300,amp=0.5;
let freqMin=100,freqMax=800,ampMin=0.1,ampMax=1.0;
let freqSliderX=350,ampSliderX=350;
let draggingFreq=false,draggingAmp=false;
let wavePhase=0,speakerVibT=0,playing=false,playTimer=0;
let feedback='',feedbackTimer=0,feedbackOk=false;

const TASKS=[
{desc:'İnce (yüksek frekans) ve Güçlü (yüksek genlik) ses yap!',freqRange:[500,800],ampRange:[0.7,1.0],freqLabel:'Yüksek',ampLabel:'Güçlü'},
{desc:'Kalın (düşük frekans) ve Zayıf (düşük genlik) ses yap!',freqRange:[100,300],ampRange:[0.1,0.4],freqLabel:'Düşük',ampLabel:'Zayıf'},
{desc:'Kalın (düşük frekans) ve Güçlü (yüksek genlik) ses yap!',freqRange:[100,300],ampRange:[0.7,1.0],freqLabel:'Düşük',ampLabel:'Güçlü'},
{desc:'İnce (yüksek frekans) ve Zayıf (düşük genlik) ses yap!',freqRange:[500,800],ampRange:[0.1,0.4],freqLabel:'Yüksek',ampLabel:'Zayıf'},
{desc:'Orta kalınlıkta ve Güçlü ses yap!',freqRange:[300,500],ampRange:[0.7,1.0],freqLabel:'Orta',ampLabel:'Güçlü'},
{desc:'Orta kalınlıkta ve Zayıf ses yap!',freqRange:[300,500],ampRange:[0.1,0.4],freqLabel:'Orta',ampLabel:'Zayıf'},
{desc:'Çok ince (en yüksek frekans) ses yap!',freqRange:[650,800],ampRange:[0.3,1.0],freqLabel:'En Yüksek',ampLabel:'Herhangi'},
{desc:'Çok kalın (en düşük frekans) ses yap!',freqRange:[100,200],ampRange:[0.3,1.0],freqLabel:'En Düşük',ampLabel:'Herhangi'},
{desc:'En güçlü ve ince ses yap!',freqRange:[550,800],ampRange:[0.8,1.0],freqLabel:'Yüksek',ampLabel:'En Güçlü'},
{desc:'En zayıf ve kalın ses yap!',freqRange:[100,250],ampRange:[0.1,0.3],freqLabel:'Düşük',ampLabel:'En Zayıf'}
];
let currentTask=TASKS[0];
let taskOrder=[0,1,2,3,4,5,6,7,8,9];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<8;i++)particles.push({x,y,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*3})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}

function playSound(){
try{const actx=new AudioContext();const osc=actx.createOscillator();const gain=actx.createGain();
osc.connect(gain);gain.connect(actx.destination);osc.frequency.value=freq;osc.type='sine';
gain.gain.value=amp*0.4;osc.start();
gain.gain.exponentialRampToValueAtTime(0.001,actx.currentTime+0.8);osc.stop(actx.currentTime+0.8);
playing=true;playTimer=50;speakerVibT=0}catch(e){}}

function setupRound(){
currentTask=TASKS[taskOrder[(round-1)%taskOrder.length]];
freq=300;amp=0.5;
freqSliderX=150+(freq-freqMin)/(freqMax-freqMin)*400;
ampSliderX=150+(amp-ampMin)/(ampMax-ampMin)*400;
feedback='';feedbackTimer=0}

function startGame(){state='play';score=0;round=1;taskOrder=shuffle([...Array(10).keys()]);setupRound()}

function drawWaveform(){
const cx=W/2,cy=200,ww=500,wh=100;
ctx.fillStyle='rgba(30,27,75,0.6)';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
ctx.beginPath();ctx.roundRect(cx-ww/2,cy-wh,ww,wh*2,12);ctx.fill();ctx.stroke();
ctx.fillStyle='rgba(167,139,250,0.1)';
ctx.beginPath();ctx.moveTo(cx-ww/2,cy);ctx.lineTo(cx+ww/2,cy);ctx.stroke();
const period=freqMax/freq;const amplitude=amp*wh*0.8;
ctx.strokeStyle='#60a5fa';ctx.lineWidth=3;ctx.beginPath();
for(let x=-ww/2;x<=ww/2;x++){
const y=Math.sin((x/period)*0.3+wavePhase)*amplitude;
if(x===-ww/2)ctx.moveTo(cx+x,cy+y);else ctx.lineTo(cx+x,cy+y)}
ctx.stroke();
const glow=ctx.createLinearGradient(cx-ww/2,cy-amplitude,cx-ww/2,cy+amplitude);
glow.addColorStop(0,'rgba(96,165,250,0)');glow.addColorStop(0.5,'rgba(96,165,250,0.1)');glow.addColorStop(1,'rgba(96,165,250,0)');
ctx.fillStyle=glow;ctx.beginPath();
for(let x=-ww/2;x<=ww/2;x++){
const y=Math.sin((x/period)*0.3+wavePhase)*amplitude;
if(x===-ww/2)ctx.moveTo(cx+x,cy+y);else ctx.lineTo(cx+x,cy+y)}
for(let x=ww/2;x>=-ww/2;x--){ctx.lineTo(cx+x,cy)}
ctx.fill();
ctx.fillStyle='#e9d5ff';ctx.font='11px Segoe UI';ctx.textAlign='left';ctx.fillText('Dalga Formu',cx-ww/2+10,cy-wh+18)}

function drawSlider(label,x,y,val,minV,maxV,leftLabel,rightLabel,color){
const slW=400,slH=8,knobR=14;
ctx.fillStyle='rgba(30,27,75,0.8)';ctx.fillRect(x,y-slH/2,slW,slH);
const filled=(val-minV)/(maxV-minV);
ctx.fillStyle=color;ctx.fillRect(x,y-slH/2,slW*filled,slH);
const knobX=x+slW*filled;
ctx.fillStyle=color;ctx.beginPath();ctx.arc(knobX,y,knobR,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 11px Segoe UI';ctx.textAlign='center';
ctx.fillText(Math.round(val),knobX,y+4);
ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.textAlign='right';ctx.fillText(label,x-10,y+5);
ctx.fillStyle='#94a3b8';ctx.font='11px Segoe UI';ctx.textAlign='center';
ctx.fillText(leftLabel,x+30,y+28);ctx.fillText(rightLabel,x+slW-30,y+28);
return{x,y,w:slW,knobX}}

function drawSpeaker(){
const sx=580,sy=200;
const vibOff=playing?Math.sin(speakerVibT*0.5)*4:0;
ctx.font='50px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('🔊',sx+vibOff,sy);ctx.textBaseline='alphabetic';
if(playing){
for(let i=1;i<=3;i++){
ctx.strokeStyle='rgba(96,165,250,'+(0.5-i*0.12)+')';ctx.lineWidth=2;
ctx.beginPath();ctx.arc(sx+15,sy,20+i*12,-0.5,0.5);ctx.stroke()}}}

function drawPlayBtn(){
ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.roundRect(150,520,150,45,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('🔊 Çal!',225,550)}

function drawCheckBtn(){
ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(400,520,150,45,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('✓ Kontrol!',475,550)}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎵 Ses Dalgası Stüdyosu',W/2,160);
ctx.font='20px Segoe UI';ctx.fillText('Frekans ve genliği ayarla, sesi duy!',W/2,210);
ctx.font='16px Segoe UI';ctx.fillStyle='#a78bfa';
ctx.fillText('Frekans ↑ = İnce ses | Frekans ↓ = Kalın ses',W/2,260);
ctx.fillText('Genlik ↑ = Güçlü ses | Genlik ↓ = Zayıf ses',W/2,285);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,330,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,360);
return}

if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Ses Mühendisi! 🎉',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxR*10,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);

ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';
const taskLines=currentTask.desc;
ctx.fillText(taskLines,W/2,60);

drawWaveform();drawSpeaker();

const freqInfo=drawSlider('Frekans',150,380,freq,freqMin,freqMax,'Kalın Ses','İnce Ses','#60a5fa');
const ampInfo=drawSlider('Genlik',150,450,amp,ampMin,ampMax,'Zayıf','Güçlü','#f472b6');

ctx.fillStyle='#94a3b8';ctx.font='12px Segoe UI';ctx.textAlign='center';
ctx.fillText('Frekans: '+Math.round(freq)+' Hz',W/2,410);
ctx.fillText('Genlik: '+amp.toFixed(2),W/2,480);

drawPlayBtn();drawCheckBtn();

if(feedbackTimer>0){
feedbackTimer--;
ctx.fillStyle=feedbackOk?'rgba(16,185,129,0.9)':'rgba(239,68,68,0.9)';
ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,600)}

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
wavePhase+=0.08;
if(playing){speakerVibT++;playTimer--;if(playTimer<=0)playing=false}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}

function checkAnswer(){
const t=currentTask;
const freqOk=freq>=t.freqRange[0]&&freq<=t.freqRange[1];
const ampOk=amp>=t.ampRange[0]&&amp<=t.ampRange[1];
if(freqOk&&ampOk){
score+=10;snd(true);feedback='Harika! Doğru ses kombinasyonu! ✓';feedbackOk=true;feedbackTimer=80;addP(W/2,580,'#34d399')}
else{
let hint='';
if(!freqOk)hint+='Frekans '+t.freqLabel+' olmalı. ';
if(!ampOk)hint+='Genlik '+t.ampLabel+' olmalı.';
snd(false);feedback=hint;feedbackOk=false;feedbackTimer=100;addP(W/2,580,'#ef4444')}
setTimeout(()=>{round++;if(round>maxR){state='win';for(let i=0;i<25;i++)addP(W/2+Math.random()*200-100,300)}else setupRound()},1500)}

cv.addEventListener('mousedown',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<380){startGame()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){startGame()}return}
if(state==='play'){
if(mx>150&&mx<400&&my>520&&my<565){playSound();return}
if(mx>400&&mx<550&&my>520&&my<565){checkAnswer();return}
if(my>365&&my<395&&mx>140&&mx<560){draggingFreq=true}
if(my>435&&my<465&&mx>140&&mx<560){draggingAmp=true}}});

cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width);
if(draggingFreq){const t=Math.max(0,Math.min(1,(mx-150)/400));freq=freqMin+t*(freqMax-freqMin);freqSliderX=150+t*400}
if(draggingAmp){const t=Math.max(0,Math.min(1,(mx-150)/400));amp=ampMin+t*(ampMax-ampMin);ampSliderX=150+t*400}});

cv.addEventListener('mouseup',()=>{draggingFreq=false;draggingAmp=false});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',e=>{e.preventDefault();
cv.dispatchEvent(new MouseEvent('mouseup',{}))});

setupRound();upd();
</script></body></html>"""


def _build_elem_sci_miknatis_pusula_html():
    """Mıknatıs & Pusula Kaşifi — Pusula ve mıknatıs ipuçlarıyla hazine bul."""
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
const GS=8,cellW=50,cellH=50;
const gridX=60,gridY=100;
let treasureR=0,treasureC=0;
let magnetR=-1,magnetC=-1,magnetPlaced=false;
let compassAngle=0,compassTargetAngle=0;
let feedback='',feedbackTimer=0,feedbackOk=false;
let dugCells=[];
let mode='magnet';
let hintText='';
let revealTreasure=false,revealTimer=0;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<8;i++)particles.push({x,y,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*3})}

function setupRound(){
treasureR=Math.floor(Math.random()*GS);treasureC=Math.floor(Math.random()*GS);
magnetR=-1;magnetC=-1;magnetPlaced=false;
dugCells=[];mode='magnet';hintText='Mıknatısı haritaya yerleştir!';
revealTreasure=false;revealTimer=0;
compassTargetAngle=0;feedback='';feedbackTimer=0}

function startGame(){state='play';score=0;round=1;setupRound()}

function getAngleToTreasure(fromR,fromC){
const dx=treasureC-fromC;const dy=treasureR-fromR;
return Math.atan2(dy,dx)}

function getDistance(r1,c1,r2,c2){return Math.sqrt((r1-r2)*(r1-r2)+(c1-c2)*(c1-c2))}

function getHeatText(dist){
if(dist<=1)return '🔥 Çok Sıcak!';
if(dist<=2)return '🌡️ Sıcak!';
if(dist<=3.5)return '😐 Ilık';
if(dist<=5)return '❄️ Soğuk';
return '🧊 Çok Soğuk!'}

function getHeatColor(dist){
if(dist<=1)return '#ef4444';
if(dist<=2)return '#f97316';
if(dist<=3.5)return '#fbbf24';
if(dist<=5)return '#60a5fa';
return '#94a3b8'}

function drawGrid(){
for(let r=0;r<GS;r++){for(let c=0;c<GS;c++){
const x=gridX+c*cellW,y=gridY+r*cellH;
const isDug=dugCells.some(d=>d.r===r&&d.c===c);
if(isDug){
const dist=getDistance(r,c,treasureR,treasureC);
ctx.fillStyle=getHeatColor(dist);ctx.globalAlpha=0.3;ctx.fillRect(x,y,cellW,cellH);ctx.globalAlpha=1}
else{
ctx.fillStyle=(r+c)%2===0?'rgba(34,197,94,0.25)':'rgba(22,163,74,0.2)';ctx.fillRect(x,y,cellW,cellH)}
ctx.strokeStyle='rgba(34,197,94,0.3)';ctx.lineWidth=1;ctx.strokeRect(x,y,cellW,cellH);
if(isDug){
const dist=getDistance(r,c,treasureR,treasureC);
ctx.font='9px Segoe UI';ctx.textAlign='center';ctx.fillStyle=getHeatColor(dist);
ctx.fillText(getHeatText(dist).split(' ')[1]||'',x+cellW/2,y+cellH/2+4)}
if(revealTreasure&&r===treasureR&&c===treasureC){
ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('💎',x+cellW/2,y+cellH/2);ctx.textBaseline='alphabetic'}
if(magnetPlaced&&r===magnetR&&c===magnetC){
ctx.font='24px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('🧲',x+cellW/2,y+cellH/2);ctx.textBaseline='alphabetic'}
}}}

function drawCompass(){
const cx=570,cy=250,cr=65;
ctx.fillStyle='rgba(30,27,75,0.8)';ctx.beginPath();ctx.arc(cx,cy,cr+10,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();ctx.arc(cx,cy,cr+10,0,Math.PI*2);ctx.stroke();
ctx.fillStyle='rgba(167,139,250,0.1)';ctx.beginPath();ctx.arc(cx,cy,cr,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='rgba(167,139,250,0.5)';ctx.lineWidth=1;ctx.beginPath();ctx.arc(cx,cy,cr,0,Math.PI*2);ctx.stroke();
const dirs=[{l:'K',a:-Math.PI/2},{l:'D',a:0},{l:'G',a:Math.PI/2},{l:'B',a:Math.PI}];
dirs.forEach(d=>{
ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(d.l,cx+Math.cos(d.a)*(cr-12),cy+Math.sin(d.a)*(cr-12))});ctx.textBaseline='alphabetic';
ctx.save();ctx.translate(cx,cy);ctx.rotate(compassAngle);
ctx.fillStyle='#ef4444';ctx.beginPath();ctx.moveTo(0,-cr+20);ctx.lineTo(-8,0);ctx.lineTo(8,0);ctx.closePath();ctx.fill();
ctx.fillStyle='#e2e8f0';ctx.beginPath();ctx.moveTo(0,cr-20);ctx.lineTo(-8,0);ctx.lineTo(8,0);ctx.closePath();ctx.fill();
ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(0,0,6,0,Math.PI*2);ctx.fill();
ctx.restore();
ctx.fillStyle='#e9d5ff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';ctx.fillText('Pusula',cx,cy+cr+25);
if(magnetPlaced){ctx.fillStyle='#fbbf24';ctx.font='11px Segoe UI';ctx.fillText('Mıknatıs etki alanında',cx,cy+cr+40)}}

function drawModeButtons(){
const bx1=490,bx2=490,by1=420,by2=475,bw=160,bh=40;
ctx.fillStyle=mode==='magnet'?'#7c3aed':'rgba(30,27,75,0.6)';
ctx.beginPath();ctx.roundRect(bx1,by1,bw,bh,10);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText('🧲 Mıknatıs',bx1+bw/2,by1+26);
ctx.fillStyle=mode==='dig'?'#7c3aed':'rgba(30,27,75,0.6)';
ctx.beginPath();ctx.roundRect(bx2,by2,bw,bh,10);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText('⛏️ Kaz!',bx2+bw/2,by2+26)}

function drawHintPanel(){
ctx.fillStyle='rgba(30,27,75,0.6)';ctx.beginPath();ctx.roundRect(470,530,210,80,10);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';
ctx.fillText('İpucu',575,550);
ctx.fillStyle='#fbbf24';ctx.font='14px Segoe UI';
const lines=hintText.match(/.{1,25}(\\s|$)/g)||[hintText];
lines.forEach((line,i)=>{ctx.fillText(line.trim(),575,570+i*16)})}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🧲 Mıknatıs & Pusula Kaşifi',W/2,160);
ctx.font='20px Segoe UI';ctx.fillText('Pusula ve mıknatıs ipuçlarıyla',W/2,210);
ctx.fillText('gizli hazineyi bul!',W/2,240);
ctx.font='16px Segoe UI';ctx.fillStyle='#a78bfa';
ctx.fillText('1. Mıknatısı yerleştir → Pusula yönünü izle',W/2,280);
ctx.fillText('2. Kaz moduna geç → Hazineyi bul!',W/2,305);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,340,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,370);
return}

if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Hazine Avcısı! 🎉',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxR*10,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';
ctx.fillText(mode==='magnet'?'🧲 Mıknatısı haritaya yerleştir':'⛏️ Hazineyi bulmak için bir kareye tıkla',W/2,70);

drawGrid();drawCompass();drawModeButtons();drawHintPanel();

if(feedbackTimer>0){
feedbackTimer--;
ctx.fillStyle=feedbackOk?'rgba(16,185,129,0.9)':'rgba(239,68,68,0.9)';
ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,300,580)}

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function upd(){
const angleDiff=compassTargetAngle-compassAngle;
let da=angleDiff;
while(da>Math.PI)da-=Math.PI*2;
while(da<-Math.PI)da+=Math.PI*2;
compassAngle+=da*0.08;
if(feedbackTimer>0)feedbackTimer--;
if(revealTreasure){revealTimer++;
if(revealTimer>80){round++;
if(round>maxR){state='win';for(let i=0;i<30;i++)addP(W/2+Math.random()*200-100,300)}else setupRound()}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}

cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);

if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>340&&my<390){startGame()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){startGame()}return}
if(state!=='play'||revealTreasure)return;

if(mx>490&&mx<650&&my>420&&my<460){mode='magnet';return}
if(mx>490&&mx<650&&my>475&&my<515){mode='dig';return}

const gc=Math.floor((mx-gridX)/cellW);
const gr=Math.floor((my-gridY)/cellH);
if(gc>=0&&gc<GS&&gr>=0&&gr<GS){
if(mode==='magnet'){
magnetR=gr;magnetC=gc;magnetPlaced=true;
const angleToTreasure=getAngleToTreasure(gr,gc);
compassTargetAngle=angleToTreasure+Math.PI/2;
const dist=getDistance(gr,gc,treasureR,treasureC);
hintText=getHeatText(dist);
addP(gridX+gc*cellW+cellW/2,gridY+gr*cellH+cellH/2,'#a78bfa')}
else if(mode==='dig'){
if(dugCells.some(d=>d.r===gr&&d.c===gc))return;
dugCells.push({r:gr,c:gc});
if(gr===treasureR&&gc===treasureC){
score+=10;snd(true);feedback='Hazineyi buldun! 💎';feedbackOk=true;feedbackTimer=80;
revealTreasure=true;revealTimer=0;
addP(gridX+gc*cellW+cellW/2,gridY+gr*cellH+cellH/2,'#fbbf24')}
else{
const dist=getDistance(gr,gc,treasureR,treasureC);
hintText=getHeatText(dist);
if(dugCells.length>=10&&!revealTreasure){
feedback='Çok fazla kazma! Hazine kaçtı...';feedbackOk=false;feedbackTimer=80;snd(false);
revealTreasure=true;revealTimer=0}
else{addP(gridX+gc*cellW+cellW/2,gridY+gr*cellH+cellH/2,'#78716c')}}}}});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
setupRound();upd();
</script></body></html>"""


def _build_elem_sci_su_dongusu_html():
    """Su Döngüsü Simülatörü — Su döngüsünün 4 aşamasını sırasıyla tamamla."""
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
let phase=0,waveT=0;
let steamParts=[],rainDrops=[],riverDrops=[];
let sunClicks=0,sunNeeded=5;
let cloudFill=0,cloudMax=80;
let rainClicks=0,rainNeeded=3;
let flowClicks=0,flowNeeded=3;
let stageOrder=[],stageOrderIdx=0;
let orderPhase='order';
let orderSlots=[null,null,null,null];
let availableStages=[0,1,2,3];
let feedback='',feedbackTimer=0,feedbackOk=false;
let extraType='normal';

const STAGES=[
{name:'Buharlaşma',emoji:'☀️',color:'#fbbf24',desc:'Güneş suyu ısıtır'},
{name:'Yoğunlaşma',emoji:'☁️',color:'#94a3b8',desc:'Buhar bulut olur'},
{name:'Yağış',emoji:'🌧️',color:'#60a5fa',desc:'Bulut yağmur yağdırır'},
{name:'Akış',emoji:'🌊',color:'#3b82f6',desc:'Su okyanusa döner'}
];
const CORRECT_ORDER=[0,1,2,3];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<8;i++)particles.push({x,y,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,life:1,clr:c||COLORS[Math.floor(Math.random()*COLORS.length)],r:2+Math.random()*3})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}

function setupRound(){
phase=0;orderPhase='order';
orderSlots=[null,null,null,null];
availableStages=shuffle([0,1,2,3]);
steamParts=[];rainDrops=[];riverDrops=[];
sunClicks=0;sunNeeded=Math.max(3,7-Math.floor(round/3));
cloudFill=0;cloudMax=60+round*5;
rainClicks=0;rainNeeded=3;
flowClicks=0;flowNeeded=3;
feedback='';feedbackTimer=0;
if(round<=3)extraType='normal';
else if(round<=6)extraType=Math.random()>0.5?'snow':'normal';
else if(round<=8)extraType=Math.random()>0.5?'hail':'snow';
else extraType=['snow','hail','ground'][Math.floor(Math.random()*3)]}

function startGame(){state='play';score=0;round=1;setupRound()}

function drawSky(){
const g=ctx.createLinearGradient(0,0,0,200);
g.addColorStop(0,'#0c1445');g.addColorStop(1,'#1e3a5f');
ctx.fillStyle=g;ctx.fillRect(0,0,W,200)}

function drawMountain(){
ctx.fillStyle='#2d4a22';ctx.beginPath();
ctx.moveTo(200,350);ctx.lineTo(350,150);ctx.lineTo(500,350);ctx.closePath();ctx.fill();
ctx.fillStyle='#3a5f2e';ctx.beginPath();
ctx.moveTo(350,350);ctx.lineTo(480,200);ctx.lineTo(600,350);ctx.closePath();ctx.fill();
if(extraType==='snow'||extraType==='hail'){
ctx.fillStyle='#fff';ctx.beginPath();ctx.moveTo(330,180);ctx.lineTo(350,150);ctx.lineTo(370,180);ctx.closePath();ctx.fill();
ctx.beginPath();ctx.moveTo(465,220);ctx.lineTo(480,200);ctx.lineTo(495,220);ctx.closePath();ctx.fill()}}

function drawOcean(){
waveT+=0.03;
const oy=420;
const g=ctx.createLinearGradient(0,oy,0,H);
g.addColorStop(0,'#1e90ff');g.addColorStop(0.5,'#1565c0');g.addColorStop(1,'#0d47a1');
ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(0,H);
for(let x=0;x<=200;x+=3){const y=oy+Math.sin(x*0.03+waveT)*5;ctx.lineTo(x,y)}
ctx.lineTo(200,H);ctx.closePath();ctx.fill();
ctx.beginPath();ctx.moveTo(500,H);
for(let x=500;x<=W;x+=3){const y=oy+Math.sin(x*0.03+waveT+1)*5;ctx.lineTo(x,y)}
ctx.lineTo(W,H);ctx.closePath();ctx.fill()}

function drawGround(){
ctx.fillStyle='#2d5016';ctx.fillRect(0,350,W,70);
const g=ctx.createLinearGradient(0,350,0,420);
g.addColorStop(0,'#3a6b20');g.addColorStop(1,'#1e3a0e');
ctx.fillStyle=g;ctx.fillRect(200,350,300,70);
if(extraType==='ground'){
ctx.fillStyle='rgba(30,144,255,0.3)';ctx.font='11px Segoe UI';ctx.textAlign='center';
ctx.fillText('Yer altı suyu ↓',350,405);
ctx.strokeStyle='rgba(30,144,255,0.3)';ctx.setLineDash([3,3]);ctx.lineWidth=1;
ctx.beginPath();ctx.moveTo(250,395);ctx.lineTo(450,395);ctx.stroke();ctx.setLineDash([])}}

function drawRiver(){
ctx.strokeStyle='#3b82f6';ctx.lineWidth=12;ctx.lineCap='round';
ctx.beginPath();ctx.moveTo(350,350);
ctx.quadraticCurveTo(300,380,250,400);
ctx.quadraticCurveTo(200,420,150,430);
ctx.quadraticCurveTo(100,440,80,445);
ctx.stroke();
ctx.strokeStyle='rgba(100,200,255,0.3)';ctx.lineWidth=6;ctx.stroke();
riverDrops.forEach(d=>{
ctx.fillStyle='rgba(100,180,255,'+d.alpha+')';
ctx.beginPath();ctx.arc(d.x,d.y,3,0,Math.PI*2);ctx.fill()})}

function drawSun(){
const sx=100,sy=80,sr=40;
const hot=orderPhase==='animate'&&phase===0;
if(hot){
for(let i=0;i<12;i++){const a=i*Math.PI/6+Date.now()*0.002;
ctx.strokeStyle='rgba(255,200,0,0.3)';ctx.lineWidth=3;ctx.beginPath();
ctx.moveTo(sx+Math.cos(a)*(sr+5),sy+Math.sin(a)*(sr+5));
ctx.lineTo(sx+Math.cos(a)*(sr+20),sy+Math.sin(a)*(sr+20));ctx.stroke()}}
const sg=ctx.createRadialGradient(sx,sy,0,sx,sy,sr);
sg.addColorStop(0,'#fff700');sg.addColorStop(0.5,'#ffb300');sg.addColorStop(1,'rgba(255,150,0,0.3)');
ctx.fillStyle=sg;ctx.beginPath();ctx.arc(sx,sy,sr,0,Math.PI*2);ctx.fill();
ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('☀️',sx,sy);ctx.textBaseline='alphabetic';
if(orderPhase==='animate'&&phase===0){
ctx.fillStyle='#fbbf24';ctx.font='bold 12px Segoe UI';
ctx.fillText('Tıkla! ('+sunClicks+'/'+sunNeeded+')',sx,sy+sr+18)}}

function drawCloud(){
const cx=350,cy=100;
const fill=Math.min(cloudFill/cloudMax,1);
const gray=Math.floor(220-fill*170);
ctx.fillStyle='rgb('+gray+','+gray+','+(gray+15)+')';
const s=0.5+fill*0.6;
ctx.beginPath();ctx.arc(cx,cy,30*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx-30*s,cy+8,22*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx+30*s,cy+8,25*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx-12*s,cy-12*s,18*s,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(cx+14*s,cy-10*s,20*s,0,Math.PI*2);ctx.fill();
if(orderPhase==='animate'&&phase===2){
ctx.fillStyle='#60a5fa';ctx.font='bold 12px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tıkla! ('+rainClicks+'/'+rainNeeded+')',cx,cy+40*s+15)}}

function drawSteam(){
steamParts.forEach(s=>{
ctx.fillStyle='rgba(200,220,255,'+s.alpha*0.6+')';
ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill()})}

function drawRain(){
rainDrops.forEach(d=>{
ctx.fillStyle='rgba(100,180,255,'+d.alpha+')';
if(extraType==='snow'&&round>3){
ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText('❄️',d.x,d.y)}
else if(extraType==='hail'&&round>5){
ctx.beginPath();ctx.arc(d.x,d.y,4,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='rgba(255,255,255,0.5)';ctx.lineWidth=1;ctx.stroke()}
else{
ctx.beginPath();ctx.moveTo(d.x,d.y-5);ctx.quadraticCurveTo(d.x+3,d.y,d.x,d.y+5);
ctx.quadraticCurveTo(d.x-3,d.y,d.x,d.y-5);ctx.fill()}})}

function drawFlowArrows(){
if(orderPhase==='animate'&&phase===3){
const arrows=[[200,380,'→'],[150,410,'→'],[100,435,'→']];
arrows.forEach(a=>{
ctx.fillStyle='rgba(59,130,246,'+Math.abs(Math.sin(Date.now()*0.005))+')';
ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText(a[2],a[0],a[1])});
ctx.fillStyle='#3b82f6';ctx.font='bold 12px Segoe UI';ctx.textAlign='center';
ctx.fillText('Oklara tıkla! ('+flowClicks+'/'+flowNeeded+')',180,460)}}

function drawPhaseIndicator(){
const py=H-55;
for(let i=0;i<4;i++){
const px=120+i*140;
const done=orderPhase==='animate'&&i<phase;
const active=orderPhase==='animate'&&i===phase;
ctx.fillStyle=done?'rgba(16,185,129,0.3)':active?'rgba(251,191,36,0.3)':'rgba(30,27,75,0.5)';
ctx.beginPath();ctx.roundRect(px,py,120,40,8);ctx.fill();
ctx.strokeStyle=done?'#10b981':active?'#fbbf24':'#4b5563';ctx.lineWidth=active?2:1;ctx.stroke();
ctx.fillStyle=done?'#10b981':active?'#fbbf24':'#94a3b8';
ctx.font='bold 12px Segoe UI';ctx.textAlign='center';
ctx.fillText(STAGES[i].emoji+' '+STAGES[i].name,px+60,py+26);
if(i<3){ctx.fillStyle='#4b5563';ctx.fillText('→',px+128,py+20)}}}

function drawOrderPhase(){
ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Su döngüsünün doğru sırasını oluştur!',W/2,50);
for(let i=0;i<4;i++){
const x=80+i*160,y=480;
ctx.fillStyle='rgba(30,27,75,0.6)';ctx.beginPath();ctx.roundRect(x,y,140,60,10);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.stroke();
if(orderSlots[i]!==null){
const s=STAGES[orderSlots[i]];
ctx.fillStyle=s.color;ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText(s.emoji+' '+s.name,x+70,y+25);
ctx.fillStyle='#94a3b8';ctx.font='11px Segoe UI';ctx.fillText(s.desc,x+70,y+45)}
else{ctx.fillStyle='#4b5563';ctx.font='14px Segoe UI';ctx.textAlign='center';ctx.fillText((i+1)+'. aşama',x+70,y+35)}}
ctx.fillStyle='#e9d5ff';ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText('Aşağıdan doğru sırayla seç:',W/2,560);
const remaining=availableStages.filter(s=>!orderSlots.includes(s));
remaining.forEach((si,idx)=>{
const bx=150+idx*140,by=580;
ctx.fillStyle=STAGES[si].color;ctx.globalAlpha=0.8;ctx.beginPath();ctx.roundRect(bx,by,120,45,8);ctx.fill();ctx.globalAlpha=1;
ctx.strokeStyle='#fff';ctx.lineWidth=1;ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';
ctx.fillText(STAGES[si].emoji+' '+STAGES[si].name,bx+60,by+28)})}

function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('💧 Su Döngüsü Simülatörü',W/2,140);
ctx.font='20px Segoe UI';ctx.fillText('Su döngüsünün 4 aşamasını',W/2,190);
ctx.fillText('doğru sırayla tamamla!',W/2,220);
ctx.font='16px Segoe UI';ctx.fillStyle='#a78bfa';
ctx.fillText('☀️ Buharlaşma → ☁️ Yoğunlaşma → 🌧️ Yağış → 🌊 Akış',W/2,270);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);
return}

if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Su Döngüsü Uzmanı! 🎉',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxR*10,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,320,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
return}

ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,25);
if(extraType!=='normal'){
ctx.fillStyle='#fbbf24';ctx.font='13px Segoe UI';
const xt=extraType==='snow'?'❄️ Kar yağışlı tur':extraType==='hail'?'🧊 Dolu yağışlı tur':'🌍 Yer altı sulu tur';
ctx.fillText(xt,W/2,45)}

drawSky();drawOcean();drawGround();drawMountain();drawRiver();drawSun();drawCloud();drawSteam();drawRain();drawFlowArrows();

if(orderPhase==='order'){drawOrderPhase()}
else{drawPhaseIndicator();
if(phase===0){ctx.fillStyle='rgba(255,200,50,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('☀️ Buharlaşma — Güneşe tıkla!',W/2,55)}
if(phase===1){ctx.fillStyle='rgba(200,200,255,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('☁️ Yoğunlaşma — Buhar yükseliyor...',W/2,55)}
if(phase===2){ctx.fillStyle='rgba(100,180,255,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('🌧️ Yağış — Buluta tıkla!',W/2,55)}
if(phase===3){ctx.fillStyle='rgba(59,130,246,'+Math.abs(Math.sin(Date.now()*0.003))*0.8+')';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('🌊 Akış — Oklara tıkla!',W/2,55)}}

if(feedbackTimer>0){
feedbackTimer--;
ctx.fillStyle=feedbackOk?'rgba(16,185,129,0.9)':'rgba(239,68,68,0.9)';
ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,470)}

particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}

function addSteam(){
for(let i=0;i<3;i++){steamParts.push({x:80+Math.random()*120,y:410,vy:-1.5-Math.random()*1,vx:(Math.random()-.5)*0.8,r:3+Math.random()*4,alpha:1})}}

function addRain(){
for(let i=0;i<8;i++){rainDrops.push({x:320+Math.random()*60,y:130+Math.random()*10,vy:2+Math.random()*2,alpha:0.8+Math.random()*0.2})}}

function addRiverDrop(){
riverDrops.push({x:350,y:350,vx:-2-Math.random(),vy:0.5+Math.random(),alpha:1})}

function upd(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.08});
particles=particles.filter(p=>p.life>0);
if(feedbackTimer>0)feedbackTimer--;

if(state==='play'&&orderPhase==='animate'){
if(phase===0&&sunClicks>=sunNeeded){phase=1;addSteam();addSteam();addSteam()}

steamParts.forEach(s=>{s.y+=s.vy;s.x+=s.vx;
if(s.y<130){s.alpha-=0.03;cloudFill+=0.5}else{s.alpha-=0.003}});
steamParts=steamParts.filter(s=>s.alpha>0);

if(phase===1){
if(Math.random()<0.06)addSteam();
if(cloudFill>=cloudMax){phase=2}}

if(phase===2){
rainDrops.forEach(d=>{d.y+=d.vy;d.vy+=0.04;
if(d.y>400){d.alpha-=0.15;addP(d.x,400,'#60a5fa')}});
rainDrops=rainDrops.filter(d=>d.alpha>0);
if(rainClicks>=rainNeeded&&rainDrops.length===0){phase=3}}

if(phase===3){
riverDrops.forEach(d=>{d.x+=d.vx;d.y+=d.vy;d.alpha-=0.008;
if(d.x<80)d.alpha-=0.05});
riverDrops=riverDrops.filter(d=>d.alpha>0);
if(flowClicks>=flowNeeded&&riverDrops.length===0){
score+=10;snd(true);addP(W/2,300,'#fbbf24');
feedback='Su döngüsü tamamlandı! ✓';feedbackOk=true;feedbackTimer=80;
setTimeout(()=>{round++;
if(round>maxR){state='win';for(let i=0;i<30;i++)addP(W/2+Math.random()*200-100,300)}
else setupRound()},1200)}}}

draw();requestAnimationFrame(upd)}

cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();
const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);

if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){startGame()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){startGame()}return}
if(state!=='play')return;

if(orderPhase==='order'){
const remaining=availableStages.filter(s=>!orderSlots.includes(s));
remaining.forEach((si,idx)=>{
const bx=150+idx*140,by=580;
if(mx>bx&&mx<bx+120&&my>by&&my<by+45){
const nextSlot=orderSlots.indexOf(null);
if(nextSlot>=0){orderSlots[nextSlot]=si;addP(bx+60,by+22,STAGES[si].color);
if(nextSlot===3){
const correct=orderSlots.every((s,i)=>s===CORRECT_ORDER[i]);
if(correct){feedback='Doğru sıra! Şimdi döngüyü başlat!';feedbackOk=true;feedbackTimer=80;snd(true);
setTimeout(()=>{orderPhase='animate';phase=0},800)}
else{feedback='Yanlış sıra! Tekrar dene.';feedbackOk=false;feedbackTimer=80;snd(false);
setTimeout(()=>{orderSlots=[null,null,null,null]},1000)}}}}});
return}

if(orderPhase==='animate'){
if(phase===0){
const sx=100,sy=80;
if(Math.hypot(mx-sx,my-sy)<50){sunClicks++;addSteam();addP(sx,sy,'#fbbf24');if(sunClicks<sunNeeded)snd(true)}}
if(phase===2){
const cx=350,cy=100;
if(Math.hypot(mx-cx,my-cy)<50){rainClicks++;addRain();addP(cx,cy,'#60a5fa');snd(true)}}
if(phase===3){
if(mx>80&&mx<300&&my>360&&my<470){flowClicks++;addRiverDrop();addRiverDrop();addP(mx,my,'#3b82f6');snd(true)}}}});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
setupRound();upd();
</script></body></html>"""
