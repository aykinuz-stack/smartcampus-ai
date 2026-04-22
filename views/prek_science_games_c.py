# -*- coding: utf-8 -*-
"""Okul Öncesi Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm C: 11-15)."""


def _build_prek_sci_hizli_yavas_araba_html():
    """Hızlı–Yavaş Araba — Rampa açısını ayarla, arabayı bırak, hızı karşılaştır."""
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
let rampAngle=1,carX=0,carY=0,carVx=0,carVy=0,carRolling=false,carFinished=false;
let timer=0,timerStart=0,phase='adjust',questionPhase=false;
let angles=[15,30,50],angleIdx=1;
let trialResults=[],correctAnswer=-1,selectedAnswer=-1;
let dustParticles=[],speedLines=[];
let rampStartX,rampStartY,rampEndX,rampEndY,finishX=600;
let friction=0,weight=1;
let dualMode=false,car2X=0,car2Y=0,car2Vx=0,car2Vy=0,car2Rolling=false,car2Finished=false;
let car2AngleIdx=0,car2Timer=0;
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function playEngineSound(){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=90;o.type='sawtooth';
g.gain.value=0.1;o.start();g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.8);
o.stop(a.currentTime+0.8)}catch(e){}}
function addParticles(x,y,clr,n){for(let i=0;i<(n||12);i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr:clr||COLORS[Math.floor(Math.random()*10)],r:2+Math.random()*4})}
function addDust(x,y){for(let i=0;i<3;i++)
dustParticles.push({x,y,vx:(Math.random()-0.5)*2,vy:-Math.random()*2,life:1,r:3+Math.random()*3})}
function calcRamp(aIdx){
const ang=angles[aIdx]*Math.PI/180;
const sx=80,sy=180;
const len=400;
const ex=sx+Math.cos(ang)*len;
const ey=sy+Math.sin(ang)*len;
return{sx,sy,ex,ey,ang}}
function resetCar(){
const r=calcRamp(angleIdx);
rampStartX=r.sx;rampStartY=r.sy;rampEndX=r.ex;rampEndY=r.ey;
carX=r.sx+10;carY=r.sy-15;carVx=0;carVy=0;carRolling=false;carFinished=false;timer=0;
dustParticles=[];speedLines=[];
friction=round>=7?0.15:0;
weight=round>=9?1.5:1}
function resetRound(){
phase='adjust';questionPhase=false;trialResults=[];
dualMode=round>=5;
if(dualMode){
car2AngleIdx=(angleIdx+1)%3;
if(car2AngleIdx===angleIdx)car2AngleIdx=(angleIdx+2)%3}
resetCar()}
function startRoll(){
if(carRolling)return;
const r=calcRamp(angleIdx);
const gravity=0.3*weight;
const ang=r.ang;
carVx=Math.cos(ang)*gravity*2;
carVy=Math.sin(ang)*gravity*2;
carRolling=true;timerStart=Date.now();
playEngineSound();
if(dualMode){
const r2=calcRamp(car2AngleIdx);
const ang2=r2.ang;
car2Vx=Math.cos(ang2)*gravity*2;
car2Vy=Math.sin(ang2)*gravity*2;
car2Rolling=true;car2Finished=false;
const rr=calcRamp(car2AngleIdx);
car2X=rr.sx+10;car2Y=rr.sy-15;car2Timer=0}}
function drawCar(x,y,clr,label){
ctx.save();ctx.translate(x,y);
ctx.fillStyle=clr||'#ef4444';
ctx.beginPath();ctx.roundRect(-20,-18,40,14,4);ctx.fill();
ctx.fillStyle=clr?'#fff':'#fbbf24';
ctx.beginPath();ctx.roundRect(-14,-26,20,10,3);ctx.fill();
ctx.fillStyle='#333';
ctx.beginPath();ctx.arc(-12,0,6,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(12,0,6,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#666';
ctx.beginPath();ctx.arc(-12,0,3,0,Math.PI*2);ctx.fill();
ctx.beginPath();ctx.arc(12,0,3,0,Math.PI*2);ctx.fill();
if(label){ctx.fillStyle='#fff';ctx.font='bold 10px Segoe UI';ctx.textAlign='center';ctx.fillText(label,-0,-12)}
ctx.restore()}
function drawRamp(aIdx,yOff,clr){
const r=calcRamp(aIdx);
ctx.save();
ctx.strokeStyle=clr||'#a78bfa';ctx.lineWidth=6;ctx.lineCap='round';
ctx.beginPath();ctx.moveTo(r.sx,r.sy+(yOff||0));ctx.lineTo(r.ex,r.ey+(yOff||0));ctx.stroke();
ctx.strokeStyle='#7c3aed';ctx.lineWidth=2;
for(let i=0;i<10;i++){
const t=i/10;
const px=r.sx+(r.ex-r.sx)*t;
const py=(r.sy+(yOff||0))+(r.ey-r.sy+(yOff||0)-r.sy-(yOff||0))*t;
const py2=r.sy+(yOff||0)+(r.ey+(yOff||0)-r.sy-(yOff||0))*t;
ctx.beginPath();ctx.moveTo(r.sx+(r.ex-r.sx)*t,r.sy+(yOff||0)+(r.ey-r.sy)*t);
ctx.lineTo(r.sx+(r.ex-r.sx)*t,r.sy+(yOff||0)+(r.ey-r.sy)*t+8);ctx.stroke()}
if(friction>0){ctx.fillStyle='#8B4513';ctx.globalAlpha=0.4;
ctx.beginPath();ctx.moveTo(r.sx,r.sy+(yOff||0));ctx.lineTo(r.ex,r.ey+(yOff||0));
ctx.lineTo(r.ex,r.ey+(yOff||0)+8);ctx.lineTo(r.sx,r.sy+(yOff||0)+8);ctx.fill();ctx.globalAlpha=1}
ctx.fillStyle='#fbbf24';ctx.font='12px Segoe UI';ctx.textAlign='center';
ctx.fillText(angles[aIdx]+'°',r.sx+30,r.sy+(yOff||0)-15);
ctx.restore()}
function drawFinishLine(yOff){
const y1=150+(yOff||0),y2=500+(yOff||0);
for(let i=0;i<20;i++){
ctx.fillStyle=i%2===0?'#fff':'#333';
ctx.fillRect(finishX,y1+i*((y2-y1)/20),10,(y2-y1)/20)}
ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏁',finishX+5,y1-10)}
function draw(){
ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
ctx.fillStyle='#1a3a1a';ctx.fillRect(0,H-60,W,60);
if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🚗 Hızlı–Yavaş Araba 🏎️',W/2,180);
ctx.font='20px Segoe UI';ctx.fillText('Rampa açısını ayarla ve arabayı bırak!',W/2,230);
ctx.fillText('Dik rampa = Hızlı araba!',W/2,265);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏆 Tebrikler! 🏆',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxRound*10,W/2,260);
ctx.font='18px Segoe UI';ctx.fillStyle='#c084fc';
ctx.fillText('Rampaları öğrendin!',W/2,300);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,340,180,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,370);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,30);
ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
if(questionPhase){
ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
const q=dualMode?'Hangi araba daha hızlıydı?':'Hangi rampa daha hızlı?';
ctx.fillText(q,W/2,80);
const opts=dualMode?[angles[angleIdx]+'° (Kırmızı)',angles[car2AngleIdx]+'° (Mavi)']
:[angles[0]+'° (Az Eğim)',angles[1]+'° (Orta)',angles[2]+'° (Dik)'];
const bw=180,bh=45;
for(let i=0;i<opts.length;i++){
const bx=W/2-bw/2;
const by=120+i*60;
const isSelected=selectedAnswer===i;
const isCorrect=i===correctAnswer;
ctx.fillStyle=isSelected?(isCorrect?'#22c55e':'#ef4444'):'#7c3aed';
ctx.beginPath();ctx.roundRect(bx,by,bw,bh,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';
ctx.fillText(opts[i],W/2,by+28)}
if(selectedAnswer>=0){
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-70,120+opts.length*60+20,140,40,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('Devam →',W/2,120+opts.length*60+45)}
} else {
drawRamp(angleIdx,0,'#a78bfa');
drawFinishLine(0);
if(dualMode){drawRamp(car2AngleIdx,150,'#60a5fa')}
if(!carRolling&&phase==='adjust'){
ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Açı: '+angles[angleIdx]+'°',W/2,65);
const btnW=50,btnH=40;
ctx.fillStyle='#34d399';ctx.beginPath();ctx.roundRect(200,75,btnW,btnH,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▲',225,100);
ctx.fillStyle='#f472b6';ctx.beginPath();ctx.roundRect(270,75,btnW,btnH,8);ctx.fill();
ctx.fillStyle='#fff';ctx.fillText('▼',295,100);
ctx.fillStyle='#ff6b9d';ctx.beginPath();ctx.roundRect(380,75,120,btnH,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Bırak! 🚗',440,100)}
drawCar(carX,carY,'#ef4444','1');
if(dualMode&&car2Rolling){drawCar(car2X,car2Y,'#60a5fa','2')}
else if(dualMode&&!car2Rolling){
const r2=calcRamp(car2AngleIdx);
drawCar(r2.sx+10,r2.sy+150-15,'#60a5fa','2')}
if(carRolling){
const elapsed=((Date.now()-timerStart)/1000).toFixed(1);
ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('⏱️ '+elapsed+'s',W/2,65);
speedLines.forEach(s=>{ctx.strokeStyle='rgba(251,191,36,'+s.life+')';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.lineTo(s.x-20,s.y);ctx.stroke()})}
if(carFinished){
ctx.fillStyle='#22c55e';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏁 '+timer.toFixed(1)+'s',finishX,140)}}
dustParticles.forEach(d=>{ctx.globalAlpha=d.life*0.5;ctx.fillStyle='#a0845e';
ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
dustParticles.forEach(d=>{d.x+=d.vx;d.y+=d.vy;d.life-=0.03});
dustParticles=dustParticles.filter(d=>d.life>0);
speedLines.forEach(s=>{s.x-=2;s.life-=0.03});
speedLines=speedLines.filter(s=>s.life>0);
if(state==='play'&&carRolling&&!carFinished){
const r=calcRamp(angleIdx);
const ang=r.ang;
const gravity=0.15*weight;
const accel=gravity*Math.sin(ang)-friction*0.02;
const speed=Math.sqrt(carVx*carVx+carVy*carVy);
carVx+=Math.cos(ang)*accel;
carVy+=Math.sin(ang)*accel;
if(carY>=r.ey-15){carVy=0;carVx=Math.abs(carVx)-friction*0.01;if(carVx<0.5)carVx=0.5}
carX+=carVx;carY+=carVy;
if(carY>r.ey-15)carY=r.ey-15;
if(Math.random()<0.3)addDust(carX-15,carY+8);
if(speed>2&&Math.random()<0.4)speedLines.push({x:carX-20,y:carY+Math.random()*10-5,life:1});
if(carX>=finishX){carFinished=true;timer=(Date.now()-timerStart)/1000;
trialResults.push({angle:angleIdx,time:timer});
addParticles(finishX,carY,'#fbbf24',20);playSound(true);
if(!dualMode){
correctAnswer=2;
setTimeout(()=>{questionPhase=true},800)}}}
if(state==='play'&&dualMode&&car2Rolling&&!car2Finished){
const r2=calcRamp(car2AngleIdx);
const ang2=r2.ang;
const gravity2=0.15*weight;
const accel2=gravity2*Math.sin(ang2)-friction*0.02;
car2Vx+=Math.cos(ang2)*accel2;
car2Vy+=Math.sin(ang2)*accel2;
if(car2Y>=r2.ey+150-15){car2Vy=0;car2Vx=Math.abs(car2Vx)-friction*0.01;if(car2Vx<0.5)car2Vx=0.5}
car2X+=car2Vx;car2Y+=car2Vy;
if(car2Y>r2.ey+150-15)car2Y=r2.ey+150-15;
if(car2X>=finishX){car2Finished=true;car2Timer=(Date.now()-timerStart)/1000;
addParticles(finishX,car2Y,'#60a5fa',15)}}
if(state==='play'&&dualMode&&carFinished&&car2Finished&&!questionPhase){
correctAnswer=angles[angleIdx]>angles[car2AngleIdx]?0:1;
setTimeout(()=>{questionPhase=true},600)}
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{
const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';resetRound()}return}
if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>340&&my<390){round=1;score=0;state='play';resetRound()}return}
if(state==='play'){
if(questionPhase){
const opts=dualMode?2:3;
const bw=180,bh=45;
for(let i=0;i<opts;i++){
const bx=W/2-bw/2;const by=120+i*60;
if(mx>bx&&mx<bx+bw&&my>by&&my<by+bh&&selectedAnswer<0){
selectedAnswer=i;
if(i===correctAnswer){score+=10;playSound(true);addParticles(W/2,by+22,COLORS[3],15)}
else{playSound(false)}}}
if(selectedAnswer>=0){
const contY=120+opts*60+20;
if(mx>W/2-70&&mx<W/2+70&&my>contY&&my<contY+40){
round++;selectedAnswer=-1;questionPhase=false;
if(round>maxRound){state='win'}else{resetRound()}}}
return}
if(!carRolling&&phase==='adjust'){
if(mx>200&&mx<250&&my>75&&my<115){angleIdx=Math.min(2,angleIdx+1);resetCar()}
if(mx>270&&mx<320&&my>75&&my<115){angleIdx=Math.max(0,angleIdx-1);resetCar()}
if(mx>380&&mx<500&&my>75&&my<115){phase='rolling';startRoll()}}}});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_prek_sci_sesli_enstrumanlar_html():
    """Sesli Enstrümanlar — Çalan sesi doğru enstrümanla eşleştir."""
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
const instruments=[
{name:'Davul',emoji:'🥁',freq:120,type:'triangle',color:'#ef4444',desc:'Kalın ses'},
{name:'Gitar',emoji:'🎸',freq:330,type:'sine',color:'#f59e0b',desc:'Orta ses'},
{name:'Flüt',emoji:'🎵',freq:600,type:'sine',color:'#22c55e',desc:'İnce ses'},
{name:'Zil',emoji:'🔔',freq:900,type:'sine',color:'#3b82f6',desc:'Çok ince ses'}
];
let currentInstrument=0,answered=false,correctIdx=-1,selectedIdx=-1;
let cardScales=[1,1,1,1],cardShakes=[0,0,0,0],waveAnim=0,waveActive=false;
let showResult=false,resultTimer=0;
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function playInstrumentSound(idx){
try{const a=new AudioContext();
const inst=instruments[idx];
const o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);
o.frequency.value=inst.freq;
o.type=inst.type;
g.gain.value=0.35;o.start();
waveActive=true;waveAnim=0;
if(idx===0){
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.5);
o.stop(a.currentTime+0.5);
const o2=a.createOscillator(),g2=a.createGain();
o2.connect(g2);g2.connect(a.destination);o2.frequency.value=80;o2.type='triangle';
g2.gain.value=0.2;o2.start(a.currentTime+0.05);
g2.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o2.stop(a.currentTime+0.4);
setTimeout(()=>waveActive=false,500)
} else if(idx===1){
o.frequency.exponentialRampToValueAtTime(inst.freq*0.95,a.currentTime+0.3);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.8);
o.stop(a.currentTime+0.8);
setTimeout(()=>waveActive=false,800)
} else if(idx===2){
o.frequency.setValueAtTime(inst.freq,a.currentTime);
o.frequency.linearRampToValueAtTime(inst.freq*1.05,a.currentTime+0.2);
o.frequency.linearRampToValueAtTime(inst.freq,a.currentTime+0.4);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.7);
o.stop(a.currentTime+0.7);
setTimeout(()=>waveActive=false,700)
} else {
o.frequency.setValueAtTime(inst.freq,a.currentTime);
g.gain.setValueAtTime(0.3,a.currentTime);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+1.2);
o.stop(a.currentTime+1.2);
setTimeout(()=>waveActive=false,1200)
}
}catch(e){}}
function addParticles(x,y,clr,n){for(let i=0;i<(n||12);i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr:clr||COLORS[Math.floor(Math.random()*10)],r:2+Math.random()*4})}
function setupRound(){
currentInstrument=Math.floor(Math.random()*4);
answered=false;selectedIdx=-1;correctIdx=currentInstrument;
cardScales=[1,1,1,1];cardShakes=[0,0,0,0];
showResult=false;resultTimer=0;
setTimeout(()=>playInstrumentSound(currentInstrument),500)}
function getCardRect(i){
const cols=2,cw=200,ch=180,gap=30;
const row=Math.floor(i/cols),col=i%cols;
const totalW=cols*cw+(cols-1)*gap;
const startX=(W-totalW)/2;
const startY=240;
return{x:startX+col*(cw+gap),y:startY+row*(ch+gap),w:cw,h:ch}}
function drawWaveVis(){
if(!waveActive)return;
waveAnim+=0.15;
const cx=W/2,cy=160;
const inst=instruments[currentInstrument];
ctx.save();
for(let i=0;i<5;i++){
const r=20+i*15+Math.sin(waveAnim+i)*8;
ctx.strokeStyle=inst.color;ctx.globalAlpha=0.6-i*0.1;ctx.lineWidth=3;
ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.stroke()}
ctx.globalAlpha=1;
const amp=20+Math.sin(waveAnim*2)*10;
ctx.strokeStyle=inst.color;ctx.lineWidth=2;ctx.beginPath();
for(let x=cx-80;x<cx+80;x++){
const t=(x-cx+80)/160;
const y=cy+Math.sin(t*Math.PI*4+waveAnim*3)*amp*(1-Math.abs(t-0.5)*2);
if(x===cx-80)ctx.moveTo(x,y);else ctx.lineTo(x,y)}
ctx.stroke();ctx.restore()}
function draw(){
ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎵 Sesli Enstrümanlar 🎶',W/2,160);
ctx.font='20px Segoe UI';ctx.fillText('Çalan sesi hangi enstrüman çıkarıyor?',W/2,210);
ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';
ctx.fillText('🥁 Davul = Kalın  |  🎸 Gitar = Orta',W/2,260);
ctx.fillText('🎵 Flüt = İnce  |  🔔 Zil = Çok İnce',W/2,290);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,330,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,360);return}
if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Harika Müzisyen! 🎉',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxRound*10,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,310,180,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,30);
ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
ctx.textAlign='center';
drawWaveVis();
ctx.fillStyle='#60a5fa';ctx.beginPath();ctx.roundRect(W/2-100,100,200,40,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';
ctx.fillText('🔊 Sesi Tekrar Dinle',W/2,125);
for(let i=0;i<4;i++){
const r=getCardRect(i);
const inst=instruments[i];
const shk=cardShakes[i];
const sc=cardScales[i];
ctx.save();
ctx.translate(r.x+r.w/2+shk,r.y+r.h/2);
ctx.scale(sc,sc);
const isCorrectShow=answered&&i===correctIdx;
const isWrong=answered&&i===selectedIdx&&i!==correctIdx;
let bgClr=inst.color+'40';
if(isCorrectShow)bgClr='#22c55e80';
if(isWrong)bgClr='#ef444480';
ctx.fillStyle=bgClr;ctx.beginPath();ctx.roundRect(-r.w/2,-r.h/2,r.w,r.h,16);ctx.fill();
ctx.strokeStyle=isCorrectShow?'#22c55e':isWrong?'#ef4444':inst.color;
ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(-r.w/2,-r.h/2,r.w,r.h,16);ctx.stroke();
ctx.font='52px Segoe UI';ctx.fillStyle='#fff';ctx.fillText(inst.emoji,0,-20);
ctx.font='bold 18px Segoe UI';ctx.fillStyle='#fff';ctx.fillText(inst.name,0,35);
ctx.font='13px Segoe UI';ctx.fillStyle='#c084fc';ctx.fillText(inst.desc,0,56);
ctx.restore()}
if(showResult){
resultTimer++;
if(resultTimer>60){round++;
if(round>maxRound){state='win'}else{setupRound()}}}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
for(let i=0;i<4;i++){
if(cardShakes[i]!==0)cardShakes[i]*=-0.8;
if(Math.abs(cardShakes[i])<0.5)cardShakes[i]=0;
if(cardScales[i]>1)cardScales[i]-=0.02;
if(cardScales[i]<1)cardScales[i]+=0.02}
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{
const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<380){state='play';setupRound()}return}
if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>310&&my<360){round=1;score=0;state='play';setupRound()}return}
if(state==='play'){
if(mx>W/2-100&&mx<W/2+100&&my>100&&my<140){playInstrumentSound(currentInstrument);return}
if(!answered){
for(let i=0;i<4;i++){
const r=getCardRect(i);
if(mx>r.x&&mx<r.x+r.w&&my>r.y&&my<r.y+r.h){
selectedIdx=i;answered=true;
if(i===correctIdx){score+=10;playSound(true);cardScales[i]=1.2;
addParticles(r.x+r.w/2,r.y+r.h/2,instruments[i].color,20)}
else{playSound(false);cardShakes[i]=12;cardScales[correctIdx]=1.15}
showResult=true;resultTimer=0;break}}}}});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_prek_sci_hayvan_yuvasi_html():
    """Hayvan Yuvası — Hayvanları doğru yaşam alanlarına sürükle."""
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
const habitats=[
{name:'Orman',emoji:'🌲',color:'#22c55e',bgColor:'#14532d'},
{name:'Deniz',emoji:'🌊',color:'#3b82f6',bgColor:'#1e3a5f'},
{name:'Kutup',emoji:'❄️',color:'#93c5fd',bgColor:'#94A3B8'}
];
const animalPool=[
{emoji:'🐻',name:'Ayı',habitat:0},
{emoji:'🐟',name:'Balık',habitat:1},
{emoji:'🐧',name:'Penguen',habitat:2},
{emoji:'🦊',name:'Tilki',habitat:0},
{emoji:'🐬',name:'Yunus',habitat:1},
{emoji:'🐻‍❄️',name:'Kutup Ayısı',habitat:2},
{emoji:'🦌',name:'Geyik',habitat:0},
{emoji:'🐙',name:'Ahtapot',habitat:1},
{emoji:'🦭',name:'Fok',habitat:2},
{emoji:'🐿️',name:'Sincap',habitat:0},
{emoji:'🦈',name:'Köpekbalığı',habitat:1},
{emoji:'🦉',name:'Baykuş',habitat:0},
{emoji:'🦀',name:'Yengeç',habitat:1},
{emoji:'🫎',name:'Ren Geyiği',habitat:2},
{emoji:'🐇',name:'Tavşan',habitat:0}
];
let currentAnimal=null,animalX=0,animalY=0,dragging=false,dragOffX=0,dragOffY=0;
let startAnimalX=W/2,startAnimalY=120;
let animating=false,animTarget=null,animProgress=0;
let showResult=false,resultTimer=0,resultCorrect=false;
let usedAnimals=[],glowHabitat=-1,glowTimer=0;
let bounceBack=false,bounceProgress=0;
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addParticles(x,y,clr,n){for(let i=0;i<(n||12);i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr:clr||COLORS[Math.floor(Math.random()*10)],r:2+Math.random()*4})}
function pickAnimal(){
if(usedAnimals.length>=animalPool.length)usedAnimals=[];
let idx;
do{idx=Math.floor(Math.random()*animalPool.length)}while(usedAnimals.includes(idx));
usedAnimals.push(idx);
currentAnimal=animalPool[idx];
animalX=startAnimalX;animalY=startAnimalY;
dragging=false;animating=false;showResult=false;
bounceBack=false;glowHabitat=-1}
function getHabitatRect(i){
const hw=190,hh=160,gap=20;
const totalW=3*hw+2*gap;
const sx=(W-totalW)/2;
return{x:sx+i*(hw+gap),y:H-200,w:hw,h:hh}}
function draw(){
ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🦊 Hayvan Yuvası 🐧',W/2,170);
ctx.font='20px Segoe UI';ctx.fillText('Hayvanları doğru yaşam alanına sürükle!',W/2,220);
ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';
ctx.fillText('🌲 Orman   🌊 Deniz   ❄️ Kutup',W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,300,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Harika Doğa Bilgini! 🎉',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxRound*10,W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,310,180,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,30);
ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
ctx.textAlign='center';
ctx.fillStyle='#c084fc';ctx.font='bold 18px Segoe UI';
ctx.fillText('Hayvanı doğru yuvaya sürükle!',W/2,60);
for(let i=0;i<3;i++){
const r=getHabitatRect(i);
const h=habitats[i];
const isGlow=glowHabitat===i;
ctx.save();
if(isGlow){ctx.shadowColor=h.color;ctx.shadowBlur=20}
ctx.fillStyle=h.bgColor;ctx.beginPath();ctx.roundRect(r.x,r.y,r.w,r.h,16);ctx.fill();
ctx.strokeStyle=isGlow?'#fbbf24':h.color;ctx.lineWidth=isGlow?4:3;
ctx.beginPath();ctx.roundRect(r.x,r.y,r.w,r.h,16);ctx.stroke();
ctx.restore();
ctx.font='40px Segoe UI';ctx.fillText(h.emoji,r.x+r.w/2,r.y+55);
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText(h.name,r.x+r.w/2,r.y+90);
if(isGlow){
ctx.fillStyle=h.color;ctx.globalAlpha=0.3;
ctx.beginPath();ctx.roundRect(r.x,r.y,r.w,r.h,16);ctx.fill();
ctx.globalAlpha=1}}
if(currentAnimal&&!animating){
ctx.font='56px Segoe UI';ctx.fillText(currentAnimal.emoji,animalX,animalY+20);
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText(currentAnimal.name,animalX,animalY+55)}
if(animating&&currentAnimal){
ctx.font='56px Segoe UI';ctx.fillText(currentAnimal.emoji,animalX,animalY+20)}
if(showResult){
ctx.fillStyle=resultCorrect?'#22c55e':'#ef4444';ctx.font='bold 24px Segoe UI';
ctx.fillText(resultCorrect?'✅ Doğru!':'❌ Yanlış!',W/2,200)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
if(glowTimer>0){glowTimer--;if(glowTimer<=0)glowHabitat=-1}
if(animating&&animTarget){
animProgress+=0.04;
const t=Math.min(animProgress,1);
const ease=t<0.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
animalX=animTarget.sx+(animTarget.tx-animTarget.sx)*ease;
animalY=animTarget.sy+(animTarget.ty-animTarget.sy)*ease;
if(animProgress>=1){animating=false;
if(resultCorrect){
addParticles(animalX,animalY,habitats[currentAnimal.habitat].color,20)}
showResult=true;resultTimer=0}}
if(bounceBack){
bounceProgress+=0.05;
const t=Math.min(bounceProgress,1);
animalX=animTarget.sx+(startAnimalX-animTarget.sx)*t;
animalY=animTarget.sy+(startAnimalY-animTarget.sy)*t;
if(bounceProgress>=1){bounceBack=false;animalX=startAnimalX;animalY=startAnimalY}}
if(showResult){resultTimer++;
if(resultTimer>50){round++;
if(round>maxRound){state='win'}else{pickAnimal()}}}
draw();requestAnimationFrame(update)}
function checkDrop(){
for(let i=0;i<3;i++){
const r=getHabitatRect(i);
if(animalX>r.x&&animalX<r.x+r.w&&animalY>r.y-30&&animalY<r.y+r.h){
const correct=currentAnimal.habitat===i;
resultCorrect=correct;
if(correct){score+=10;playSound(true);
animTarget={sx:animalX,sy:animalY,tx:r.x+r.w/2,ty:r.y+r.h/2};
animating=true;animProgress=0}
else{playSound(false);
glowHabitat=currentAnimal.habitat;glowTimer=60;
animTarget={sx:animalX,sy:animalY};
bounceBack=true;bounceProgress=0;
showResult=true;resultTimer=0}
return}}
animalX=startAnimalX;animalY=startAnimalY}
canvas.addEventListener('mousedown',e=>{
if(state!=='play'||animating||showResult||bounceBack)return;
const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(currentAnimal&&Math.abs(mx-animalX)<40&&Math.abs(my-animalY-10)<40){
dragging=true;dragOffX=animalX-mx;dragOffY=animalY-my}});
canvas.addEventListener('mousemove',e=>{
if(!dragging)return;
const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
animalX=mx+dragOffX;animalY=my+dragOffY});
canvas.addEventListener('mouseup',e=>{
if(dragging){dragging=false;checkDrop()}});
canvas.addEventListener('click',e=>{
const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';usedAnimals=[];pickAnimal()}return}
if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>310&&my<360){round=1;score=0;usedAnimals=[];state='play';pickAnimal()}return}});
canvas.addEventListener('touchstart',e=>{
e.preventDefault();const t=e.touches[0];
const rect=canvas.getBoundingClientRect();
const mx=(t.clientX-rect.left)*(W/rect.width),my=(t.clientY-rect.top)*(H/rect.height);
if(state!=='play'){
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));return}
if(currentAnimal&&Math.abs(mx-animalX)<40&&Math.abs(my-animalY-10)<40){
dragging=true;dragOffX=animalX-mx;dragOffY=animalY-my}});
canvas.addEventListener('touchmove',e=>{
e.preventDefault();if(!dragging)return;const t=e.touches[0];
const rect=canvas.getBoundingClientRect();
const mx=(t.clientX-rect.left)*(W/rect.width),my=(t.clientY-rect.top)*(H/rect.height);
animalX=mx+dragOffX;animalY=my+dragOffY});
canvas.addEventListener('touchend',e=>{
e.preventDefault();if(dragging){dragging=false;checkDrop()}});
update();
</script></body></html>"""


def _build_prek_sci_geri_donusum_html():
    """Geri Dönüşüm Sorter — Atık maddelerini doğru geri dönüşüm kutusuna at."""
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
const bins=[
{name:'Kâğıt',emoji:'📄',color:'#3b82f6',bgColor:'#1e3a5f'},
{name:'Plastik',emoji:'🥤',color:'#eab308',bgColor:'#713f12'},
{name:'Cam',emoji:'🫙',color:'#22c55e',bgColor:'#14532d'}
];
const itemPool=[
{emoji:'📰',name:'Gazete',bin:0},
{emoji:'🧴',name:'Şişe',bin:1},
{emoji:'🍶',name:'Kavanoz',bin:2},
{emoji:'📦',name:'Karton',bin:0},
{emoji:'🛍️',name:'Poşet',bin:1},
{emoji:'🪟',name:'Cam',bin:2},
{emoji:'📚',name:'Kitap',bin:0},
{emoji:'🥤',name:'Bardak',bin:1},
{emoji:'🫗',name:'Şişe',bin:2},
{emoji:'✉️',name:'Zarf',bin:0},
{emoji:'🧃',name:'Kutu',bin:1},
{emoji:'💡',name:'Ampul',bin:2},
{emoji:'🗞️',name:'Dergi',bin:0},
{emoji:'🧹',name:'Plastik',bin:1},
{emoji:'🥃',name:'Bardak',bin:2}
];
let items=[],fallingSpeed=1,beltOffset=0;
let flyingItems=[],missedItems=[];
let roundItems=0,roundMax=1;
let spawnTimer=0,spawnDelay=120;
let showRoundText='',showRoundTimer=0;
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addParticles(x,y,clr,n){for(let i=0;i<(n||12);i++)
particles.push({x,y,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1,clr:clr||COLORS[Math.floor(Math.random()*10)],r:2+Math.random()*4})}
function getBinRect(i){
const bw=180,bh=130,gap=25;
const totalW=3*bw+2*gap;
const sx=(W-totalW)/2;
return{x:sx+i*(bw+gap),y:H-160,w:bw,h:bh}}
function spawnItem(){
const idx=Math.floor(Math.random()*itemPool.length);
const item=itemPool[idx];
const x=100+Math.random()*(W-200);
items.push({emoji:item.emoji,name:item.name,bin:item.bin,x:x,y:-30,
speed:fallingSpeed+Math.random()*0.3,wobble:Math.random()*Math.PI*2,alive:true})}
function setupRound(){
items=[];flyingItems=[];missedItems=[];
roundItems=0;
roundMax=round<=3?1:round<=6?2:3;
fallingSpeed=0.4+round*0.15;
spawnDelay=Math.max(40,120-round*8);
spawnTimer=0;
showRoundText='Tur '+round;showRoundTimer=60;
spawnItem()}
function drawConveyorBelt(){
beltOffset=(beltOffset+1)%20;
ctx.fillStyle='#4a4a4a';ctx.fillRect(0,60,W,30);
ctx.fillStyle='#666';
for(let x=-beltOffset;x<W;x+=20){
ctx.fillRect(x,62,10,26)}
ctx.fillStyle='#333';ctx.fillRect(0,58,W,4);ctx.fillRect(0,90,W,4)}
function drawBin(i,shake){
const r=getBinRect(i);const b=bins[i];
ctx.save();
if(shake)ctx.translate(Math.sin(Date.now()*0.05)*4,0);
ctx.fillStyle=b.bgColor;ctx.beginPath();ctx.roundRect(r.x,r.y,r.w,r.h,12);ctx.fill();
ctx.strokeStyle=b.color;ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(r.x,r.y,r.w,r.h,12);ctx.stroke();
ctx.fillStyle=b.color;ctx.beginPath();ctx.roundRect(r.x,r.y,r.w,25,{upperLeft:12,upperRight:12,lowerLeft:0,lowerRight:0});
ctx.roundRect(r.x,r.y,r.w,25,[12,12,0,0]);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText(b.name,r.x+r.w/2,r.y+17);
ctx.font='36px Segoe UI';ctx.fillText(b.emoji,r.x+r.w/2,r.y+75);
ctx.font='13px Segoe UI';ctx.fillStyle='#ccc';
const labels=['♻️ Mavi Kutu','♻️ Sarı Kutu','♻️ Yeşil Kutu'];
ctx.fillText(labels[i],r.x+r.w/2,r.y+110);
ctx.restore()}
let shakeBins=[0,0,0];
function draw(){
ctx.clearRect(0,0,W,H);
const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');
ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('♻️ Geri Dönüşüm ♻️',W/2,170);
ctx.font='20px Segoe UI';ctx.fillText('Atıkları doğru kutuya at!',W/2,220);
ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';
ctx.fillText('📄 Kâğıt → Mavi  |  🥤 Plastik → Sarı  |  🫙 Cam → Yeşil',W/2,260);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌍 Süper Geri Dönüşümcü! 🌍',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxRound*10,W/2,260);
ctx.font='16px Segoe UI';ctx.fillStyle='#34d399';
ctx.fillText('Dünyamızı korudun!',W/2,295);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,320,180,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,30);
ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
ctx.textAlign='center';
drawConveyorBelt();
for(let i=0;i<3;i++){drawBin(i,shakeBins[i]>0)}
items.forEach(item=>{
if(!item.alive)return;
item.wobble+=0.03;
const wx=Math.sin(item.wobble)*15;
ctx.font='40px Segoe UI';ctx.textAlign='center';
ctx.fillText(item.emoji,item.x+wx,item.y);
ctx.fillStyle='#fff';ctx.font='bold 13px Segoe UI';
ctx.fillText(item.name,item.x+wx,item.y+25)});
flyingItems.forEach(fi=>{
ctx.globalAlpha=fi.life;
ctx.font='34px Segoe UI';ctx.textAlign='center';
ctx.fillText(fi.emoji,fi.x,fi.y);ctx.globalAlpha=1});
missedItems.forEach(mi=>{
ctx.globalAlpha=mi.life;
ctx.font='30px Segoe UI';ctx.textAlign='center';
ctx.fillText(mi.emoji,mi.x,mi.y);
ctx.fillStyle='#ef4444';ctx.font='bold 14px Segoe UI';
ctx.fillText('✗',mi.x+20,mi.y-10);ctx.globalAlpha=1});
if(showRoundTimer>0){
ctx.fillStyle='#fbbf24';ctx.globalAlpha=showRoundTimer/60;
ctx.font='bold 28px Segoe UI';ctx.textAlign='center';
ctx.fillText(showRoundText,W/2,H/2-40);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});
particles=particles.filter(p=>p.life>0);
flyingItems.forEach(fi=>{
fi.x+=(fi.tx-fi.x)*0.1;fi.y+=(fi.ty-fi.y)*0.1;fi.life-=0.02});
flyingItems=flyingItems.filter(fi=>fi.life>0);
missedItems.forEach(mi=>{mi.y+=1;mi.life-=0.015});
missedItems=missedItems.filter(mi=>mi.life>0);
for(let i=0;i<3;i++){if(shakeBins[i]>0)shakeBins[i]--}
if(showRoundTimer>0)showRoundTimer--;
if(state==='play'){
items.forEach(item=>{
if(!item.alive)return;
item.y+=item.speed;
if(item.y>H-170){
item.alive=false;
missedItems.push({emoji:item.emoji,x:item.x,y:item.y,life:1})}});
items=items.filter(i=>i.alive);
spawnTimer++;
if(items.length===0&&roundItems<roundMax&&spawnTimer>spawnDelay){
spawnItem();spawnTimer=0}
if(items.length===0&&roundItems>=roundMax){
round++;
if(round>maxRound){state='win'}
else{setupRound()}}}
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{
const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';setupRound()}return}
if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>320&&my<370){round=1;score=0;state='play';setupRound()}return}
if(state==='play'){
for(let i=0;i<3;i++){
const r=getBinRect(i);
if(mx>r.x&&mx<r.x+r.w&&my>r.y&&my<r.y+r.h){
const activeItem=items.find(it=>it.alive);
if(activeItem){
activeItem.alive=false;
roundItems++;
if(activeItem.bin===i){
score+=10;playSound(true);
flyingItems.push({emoji:activeItem.emoji,x:activeItem.x,y:activeItem.y,
tx:r.x+r.w/2,ty:r.y+r.h/2,life:1});
addParticles(r.x+r.w/2,r.y+r.h/2,bins[i].color,15)}
else{
playSound(false);shakeBins[i]=30;
const correctR=getBinRect(activeItem.bin);
shakeBins[activeItem.bin]=-30;
missedItems.push({emoji:activeItem.emoji,x:activeItem.x,y:activeItem.y,life:1})}}
break}}}});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_prek_sci_gezegen_balonlari_html():
    """Gezegen Balonları — Gezegenleri küçükten büyüğe veya Güneş'e yakından uzağa sırala."""
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
const allPlanets=[
{name:'Merkür',color:'#a0a0a0',size:12,order:0,ring:false,emoji:'☿️'},
{name:'Venüs',color:'#e8a838',size:16,order:1,ring:false,emoji:'♀️'},
{name:'Dünya',color:'#4488ee',size:17,order:2,ring:false,emoji:'🌍'},
{name:'Mars',color:'#cc4422',size:14,order:3,ring:false,emoji:'♂️'},
{name:'Jüpiter',color:'#dd9944',size:30,order:4,ring:false,emoji:'♃'},
{name:'Satürn',color:'#ddc866',size:26,order:5,ring:true,emoji:'♄'},
{name:'Uranüs',color:'#66cccc',size:22,order:6,ring:true,emoji:'⛢'},
{name:'Neptün',color:'#4466dd',size:20,order:7,ring:false,emoji:'♆'}
];
const sizeOrder=[0,3,1,2,7,6,5,4];
let activePlanets=[],sortMode='size',clickOrder=[],nextExpected=0;
let planetPositions=[],placedPlanets=[];
let wigglePlanet=-1,wiggleTimer=0;
let starField=[];
let showComplete=false,completeTimer=0;
for(let i=0;i<120;i++)starField.push({x:Math.random()*W,y:Math.random()*H,
r:0.5+Math.random()*2,twinkle:Math.random()*Math.PI*2,speed:0.02+Math.random()*0.03});
function playSound(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';
g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);
g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function playChime(note){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();
o.connect(g);g.connect(a.destination);o.frequency.value=note;o.type='sine';
g.gain.value=0.2;o.start();g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.6);
o.stop(a.currentTime+0.6)}catch(e){}}
function addParticles(x,y,clr,n){for(let i=0;i<(n||12);i++)
particles.push({x,y,vx:(Math.random()-0.5)*5,vy:(Math.random()-0.5)*5,life:1,clr:clr||COLORS[Math.floor(Math.random()*10)],r:2+Math.random()*3})}
function setupRound(){
let count=round<=3?3+Math.floor(round/2):round<=7?5+Math.floor((round-4)/2):8;
count=Math.min(count,8);
sortMode=round%2===1?'size':'distance';
let indices=[...Array(8).keys()];
for(let i=indices.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[indices[i],indices[j]]=[indices[j],indices[i]]}
activePlanets=indices.slice(0,count).map(i=>({...allPlanets[i],idx:i}));
let correctOrder;
if(sortMode==='size'){
const sorted=[...activePlanets].sort((a,b)=>a.size-b.size);
correctOrder=sorted.map(p=>p.idx)}
else{
const sorted=[...activePlanets].sort((a,b)=>a.order-b.order);
correctOrder=sorted.map(p=>p.idx)}
activePlanets.forEach(p=>{p.correctOrder=correctOrder;p.placed=false});
clickOrder=correctOrder;nextExpected=0;placedPlanets=[];
showComplete=false;completeTimer=0;
const margin=60;
const usableW=W-2*margin;
const usableH=300;
const startY=160;
activePlanets.forEach((p,i)=>{
let placed=false,attempts=0;
while(!placed&&attempts<100){
const px=margin+40+Math.random()*(usableW-80);
const py=startY+40+Math.random()*(usableH-80);
let overlap=false;
for(let j=0;j<i;j++){
const op=activePlanets[j];
if(Math.hypot(px-op.px,py-op.py)<(p.size+op.size+40)){overlap=true;break}}
if(!overlap){p.px=px;p.py=py;placed=true}
attempts++}
if(!placed){p.px=margin+40+(i/(activePlanets.length-1||1))*(usableW-80);
p.py=startY+60+Math.random()*200}
p.floatOffset=Math.random()*Math.PI*2;p.floatSpeed=0.01+Math.random()*0.015})}
function drawStar(x,y,r,alpha){
ctx.globalAlpha=alpha;ctx.fillStyle='#fff';
ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}
function drawPlanet(p,x,y,scale,alpha){
ctx.save();ctx.globalAlpha=alpha||1;ctx.translate(x,y);
const r=p.size*(scale||1);
const grad=ctx.createRadialGradient(-r*0.3,-r*0.3,r*0.1,0,0,r);
grad.addColorStop(0,p.color);grad.addColorStop(0.7,p.color);
grad.addColorStop(1,'#00000080');
ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='#ffffff30';ctx.lineWidth=1;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.stroke();
if(p.ring){
ctx.strokeStyle=p.color+'90';ctx.lineWidth=3;
ctx.beginPath();ctx.ellipse(0,0,r*1.7,r*0.4,0,0,Math.PI*2);ctx.stroke();
ctx.strokeStyle='#ffffff30';ctx.lineWidth=1;
ctx.beginPath();ctx.ellipse(0,0,r*1.5,r*0.35,0,0,Math.PI*2);ctx.stroke()}
ctx.fillStyle='#fff';ctx.font='bold '+Math.max(11,r*0.8)+'px Segoe UI';
ctx.textAlign='center';ctx.fillText(p.name,0,r+16);
ctx.restore()}
function drawPlacementSlots(){
const n=activePlanets.length;
const slotW=70,gap=8;
const totalW=n*(slotW+gap)-gap;
const sx=(W-totalW)/2;
const sy=H-110;
for(let i=0;i<n;i++){
const x=sx+i*(slotW+gap);
ctx.strokeStyle='#ffffff40';ctx.lineWidth=2;ctx.setLineDash([5,5]);
ctx.beginPath();ctx.roundRect(x,sy,slotW,60,8);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#ffffff30';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText(i+1,x+slotW/2,sy+55);
if(i<placedPlanets.length){
const pp=placedPlanets[i];
drawPlanet(pp,x+slotW/2,sy+25,0.6,1)}}
ctx.fillStyle='#c084fc';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
const label=sortMode==='size'?'Küçükten → Büyüğe':'Güneşe Yakından → Uzağa';
ctx.fillText(label,(sx+totalW/2),sy-12)}
function draw(){
ctx.clearRect(0,0,W,H);
ctx.fillStyle='#0a0015';ctx.fillRect(0,0,W,H);
starField.forEach(s=>{
s.twinkle+=s.speed;
const alpha=0.3+Math.sin(s.twinkle)*0.4;
drawStar(s.x,s.y,s.r,Math.max(0.1,alpha))});
if(state==='start'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🪐 Gezegen Balonları 🚀',W/2,170);
ctx.font='20px Segoe UI';ctx.fillText('Gezegenleri sırayla tıkla!',W/2,220);
ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';
ctx.fillText('Küçükten büyüğe veya yakından uzağa',W/2,255);
for(let i=0;i<8;i++){
const p=allPlanets[i];
const angle=i*Math.PI*2/8;
const cx=W/2+Math.cos(angle)*120;
const cy=380+Math.sin(angle)*50;
drawPlanet(p,cx,cy,0.8,0.8)}
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,470,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
ctx.fillText('Başla!',W/2,500);return}
if(state==='win'){
ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🌟 Uzay Kaşifi! 🌟',W/2,200);
ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+' / '+maxRound*10,W/2,260);
ctx.font='16px Segoe UI';ctx.fillStyle='#60a5fa';
ctx.fillText('Güneş Sistemini öğrendin!',W/2,295);
ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,320,180,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,350);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
ctx.fillText('Tur: '+round+'/'+maxRound,20,30);
ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
ctx.textAlign='center';
const taskText=sortMode==='size'?'🔍 Küçükten büyüğe sırala!':'☀️ Güneşe yakından uzağa sırala!';
ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';
ctx.fillText(taskText,W/2,60);
activePlanets.forEach((p,i)=>{
if(p.placed)return;
const floatY=Math.sin(p.floatOffset)*8;
const isWiggle=wigglePlanet===p.idx;
let ox=0;
if(isWiggle){ox=Math.sin(wiggleTimer*0.5)*8}
drawPlanet(p,p.px+ox,p.py+floatY,1,1)});
drawPlacementSlots();
if(showComplete){
ctx.fillStyle='#fbbf24';ctx.globalAlpha=Math.min(1,completeTimer/30);
ctx.font='bold 28px Segoe UI';ctx.textAlign='center';
ctx.fillText('⭐ Güneş Sistemi! ⭐',W/2,H-160);
ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;
ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.05});
particles=particles.filter(p=>p.life>0);
activePlanets.forEach(p=>{p.floatOffset+=p.floatSpeed});
if(wigglePlanet>=0){wiggleTimer++;if(wiggleTimer>30){wigglePlanet=-1;wiggleTimer=0}}
if(showComplete){completeTimer++;
if(completeTimer>90){round++;
if(round>maxRound){state='win'}else{setupRound()}}}
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{
const rect=canvas.getBoundingClientRect();
const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>470&&my<520){state='play';setupRound()}return}
if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>320&&my<370){round=1;score=0;state='play';setupRound()}return}
if(state==='play'&&!showComplete){
for(let i=0;i<activePlanets.length;i++){
const p=activePlanets[i];
if(p.placed)continue;
const floatY=Math.sin(p.floatOffset)*8;
const dist=Math.hypot(mx-p.px,my-(p.py+floatY));
if(dist<p.size+20){
if(p.idx===clickOrder[nextExpected]){
p.placed=true;placedPlanets.push(p);
score+=10;
const notes=[262,294,330,349,392,440,494,523];
playChime(notes[nextExpected%8]);
addParticles(p.px,p.py,p.color,15);
nextExpected++;
if(nextExpected>=clickOrder.length){
showComplete=true;completeTimer=0;
addParticles(W/2,H/2,'#fbbf24',30)}}
else{
playSound(false);wigglePlanet=p.idx;wiggleTimer=0}
break}}}});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""
