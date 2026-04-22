# -*- coding: utf-8 -*-
"""Okul Öncesi Genel Yetenek Oyunları — 20 Premium HTML5 Oyun (Bölüm A: 1-5)."""


def _build_prek_ab_aynisinibul_html():
    """Aynısını Bul — Eşleştirme kartları hafıza oyunu."""
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
let state='start',round=1,maxRound=10,score=0,particles=[];
let cards=[],firstPick=null,secondPick=null,lockBoard=false,flipTimer=0;
let matchedPairs=0,totalPairs=0,flipAnim=[];
const ALL_EMOJI=['🍎','🌟','🐱','🐶','🌈','🎈','🍕','🦋','🌺','🐠','🎵','🍉','🚀','🐸','🎨','🌙','🍓','🐻','🎁','🔔'];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function getGridSize(){if(round<=3)return{cols:3,rows:2};if(round<=7)return{cols:4,rows:3};return{cols:4,rows:4}}
function initRound(){const g=getGridSize();totalPairs=Math.floor(g.cols*g.rows/2);matchedPairs=0;
const emojis=shuffle([...ALL_EMOJI]).slice(0,totalPairs);
let pairs=[];emojis.forEach(e=>{pairs.push(e);pairs.push(e)});shuffle(pairs);
const cardW=Math.min(100,Math.floor((W-80)/(g.cols))-10);
const cardH=Math.min(100,Math.floor((H-200)/(g.rows))-10);
const totalW=g.cols*(cardW+10)-10;const totalH=g.rows*(cardH+10)-10;
const startX=(W-totalW)/2;const startY=(H-totalH)/2+40;
cards=[];for(let r=0;r<g.rows;r++){for(let c=0;c<g.cols;c++){
const idx=r*g.cols+c;if(idx<pairs.length){
cards.push({x:startX+c*(cardW+10),y:startY+r*(cardH+10),w:cardW,h:cardH,emoji:pairs[idx],faceUp:false,matched:false,flipScale:1,shakeX:0})}}}
firstPick=null;secondPick=null;lockBoard=false}
function drawCard(card){ctx.save();const cx=card.x+card.w/2;const cy=card.y+card.h/2;
ctx.translate(cx+card.shakeX,cy);ctx.scale(card.flipScale,1);ctx.translate(-cx,-cy);
if(card.faceUp||card.matched){roundRect(card.x,card.y,card.w,card.h,10);ctx.fillStyle=card.matched?'#166534':'#1e1b4b';ctx.fill();ctx.strokeStyle=card.matched?'#4ade80':'#818cf8';ctx.lineWidth=2;ctx.stroke();
ctx.font=Math.min(card.w,card.h)*0.5+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(card.emoji,card.x+card.w/2,card.y+card.h/2)}
else{roundRect(card.x,card.y,card.w,card.h,10);const bg=ctx.createLinearGradient(card.x,card.y,card.x+card.w,card.y+card.h);bg.addColorStop(0,'#6d28d9');bg.addColorStop(1,'#7c3aed');ctx.fillStyle=bg;ctx.fill();ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.stroke();
ctx.fillStyle='#a78bfa40';for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(card.x+card.w*0.3+i*card.w*0.2,card.y+card.h*0.5,6,0,Math.PI*2);ctx.fill()}
ctx.fillStyle='#e9d5ff';ctx.font='bold '+Math.min(card.w,card.h)*0.3+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('?',card.x+card.w/2,card.y+card.h/2)}
ctx.restore()}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🃏 Aynısını Bul 🃏',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Eşleşen kart çiftlerini bul!',W/2,230);ctx.font='18px Segoe UI';ctx.fillStyle='#c4b5fd';ctx.fillText('İki karta tıkla, aynıysa eşleşir!',W/2,265);
roundRect(W/2-80,300,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);
roundRect(W/2-80,310,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,35);ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';ctx.fillText('Eşleşen: '+matchedPairs+'/'+totalPairs,W/2,35);
cards.forEach(c=>drawCard(c));
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
cards.forEach(c=>{if(c.shakeX!==0){c.shakeX*=-0.7;if(Math.abs(c.shakeX)<0.5)c.shakeX=0}});
flipAnim=flipAnim.filter(fa=>{fa.card.flipScale+=fa.dir*0.1;if(fa.dir<0&&fa.card.flipScale<=0){fa.card.flipScale=0;fa.card.faceUp=fa.target;fa.dir=1;return true}if(fa.dir>0&&fa.card.flipScale>=1){fa.card.flipScale=1;return false}return true});
if(flipTimer>0){flipTimer--;if(flipTimer===0&&firstPick&&secondPick){
flipAnim.push({card:firstPick,dir:-0.1,target:false});flipAnim.push({card:secondPick,dir:-0.1,target:false});
setTimeout(()=>{firstPick=null;secondPick=null;lockBoard=false},300)}}
draw();requestAnimationFrame(update)}
function flipCard(card){if(lockBoard||card.faceUp||card.matched)return;
flipAnim.push({card,dir:-0.1,target:true});
if(!firstPick){firstPick=card}else{secondPick=card;lockBoard=true;
setTimeout(()=>{if(firstPick.emoji===secondPick.emoji){firstPick.matched=true;secondPick.matched=true;score+=10;matchedPairs++;
addP(firstPick.x+firstPick.w/2,firstPick.y+firstPick.h/2,'#4ade80');addP(secondPick.x+secondPick.w/2,secondPick.y+secondPick.h/2,'#4ade80');snd(true);
firstPick=null;secondPick=null;lockBoard=false;
if(matchedPairs>=totalPairs){round++;if(round>maxRound){state='win'}else{setTimeout(()=>initRound(),800)}}}
else{snd(false);firstPick.shakeX=8;secondPick.shakeX=8;flipTimer=40}},500)}}
canvas.addEventListener('click',e=>{const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;state='play';initRound()}return}
cards.forEach(c=>{if(mx>=c.x&&mx<=c.x+c.w&&my>=c.y&&my<=c.y+c.h)flipCard(c)})});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_prek_ab_golge_eslestir_html():
    """Gölge Eşleştir — Nesneleri gölgeleriyle eşleştir."""
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
let state='start',round=1,maxRound=10,score=0,particles=[];
let objects=[],shadows=[],selectedObj=null,matchedLines=[],shakeIdx=-1,shakeTick=0;
const SETS=[
['🍎','🍌','🍊','🍇'],['🐱','🐶','🐰','🐸'],['🚗','🚌','🚀','🛩️'],
['🌸','🌻','🌺','🌹'],['⭐','🌙','☀️','⚡'],['🎈','🎁','🎵','🎨'],
['🦋','🐞','🐝','🐛'],['🏠','🏰','⛺','🗼'],['🍕','🍔','🌮','🍩'],
['⚽','🏀','🎾','🏐'],['🐘','🦁','🐧','🐬'],['🎸','🎹','🥁','🎺']
];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function getPairCount(){if(round<=3)return 3;if(round<=7)return 4;return 4}
function initRound(){const cnt=getPairCount();const setIdx=(round-1)%SETS.length;
const emojis=SETS[setIdx].slice(0,cnt);
const spacing=Math.min(100,(H-200)/cnt);const startY=(H-(cnt*spacing))/2+30;
objects=[];shadows=[];matchedLines=[];selectedObj=null;
for(let i=0;i<cnt;i++){objects.push({x:100,y:startY+i*spacing,emoji:emojis[i],matched:false,selected:false,glow:0})}
const shuffled=shuffle([...emojis]);
for(let i=0;i<cnt;i++){shadows.push({x:W-160,y:startY+i*spacing,emoji:shuffled[i],matched:false,glow:0})}}
function drawObj(o,isShadow){ctx.save();const cx=o.x,cy=o.y;
if(o.glow>0){ctx.shadowColor=isShadow?'#4ade80':'#fbbf24';ctx.shadowBlur=o.glow*20}
roundRect(cx-35,cy-35,70,70,12);
if(isShadow&&!o.matched){ctx.fillStyle='#1e1b4b';ctx.fill();ctx.strokeStyle='#4b5563';ctx.lineWidth=2;ctx.stroke();
ctx.font='40px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.globalAlpha=0.15;ctx.fillStyle='#fff';ctx.fillText(o.emoji,cx,cy);ctx.globalAlpha=1}
else{const bg=o.matched?'#166534':(o.selected?'#4c1d95':'#312e81');ctx.fillStyle=bg;ctx.fill();
ctx.strokeStyle=o.selected?'#fbbf24':(o.matched?'#4ade80':'#818cf8');ctx.lineWidth=o.selected?3:2;ctx.stroke();
ctx.font='40px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(o.emoji,cx,cy)}
ctx.restore()}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('👤 Gölge Eşleştir 👤',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Nesneleri gölgeleriyle eşleştir!',W/2,230);ctx.font='18px Segoe UI';ctx.fillStyle='#c4b5fd';ctx.fillText('Önce nesneye, sonra gölgesine tıkla',W/2,265);
roundRect(W/2-80,300,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);
roundRect(W/2-80,310,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,35);
ctx.textAlign='center';ctx.fillStyle='#c4b5fd';ctx.font='18px Segoe UI';ctx.fillText('Nesne',100,70);ctx.fillText('Gölge',W-160,70);
ctx.strokeStyle='#4b556340';ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(W/2,80);ctx.lineTo(W/2,H-20);ctx.stroke();ctx.setLineDash([]);
matchedLines.forEach(ml=>{ctx.strokeStyle='#4ade8080';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(ml.x1,ml.y1);ctx.lineTo(ml.x2,ml.y2);ctx.stroke()});
objects.forEach(o=>drawObj(o,false));shadows.forEach(s=>drawObj(s,true));
if(shakeIdx>=0&&shakeTick>0){const s=shadows[shakeIdx];if(s)s.x=W-160+Math.sin(shakeTick*2)*5}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
objects.forEach(o=>{if(o.glow>0)o.glow=Math.max(0,o.glow-0.02)});shadows.forEach(s=>{if(s.glow>0)s.glow=Math.max(0,s.glow-0.02)});
if(shakeTick>0){shakeTick--;if(shakeTick===0&&shakeIdx>=0){if(shadows[shakeIdx])shadows[shakeIdx].x=W-160;shakeIdx=-1}}
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;state='play';initRound()}return}
for(let i=0;i<objects.length;i++){const o=objects[i];if(!o.matched&&Math.abs(mx-o.x)<35&&Math.abs(my-o.y)<35){
if(selectedObj)selectedObj.selected=false;selectedObj=o;o.selected=true;return}}
if(selectedObj){for(let i=0;i<shadows.length;i++){const s=shadows[i];if(!s.matched&&Math.abs(mx-s.x)<35&&Math.abs(my-s.y)<35){
if(s.emoji===selectedObj.emoji){s.matched=true;selectedObj.matched=true;s.glow=1;selectedObj.glow=1;
matchedLines.push({x1:selectedObj.x+35,y1:selectedObj.y,x2:s.x-35,y2:s.y});
score+=10;addP(s.x,s.y,'#4ade80');snd(true);selectedObj.selected=false;selectedObj=null;
const allDone=objects.every(o=>o.matched);if(allDone){round++;if(round>maxRound){setTimeout(()=>{state='win'},500)}else{setTimeout(()=>initRound(),800)}}}
else{snd(false);shakeIdx=i;shakeTick=20}
return}}}});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_prek_ab_renk_avi_html():
    """Renk Avı — Hedef renkteki şekillere dokun."""
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
let state='start',round=1,maxRound=10,score=0,particles=[];
let shapes=[],targetColor='',targetName='',timer=0,maxTime=5,found=0,totalTarget=0;
let lastTime=0,shakeShape=-1,shakeTick=0;
const RENK=[{name:'KIRMIZI',hex:'#ef4444'},{name:'MAVİ',hex:'#3b82f6'},{name:'YEŞİL',hex:'#22c55e'},{name:'SARI',hex:'#eab308'},{name:'TURUNCU',hex:'#f97316'},{name:'MOR',hex:'#a855f7'},{name:'PEMBE',hex:'#ec4899'},{name:'CYAN',hex:'#06b6d4'}];
const SHAPE_TYPES=['circle','square','star','triangle','diamond'];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function drawStar(cx,cy,r,pts){ctx.beginPath();for(let i=0;i<pts*2;i++){const a=i*Math.PI/pts-Math.PI/2;const rad=i%2===0?r:r*0.45;ctx.lineTo(cx+Math.cos(a)*rad,cy+Math.sin(a)*rad)}ctx.closePath()}
function drawShape(s){ctx.save();if(s.pop>0){ctx.globalAlpha=s.pop;const sc=1+(1-s.pop)*0.5;ctx.translate(s.x,s.y);ctx.scale(sc,sc);ctx.translate(-s.x,-s.y)}
const sx=s.x+(s.idx===shakeShape?Math.sin(shakeTick*3)*4:0);
ctx.fillStyle=s.clr;ctx.strokeStyle='#fff3';ctx.lineWidth=2;
if(s.type==='circle'){ctx.beginPath();ctx.arc(sx,s.y,s.r,0,Math.PI*2);ctx.fill();ctx.stroke()}
else if(s.type==='square'){ctx.fillRect(sx-s.r,s.y-s.r,s.r*2,s.r*2);ctx.strokeRect(sx-s.r,s.y-s.r,s.r*2,s.r*2)}
else if(s.type==='star'){drawStar(sx,s.y,s.r,5);ctx.fill();ctx.stroke()}
else if(s.type==='triangle'){ctx.beginPath();ctx.moveTo(sx,s.y-s.r);ctx.lineTo(sx-s.r,s.y+s.r);ctx.lineTo(sx+s.r,s.y+s.r);ctx.closePath();ctx.fill();ctx.stroke()}
else if(s.type==='diamond'){ctx.beginPath();ctx.moveTo(sx,s.y-s.r);ctx.lineTo(sx+s.r*0.7,s.y);ctx.lineTo(sx,s.y+s.r);ctx.lineTo(sx-s.r*0.7,s.y);ctx.closePath();ctx.fill();ctx.stroke()}
ctx.restore()}
function initRound(){shapes=[];
const numShapes=Math.min(8+round,15);
const numColors=Math.min(2+Math.floor(round/2),RENK.length);
const colorPool=[];for(let i=0;i<numColors;i++)colorPool.push(RENK[i]);
const ti=Math.floor(Math.random()*colorPool.length);targetColor=colorPool[ti].hex;targetName=colorPool[ti].name;
const numTarget=2+Math.floor(Math.random()*3);totalTarget=numTarget;found=0;
for(let i=0;i<numShapes;i++){let clr;if(i<numTarget)clr=targetColor;else{let c;do{c=colorPool[Math.floor(Math.random()*colorPool.length)]}while(c.hex===targetColor);clr=c.hex}
let x,y,ok=false;while(!ok){x=60+Math.random()*(W-120);y=130+Math.random()*(H-220);
ok=shapes.every(s=>Math.hypot(s.x-x,s.y-y)>70)}
shapes.push({x,y,r:22+Math.random()*10,clr,type:SHAPE_TYPES[Math.floor(Math.random()*SHAPE_TYPES.length)],alive:true,pop:0,isTarget:clr===targetColor,idx:i})}
for(let i=shapes.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[shapes[i],shapes[j]]=[shapes[j],shapes[i]];shapes[i].idx=i;shapes[j].idx=j}
timer=maxTime;lastTime=performance.now()}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎨 Renk Avı 🎨',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Hedef renkteki şekillere dokun!',W/2,230);ctx.font='18px Segoe UI';ctx.fillStyle='#c4b5fd';ctx.fillText('Doğru renkleri hızlıca bul!',W/2,265);
roundRect(W/2-80,300,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);
roundRect(W/2-80,310,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,35);
ctx.textAlign='center';ctx.fillStyle=targetColor;ctx.font='bold 32px Segoe UI';ctx.fillText(targetName+'!',W/2,80);
const barW=300,barX=(W-barW)/2,barY=100;ctx.fillStyle='#1e1b4b';roundRect(barX,barY,barW,16,8);ctx.fill();
const pct=Math.max(0,timer/maxTime);ctx.fillStyle=pct>0.3?'#22c55e':'#ef4444';roundRect(barX,barY,barW*pct,16,8);ctx.fill();
ctx.fillStyle='#e9d5ff';ctx.font='14px Segoe UI';ctx.fillText(Math.ceil(timer)+'s',W/2,barY+34);
shapes.forEach(s=>{if(s.alive||s.pop>0)drawShape(s)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(ts){if(!ts)ts=performance.now();
const dt=(ts-lastTime)/1000;lastTime=ts;
if(state==='play'){timer-=dt;if(timer<=0){timer=0;round++;if(round>maxRound){state='win'}else{initRound()}}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
shapes.forEach(s=>{if(s.pop>0){s.pop-=0.03;if(s.pop<=0)s.pop=0}});
if(shakeTick>0)shakeTick--;else shakeShape=-1;
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';lastTime=performance.now();initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;state='play';lastTime=performance.now();initRound()}return}
for(let i=shapes.length-1;i>=0;i--){const s=shapes[i];if(!s.alive)continue;
if(Math.hypot(mx-s.x,my-s.y)<s.r+10){
if(s.isTarget){s.alive=false;s.pop=1;score+=5;found++;addP(s.x,s.y,targetColor);snd(true);
if(found>=totalTarget){score+=5;round++;if(round>maxRound){state='win'}else{setTimeout(()=>initRound(),500)}}}
else{snd(false);timer=Math.max(0,timer-1);shakeShape=s.idx;shakeTick=15}
return}}});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
requestAnimationFrame(update);
</script></body></html>"""


def _build_prek_ab_sekil_yerlestir_html():
    """Şekil Yerleştir — Tangram tarzı şekil yerleştirme."""
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
let state='start',round=1,maxRound=10,score=0,particles=[];
let pieces=[],slots=[],dragging=null,dragOX=0,dragOY=0,placedCount=0,totalSlots=0;
const COLORS=['#ef4444','#3b82f6','#22c55e','#eab308','#a855f7','#ec4899','#f97316'];
const PUZZLES=[
{name:'Ev',slots:[{type:'square',x:0,y:20,w:80,h:70},{type:'triangle',x:0,y:-30,w:80,h:50}],pc:2},
{name:'Tekne',slots:[{type:'trapezoid',x:0,y:20,w:100,h:40},{type:'triangle',x:-20,y:-20,w:30,h:40},{type:'rect',x:20,y:-20,w:10,h:40}],pc:3},
{name:'Ağaç',slots:[{type:'triangle',x:0,y:-30,w:70,h:60},{type:'rect',x:0,y:30,w:20,h:40}],pc:2},
{name:'Araba',slots:[{type:'rect',x:0,y:0,w:100,h:40},{type:'circle',x:-30,y:30,r:15},{type:'circle',x:30,y:30,r:15}],pc:3},
{name:'Roket',slots:[{type:'triangle',x:0,y:-50,w:40,h:40},{type:'rect',x:0,y:0,w:40,h:60},{type:'triangle',x:-30,y:40,w:20,h:25},{type:'triangle',x:30,y:40,w:20,h:25}],pc:4},
{name:'Balık',slots:[{type:'ellipse',x:0,y:0,w:70,h:35},{type:'triangle',x:-55,y:0,w:35,h:40},{type:'circle',x:25,y:-8,r:6}],pc:3},
{name:'Yıldız',slots:[{type:'triangle',x:0,y:-30,w:50,h:30},{type:'triangle_inv',x:0,y:10,w:50,h:30},{type:'diamond',x:0,y:-10,w:20,h:40}],pc:3},
{name:'Kale',slots:[{type:'rect',x:0,y:10,w:80,h:50},{type:'square',x:-25,y:-25,w:20,h:20},{type:'square',x:25,y:-25,w:20,h:20},{type:'rect',x:0,y:-25,w:15,h:20}],pc:4},
{name:'Uçak',slots:[{type:'rect',x:0,y:0,w:80,h:20},{type:'triangle',x:45,y:0,w:20,h:20},{type:'rect',x:0,y:-15,w:50,h:8},{type:'triangle',x:-10,y:15,w:15,h:12},{type:'triangle',x:10,y:15,w:15,h:12}],pc:5},
{name:'Kelebek',slots:[{type:'ellipse',x:-25,y:-15,w:30,h:25},{type:'ellipse',x:25,y:-15,w:30,h:25},{type:'ellipse',x:-20,y:15,w:25,h:20},{type:'ellipse',x:20,y:15,w:25,h:20},{type:'rect',x:0,y:0,w:6,h:40}],pc:5}
];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function drawSlotShape(s,cx,cy,filled,clr){ctx.save();ctx.translate(cx,cy);
if(s.type==='square'){ctx.beginPath();ctx.rect(-s.w/2,-s.h/2,s.w,s.h);if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
else if(s.type==='rect'){ctx.beginPath();ctx.rect(-s.w/2,-s.h/2,s.w,s.h);if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
else if(s.type==='triangle'){ctx.beginPath();ctx.moveTo(0,-s.h/2);ctx.lineTo(-s.w/2,s.h/2);ctx.lineTo(s.w/2,s.h/2);ctx.closePath();if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
else if(s.type==='triangle_inv'){ctx.beginPath();ctx.moveTo(0,s.h/2);ctx.lineTo(-s.w/2,-s.h/2);ctx.lineTo(s.w/2,-s.h/2);ctx.closePath();if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
else if(s.type==='circle'){ctx.beginPath();ctx.arc(0,0,s.r,0,Math.PI*2);if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
else if(s.type==='ellipse'){ctx.beginPath();ctx.ellipse(0,0,s.w/2,s.h/2,0,0,Math.PI*2);if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
else if(s.type==='trapezoid'){ctx.beginPath();ctx.moveTo(-s.w/2,s.h/2);ctx.lineTo(-s.w/3,-s.h/2);ctx.lineTo(s.w/3,-s.h/2);ctx.lineTo(s.w/2,s.h/2);ctx.closePath();if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
else if(s.type==='diamond'){ctx.beginPath();ctx.moveTo(0,-s.h/2);ctx.lineTo(s.w/2,0);ctx.lineTo(0,s.h/2);ctx.lineTo(-s.w/2,0);ctx.closePath();if(filled){ctx.fillStyle=clr;ctx.fill()}ctx.strokeStyle=filled?'#fff6':'#818cf880';ctx.lineWidth=filled?1:2;ctx.setLineDash(filled?[]:[6,4]);ctx.stroke();ctx.setLineDash([])}
ctx.restore()}
function hitSlotShape(s,cx,cy,mx,my){const dx=mx-cx,dy=my-cy;
if(s.type==='circle')return Math.hypot(dx,dy)<=s.r+5;
if(s.type==='ellipse')return(dx*dx)/((s.w/2+5)*(s.w/2+5))+(dy*dy)/((s.h/2+5)*(s.h/2+5))<=1;
const hw=(s.w||s.r*2||40)/2+5,hh=(s.h||s.r*2||40)/2+5;return Math.abs(dx)<=hw&&Math.abs(dy)<=hh}
function initRound(){const pz=PUZZLES[(round-1)%PUZZLES.length];
const centerX=W/2,centerY=H/2-20;
slots=pz.slots.map((s,i)=>({...s,cx:centerX+s.x,cy:centerY+s.y,filled:false,idx:i}));
totalSlots=slots.length;placedCount=0;
pieces=[];const margin=60;const spacing=Math.min(120,(W-margin*2)/totalSlots);
const startX=margin+(W-margin*2-spacing*(totalSlots-1))/2;
for(let i=0;i<totalSlots;i++){const s=pz.slots[i];
pieces.push({slot:s,idx:i,x:startX+i*spacing,y:H-90,origX:startX+i*spacing,origY:H-90,placed:false,clr:COLORS[i%COLORS.length],glow:0})}
dragging=null}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🧩 Şekil Yerleştir 🧩',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Şekilleri doğru yere sürükle!',W/2,230);ctx.font='18px Segoe UI';ctx.fillStyle='#c4b5fd';ctx.fillText('Parçaları çerçeveye yerleştir',W/2,265);
roundRect(W/2-80,300,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);
roundRect(W/2-80,310,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxRound,20,35);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,35);
const pz=PUZZLES[(round-1)%PUZZLES.length];ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.fillText(pz.name,W/2,70);
ctx.strokeStyle='#818cf840';ctx.lineWidth=2;roundRect(W/2-120,H/2-120,240,220,16);ctx.stroke();
slots.forEach(s=>{if(s.filled){const p=pieces.find(pp=>pp.idx===s.idx);if(p)drawSlotShape(s,s.cx,s.cy,true,p.clr)}else{drawSlotShape(s,s.cx,s.cy,false,null)}});
pieces.forEach(p=>{if(!p.placed){ctx.save();if(p.glow>0){ctx.shadowColor='#fbbf24';ctx.shadowBlur=p.glow*15}
drawSlotShape(p.slot,p.x,p.y,true,p.clr);ctx.restore()}});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
pieces.forEach(p=>{if(p.glow>0)p.glow=Math.max(0,p.glow-0.02)});
draw();requestAnimationFrame(update)}
function getMousePos(e){const rect=canvas.getBoundingClientRect();return{x:(e.clientX-rect.left)*(W/rect.width),y:(e.clientY-rect.top)*(H/rect.height)}}
canvas.addEventListener('mousedown',e=>{const{x:mx,y:my}=getMousePos(e);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;state='play';initRound()}return}
for(let i=pieces.length-1;i>=0;i--){const p=pieces[i];if(!p.placed&&hitSlotShape(p.slot,p.x,p.y,mx,my)){dragging=p;dragOX=mx-p.x;dragOY=my-p.y;break}}});
canvas.addEventListener('mousemove',e=>{if(!dragging)return;const{x:mx,y:my}=getMousePos(e);dragging.x=mx-dragOX;dragging.y=my-dragOY});
canvas.addEventListener('mouseup',e=>{if(!dragging)return;
const p=dragging;dragging=null;
const target=slots[p.idx];const dist=Math.hypot(p.x-target.cx,p.y-target.cy);
if(dist<35){p.x=target.cx;p.y=target.cy;p.placed=true;target.filled=true;placedCount++;score+=10;
addP(target.cx,target.cy,p.clr);snd(true);
if(placedCount>=totalSlots){round++;if(round>maxRound){setTimeout(()=>{state='win'},500)}else{setTimeout(()=>initRound(),800)}}}
else{snd(false);p.x=p.origX;p.y=p.origY;p.glow=1}});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
const mev=new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY});canvas.dispatchEvent(mev)},{passive:false});
canvas.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];
const mev=new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY});canvas.dispatchEvent(mev)},{passive:false});
canvas.addEventListener('touchend',e=>{e.preventDefault();canvas.dispatchEvent(new MouseEvent('mouseup',{}))},{passive:false});
update();
</script></body></html>"""


def _build_prek_ab_farklari_bul_html():
    """Farkları Bul — İki sahne arasındaki 3 farkı bul."""
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
let state='start',round=1,maxRound=10,score=0,particles=[];
let diffs=[],foundDiffs=[],timer=15,lastTime=0,bonusAwarded=false;
const SW=310,SH=420,LX=15,RX=W-SW-15,SY=100;
const SCENES=[
{name:'Bahçe',draw:function(ox,oy,mods){
ctx.fillStyle='#87ceeb';ctx.fillRect(ox,oy,SW,SH);ctx.fillStyle='#228b22';ctx.fillRect(ox,oy+SH-80,SW,80);
ctx.fillStyle=mods[0]?'#ff6347':'#ffd700';ctx.beginPath();ctx.arc(ox+SW-50,oy+50,30,0,Math.PI*2);ctx.fill();
for(let i=0;i<5;i++){const bx=ox+30+i*65;ctx.fillStyle='#8b4513';ctx.fillRect(bx+8,oy+SH-130,8,50);
ctx.fillStyle=mods[1]&&i===2?'#ff69b4':'#228b22';ctx.beginPath();ctx.arc(bx+12,oy+SH-140,25,0,Math.PI*2);ctx.fill()}
if(!mods[2]){ctx.fillStyle='#ff4500';ctx.beginPath();ctx.arc(ox+160,oy+SH-40,12,0,Math.PI*2);ctx.fill();ctx.fillStyle='#228b22';ctx.fillRect(ox+157,oy+SH-60,6,10)}
ctx.fillStyle='#deb887';ctx.fillRect(ox+80,oy+SH-180,100,100);ctx.fillStyle='#a0522d';ctx.beginPath();ctx.moveTo(ox+70,oy+SH-180);ctx.lineTo(ox+130,oy+SH-240);ctx.lineTo(ox+190,oy+SH-180);ctx.fill();
ctx.fillStyle='#87ceeb';ctx.fillRect(ox+110,oy+SH-155,30,30);ctx.fillStyle='#8b4513';ctx.fillRect(ox+120,oy+SH-105,20,25)}},
{name:'Oda',draw:function(ox,oy,mods){
ctx.fillStyle='#f5deb3';ctx.fillRect(ox,oy,SW,SH);ctx.fillStyle='#deb887';ctx.fillRect(ox,oy+SH-50,SW,50);
ctx.fillStyle=mods[0]?'#4169e1':'#ff6347';ctx.fillRect(ox+20,oy+SH-200,120,150);
ctx.fillStyle='#8b4513';ctx.fillRect(ox+200,oy+SH-280,90,230);
for(let i=0;i<3;i++){ctx.fillStyle='#a0522d';ctx.fillRect(ox+205,oy+SH-270+i*75,80,5)}
ctx.fillStyle=mods[1]?'#ffd700':'#c0c0c0';ctx.beginPath();ctx.arc(ox+SW/2,oy+60,35,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#888';ctx.lineWidth=2;ctx.stroke();
if(!mods[2]){ctx.fillStyle='#ff69b4';const px=ox+170,py=oy+SH-120;ctx.beginPath();ctx.arc(px,py,15,0,Math.PI*2);ctx.fill();ctx.fillStyle='#228b22';ctx.fillRect(px-2,py+12,4,15)}}},
{name:'Park',draw:function(ox,oy,mods){
ctx.fillStyle='#87ceeb';ctx.fillRect(ox,oy,SW,SH);ctx.fillStyle='#90ee90';ctx.fillRect(ox,oy+SH-100,SW,100);
ctx.fillStyle='#8b4513';ctx.fillRect(ox+130,oy+SH-220,15,120);ctx.fillStyle='#228b22';ctx.beginPath();ctx.arc(ox+137,oy+SH-230,mods[0]?50:40,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#4682b4';ctx.beginPath();ctx.ellipse(ox+SW/2,oy+SH-50,60,25,0,0,Math.PI*2);ctx.fill();
if(!mods[1]){ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(ox+80,oy+70,25,12,0.3,0,Math.PI*2);ctx.fill()}
ctx.fillStyle=mods[2]?'#ff4500':'#ffd700';ctx.beginPath();ctx.arc(ox+50,oy+50,22,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#8b4513';ctx.fillRect(ox+40,oy+SH-140,8,40);ctx.fillRect(ox+80,oy+SH-140,8,40);ctx.fillStyle='#ff6347';ctx.fillRect(ox+30,oy+SH-150,70,15)}},
{name:'Deniz',draw:function(ox,oy,mods){
ctx.fillStyle='#87ceeb';ctx.fillRect(ox,oy,SW,SH/2);ctx.fillStyle='#4169e1';ctx.fillRect(ox,oy+SH/2,SW,SH/2);
ctx.fillStyle=mods[0]?'#ffa500':'#ffd700';ctx.beginPath();ctx.arc(ox+SW-60,oy+50,28,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#deb887';ctx.fillRect(ox,oy+SH-60,SW,60);
ctx.fillStyle='#8b4513';ctx.beginPath();ctx.moveTo(ox+80,oy+SH/2+20);ctx.lineTo(ox+80,oy+SH/2-60);ctx.lineTo(ox+130,oy+SH/2-30);ctx.closePath();ctx.fill();
ctx.fillStyle='#fff';ctx.beginPath();ctx.moveTo(ox+80,oy+SH/2-55);ctx.lineTo(ox+80,oy+SH/2+10);ctx.lineTo(ox+125,oy+SH/2-25);ctx.closePath();ctx.fill();
if(!mods[1]){ctx.fillStyle='#ff6347';const sx=ox+200;ctx.beginPath();ctx.moveTo(sx,oy+SH-70);ctx.lineTo(sx-15,oy+SH-40);ctx.lineTo(sx+15,oy+SH-40);ctx.closePath();ctx.fill()}
for(let i=0;i<3;i++){ctx.fillStyle=mods[2]&&i===1?'#90ee90':'#fff';ctx.beginPath();ctx.ellipse(ox+60+i*80,oy+40,20,8,0.2*i,0,Math.PI*2);ctx.fill()}}},
{name:'Mutfak',draw:function(ox,oy,mods){
ctx.fillStyle='#fffacd';ctx.fillRect(ox,oy,SW,SH);ctx.fillStyle='#deb887';ctx.fillRect(ox,oy+SH-40,SW,40);
ctx.fillStyle='#a0522d';ctx.fillRect(ox+20,oy+SH-200,SW-40,160);ctx.fillStyle='#8b4513';ctx.fillRect(ox+20,oy+SH-205,SW-40,8);
ctx.fillStyle=mods[0]?'#ff4500':'#3b82f6';ctx.beginPath();ctx.arc(ox+100,oy+SH-130,20,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#c0c0c0';ctx.fillRect(ox+180,oy+SH-180,60,80);ctx.fillStyle='#888';ctx.fillRect(ox+195,oy+SH-165,30,20);
if(!mods[1]){ctx.fillStyle='#ffd700';ctx.beginPath();ctx.arc(ox+60,oy+SH-240,15,0,Math.PI*2);ctx.fill();ctx.fillStyle='#228b22';ctx.fillRect(ox+57,oy+SH-270,6,18)}
ctx.fillStyle=mods[2]?'#ff69b4':'#9370db';for(let i=0;i<3;i++){ctx.fillRect(ox+50+i*70,oy+30,40,50)}}},
{name:'Oyun Alanı',draw:function(ox,oy,mods){
ctx.fillStyle='#87ceeb';ctx.fillRect(ox,oy,SW,SH*0.6);ctx.fillStyle='#90ee90';ctx.fillRect(ox,oy+SH*0.6,SW,SH*0.4);
ctx.fillStyle='#ff4500';ctx.fillRect(ox+50,oy+SH*0.6-100,10,100);ctx.fillRect(ox+150,oy+SH*0.6-100,10,100);
ctx.fillStyle=mods[0]?'#ffd700':'#ff4500';ctx.beginPath();ctx.moveTo(ox+40,oy+SH*0.6-100);ctx.lineTo(ox+105,oy+SH*0.6-140);ctx.lineTo(ox+170,oy+SH*0.6-100);ctx.closePath();ctx.fill();
ctx.strokeStyle='#8b4513';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(ox+220,oy+SH*0.6-80);ctx.quadraticCurveTo(ox+250,oy+SH*0.6-120,ox+280,oy+SH*0.6-80);ctx.stroke();
if(!mods[1]){ctx.fillStyle='#ff6347';ctx.beginPath();ctx.arc(ox+250,oy+SH*0.6+30,12,0,Math.PI*2);ctx.fill()}
ctx.fillStyle=mods[2]?'#4169e1':'#228b22';ctx.beginPath();ctx.arc(ox+80,oy+SH*0.6+40,18,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#ffd700';ctx.beginPath();ctx.arc(ox+SW-40,oy+40,25,0,Math.PI*2);ctx.fill()}},
{name:'Sınıf',draw:function(ox,oy,mods){
ctx.fillStyle='#f0f0f0';ctx.fillRect(ox,oy,SW,SH);ctx.fillStyle='#2d5016';ctx.fillRect(ox+30,oy+40,SW-60,120);
ctx.fillStyle='#fff';ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText('ABC',ox+SW/2,oy+110);
ctx.fillStyle=mods[0]?'#ff4500':'#4169e1';ctx.fillRect(ox+50,oy+200,80,60);ctx.fillRect(ox+170,oy+200,80,60);
if(!mods[1]){ctx.fillStyle='#ffd700';ctx.beginPath();const bx=ox+SW-40,by=oy+SH-60;ctx.moveTo(bx,by-15);for(let i=0;i<5;i++){const a=i*Math.PI*2/5-Math.PI/2;ctx.lineTo(bx+Math.cos(a)*15,by+Math.sin(a)*15);const a2=a+Math.PI/5;ctx.lineTo(bx+Math.cos(a2)*7,by+Math.sin(a2)*7)}ctx.fill()}
ctx.fillStyle=mods[2]?'#ff69b4':'#ffa500';ctx.beginPath();ctx.arc(ox+SW/2,oy+SH-80,20,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#8b4513';ctx.fillRect(ox+40,oy+SH-40,SW-80,8)}},
{name:'Çiftlik',draw:function(ox,oy,mods){
ctx.fillStyle='#87ceeb';ctx.fillRect(ox,oy,SW,SH*0.5);ctx.fillStyle='#90ee90';ctx.fillRect(ox,oy+SH*0.5,SW,SH*0.5);
ctx.fillStyle='#8b0000';ctx.fillRect(ox+100,oy+SH*0.5-120,110,120);ctx.fillStyle=mods[0]?'#ffd700':'#8b0000';ctx.beginPath();ctx.moveTo(ox+95,oy+SH*0.5-120);ctx.lineTo(ox+155,oy+SH*0.5-170);ctx.lineTo(ox+215,oy+SH*0.5-120);ctx.closePath();ctx.fill();
ctx.fillStyle='#fff';for(let i=0;i<2;i++){ctx.beginPath();ctx.ellipse(ox+50+i*20,oy+SH*0.5+40,12,10,0,0,Math.PI*2);ctx.fill()}
if(!mods[1]){ctx.fillStyle='#ffa500';ctx.beginPath();ctx.ellipse(ox+250,oy+SH*0.5+30,10,12,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#ff4500';ctx.beginPath();ctx.moveTo(ox+248,oy+SH*0.5+15);ctx.lineTo(ox+252,oy+SH*0.5+15);ctx.lineTo(ox+255,oy+SH*0.5+10);ctx.lineTo(ox+245,oy+SH*0.5+10);ctx.fill()}
ctx.fillStyle=mods[2]?'#ffd700':'#fff';ctx.beginPath();ctx.arc(ox+SW-60,oy+40,20,0,Math.PI*2);ctx.fill()}},
{name:'Plaj',draw:function(ox,oy,mods){
ctx.fillStyle='#87ceeb';ctx.fillRect(ox,oy,SW,SH*0.4);ctx.fillStyle='#4169e1';ctx.fillRect(ox,oy+SH*0.4,SW,SH*0.25);ctx.fillStyle='#f4a460';ctx.fillRect(ox,oy+SH*0.65,SW,SH*0.35);
ctx.fillStyle=mods[0]?'#ff6347':'#ffd700';ctx.beginPath();ctx.arc(ox+50,oy+40,25,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#ff4500';ctx.beginPath();ctx.moveTo(ox+SW/2,oy+SH*0.65+10);ctx.lineTo(ox+SW/2-40,oy+SH*0.65+60);ctx.lineTo(ox+SW/2+40,oy+SH*0.65+60);ctx.closePath();ctx.fill();
ctx.fillStyle='#8b4513';ctx.fillRect(ox+SW/2-3,oy+SH*0.65+10,6,80);
if(!mods[1]){ctx.fillStyle='#ff69b4';ctx.beginPath();ctx.ellipse(ox+80,oy+SH*0.65+40,18,10,0.3,0,Math.PI*2);ctx.fill()}
ctx.fillStyle=mods[2]?'#00ff00':'#fff';for(let i=0;i<2;i++){ctx.beginPath();ctx.ellipse(ox+180+i*40,oy+30,22,10,0.1,0,Math.PI*2);ctx.fill()}}},
{name:'Uzay',draw:function(ox,oy,mods){
ctx.fillStyle='#0B0F19';ctx.fillRect(ox,oy,SW,SH);
for(let i=0;i<20;i++){ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(ox+((i*73+17)%SW),oy+((i*47+23)%SH),1+i%2,0,Math.PI*2);ctx.fill()}
ctx.fillStyle=mods[0]?'#c0c0c0':'#ffd700';ctx.beginPath();ctx.arc(ox+SW*0.7,oy+80,35,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#c0c0c0';ctx.beginPath();ctx.arc(ox+SW*0.7-10,oy+75,5,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(ox+SW*0.7+12,oy+90,7,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#ff4500';const rx=ox+100,ry=oy+SH/2;ctx.beginPath();ctx.moveTo(rx,ry-40);ctx.lineTo(rx-20,ry+30);ctx.lineTo(rx+20,ry+30);ctx.closePath();ctx.fill();ctx.fillStyle='#c0c0c0';ctx.fillRect(rx-15,ry-10,30,40);
if(!mods[1]){ctx.fillStyle='#4169e1';ctx.beginPath();ctx.arc(ox+220,oy+SH*0.6,18,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#87ceeb';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(ox+220,oy+SH*0.6,28,10,0.3,0,Math.PI*2);ctx.stroke()}
ctx.fillStyle=mods[2]?'#ff69b4':'#00ff00';ctx.beginPath();const sx=ox+60,sy=oy+SH-80;ctx.moveTo(sx,sy-12);for(let i=0;i<5;i++){const a=i*Math.PI*2/5-Math.PI/2;ctx.lineTo(sx+Math.cos(a)*12,sy+Math.sin(a)*12);const a2=a+Math.PI/5;ctx.lineTo(sx+Math.cos(a2)*5,sy+Math.sin(a2)*5)}ctx.fill()}}
];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function initRound(){const si=(round-1)%SCENES.length;
diffs=[
{lx:0,ly:0,rx:0,ry:0,desc:'color',found:false},
{lx:0,ly:0,rx:0,ry:0,desc:'missing',found:false},
{lx:0,ly:0,rx:0,ry:0,desc:'change',found:false}
];
foundDiffs=[];timer=15;bonusAwarded=false;lastTime=performance.now();
const scene=SCENES[si];
const regions=getDiffRegions(si);
for(let i=0;i<3;i++){diffs[i].lx=LX+regions[i].x;diffs[i].ly=SY+regions[i].y;
diffs[i].rx=RX+regions[i].x;diffs[i].ry=SY+regions[i].y;diffs[i].radius=regions[i].r||25}}
function getDiffRegions(si){
const R=[
[{x:SW-50,y:50,r:35},{x:SW/2,y:SH-140,r:30},{x:160,y:SH-40,r:20}],
[{x:80,y:SH-130,r:30},{x:SW/2,y:60,r:40},{x:170,y:SH-120,r:20}],
[{x:137,y:SH-230,r:55},{x:80,y:70,r:30},{x:50,y:50,r:28}],
[{x:SW-60,y:50,r:32},{x:200,y:SH-55,r:20},{x:140,y:40,r:25}],
[{x:100,y:SH-130,r:25},{x:60,y:SH-240,r:20},{x:SW/2,y:30,r:45}],
[{x:105,y:SH*0.6-120,r:40},{x:250,y:SH*0.6+30,r:18},{x:80,y:SH*0.6+40,r:22}],
[{x:80,y:200,r:40},{x:SW-40,y:SH-60,r:20},{x:SW/2,y:SH-80,r:25}],
[{x:155,y:SH*0.5-145,r:40},{x:250,y:SH*0.5+25,r:18},{x:SW-60,y:40,r:25}],
[{x:50,y:40,r:30},{x:80,y:SH*0.65+40,r:22},{x:200,y:30,r:28}],
[{x:SW*0.7,y:80,r:40},{x:220,y:SH*0.6,r:32},{x:60,y:SH-80,r:18}]
];
return R[si%R.length]}
function drawScenes(){const si=(round-1)%SCENES.length;const scene=SCENES[si];
ctx.save();ctx.beginPath();ctx.rect(LX,SY,SW,SH);ctx.clip();scene.draw(LX,SY,[false,false,false]);ctx.restore();
ctx.save();ctx.beginPath();ctx.rect(RX,SY,SW,SH);ctx.clip();scene.draw(RX,SY,[true,true,true]);ctx.restore();
ctx.strokeStyle='#818cf8';ctx.lineWidth=2;ctx.strokeRect(LX,SY,SW,SH);ctx.strokeRect(RX,SY,SW,SH)}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🔍 Farkları Bul 🔍',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('İki resim arasındaki 3 farkı bul!',W/2,230);ctx.font='18px Segoe UI';ctx.fillStyle='#c4b5fd';ctx.fillText('Farklı yere tıkla, hızlı ol!',W/2,265);
roundRect(W/2-80,300,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);
roundRect(W/2-80,310,160,50,12);ctx.fillStyle='#a78bfa';ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,340);return}
drawScenes();
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxRound,20,30);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';
const fc=diffs.filter(d=>d.found).length;ctx.fillText('Fark: '+fc+'/3',W/2,30);
const barW=200,barX=(W-barW)/2,barY=SY+SH+15;ctx.fillStyle='#1e1b4b';roundRect(barX,barY,barW,14,7);ctx.fill();
const pct=Math.max(0,timer/15);ctx.fillStyle=pct>0.3?'#22c55e':'#ef4444';roundRect(barX,barY,barW*pct,14,7);ctx.fill();
ctx.fillStyle='#e9d5ff';ctx.font='14px Segoe UI';ctx.fillText(Math.ceil(timer)+'s',W/2,barY+32);
diffs.forEach(d=>{if(d.found){ctx.strokeStyle='#4ade80';ctx.lineWidth=3;ctx.beginPath();ctx.arc(d.lx,d.ly,d.radius,0,Math.PI*2);ctx.stroke();
ctx.beginPath();ctx.arc(d.rx,d.ry,d.radius,0,Math.PI*2);ctx.stroke()}});
ctx.fillStyle='#c4b5fd';ctx.font='14px Segoe UI';ctx.textAlign='center';ctx.fillText('Orijinal',LX+SW/2,SY-8);ctx.fillText('Farklı',RX+SW/2,SY-8);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(ts){if(!ts)ts=performance.now();
const dt=(ts-lastTime)/1000;lastTime=ts;
if(state==='play'){timer-=dt;if(timer<=0){timer=0;round++;if(round>maxRound){state='win'}else{initRound()}}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',e=>{const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';lastTime=performance.now();initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){round=1;score=0;state='play';lastTime=performance.now();initRound()}return}
for(let i=0;i<diffs.length;i++){const d=diffs[i];if(d.found)continue;
const hitL=Math.hypot(mx-d.lx,my-d.ly)<d.radius+10;const hitR=Math.hypot(mx-d.rx,my-d.ry)<d.radius+10;
if(hitL||hitR){d.found=true;score+=10;addP(d.lx,d.ly,'#4ade80');addP(d.rx,d.ry,'#4ade80');snd(true);
if(timer>10&&!bonusAwarded){score+=5;bonusAwarded=true}
if(diffs.every(dd=>dd.found)){round++;if(round>maxRound){setTimeout(()=>{state='win'},500)}else{setTimeout(()=>initRound(),800)}}
return}}
snd(false)});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
requestAnimationFrame(update);
</script></body></html>"""
