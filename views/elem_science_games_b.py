# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm B: 6-10)."""


def _build_elem_sci_egik_duzlem_html():
    """Eğik Düzlem Parkuru — Rampa uzunluğunu ayarlayarak kutuyu platforma çıkar."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=0,maxR=10,particles=[];
let rampSetting=2,boxWeight=10,platformH=150,boxX=0,boxY=0,boxMoving=false,boxSuccess=false,boxFail=false;
let animT=0,failMsg='',playerForce=50;
const rampLengths=[120,180,250,320,400];
const rampLabels=['Çok Kısa','Kısa','Orta','Uzun','Çok Uzun'];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function startLevel(){rampSetting=2;boxMoving=false;boxSuccess=false;boxFail=false;failMsg='';animT=0;
platformH=100+round*18;boxWeight=8+round*5;playerForce=40+round*3;
boxX=0;boxY=0}
function getRampLen(){return rampLengths[rampSetting]}
function getAngle(){const rL=getRampLen();return Math.atan2(platformH,rL)}
function getForceNeeded(){return boxWeight*Math.sin(getAngle())}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('📐 Eğik Düzlem Parkuru',W/2,160);ctx.font='20px Segoe UI';ctx.fillText('Rampa uzunluğunu ayarla,',W/2,210);ctx.fillText('kutuyu platforma çıkar!',W/2,240);ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';ctx.fillText('Uzun rampa = Az kuvvet, Kısa rampa = Çok kuvvet',W/2,280);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,320,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,350);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Tebrikler!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,250);ctx.fillText('Eğik düzlem ustası oldun!',W/2,290);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,330,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,360);return}
/* HUD */
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+(round+1)+'/'+maxR,15,30);
ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Ground */
const groundY=520;ctx.fillStyle='#1e3a1e';ctx.fillRect(0,groundY,W,H-groundY);
ctx.fillStyle='#2d5a2d';for(let x=0;x<W;x+=30){ctx.fillRect(x,groundY,15,4)}
/* Platform on right */
const platX=480,platW=140,platTop=groundY-platformH;
ctx.fillStyle='#6d4c41';ctx.fillRect(platX,platTop,platW,platformH);
ctx.fillStyle='#8d6e63';ctx.fillRect(platX,platTop,platW,10);
ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.fillText('Platform',platX+platW/2,platTop-8);
ctx.fillText('↕ '+platformH+' cm',platX+platW/2,platTop+platformH/2);
/* Ramp */
const rL=getRampLen();const rampBaseX=platX;const rampBaseY=groundY;const rampTopX=platX;const rampTopY=platTop+10;
const rampBottomX=platX-rL;const rampBottomY=groundY;
ctx.fillStyle='#78909c';ctx.beginPath();ctx.moveTo(rampTopX,rampTopY);ctx.lineTo(rampBottomX,rampBottomY);ctx.lineTo(rampTopX,rampBottomY);ctx.closePath();ctx.fill();
ctx.strokeStyle='#b0bec5';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(rampTopX,rampTopY);ctx.lineTo(rampBottomX,rampBottomY);ctx.stroke();
/* Ramp surface lines */
ctx.strokeStyle='#90a4ae';ctx.lineWidth=1;
for(let i=1;i<5;i++){const t=i/5;const lx=rampBottomX+(rampTopX-rampBottomX)*t;const ly=rampBottomY+(rampTopY-rampBottomY)*t;
ctx.beginPath();ctx.moveTo(lx-5,ly+5);ctx.lineTo(lx+5,ly-5);ctx.stroke()}
/* Angle arc */
ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;const ang=getAngle();
ctx.beginPath();ctx.arc(rampBottomX,rampBottomY,40,Math.PI*2-ang,0);ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 13px Segoe UI';ctx.textAlign='left';ctx.fillText(Math.round(ang*180/Math.PI)+'°',rampBottomX+45,rampBottomY-8);
/* Box on ramp */
let bxDraw,byDraw;
if(boxMoving&&boxSuccess){const t=Math.min(animT/60,1);const cx=rampBottomX+(rampTopX-rampBottomX)*t;const cy=rampBottomY+(rampTopY-rampBottomY)*t;bxDraw=cx-20;byDraw=cy-35}
else if(boxMoving&&boxFail){const t=Math.min(animT/30,1);const startFrac=0.3;const cx=rampBottomX+(rampTopX-rampBottomX)*(startFrac*(1-t));const cy=rampBottomY+(rampTopY-rampBottomY)*(startFrac*(1-t));bxDraw=cx-20;byDraw=cy-35}
else{bxDraw=rampBottomX-20;byDraw=rampBottomY-35}
ctx.fillStyle=COLORS[round%COLORS.length];ctx.fillRect(bxDraw,byDraw,40,30);
ctx.fillStyle='#fff';ctx.font='bold 12px Segoe UI';ctx.textAlign='center';ctx.fillText(boxWeight+'kg',bxDraw+20,byDraw+20);
/* Effort arrows */
const forceNeeded=getForceNeeded();const forcePct=Math.round(forceNeeded/playerForce*100);
/* Force meters */
ctx.fillStyle='#1e1b4b';ctx.fillRect(30,80,200,30);
ctx.fillStyle=forcePct<=100?'#34d399':'#ef4444';ctx.fillRect(30,80,Math.min(200,200*(forceNeeded/playerForce)),30);
ctx.fillStyle='#fff';ctx.font='bold 13px Segoe UI';ctx.textAlign='left';ctx.fillText('Gereken Kuvvet: '+Math.round(forceNeeded)+' N',35,100);
ctx.fillStyle='#1e1b4b';ctx.fillRect(30,120,200,30);
ctx.fillStyle='#60a5fa';ctx.fillRect(30,120,200,30);
ctx.fillStyle='#fff';ctx.fillText('Senin Gücün: '+playerForce+' N',35,140);
/* Ramp length setting buttons */
ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('Rampa Uzunluğu: '+rampLabels[rampSetting],W/2,groundY+45);
/* - button */
ctx.fillStyle='#7c3aed';ctx.fillRect(200,groundY+55,50,35);
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('−',225,groundY+79);
/* + button */
ctx.fillStyle='#7c3aed';ctx.fillRect(450,groundY+55,50,35);
ctx.fillStyle='#fff';ctx.fillText('+',475,groundY+79);
/* Length display */
ctx.fillStyle='#c084fc';ctx.font='bold 18px Segoe UI';ctx.fillText(getRampLen()+' cm',W/2,groundY+80);
/* Push button */
if(!boxMoving){ctx.fillStyle=forcePct<=100?'#10b981':'#6b7280';ctx.fillRect(270,groundY+100,160,40);
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('🏋️ Taşı!',W/2,groundY+126)}
/* Result messages */
if(boxSuccess&&animT>60){ctx.fillStyle='#34d399';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText('✅ Harika! Kutu platforma çıktı!',W/2,platTop-40);
if(animT>90){ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-60,platTop-30,120,35);ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('Sonraki ▶',W/2,platTop-8)}}
if(boxFail&&animT>30){ctx.fillStyle='#ef4444';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText(failMsg,W/2,platTop-40);
if(animT>50){ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-60,platTop-30,120,35);ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('Tekrar Dene',W/2,platTop-8)}}
/* Info box */
ctx.fillStyle='rgba(30,27,75,0.8)';ctx.fillRect(15,170,230,60);ctx.fillStyle='#e9d5ff';ctx.font='13px Segoe UI';ctx.textAlign='left';
ctx.fillText('Kuvvet = Ağırlık × sin(açı)',25,190);ctx.fillText('Uzun rampa → Küçük açı → Az kuvvet',25,208);ctx.fillText('Ağırlık: '+boxWeight+' kg × 10 = '+boxWeight*10+' N',25,224);
/* Particles */
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(state==='play'&&boxMoving){animT++;
if(boxSuccess&&animT>90){}
if(boxFail&&animT>50){}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function tryPush(){if(boxMoving)return;const forceNeeded=getForceNeeded();
boxMoving=true;animT=0;
if(forceNeeded<=playerForce){boxSuccess=true;boxFail=false;score+=10;snd(true);addP(480,520-platformH,'#34d399')}
else{boxSuccess=false;boxFail=true;failMsg='Rampa çok kısa! ('+Math.round(forceNeeded)+' N > '+playerForce+' N)';snd(false);addP(480-getRampLen(),520,'#ef4444')}}
function nextRound(){round++;if(round>=maxR){state='win';return}startLevel()}
function retryRound(){boxMoving=false;boxSuccess=false;boxFail=false;animT=0}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){state='play';score=0;round=0;startLevel()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<380){state='play';score=0;round=0;startLevel()}return}
const groundY=520;const platTop=groundY-platformH;
/* - button */
if(mx>200&&mx<250&&my>groundY+55&&my<groundY+90&&!boxMoving){rampSetting=Math.max(0,rampSetting-1);return}
/* + button */
if(mx>450&&mx<500&&my>groundY+55&&my<groundY+90&&!boxMoving){rampSetting=Math.min(4,rampSetting+1);return}
/* Push button */
if(mx>270&&mx<430&&my>groundY+100&&my<groundY+140&&!boxMoving){tryPush();return}
/* Next/Retry button */
if(boxSuccess&&animT>90&&mx>W/2-60&&mx<W/2+60&&my>platTop-30&&my<platTop+5){nextRound();return}
if(boxFail&&animT>50&&mx>W/2-60&&mx<W/2+60&&my>platTop-30&&my<platTop+5){retryRound();return}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_sci_makara_html():
    """Makara Operasyonu — Makara türünü seçerek ağırlığı kaldır."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=0,maxR=10,particles=[];
let selectedPulley=-1,pulling=false,pullProgress=0,weightY=0,targetY=0;
let weightKg=10,liftDone=false,liftFail=false,showQuestion=false,questionAnswered=false,bonusEarned=false;
let animT=0,handY=0,ropeAngle=0;
const pulleyTypes=['Direkt','Sabit Makara','Hareketli Makara'];
const pulleyEmoji=['🤚','⚙️','⚙️⚙️'];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function startLevel(){selectedPulley=-1;pulling=false;pullProgress=0;liftDone=false;liftFail=false;showQuestion=false;questionAnswered=false;bonusEarned=false;animT=0;
weightKg=8+round*6;if(round>=7)weightKg=8+round*8;
weightY=420;targetY=140;handY=350}
function getEffort(pType){if(pType===0)return 100;if(pType===1)return 100;if(pType===2)return 50;return 100}
function getForceLabel(pType){if(pType===0)return 'Kuvvet değişmez, yön değişmez';if(pType===1)return 'Kuvvet aynı, yön değişir (aşağı çek)';if(pType===2)return 'Kuvvet yarıya düşer!';return ''}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('⚙️ Makara Operasyonu',W/2,160);ctx.font='20px Segoe UI';ctx.fillText('Doğru makara ile ağırlığı kaldır!',W/2,210);ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';ctx.fillText('Hareketli makara kuvveti yarıya indirir',W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,300,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Makara Ustası!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxR*15),W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,300,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,330);return}
/* HUD */
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+(round+1)+'/'+maxR,15,30);
ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Ceiling beam */
ctx.fillStyle='#5d4037';ctx.fillRect(100,60,500,20);
ctx.fillStyle='#795548';ctx.fillRect(100,60,500,8);
/* Target platform */
ctx.fillStyle='#4caf50';ctx.fillRect(280,targetY-5,140,10);
ctx.fillStyle='#81c784';ctx.fillRect(280,targetY-5,140,4);
ctx.fillStyle='#e9d5ff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';ctx.fillText('🏁 Hedef',350,targetY-12);
/* Draw based on selected pulley */
const ctrX=350;
if(selectedPulley>=0){
/* Rope and weight */
const curWeightY=liftDone?targetY+20:weightY-(weightY-targetY-20)*pullProgress;
/* Pulley wheel(s) */
if(selectedPulley===1||selectedPulley===2){
const pulleyY=80;
ctx.fillStyle='#78909c';ctx.strokeStyle='#b0bec5';ctx.lineWidth=3;
ctx.beginPath();ctx.arc(ctrX,pulleyY,22,0,Math.PI*2);ctx.fill();ctx.stroke();
ctx.fillStyle='#546e7a';ctx.beginPath();ctx.arc(ctrX,pulleyY,8,0,Math.PI*2);ctx.fill();
/* Rotation indicator */
const rAng=ropeAngle;
ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(ctrX+15*Math.cos(rAng),pulleyY+15*Math.sin(rAng));
ctx.lineTo(ctrX-15*Math.cos(rAng),pulleyY-15*Math.sin(rAng));ctx.stroke();
if(selectedPulley===2){
const mp=(curWeightY+targetY)/2+30;
ctx.fillStyle='#78909c';ctx.strokeStyle='#b0bec5';ctx.lineWidth=3;
ctx.beginPath();ctx.arc(ctrX,mp,18,0,Math.PI*2);ctx.fill();ctx.stroke();
ctx.fillStyle='#546e7a';ctx.beginPath();ctx.arc(ctrX,mp,6,0,Math.PI*2);ctx.fill()}}
/* Rope */
ctx.strokeStyle='#bcaaa4';ctx.lineWidth=3;
if(selectedPulley===0){ctx.beginPath();ctx.moveTo(ctrX,curWeightY);ctx.lineTo(ctrX,curWeightY-50);ctx.stroke();
/* Hand */
ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText('🤚',ctrX,curWeightY-50)}
else if(selectedPulley===1){ctx.beginPath();ctx.moveTo(ctrX,curWeightY);ctx.lineTo(ctrX,80);ctx.stroke();
ctx.beginPath();ctx.moveTo(ctrX,80);ctx.lineTo(ctrX+100,handY);ctx.stroke();
ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText('🤚',ctrX+100,handY+15)}
else{const mp=(curWeightY+targetY)/2+30;
ctx.beginPath();ctx.moveTo(ctrX-20,curWeightY);ctx.lineTo(ctrX-20,mp);ctx.stroke();
ctx.beginPath();ctx.moveTo(ctrX+20,mp);ctx.lineTo(ctrX+20,80);ctx.stroke();
ctx.beginPath();ctx.moveTo(ctrX,80);ctx.lineTo(ctrX+120,handY);ctx.stroke();
ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText('🤚',ctrX+120,handY+15)}
/* Weight box */
ctx.fillStyle=COLORS[round%COLORS.length];ctx.fillRect(ctrX-30,curWeightY,60,45);
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.fillText(weightKg+'kg',ctrX,curWeightY+28);
/* Effort display */
const eff=getEffort(selectedPulley);const forceN=Math.round(weightKg*10*eff/100);
ctx.fillStyle='rgba(30,27,75,0.85)';ctx.fillRect(20,480,280,80);
ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
ctx.fillText('Makara: '+pulleyTypes[selectedPulley],30,500);
ctx.fillText('Ağırlık: '+(weightKg*10)+' N',30,520);
ctx.fillText('Gereken Kuvvet: '+forceN+' N ('+eff+'%)',30,540);
ctx.fillStyle='#c084fc';ctx.font='13px Segoe UI';ctx.fillText(getForceLabel(selectedPulley),30,555);
/* Pull button */
if(!pulling&&!liftDone){ctx.fillStyle='#10b981';ctx.fillRect(400,500,180,45);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('⬆️ Çek!',490,528)}}
else{
/* Pulley selection */
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Makara Türü Seç:',W/2,200);
for(let i=0;i<3;i++){const bx=80+i*210,by=240;
ctx.fillStyle='#7c3aed';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(bx,by,180,100,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText(pulleyEmoji[i],bx+90,by+35);ctx.fillText(pulleyTypes[i],bx+90,by+60);
ctx.fillStyle='#c084fc';ctx.font='13px Segoe UI';
if(i===0)ctx.fillText('Kuvvet: 100%',bx+90,by+82);
if(i===1)ctx.fillText('Kuvvet: 100% (yön değişir)',bx+90,by+82);
if(i===2)ctx.fillText('Kuvvet: 50%',bx+90,by+82)}
/* Weight display */
ctx.fillStyle=COLORS[round%COLORS.length];ctx.fillRect(ctrX-30,420,60,45);ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.fillText(weightKg+'kg',ctrX,448)}
/* Lift result */
if(liftDone){ctx.fillStyle='#34d399';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText('✅ Ağırlık kaldırıldı! +10 puan',W/2,targetY-35);
/* Show question for bonus */
if(showQuestion&&!questionAnswered){ctx.fillStyle='rgba(30,27,75,0.9)';ctx.fillRect(100,430,500,120);
ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('Bonus: Hangi makara en az kuvvetle kaldırır?',W/2,460);
for(let i=0;i<3;i++){const bx=130+i*170,by=475;ctx.fillStyle='#7c3aed';ctx.fillRect(bx,by,150,30);ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.fillText(pulleyTypes[i],bx+75,by+20)}}
if(questionAnswered){ctx.fillStyle=bonusEarned?'#34d399':'#ef4444';ctx.font='bold 18px Segoe UI';ctx.fillText(bonusEarned?'🎁 Bonus +5!':'Hareketli makara doğru cevap!',W/2,470);
if(animT>40){ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-60,490,120,35);ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('Sonraki ▶',W/2,512)}}}
/* Particles */
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(state==='play'){
if(pulling&&!liftDone){pullProgress+=0.015;ropeAngle+=0.1;handY+=1.5;
if(pullProgress>=1){pullProgress=1;pulling=false;liftDone=true;showQuestion=true;animT=0;score+=10;snd(true);addP(350,targetY,'#34d399')}}
if(liftDone)animT++}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function nextRound(){round++;if(round>=maxR){state='win';return}startLevel()}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=0;startLevel()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=0;startLevel()}return}
/* Pulley selection */
if(selectedPulley<0){for(let i=0;i<3;i++){const bx=80+i*210,by=240;if(mx>bx&&mx<bx+180&&my>by&&my<by+100){selectedPulley=i;return}}}
/* Pull button */
if(selectedPulley>=0&&!pulling&&!liftDone&&mx>400&&mx<580&&my>500&&my<545){pulling=true;return}
/* Question answers */
if(showQuestion&&!questionAnswered&&liftDone){for(let i=0;i<3;i++){const bx=130+i*170,by=475;if(mx>bx&&mx<bx+150&&my>by&&my<by+30){questionAnswered=true;animT=0;
if(i===2){bonusEarned=true;score+=5;snd(true);addP(W/2,460,'#fbbf24')}else{bonusEarned=false;snd(false)}return}}}
/* Next button */
if(liftDone&&questionAnswered&&animT>40&&mx>W/2-60&&mx<W/2+60&&my>490&&my<525){nextRound();return}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_sci_hal_degisimi_html():
    """Hâl Değişimi Mutfağı — Isıtma/soğutma ile maddenin halini değiştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=0,maxR=10,particles=[];
let currentState=0,targetState=2,temp=0,animT=0,roundDone=false,wrongHint='';
/* States: 0=buz(ice), 1=su(water), 2=buhar(steam) */
const stateNames=['Buz','Su','Buhar'];
const stateEmoji=['🧊','💧','♨️'];
const stateColors=['#60a5fa','#3b82f6','#94a3b8'];
const tasks=[
{start:0,target:2,desc:'Buzu buhara dönüştür!'},
{start:2,target:0,desc:'Buharı buza dönüştür!'},
{start:1,target:2,desc:'Suyu buhara dönüştür!'},
{start:1,target:0,desc:'Suyu buza dönüştür!'},
{start:0,target:1,desc:'Buzu suya dönüştür!'},
{start:2,target:1,desc:'Buharı suya dönüştür!'},
{start:0,target:2,desc:'Buzu buhara dönüştür!'},
{start:2,target:0,desc:'Buharı buza dönüştür!'},
{start:0,target:1,desc:'Buzu suya dönüştür!'},
{start:1,target:2,desc:'Suyu buhara dönüştür!'}
];
let taskDesc='',steamParticles=[],iceParticles=[],ripples=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function startLevel(){const task=tasks[round%tasks.length];currentState=task.start;targetState=task.target;taskDesc=task.desc;
temp=currentState===0?-20:currentState===1?50:110;
roundDone=false;wrongHint='';animT=0;steamParticles=[];iceParticles=[];ripples=[]}
function stateForTemp(t){if(t<=0)return 0;if(t>=100)return 2;return 1}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔥 Hâl Değişimi Mutfağı',W/2,160);ctx.font='20px Segoe UI';ctx.fillText('Isıt veya soğut,',W/2,210);ctx.fillText('maddenin halini değiştir!',W/2,240);ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';ctx.fillText('Buz ↔ Su ↔ Buhar',W/2,280);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,320,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,350);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Harika!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,250);ctx.fillText('Hâl değişimi uzmanısın!',W/2,290);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,330,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,360);return}
/* HUD */
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+(round+1)+'/'+maxR,15,30);
ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Task */
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2-180,50,360,45,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(taskDesc,W/2,80);
/* Kitchen background */
ctx.fillStyle='#2d1b4e';ctx.fillRect(50,110,600,380);
ctx.strokeStyle='#4a2d6e';ctx.lineWidth=2;ctx.strokeRect(50,110,600,380);
/* Stove on left */
ctx.fillStyle='#424242';ctx.fillRect(70,380,120,100);ctx.fillStyle='#616161';ctx.fillRect(75,385,110,20);
/* Flame */
if(currentState<2){for(let i=0;i<3;i++){ctx.fillStyle='#ff6b35';ctx.beginPath();const fx=100+i*25,fy=410;ctx.moveTo(fx,fy);ctx.quadraticCurveTo(fx-8,fy-20-Math.sin(animT*0.1+i)*8,fx,fy-35);ctx.quadraticCurveTo(fx+8,fy-20-Math.cos(animT*0.1+i)*8,fx,fy);ctx.fill();
ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.moveTo(fx,fy);ctx.quadraticCurveTo(fx-4,fy-12,fx,fy-20);ctx.quadraticCurveTo(fx+4,fy-12,fx,fy);ctx.fill()}}
ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.fillText('🔥 Ocak',130,490);
/* Freezer on right */
ctx.fillStyle='#b3e5fc';ctx.fillRect(510,380,120,100);ctx.fillStyle='#81d4fa';ctx.fillRect(515,385,110,90);
ctx.strokeStyle='#4fc3f7';ctx.lineWidth=2;ctx.strokeRect(510,380,120,100);
/* Snowflakes */
for(let i=0;i<4;i++){ctx.fillStyle='#fff';ctx.font='16px Segoe UI';ctx.fillText('❄️',530+i*22,420+Math.sin(animT*0.05+i)*10)}
ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.fillText('❄️ Buzluk',570,490);
/* Main substance in center */
const subX=W/2,subY=310;const cs=stateForTemp(temp);
/* Beaker */
ctx.fillStyle='rgba(200,200,255,0.15)';ctx.strokeStyle='rgba(200,200,255,0.5)';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(subX-60,220);ctx.lineTo(subX-70,400);ctx.lineTo(subX+70,400);ctx.lineTo(subX+60,220);ctx.closePath();ctx.fill();ctx.stroke();
/* Substance inside beaker */
if(cs===0){/* Ice */
ctx.fillStyle='#90caf9';ctx.fillRect(subX-55,300,110,95);
ctx.fillStyle='#bbdefb';for(let i=0;i<4;i++){ctx.fillRect(subX-50+i*28,310+i*12,24,18)}
/* Crack lines */
ctx.strokeStyle='#e3f2fd';ctx.lineWidth=1;
ctx.beginPath();ctx.moveTo(subX-30,320);ctx.lineTo(subX+10,340);ctx.lineTo(subX-10,370);ctx.stroke();
ctx.beginPath();ctx.moveTo(subX+20,310);ctx.lineTo(subX+5,350);ctx.stroke()}
else if(cs===1){/* Water */
ctx.fillStyle='#42a5f5';ctx.fillRect(subX-55,310,110,85);
/* Ripples */
ctx.strokeStyle='#90caf9';ctx.lineWidth=1;
for(let i=0;i<3;i++){const ry=315+i*8;const roff=Math.sin(animT*0.08+i)*15;
ctx.beginPath();ctx.moveTo(subX-50,ry);ctx.quadraticCurveTo(subX+roff,ry-5,subX+50,ry);ctx.stroke()}}
else{/* Steam */
ctx.fillStyle='rgba(176,190,197,0.3)';ctx.fillRect(subX-55,340,110,55);
/* Steam rising */
for(let i=0;i<8;i++){const sx=subX-40+Math.random()*80;const sy=280-i*20-animT%30;const sr=5+Math.random()*10;
ctx.fillStyle='rgba(200,200,200,'+(0.4-i*0.04)+')';ctx.beginPath();ctx.arc(sx,sy,sr,0,Math.PI*2);ctx.fill()}}
/* State label */
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(stateEmoji[cs]+' '+stateNames[cs],subX,430);
/* Phase diagram */
ctx.fillStyle='rgba(30,27,75,0.8)';ctx.fillRect(180,505,340,35);
ctx.font='bold 14px Segoe UI';
ctx.fillStyle=cs===0?'#60a5fa':'#6b7280';ctx.fillText('🧊 Buz',230,527);
ctx.fillStyle='#6b7280';ctx.fillText('→ 0°C →',300,527);
ctx.fillStyle=cs===1?'#3b82f6':'#6b7280';ctx.fillText('💧 Su',360,527);
ctx.fillStyle='#6b7280';ctx.fillText('→ 100°C →',430,527);
ctx.fillStyle=cs===2?'#94a3b8':'#6b7280';ctx.fillText('♨️ Buhar',500,527);
/* Thermometer */
const thX=660,thTop=140,thBot=470,thH=thBot-thTop;
ctx.fillStyle='#e0e0e0';ctx.fillRect(thX-8,thTop,16,thH);
ctx.beginPath();ctx.arc(thX,thBot+12,15,0,Math.PI*2);ctx.fill();
/* Mercury */
const tNorm=Math.max(0,Math.min(1,(temp+30)/160));const mercH=thH*tNorm;
const mercClr=temp<0?'#42a5f5':temp<50?'#ef5350':temp<100?'#ff7043':'#d32f2f';
ctx.fillStyle=mercClr;ctx.fillRect(thX-5,thBot-mercH,10,mercH);
ctx.beginPath();ctx.arc(thX,thBot+12,12,0,Math.PI*2);ctx.fill();
/* Temp labels */
ctx.fillStyle='#e9d5ff';ctx.font='12px Segoe UI';ctx.textAlign='right';
ctx.fillText('130°',thX-14,thTop+10);ctx.fillText('100°',thX-14,thTop+thH*0.23);
ctx.fillText('50°',thX-14,thTop+thH*0.5);ctx.fillText('0°',thX-14,thTop+thH*0.77);
ctx.fillText('-30°',thX-14,thBot);
/* Current temp */
ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(Math.round(temp)+'°C',thX,thBot+40);
/* Action buttons */
if(!roundDone){
ctx.fillStyle='#ef4444';ctx.beginPath();ctx.roundRect(140,555,180,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('🔥 Isıt',230,586);
ctx.fillStyle='#2196f3';ctx.beginPath();ctx.roundRect(380,555,180,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.fillText('❄️ Soğut',470,586)}
/* Wrong hint */
if(wrongHint){ctx.fillStyle='#ef4444';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(wrongHint,W/2,550)}
/* Round done */
if(roundDone){ctx.fillStyle='#34d399';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText('✅ Doğru hâl değişimi! +10',W/2,555);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-60,575,120,35);ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('Sonraki ▶',W/2,597)}
/* Particles */
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){animT++;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function doHeat(){if(roundDone)return;
const cs=stateForTemp(temp);if(cs>=targetState&&targetState<cs){wrongHint='Bu yönde değil! Soğutman gerek ❄️';snd(false);return}
wrongHint='';temp+=15;if(temp>130)temp=130;
const ns=stateForTemp(temp);
if(ns!==cs){addP(W/2,310,ns===1?'#42a5f5':'#b0bec5');snd(true)}
if(ns===targetState){roundDone=true;score+=10;snd(true);addP(W/2,310,'#34d399')}}
function doCool(){if(roundDone)return;
const cs=stateForTemp(temp);if(cs<=targetState&&targetState>cs){wrongHint='Bu yönde değil! Isıtman gerek 🔥';snd(false);return}
wrongHint='';temp-=15;if(temp<-30)temp=-30;
const ns=stateForTemp(temp);
if(ns!==cs){addP(W/2,310,ns===0?'#90caf9':'#42a5f5');snd(true)}
if(ns===targetState){roundDone=true;score+=10;snd(true);addP(W/2,310,'#34d399')}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){state='play';score=0;round=0;startLevel()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<380){state='play';score=0;round=0;startLevel()}return}
/* Heat button */
if(!roundDone&&mx>140&&mx<320&&my>555&&my<605){doHeat();return}
/* Cool button */
if(!roundDone&&mx>380&&mx<560&&my>555&&my<605){doCool();return}
/* Next button */
if(roundDone&&mx>W/2-60&&mx<W/2+60&&my>575&&my<610){round++;if(round>=maxR){state='win'}else{startLevel()};return}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_sci_karisim_cozelti_html():
    """Karışım mı Çözelti mi? — Karışım/çözelti sınıflandır ve ayırma yöntemi seç."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=0,maxR=10,particles=[];
let phase=0,classified=false,classCorrect=false,sepCorrect=false,roundDone=false,animPhase=0,animT=0;
/* phase: 0=classify, 1=separation, 2=result */
const mixtures=[
{name:'Tuzlu Su',emoji:'🧂💧',type:'cozelti',sep:'buhar',desc:'Tuz suda çözünür',liqClr:'#90caf9',partClr:'#fff',dissolved:true},
{name:'Kumlu Su',emoji:'🏖️💧',type:'karisim',sep:'suzme',desc:'Kum suda çözünmez',liqClr:'#90caf9',partClr:'#d4a373',dissolved:false},
{name:'Şekerli Su',emoji:'🍬💧',type:'cozelti',sep:'buhar',desc:'Şeker suda çözünür',liqClr:'#e3f2fd',partClr:'#fff',dissolved:true},
{name:'Yağlı Su',emoji:'🫒💧',type:'karisim',sep:'cokeltme',desc:'Yağ suda çözünmez',liqClr:'#90caf9',partClr:'#fdd835',dissolved:false},
{name:'Sirke-Yağ',emoji:'🫒🍶',type:'karisim',sep:'cokeltme',desc:'Yağ sirkede çözünmez',liqClr:'#fff9c4',partClr:'#fdd835',dissolved:false},
{name:'Limonata',emoji:'🍋💧',type:'cozelti',sep:'buhar',desc:'Limon suyu suda çözünür',liqClr:'#fff59d',partClr:'#fff',dissolved:true},
{name:'Tebeşir Tozu-Su',emoji:'📝💧',type:'karisim',sep:'suzme',desc:'Tebeşir suda çözünmez',liqClr:'#e0e0e0',partClr:'#fafafa',dissolved:false},
{name:'Bal-Su',emoji:'🍯💧',type:'cozelti',sep:'buhar',desc:'Bal suda çözünür',liqClr:'#ffcc80',partClr:'#fff',dissolved:true},
{name:'Toprak-Su',emoji:'🌍💧',type:'karisim',sep:'suzme',desc:'Toprak suda çözünmez',liqClr:'#a1887f',partClr:'#5d4037',dissolved:false},
{name:'Soda',emoji:'🥤',type:'cozelti',sep:'buhar',desc:'CO₂ suda çözünür',liqClr:'#e0e0e0',partClr:'#fff',dissolved:true}
];
let curMix=mixtures[0];
let beakerParticles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function startLevel(){curMix=mixtures[round%mixtures.length];phase=0;classified=false;classCorrect=false;sepCorrect=false;roundDone=false;animPhase=0;animT=0;
beakerParticles=[];
for(let i=0;i<(curMix.dissolved?0:15);i++){beakerParticles.push({x:280+Math.random()*140,y:250+Math.random()*150,vx:(Math.random()-.5)*0.5,vy:Math.random()*0.3,r:3+Math.random()*4})}}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';ctx.fillText('🧪 Karışım mı Çözelti mi?',W/2,160);ctx.font='20px Segoe UI';ctx.fillText('Karışımı sınıflandır',W/2,210);ctx.fillText('ve ayırma yöntemini bul!',W/2,240);ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';ctx.fillText('Çözelti: Çözünen görünmez | Karışım: Parçacıklar görünür',W/2,280);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,320,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,350);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Bilim İnsanı!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,300,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,330);return}
/* HUD */
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+(round+1)+'/'+maxR,15,30);
ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Mixture name */
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2-160,50,320,50,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(curMix.emoji+' '+curMix.name,W/2,82);
/* Beaker */
const bx=W/2,by=300;
ctx.fillStyle='rgba(200,220,255,0.12)';ctx.strokeStyle='rgba(200,220,255,0.5)';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(bx-80,180);ctx.lineTo(bx-90,420);ctx.lineTo(bx+90,420);ctx.lineTo(bx+80,180);ctx.closePath();ctx.fill();ctx.stroke();
/* Liquid inside */
if(animPhase===0){/* Normal view */
ctx.fillStyle=curMix.liqClr;ctx.globalAlpha=0.6;
ctx.beginPath();ctx.moveTo(bx-85,240);ctx.lineTo(bx-88,415);ctx.lineTo(bx+88,415);ctx.lineTo(bx+85,240);ctx.closePath();ctx.fill();ctx.globalAlpha=1;
/* Particles for mixtures */
if(!curMix.dissolved){beakerParticles.forEach(p=>{ctx.fillStyle=curMix.partClr;ctx.globalAlpha=0.8;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1})}
else{/* Dissolved - uniform color, maybe slight shimmer */
ctx.fillStyle=curMix.liqClr;ctx.globalAlpha=0.3;for(let i=0;i<5;i++){const sx=bx-60+Math.random()*120,sy=260+Math.random()*140;ctx.beginPath();ctx.arc(sx,sy,2,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}}
else if(animPhase===1){/* Separation animation */
const t=Math.min(animT/80,1);
if(curMix.sep==='suzme'){/* Filter */
ctx.fillStyle=curMix.liqClr;ctx.globalAlpha=0.6;
ctx.beginPath();ctx.moveTo(bx-85,240);ctx.lineTo(bx-88,415);ctx.lineTo(bx+88,415);ctx.lineTo(bx+85,240);ctx.closePath();ctx.fill();ctx.globalAlpha=1;
/* Filter funnel */
ctx.fillStyle='#e0e0e0';ctx.beginPath();ctx.moveTo(bx-50,200);ctx.lineTo(bx-20,300);ctx.lineTo(bx+20,300);ctx.lineTo(bx+50,200);ctx.closePath();ctx.fill();
ctx.strokeStyle='#bdbdbd';ctx.stroke();
/* Filter paper */
ctx.fillStyle='#f5f5f5';ctx.beginPath();ctx.arc(bx,250,30,0,Math.PI,false);ctx.fill();
/* Caught particles */
beakerParticles.forEach((p,i)=>{const py=250+i*2;ctx.fillStyle=curMix.partClr;ctx.globalAlpha=t;ctx.beginPath();ctx.arc(bx-15+i*3,py,p.r*0.7,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1})
/* Clean water dropping */
ctx.fillStyle=curMix.liqClr;ctx.globalAlpha=0.5;for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(bx,310+i*15+animT%20,4,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}
else if(curMix.sep==='buhar'){/* Evaporation */
ctx.fillStyle=curMix.liqClr;ctx.globalAlpha=0.6*(1-t*0.8);
const waterTop=240+(415-240)*t*0.7;
ctx.beginPath();ctx.moveTo(bx-85,waterTop);ctx.lineTo(bx-88,415);ctx.lineTo(bx+88,415);ctx.lineTo(bx+85,waterTop);ctx.closePath();ctx.fill();ctx.globalAlpha=1;
/* Steam */
for(let i=0;i<10;i++){const sx=bx-50+Math.random()*100;const sy=waterTop-20-i*15-animT%25;ctx.fillStyle='rgba(200,200,200,'+(0.5*t*(1-i*0.08))+')';ctx.beginPath();ctx.arc(sx,sy,6+Math.random()*8,0,Math.PI*2);ctx.fill()}
/* Residue at bottom */
if(t>0.5){ctx.fillStyle=curMix.partClr==='#fff'?'#e0e0e0':curMix.partClr;ctx.globalAlpha=t;ctx.fillRect(bx-60,400,120,12);ctx.globalAlpha=1}}
else{/* Settling */
ctx.fillStyle=curMix.liqClr;ctx.globalAlpha=0.5;
ctx.beginPath();ctx.moveTo(bx-85,240);ctx.lineTo(bx-88,415);ctx.lineTo(bx+88,415);ctx.lineTo(bx+85,240);ctx.closePath();ctx.fill();ctx.globalAlpha=1;
/* Top layer (oil/light) */
const layerH=60*t;
ctx.fillStyle=curMix.partClr;ctx.globalAlpha=0.7;ctx.fillRect(bx-83,240,166,layerH);ctx.globalAlpha=1;
/* Bottom layer */
ctx.fillStyle=curMix.liqClr;ctx.globalAlpha=0.7;ctx.fillRect(bx-83,240+layerH,166,170-layerH);ctx.globalAlpha=1;
/* Separator line */
if(t>0.3){ctx.strokeStyle='#fff';ctx.lineWidth=1;ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(bx-83,240+layerH);ctx.lineTo(bx+83,240+layerH);ctx.stroke();ctx.setLineDash([])}}}
/* Phase indicator */
ctx.fillStyle='rgba(30,27,75,0.85)';ctx.fillRect(20,440,300,50);
ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
ctx.fillText('Açıklama: '+curMix.desc,30,460);
ctx.fillText(curMix.type==='cozelti'?'Tür: Çözelti (homojen)':'Tür: Karışım (heterojen)',30,480);
/* Classification buttons */
if(phase===0&&!classified){ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Bu ne tür bir karışım?',W/2,510);
ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(140,525,180,45,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Karışım',230,554);
ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(380,525,180,45,10);ctx.fill();
ctx.fillStyle='#fff';ctx.fillText('Çözelti',470,554)}
/* Classification result */
if(classified&&phase===0){ctx.fillStyle=classCorrect?'#34d399':'#ef4444';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText(classCorrect?'✅ Doğru! +5':'❌ Yanlış! Doğrusu: '+(curMix.type==='cozelti'?'Çözelti':'Karışım'),W/2,520);
if(animT>25){phase=1;classified=false;animT=0}}
/* Separation method buttons */
if(phase===1&&!classified){ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Ayırma yöntemi?',W/2,510);
const methods=[{name:'Süzme',key:'suzme'},{name:'Buharlaştırma',key:'buhar'},{name:'Çökeltme',key:'cokeltme'}];
methods.forEach((m,i)=>{const bx2=60+i*220;ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(bx2,525,190,45,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText(m.name,bx2+95,554)})}
/* Separation result */
if(phase===1&&classified){ctx.fillStyle=sepCorrect?'#34d399':'#ef4444';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
const correctName=curMix.sep==='suzme'?'Süzme':curMix.sep==='buhar'?'Buharlaştırma':'Çökeltme';
ctx.fillText(sepCorrect?'✅ Doğru yöntem! +5':'❌ Doğru yöntem: '+correctName,W/2,520);
animPhase=1}
/* Round done - next button */
if(roundDone){ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-60,585,120,35);ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('Sonraki ▶',W/2,607)}
/* Particles */
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){animT++;
if(state==='play'){
beakerParticles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;if(p.x<290||p.x>410)p.vx*=-1;if(p.y<260||p.y>400)p.vy*=-1})}
if(animPhase===1&&animT>80&&!roundDone){roundDone=true}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){state='play';score=0;round=0;startLevel()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=0;startLevel()}return}
/* Classification buttons */
if(phase===0&&!classified){
if(mx>140&&mx<320&&my>525&&my<570){classified=true;animT=0;classCorrect=curMix.type==='karisim';if(classCorrect){score+=5;snd(true);addP(230,540,'#34d399')}else{snd(false);addP(230,540,'#ef4444')};return}
if(mx>380&&mx<560&&my>525&&my<570){classified=true;animT=0;classCorrect=curMix.type==='cozelti';if(classCorrect){score+=5;snd(true);addP(470,540,'#34d399')}else{snd(false);addP(470,540,'#ef4444')};return}}
/* Separation buttons */
if(phase===1&&!classified){
const methods=['suzme','buhar','cokeltme'];
for(let i=0;i<3;i++){const bx2=60+i*220;if(mx>bx2&&mx<bx2+190&&my>525&&my<570){classified=true;animT=0;sepCorrect=methods[i]===curMix.sep;if(sepCorrect){score+=5;snd(true);addP(bx2+95,540,'#34d399')}else{snd(false);addP(bx2+95,540,'#ef4444')};return}}}
/* Next button */
if(roundDone&&mx>W/2-60&&mx<W/2+60&&my>585&&my<620){round++;if(round>=maxR){state='win'}else{startLevel()};return}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_sci_madde_siniflandir_html():
    """Maddeyi Sınıflandır — Düşen madde kartlarını Katı/Sıvı/Gaz raflarına yerleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=0,maxR=10,particles=[];
let cards=[],activeCard=null,fallSpeed=1,correctShelf=-1,wrongFlash=0,roundItems=0,roundDone=false;
let shelfGlow=-1,shelfGlowT=0,comboCount=0,animT=0;
const items=[
{name:'Taş',emoji:'🪨',type:0},{name:'Su',emoji:'💧',type:1},{name:'Oksijen',emoji:'💨',type:2},
{name:'Demir',emoji:'⚙️',type:0},{name:'Süt',emoji:'🥛',type:1},{name:'Helyum',emoji:'🎈',type:2},
{name:'Buz',emoji:'🧊',type:0},{name:'Benzin',emoji:'⛽',type:1},{name:'Karbondioksit',emoji:'🫧',type:2},
{name:'Cam',emoji:'🪟',type:0},{name:'Cıva',emoji:'🌡️',type:1},{name:'Metan',emoji:'💨',type:2},
{name:'Tuz',emoji:'🧂',type:0},{name:'Alkol',emoji:'🧴',type:1},{name:'Azot',emoji:'🌬️',type:2},
{name:'Altın',emoji:'🥇',type:0},{name:'Yağ',emoji:'🫒',type:1},{name:'Oksijen',emoji:'🌬️',type:2},
{name:'Tahta',emoji:'🪵',type:0},{name:'Sirke',emoji:'🍶',type:1},{name:'Neon',emoji:'💡',type:2}
];
const shelfNames=['🧊 Katı','💧 Sıvı','💨 Gaz'];
const shelfColors=['#3b82f6','#06b6d4','#8b5cf6'];
let usedItems=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function shuffle(arr){const a=[...arr];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function spawnCard(){if(usedItems.length===0)return false;
const item=usedItems.shift();
activeCard={name:item.name,emoji:item.emoji,type:item.type,x:100+Math.random()*(W-200),y:-60,w:130,h:60,vy:fallSpeed,shake:0,placed:false,flyX:0,flyY:0,flying:false,flyT:0};return true}
function startLevel(){roundDone=false;animT=0;shelfGlow=-1;wrongFlash=0;
fallSpeed=1+round*0.3;
/* Pick items for this round */
const numItems=Math.min(2+Math.floor(round/3),5);
const shuffled=shuffle(items);usedItems=shuffled.slice(0,numItems);
activeCard=null;spawnCard()}
function getShelfRect(i){const sw=190,sh=70,gap=(W-3*sw)/4;return{x:gap+i*(sw+gap),y:H-90,w:sw,h:sh}}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';ctx.fillText('🧪 Maddeyi Sınıflandır',W/2,160);ctx.font='20px Segoe UI';ctx.fillText('Düşen kartları doğru rafa yerleştir!',W/2,210);ctx.font='16px Segoe UI';ctx.fillStyle='#c084fc';ctx.fillText('Katı 🧊 | Sıvı 💧 | Gaz 💨',W/2,250);ctx.fillText('Hız her turda artar!',W/2,280);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,320,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,350);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Süper Bilimci!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score,W/2,250);ctx.fillText(score>=80?'Mükemmel sınıflandırma!':score>=50?'Çok iyi!':'Pratik yapmaya devam!',W/2,290);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,330,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,360);return}
/* HUD */
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+(round+1)+'/'+maxR,15,30);
ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.fillText('Kalan: '+usedItems.length+(activeCard&&!activeCard.placed?' +1':''),W/2,30);
ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';ctx.fillText('Puan: '+score,W-15,30);
if(comboCount>1){ctx.fillStyle='#ff6b9d';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('🔥 Kombo x'+comboCount,W/2,55)}
/* Conveyor belt at top */
ctx.fillStyle='#37474f';ctx.fillRect(0,50,W,25);
ctx.fillStyle='#546e7a';for(let x=(-animT*2)%30-30;x<W;x+=30){ctx.fillRect(x,55,15,15)}
/* Shelves at bottom */
for(let i=0;i<3;i++){const sr=getShelfRect(i);
const isGlow=shelfGlow===i&&shelfGlowT>0;
ctx.fillStyle=isGlow?'#fbbf24':shelfColors[i];ctx.globalAlpha=isGlow?0.3+shelfGlowT*0.4:0.25;ctx.beginPath();ctx.roundRect(sr.x,sr.y,sr.w,sr.h,12);ctx.fill();ctx.globalAlpha=1;
ctx.strokeStyle=isGlow?'#fbbf24':shelfColors[i];ctx.lineWidth=isGlow?3:2;ctx.beginPath();ctx.roundRect(sr.x,sr.y,sr.w,sr.h,12);ctx.stroke();
ctx.fillStyle=isGlow?'#fbbf24':'#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(shelfNames[i],sr.x+sr.w/2,sr.y+sr.h/2+7)}
/* Active card */
if(activeCard&&!activeCard.placed){const c=activeCard;
if(c.flying){/* Flying to shelf animation */
const sr=getShelfRect(c.type);const tx=sr.x+sr.w/2,ty=sr.y;
const t=Math.min(c.flyT/20,1);const cx=c.x+(tx-c.x)*t;const cy=c.y+(ty-c.y)*t;
ctx.save();ctx.globalAlpha=1-t*0.3;
ctx.fillStyle=COLORS[(round+roundItems)%COLORS.length];ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(cx-c.w/2,cy-c.h/2,c.w,c.h,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(c.emoji+' '+c.name,cx,cy+6);ctx.restore()}
else{/* Falling card */
ctx.save();if(c.shake>0){ctx.translate(Math.sin(c.shake*2)*5,0);c.shake-=0.5}
ctx.fillStyle=COLORS[(round+roundItems)%COLORS.length];ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(c.x-c.w/2,c.y-c.h/2,c.w,c.h,10);ctx.fill();ctx.stroke();
/* Card shadow */
ctx.shadowColor='rgba(0,0,0,0.3)';ctx.shadowBlur=8;ctx.shadowOffsetY=4;
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.shadowColor='transparent';
ctx.fillText(c.emoji+' '+c.name,c.x,c.y+6);ctx.restore()}}
/* Wrong flash overlay */
if(wrongFlash>0){ctx.fillStyle='rgba(239,68,68,'+wrongFlash*0.15+')';ctx.fillRect(0,0,W,H)}
/* Round done message */
if(roundDone){ctx.fillStyle='#34d399';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText('✅ Tur tamamlandı!',W/2,200);
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-60,230,120,35);ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('Sonraki ▶',W/2,252)}
/* Info - current item hint for young kids */
if(activeCard&&!activeCard.placed&&!activeCard.flying){
const hint=activeCard.type===0?'Bu madde şeklini korur':activeCard.type===1?'Bu madde akışkandır':'Bu madde her yere yayılır';
ctx.fillStyle='rgba(30,27,75,0.7)';ctx.fillRect(W/2-140,H-170,280,25);
ctx.fillStyle='#c084fc';ctx.font='13px Segoe UI';ctx.textAlign='center';ctx.fillText('İpucu: '+hint,W/2,H-152)}
/* Particles */
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){animT++;
if(state==='play'){
if(shelfGlowT>0)shelfGlowT-=0.03;
if(wrongFlash>0)wrongFlash-=0.05;
if(activeCard&&!activeCard.placed){
if(activeCard.flying){activeCard.flyT++;
if(activeCard.flyT>=20){activeCard.placed=true;roundItems++;
if(!spawnCard()&&usedItems.length===0){roundDone=true}}}
else{activeCard.y+=activeCard.vy;
if(activeCard.y>H-130){/* Reached bottom without clicking - wrong! */
snd(false);wrongFlash=1;comboCount=0;activeCard.shake=5;
/* Show correct shelf */
shelfGlow=activeCard.type;shelfGlowT=1;
setTimeout(()=>{if(activeCard){activeCard.placed=true;roundItems++;
if(!spawnCard()&&usedItems.length===0){roundDone=true}}},800)}}}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>320&&my<370){state='play';score=0;round=0;roundItems=0;comboCount=0;startLevel()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<380){state='play';score=0;round=0;roundItems=0;comboCount=0;startLevel()}return}
/* Click on shelves */
if(activeCard&&!activeCard.placed&&!activeCard.flying){
for(let i=0;i<3;i++){const sr=getShelfRect(i);
if(mx>sr.x&&mx<sr.x+sr.w&&my>sr.y&&my<sr.y+sr.h){
if(i===activeCard.type){/* Correct! */
score+=10;comboCount++;snd(true);
addP(sr.x+sr.w/2,sr.y,'#34d399');
activeCard.flying=true;activeCard.flyT=0;
shelfGlow=i;shelfGlowT=1}
else{/* Wrong! */
snd(false);wrongFlash=1;comboCount=0;activeCard.shake=8;
shelfGlow=activeCard.type;shelfGlowT=1}
return}}}
/* Next round button */
if(roundDone&&mx>W/2-60&&mx<W/2+60&&my>230&&my<265){round++;if(round>=maxR){state='win'}else{roundItems=0;startLevel()};return}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""
