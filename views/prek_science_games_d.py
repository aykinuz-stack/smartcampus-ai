# -*- coding: utf-8 -*-
"""Okul Öncesi Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm D: 16-20)."""


def _build_prek_sci_vucudum_puzzle_html():
    """Vücudum Puzzle — Organları doğru yere sürükle."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
const ALL_ORGANS=[
{emoji:'🧠',name:'Beyin',info:'Düşünmeyi sağlar',tx:0,ty:-0.38,clr:'#f472b6'},
{emoji:'👁️',name:'Göz',info:'Görmeyi sağlar',tx:-0.08,ty:-0.28,clr:'#60a5fa'},
{emoji:'❤️',name:'Kalp',info:'Kanı pompalar',tx:0.06,ty:-0.08,clr:'#ff6b9d'},
{emoji:'🫁',name:'Akciğer',info:'Nefes almayı sağlar',tx:-0.06,ty:-0.05,clr:'#34d399'},
{emoji:'🟤',name:'Mide',info:'Yiyecekleri sindirir',tx:0,ty:0.1,clr:'#fb923c'}
];
let organs=[],targets=[],dragging=null,dox=0,doy=0,round=1,maxR=10,score=0,state='start',particles=[],labels=[],bodyX,bodyY,bodyScale;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function drawBody(cx,cy,sc){
ctx.save();ctx.translate(cx,cy);ctx.scale(sc,sc);
ctx.strokeStyle='#c084fc';ctx.lineWidth=3;ctx.fillStyle='#1e1b4b80';
ctx.beginPath();ctx.ellipse(0,-120,35,40,0,0,Math.PI*2);ctx.fill();ctx.stroke();
ctx.beginPath();ctx.moveTo(-25,-82);ctx.lineTo(-45,-20);ctx.lineTo(-35,80);ctx.lineTo(35,80);ctx.lineTo(45,-20);ctx.lineTo(25,-82);ctx.closePath();ctx.fill();ctx.stroke();
ctx.beginPath();ctx.moveTo(-45,-20);ctx.lineTo(-80,-60);ctx.moveTo(45,-20);ctx.lineTo(80,-60);ctx.stroke();
ctx.beginPath();ctx.moveTo(-20,80);ctx.lineTo(-25,160);ctx.moveTo(20,80);ctx.lineTo(25,160);ctx.stroke();
ctx.restore()}
function setup(){
bodyX=W/2;bodyY=310;bodyScale=round<=3?1.4:round<=7?1.2:1.0;
const snap=round<=3?50:round<=7?40:30;
const cnt=round<=3?Math.min(2+Math.floor((round-1)/1),3):round<=7?4:5;
const pool=[...ALL_ORGANS].slice(0,cnt);
targets=pool.map(o=>({...o,x:bodyX+o.tx*200*bodyScale,y:bodyY+o.ty*200*bodyScale,matched:false,snap}));
organs=pool.map((o,i)=>{
const side=i%2===0?1:-1;
const sx=bodyX+side*(180+Math.random()*80);
const sy=120+Math.random()*(H-280);
return{...o,x:sx,y:sy,ox:sx,oy:sy,matched:false}});
labels=[]}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🫀 Vücudum Puzzle',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Organları vücutta doğru yere koy!',W/2,230);ctx.font='60px Segoe UI';ctx.fillText('🧒',W/2,330);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,380,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,412);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Vücut Uzmanı! 🎉',W/2,180);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,230);ctx.font='50px Segoe UI';ctx.fillText('🏆',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,382);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
drawBody(bodyX,bodyY,bodyScale);
targets.forEach(t=>{if(!t.matched){ctx.strokeStyle=t.clr+'80';ctx.lineWidth=2;ctx.setLineDash([6,4]);ctx.beginPath();ctx.arc(t.x,t.y,t.snap*0.7,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle=t.clr+'40';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText(t.name+'?',t.x,t.y+t.snap*0.7+14)}});
organs.forEach(o=>{if(!o.matched){ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(o.emoji,o.x,o.y);ctx.textBaseline='alphabetic';ctx.fillStyle='#e9d5ff';ctx.font='bold 11px Segoe UI';ctx.fillText(o.name,o.x,o.y+26)}else{ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';const glow=ctx.createRadialGradient(o.x,o.y,5,o.x,o.y,30);glow.addColorStop(0,o.clr+'60');glow.addColorStop(1,o.clr+'00');ctx.fillStyle=glow;ctx.beginPath();ctx.arc(o.x,o.y,30,0,Math.PI*2);ctx.fill();ctx.fillText(o.emoji,o.x,o.y);ctx.textBaseline='alphabetic'}});
labels.forEach(l=>{ctx.globalAlpha=Math.min(1,l.life);ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.fillText(l.name+' — '+l.info,l.x,l.y-30);ctx.globalAlpha=1});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);
labels.forEach(l=>l.life-=0.005);labels=labels.filter(l=>l.life>0);
draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play')return;
for(let i=organs.length-1;i>=0;i--){if(!organs[i].matched&&Math.hypot(m.x-organs[i].x,m.y-organs[i].y)<30){dragging=organs[i];dox=m.x-organs[i].x;doy=m.y-organs[i].y;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);dragging.x=m.x-dox;dragging.y=m.y-doy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;
let placed=false;
targets.forEach(t=>{if(!t.matched&&t.name===dragging.name&&Math.hypot(dragging.x-t.x,dragging.y-t.y)<t.snap){
t.matched=true;dragging.matched=true;dragging.x=t.x;dragging.y=t.y;score+=10;snd(true);addP(t.x,t.y,t.clr);
labels.push({x:t.x,y:t.y,name:t.name,info:t.info,life:3});placed=true;
if(targets.every(tt=>tt.matched)){round++;if(round>maxR){setTimeout(()=>{state='win'},500)}else{setTimeout(setup,800)}}}});
if(!placed){snd(false);dragging.x=dragging.ox;dragging.y=dragging.oy}
dragging=null});
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>380&&m.y<430){state='play';score=0;round=1;setup()}}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;setup()}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_sci_isik_kaynagi_html():
    """Işık Kaynağı Bul — Işık kaynaklarını seç."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
const LIGHT=[
{emoji:'☀️',name:'Güneş'},{emoji:'💡',name:'Lamba'},{emoji:'🕯️',name:'Mum'},
{emoji:'🔦',name:'Fener'},{emoji:'⭐',name:'Yıldız'},{emoji:'🪲',name:'Ateş Böceği'},
{emoji:'🔥',name:'Ateş'},{emoji:'📱',name:'Telefon Ekranı'},{emoji:'💻',name:'Bilgisayar'}
];
const NOTLIGHT=[
{emoji:'🌙',name:'Ay (yansıtır)'},{emoji:'🪞',name:'Ayna'},{emoji:'👓',name:'Gözlük'},
{emoji:'🪟',name:'Pencere'},{emoji:'💧',name:'Su'},{emoji:'📕',name:'Kitap'},
{emoji:'🪨',name:'Taş'},{emoji:'🧊',name:'Buz'},{emoji:'🥄',name:'Kaşık'}
];
let cards=[],selected=new Set(),round=1,maxR=10,score=0,state='start',particles=[],feedback=[],feedTimer=0,checked=false;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:clr||'#fbbf24',r:3+Math.random()*3})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function setup(){selected.clear();checked=false;feedback=[];feedTimer=0;
const lightCnt=round<=3?2:round<=6?3:4;
const notCnt=round<=3?4:round<=6?5:5;
const totalCols=3;
const lights=shuffle([...LIGHT]).slice(0,lightCnt);
const nots=shuffle([...NOTLIGHT]).slice(0,notCnt);
const all=shuffle([...lights.map(l=>({...l,isLight:true})),...nots.map(n=>({...n,isLight:false}))]);
const rows=Math.ceil(all.length/totalCols);
const cw=180,ch=90,gap=15;
const startX=(W-totalCols*cw-(totalCols-1)*gap)/2;
const startY=110;
cards=all.map((item,i)=>{
const col=i%totalCols,row=Math.floor(i/totalCols);
return{...item,x:startX+col*(cw+gap)+cw/2,y:startY+row*(ch+gap)+ch/2,w:cw,h:ch,idx:i}})}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#0d0221cc';ctx.fillRect(0,0,W,H);
ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('💡 Işık Kaynağı Bul',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Kendi ışığını üreten nesneleri seç!',W/2,225);ctx.font='50px Segoe UI';ctx.fillText('🔦',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,382);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Işık Uzmanı! 🎉',W/2,180);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,230);ctx.font='50px Segoe UI';ctx.fillText('🌟',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,382);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='16px Segoe UI';ctx.fillText('Işık kaynaklarını seç, sonra Kontrol Et!',W/2,56);
cards.forEach((c,i)=>{
let bg='#1e1b4b';let border='#a78bfa60';
if(selected.has(i)){bg='#312e81';border='#fbbf24'}
if(checked){
const fb=feedback.find(f=>f.idx===i);
if(fb){if(fb.type==='correct'){bg='#064e3b';border='#34d399'}
else if(fb.type==='wrong'){bg='#7f1d1d';border='#ef4444'}
else if(fb.type==='missed'){bg='#1e1b4b';border='#34d399';ctx.setLineDash([4,4])}}}
ctx.fillStyle=bg;ctx.strokeStyle=border;ctx.lineWidth=selected.has(i)?3:2;ctx.setLineDash(ctx.getLineDash()||[]);
ctx.beginPath();ctx.roundRect(c.x-c.w/2,c.y-c.h/2,c.w,c.h,10);ctx.fill();ctx.stroke();ctx.setLineDash([]);
if(selected.has(i)){
const glow=ctx.createRadialGradient(c.x,c.y,10,c.x,c.y,c.w/2);
glow.addColorStop(0,'#fbbf2420');glow.addColorStop(1,'#fbbf2400');
ctx.fillStyle=glow;ctx.beginPath();ctx.roundRect(c.x-c.w/2,c.y-c.h/2,c.w,c.h,10);ctx.fill()}
ctx.font='32px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(c.emoji,c.x,c.y-8);ctx.textBaseline='alphabetic';
ctx.fillStyle='#e9d5ff';ctx.font='bold 12px Segoe UI';ctx.fillText(c.name,c.x,c.y+30);
if(checked&&c.isLight){ctx.fillStyle='#fbbf24';ctx.font='12px Segoe UI';ctx.fillText('✨ Işık kaynağı',c.x,c.y+44)}});
if(!checked){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-70,H-70,140,45,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Kontrol Et!',W/2,H-42)}
else{ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-55,H-70,110,45,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Devam ➜',W/2,H-42)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function checkAnswers(){checked=true;feedback=[];let correct=0;
cards.forEach((c,i)=>{
if(c.isLight&&selected.has(i)){feedback.push({idx:i,type:'correct'});correct++;score+=10;addP(c.x,c.y,'#34d399')}
else if(!c.isLight&&selected.has(i)){feedback.push({idx:i,type:'wrong'})}
else if(c.isLight&&!selected.has(i)){feedback.push({idx:i,type:'missed'})}});
if(correct>0)snd(true);else snd(false)}
function nextRound(){round++;if(round>maxR){state='win'}else{setup()}}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;setup()}return}
if(state!=='play')return;
if(!checked&&m.y>H-70&&m.y<H-25&&m.x>W/2-70&&m.x<W/2+70){checkAnswers();return}
if(checked&&m.y>H-70&&m.y<H-25&&m.x>W/2-55&&m.x<W/2+55){nextRound();return}
if(!checked){cards.forEach((c,i)=>{if(m.x>c.x-c.w/2&&m.x<c.x+c.w/2&&m.y>c.y-c.h/2&&m.y<c.y+c.h/2){
if(selected.has(i))selected.delete(i);else selected.add(i)}})}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_sci_koku_bahcesi_html():
    """Koku Bahçesi — Koku kartlarını eşleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
const ALL_PAIRS=[
{a:'🌹',an:'Gül',b:'💐',bn:'Gül Kokusu',clr:'#ff6b9d'},
{a:'☕',an:'Kahve',b:'♨️',bn:'Kahve Kokusu',clr:'#fb923c'},
{a:'🍋',an:'Limon',b:'🟡',bn:'Limon Kokusu',clr:'#fbbf24'},
{a:'🌲',an:'Çam',b:'🌿',bn:'Çam Kokusu',clr:'#34d399'},
{a:'🍊',an:'Portakal',b:'🟠',bn:'Portakal Kokusu',clr:'#f472b6'},
{a:'🧁',an:'Vanilya',b:'🍦',bn:'Vanilya Kokusu',clr:'#c084fc'},
{a:'🍫',an:'Çikolata',b:'🤎',bn:'Çikolata Kokusu',clr:'#a78bfa'},
{a:'🌱',an:'Nane',b:'💚',bn:'Nane Kokusu',clr:'#4ade80'}
];
let cards=[],flipped=[],matched=new Set(),round=1,maxR=10,score=0,state='start',particles=[],swirlParts=[],canFlip=true,flipAnim=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:clr||'#fbbf24',r:3+Math.random()*3})}
function addSwirl(x,y,clr){for(let i=0;i<8;i++)swirlParts.push({x,y,angle:Math.random()*Math.PI*2,r:5+Math.random()*20,speed:0.02+Math.random()*0.03,life:2,clr:clr,sz:2+Math.random()*3})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function setup(){flipped=[];matched.clear();canFlip=true;flipAnim=[];
const pairCnt=round<=3?4:round<=6?5:6;
const pairs=shuffle([...ALL_PAIRS]).slice(0,pairCnt);
const all=[];
pairs.forEach((p,i)=>{all.push({emoji:p.a,name:p.an,pairId:i,clr:p.clr,faceUp:false});all.push({emoji:p.b,name:p.bn,pairId:i,clr:p.clr,faceUp:false})});
shuffle(all);
const total=all.length;
const cols=total<=8?4:total<=10?5:4;
const rows=Math.ceil(total/cols);
const cw=110,ch=120,gap=12;
const startX=(W-cols*cw-(cols-1)*gap)/2;
const startY=90;
cards=all.map((item,i)=>{
const col=i%cols,row=Math.floor(i/cols);
return{...item,x:startX+col*(cw+gap)+cw/2,y:startY+row*(ch+gap)+ch/2,w:cw,h:ch,idx:i,flipScale:1}})}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🌸 Koku Bahçesi',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Koku kartlarını eşleştir!',W/2,225);ctx.font='50px Segoe UI';ctx.fillText('🌹☕🍋',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,382);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Koku Uzmanı! 🎉',W/2,180);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,230);ctx.font='50px Segoe UI';ctx.fillText('💐',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,382);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score+'  Eşleşen: '+matched.size+'/'+Math.floor(cards.length/2),W/2,30);
ctx.fillStyle='#c084fc80';ctx.font='14px Segoe UI';ctx.fillText('Kokuları kaynakları ile eşleştir!',W/2,54);
cards.forEach((c,i)=>{
const isFlipped=c.faceUp||flipped.includes(i)||matched.has(c.pairId);
ctx.save();ctx.translate(c.x,c.y);ctx.scale(c.flipScale,1);
if(isFlipped){
ctx.fillStyle=matched.has(c.pairId)?'#064e3b':'#312e81';ctx.strokeStyle=matched.has(c.pairId)?c.clr:'#a78bfa';
}else{
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa60'}
ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(-c.w/2,-c.h/2,c.w,c.h,10);ctx.fill();ctx.stroke();
if(isFlipped){ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(c.emoji,0,-8);ctx.textBaseline='alphabetic';ctx.fillStyle='#e9d5ff';ctx.font='bold 11px Segoe UI';ctx.fillText(c.name,0,c.h/2-16)}
else{ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🌸',0,-4);ctx.textBaseline='alphabetic';ctx.fillStyle='#a78bfa40';ctx.font='10px Segoe UI';ctx.fillText('Koku',0,c.h/2-16)}
ctx.restore()});
swirlParts.forEach(s=>{ctx.globalAlpha=Math.min(1,s.life*0.5);ctx.fillStyle=s.clr;ctx.beginPath();ctx.arc(s.x+Math.cos(s.angle)*s.r,s.y+Math.sin(s.angle)*s.r,s.sz,0,Math.PI*2);ctx.fill()});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function checkMatch(){if(flipped.length<2)return;canFlip=false;
const c0=cards[flipped[0]],c1=cards[flipped[1]];
if(c0.pairId===c1.pairId){
matched.add(c0.pairId);score+=10;snd(true);addP(c0.x,c0.y,c0.clr);addP(c1.x,c1.y,c1.clr);
addSwirl(c0.x,c0.y,c0.clr);addSwirl(c1.x,c1.y,c1.clr);
flipped=[];canFlip=true;
if(matched.size===Math.floor(cards.length/2)){round++;if(round>maxR){setTimeout(()=>{state='win'},600)}else{setTimeout(setup,800)}}}
else{snd(false);setTimeout(()=>{flipped=[];canFlip=true},1000)}}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
swirlParts.forEach(s=>{s.angle+=s.speed;s.r+=0.3;s.life-=0.015});swirlParts=swirlParts.filter(s=>s.life>0);
draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'||state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;matched.clear();setup()}return}
if(state!=='play'||!canFlip)return;
cards.forEach((c,i)=>{if(m.x>c.x-c.w/2&&m.x<c.x+c.w/2&&m.y>c.y-c.h/2&&m.y<c.y+c.h/2){
if(matched.has(c.pairId)||flipped.includes(i))return;
if(flipped.length<2){flipped.push(i);if(flipped.length===2)setTimeout(checkMatch,600)}}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_sci_deprem_evi_html():
    """Minik Deprem Evi — Sağlam bina inşa et, depreme dayan!"""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
const FACES=['😊','😄','😁','🤗','😎'];
const GU=40;
const GCols=7,GRows=10;
const GX=(W-GCols*GU)/2,GY=80;
let placed=[],palette=[],dragging=null,dox=0,doy=0,round=1,maxR=10,score=0,state='start',particles=[];
let shaking=false,shakeT=0,shakeDur=2,fallen=[],surviving=[],debris=[],shakeOffX=0,shakeOffY=0,resultMsg='',resultTimer=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:clr||'#fb923c',r:2+Math.random()*3})}
function setup(){placed=[];fallen=[];surviving=[];debris=[];shaking=false;shakeT=0;resultMsg='';resultTimer=0;dragging=null;
const blockCnt=Math.min(4+round,12);
palette=[];
for(let i=0;i<blockCnt;i++){
const type=i<Math.ceil(blockCnt*0.4)?'wide':i<Math.ceil(blockCnt*0.8)?'narrow':'tri';
const w=type==='wide'?2:1;
const h=type==='tri'?1:1;
const clr=COLORS[i%COLORS.length];
const face=FACES[i%FACES.length];
palette.push({type,gw:w,gh:h,clr,face,x:0,y:0,placed:false})}
layoutPalette()}
function layoutPalette(){const py=H-90;let px=40;
palette.forEach(b=>{if(!b.placed){b.x=px+b.gw*GU/2;b.y=py;px+=b.gw*GU+15}})}
function snapToGrid(x,y,gw,gh){
const col=Math.round((x-gw*GU/2-GX)/GU);
const row=Math.round((y-gh*GU/2-GY)/GU);
return{col:Math.max(0,Math.min(col,GCols-gw)),row:Math.max(0,Math.min(row,GRows-gh))}}
function canPlace(col,row,gw,gh,exclude){
if(col<0||row<0||col+gw>GCols||row+gh>GRows)return false;
for(const p of placed){if(p===exclude)continue;
if(col<p.col+p.gw&&col+gw>p.col&&row<p.row+p.gh&&row+gh>p.row)return false}
return true}
function calcStability(){
if(placed.length===0)return 0;
let totalScore=0;const maxRow=Math.max(...placed.map(p=>p.row+p.gh));
placed.forEach(p=>{
const rowFromBottom=maxRow-(p.row+p.gh);
const widthBonus=p.gw>=2?2:1;
const bottomBonus=rowFromBottom<=2?3:rowFromBottom<=4?2:1;
let supported=p.row+p.gh>=maxRow;
if(!supported){for(const o of placed){if(o!==p&&o.row===p.row+p.gh&&o.col<p.col+p.gw&&o.col+o.gw>p.col){supported=true;break}}}
const supportScore=supported?2:0;
totalScore+=widthBonus*bottomBonus+supportScore});
return Math.min(100,Math.round(totalScore/placed.length*10))}
function earthquake(){shaking=true;shakeT=0;shakeDur=1.5+round*0.15;
const stability=calcStability();const surviveThresh=round<=3?30:round<=6?45:55;
fallen=[];surviving=[];
placed.forEach(p=>{
const rowFromBottom=GRows-(p.row+p.gh);
const wideFactor=p.gw>=2?1.5:1;
let supported=false;
for(const o of placed){if(o!==p&&o.row===p.row+p.gh&&o.col<p.col+p.gw&&o.col+o.gw>p.col){supported=true;break}}
if(p.row+p.gh>=GRows)supported=true;
const surviveChance=stability/100*wideFactor*(supported?1.3:0.5)*(rowFromBottom<3?1.2:0.8);
if(surviveChance>0.4+Math.random()*0.5)surviving.push(p);else{fallen.push(p);
for(let i=0;i<5;i++)debris.push({x:GX+p.col*GU+p.gw*GU/2,y:GY+p.row*GU+p.gh*GU/2,vx:(Math.random()-.5)*8,vy:-2-Math.random()*5,life:1.5,clr:p.clr,r:3+Math.random()*4})}})}
function finishShake(){shaking=false;
const survPct=placed.length>0?surviving.length/placed.length*100:0;
surviving.forEach(()=>score+=5);
if(survPct>=60){score+=20;resultMsg='🏆 Sağlam Bina! +20 Bonus';snd(true)}
else{resultMsg='💥 Bina yıkıldı... Daha geniş taban kullan!';snd(false)}
resultTimer=3;
setTimeout(()=>{round++;if(round>maxR)state='win';else setup()},3000)}
function drawBlock(b,ox,oy){
const bx=(b.col!==undefined?GX+b.col*GU:b.x-b.gw*GU/2)+ox;
const by=(b.col!==undefined?GY+b.row*GU:b.y-b.gh*GU/2)+oy;
const bw=b.gw*GU,bh=b.gh*GU;
if(b.type==='tri'){ctx.fillStyle=b.clr;ctx.beginPath();ctx.moveTo(bx+bw/2,by);ctx.lineTo(bx+bw,by+bh);ctx.lineTo(bx,by+bh);ctx.closePath();ctx.fill();ctx.strokeStyle='#fff4';ctx.lineWidth=1;ctx.stroke();ctx.font=(bh*0.5)+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(b.face,bx+bw/2,by+bh*0.6)}
else{ctx.fillStyle=b.clr;ctx.beginPath();ctx.roundRect(bx+1,by+1,bw-2,bh-2,5);ctx.fill();ctx.strokeStyle='#fff3';ctx.lineWidth=1;ctx.stroke();ctx.font=(bh*0.55)+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(b.face,bx+bw/2,by+bh/2)}
ctx.textBaseline='alphabetic'}
function draw(){ctx.clearRect(0,0,W,H);
const ox=shaking?(Math.random()-.5)*12*Math.min(1,shakeT/0.3):0;
const oy=shaking?(Math.random()-.5)*6*Math.min(1,shakeT/0.3):0;
const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🏗️ Minik Deprem Evi',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Sağlam bir bina inşa et!',W/2,225);ctx.font='50px Segoe UI';ctx.fillText('🏠',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,382);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Mühendis! 🎉',W/2,180);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,230);ctx.font='50px Segoe UI';ctx.fillText('🏆',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,382);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.save();ctx.translate(ox,oy);
ctx.strokeStyle='#a78bfa20';ctx.lineWidth=1;
for(let c=0;c<=GCols;c++){ctx.beginPath();ctx.moveTo(GX+c*GU,GY);ctx.lineTo(GX+c*GU,GY+GRows*GU);ctx.stroke()}
for(let r=0;r<=GRows;r++){ctx.beginPath();ctx.moveTo(GX,GY+r*GU);ctx.lineTo(GX+GCols*GU,GY+r*GU);ctx.stroke()}
ctx.fillStyle='#4a3728';ctx.fillRect(GX-10,GY+GRows*GU,GCols*GU+20,8);
if(!shaking){placed.forEach(b=>drawBlock(b,0,0))}
else{surviving.forEach(b=>drawBlock(b,0,0));
fallen.forEach(b=>{ctx.globalAlpha=Math.max(0,1-shakeT/shakeDur);drawBlock(b,(Math.random()-.5)*shakeT*10,shakeT*40);ctx.globalAlpha=1})}
ctx.restore();
if(!shaking&&placed.length>0&&!resultMsg){
const stab=calcStability();
ctx.fillStyle='#e9d5ff';ctx.font='14px Segoe UI';ctx.textAlign='left';ctx.fillText('Sağlamlık: '+stab+'%',GX,GY+GRows*GU+30);
const barW=100;ctx.fillStyle='#333';ctx.fillRect(GX+90,GY+GRows*GU+20,barW,12);
ctx.fillStyle=stab>60?'#34d399':stab>30?'#fbbf24':'#ef4444';ctx.fillRect(GX+90,GY+GRows*GU+20,barW*stab/100,12)}
if(!shaking&&state==='play'&&placed.length>0&&!resultMsg){
ctx.fillStyle='#ef4444';ctx.beginPath();ctx.roundRect(W/2+100,GY+GRows*GU+14,120,36,8);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('Salla! 🫨',W/2+160,GY+GRows*GU+37)}
palette.forEach(b=>{if(!b.placed)drawBlock(b,0,0)});
if(resultMsg){ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(resultMsg,W/2,GY+GRows*GU+55)}
debris.forEach(d=>{ctx.globalAlpha=Math.min(1,d.life);ctx.fillStyle=d.clr;ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,Math.PI*2);ctx.fill()});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
ctx.fillStyle='#a78bfa60';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText('İpucu: Geniş blokları alta koy!',W/2,H-8)}
function upd(ts){
if(shaking){shakeT+=0.016;if(shakeT>=shakeDur)finishShake()}
if(resultTimer>0)resultTimer-=0.016;if(resultTimer<=0)resultMsg='';
debris.forEach(d=>{d.x+=d.vx;d.y+=d.vy;d.vy+=0.3;d.life-=0.02});debris=debris.filter(d=>d.life>0);
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play'||shaking||resultMsg)return;
for(let i=palette.length-1;i>=0;i--){const b=palette[i];if(b.placed)continue;
const bx=b.x-b.gw*GU/2,by=b.y-b.gh*GU/2,bw=b.gw*GU,bh=b.gh*GU;
if(m.x>=bx&&m.x<=bx+bw&&m.y>=by&&m.y<=by+bh){dragging={src:'palette',idx:i};dox=m.x-b.x;doy=m.y-b.y;break}}
if(!dragging){for(let i=placed.length-1;i>=0;i--){const b=placed[i];
const bx=GX+b.col*GU,by=GY+b.row*GU,bw=b.gw*GU,bh=b.gh*GU;
if(m.x>=bx&&m.x<=bx+bw&&m.y>=by&&m.y<=by+bh){
const removed=placed.splice(i,1)[0];
const pb=palette.find(p=>p===removed.ref);if(pb){pb.placed=false;pb.x=m.x;pb.y=m.y;dragging={src:'palette',idx:palette.indexOf(pb)};dox=0;doy=0}break}}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);
if(dragging.src==='palette'){const b=palette[dragging.idx];b.x=m.x-dox;b.y=m.y-doy}});
cv.addEventListener('mouseup',e=>{if(!dragging)return;
if(dragging.src==='palette'){const b=palette[dragging.idx];
const snap=snapToGrid(b.x,b.y,b.gw,b.gh);
if(canPlace(snap.col,snap.row,b.gw,b.gh,null)&&b.y<H-100){
placed.push({col:snap.col,row:snap.row,gw:b.gw,gh:b.gh,type:b.type,clr:b.clr,face:b.face,ref:b});b.placed=true;
addP(GX+snap.col*GU+b.gw*GU/2,GY+snap.row*GU+b.gh*GU/2,b.clr)}else{layoutPalette()}}
dragging=null});
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;setup()}return}
if(state==='play'&&!shaking&&!resultMsg&&placed.length>0){
const btnX=W/2+100,btnY=GY+GRows*GU+14;
if(m.x>=btnX&&m.x<=btnX+120&&m.y>=btnY&&m.y<=btnY+36){earthquake()}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_sci_baloncuk_kimyasi_html():
    """Baloncuk Kimyası — Doğru karışımla baloncuk üfle!"""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
const TARGETS=[
{name:'Minik',min:15,max:30},{name:'Küçük',min:25,max:45},{name:'Orta',min:40,max:65},
{name:'Büyük',min:55,max:85},{name:'Kocaman',min:75,max:110}
];
let water=0,soap=0,blow=0,round=1,maxR=10,score=0,state='start',particles=[],droplets=[];
let bubble=null,target=null,blowing=false,resultMsg='',resultTimer=0,bubblePhase='idle';
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:clr||'#60a5fa',r:2+Math.random()*4})}
function addDroplets(x,y,r){for(let i=0;i<12;i++){const ang=Math.random()*Math.PI*2;const spd=2+Math.random()*4;droplets.push({x:x+Math.cos(ang)*r*0.5,y:y+Math.sin(ang)*r*0.5,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd-2,life:1,r:2+Math.random()*3,clr:COLORS[Math.floor(Math.random()*COLORS.length)]})}}
function setup(){water=0;soap=0;blow=0;bubble=null;blowing=false;resultMsg='';resultTimer=0;bubblePhase='idle';
const ti=round<=2?0:round<=4?1:round<=6?2:round<=8?3:4;
target=TARGETS[ti]}
function calcBubbleSize(){
if(water===0&&soap===0)return 0;
const ratio=soap>0?water/soap:10;
const idealRatio=1.5;
const ratioScore=1-Math.min(1,Math.abs(ratio-idealRatio)/3);
const soapEffect=Math.min(soap/3,1);
const baseSize=(water*8+soap*15)*soapEffect*ratioScore;
const blowEffect=blow<=0?0:blow<=2?0.6:blow<=3?1.0:blow<=4?0.8:0.4;
return Math.max(0,baseSize*blowEffect)}
function blowBubble(){
if(water===0||soap===0||blow===0){resultMsg='Her malzemeden en az 1 koy!';resultTimer=2;snd(false);return}
const size=calcBubbleSize();
if(size<5){resultMsg='Baloncuk oluşmadı! Karışımı ayarla.';resultTimer=2;snd(false);return}
bubblePhase='growing';
bubble={x:W/2,y:380,r:5,targetR:size,vy:0,wobble:0,wobbleSpd:0.05+Math.random()*0.03,life:3+size/30,growing:true,popTimer:0}}
function checkBubble(){
if(!bubble)return;
if(bubble.r>=target.min&&bubble.r<=target.max){score+=10;resultMsg='🎉 Hedef boyut! +10 puan';snd(true);addP(bubble.x,bubble.y,'#34d399')}
else if(bubble.r<target.min){resultMsg='Çok küçük! Daha fazla malzeme dene.';snd(false)}
else{resultMsg='Çok büyük! Daha az malzeme dene.';snd(false)}
resultTimer=2.5}
function popBubble(){
if(!bubble)return;addDroplets(bubble.x,bubble.y,bubble.r);bubble=null;
setTimeout(()=>{round++;if(round>maxR){state='win'}else{setup()}},2500)}
function drawBowl(cx,cy){
ctx.fillStyle='#4a3728';ctx.beginPath();ctx.ellipse(cx,cy+5,70,15,0,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#6b4c2a';ctx.beginPath();ctx.ellipse(cx,cy-10,65,40,0,0.2,Math.PI-0.2);ctx.fill();
ctx.strokeStyle='#8b6c3a';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(cx,cy-10,65,40,0,0.1,Math.PI-0.1);ctx.stroke();
ctx.fillStyle='#3a8bfa40';
const waterLevel=water*6;if(waterLevel>0){ctx.beginPath();ctx.ellipse(cx,cy-10+20-waterLevel/2,60,Math.min(35,waterLevel),0,0.1,Math.PI-0.1);ctx.fill()}
if(soap>0){for(let i=0;i<soap*3;i++){const bx=cx-40+Math.random()*80,by=cy-15-waterLevel/2+Math.random()*10;
ctx.fillStyle='#fff6';ctx.beginPath();ctx.arc(bx,by,3+Math.random()*4,0,Math.PI*2);ctx.fill()}}}
function drawSlider(x,y,label,emoji,val,maxVal){
const sw=120,sh=30;
ctx.fillStyle='#1e1b4b';ctx.beginPath();ctx.roundRect(x-sw/2-40,y-sh/2-5,sw+80,sh+30,8);ctx.fill();ctx.strokeStyle='#a78bfa40';ctx.lineWidth=1;ctx.stroke();
ctx.font='20px Segoe UI';ctx.textAlign='center';ctx.fillText(emoji,x-sw/2-15,y+8);
ctx.fillStyle='#e9d5ff';ctx.font='bold 12px Segoe UI';ctx.fillText(label,x+10,y-18);
ctx.fillStyle='#a78bfa30';ctx.beginPath();ctx.roundRect(x-sw/2+15,y-4,sw-10,12,4);ctx.fill();
for(let i=0;i<=maxVal;i++){const px=x-sw/2+15+(sw-10)*i/maxVal;ctx.fillStyle=i<=val?'#a78bfa':'#a78bfa30';ctx.beginPath();ctx.arc(px,y+2,6,0,Math.PI*2);ctx.fill()}
ctx.fillStyle='#c084fc';ctx.beginPath();ctx.roundRect(x-sw/2-5,y+16,30,22,5);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.fillText('−',x-sw/2+10,y+32);
ctx.fillStyle='#c084fc';ctx.beginPath();ctx.roundRect(x+sw/2-10,y+16,30,22,5);ctx.fill();ctx.fillStyle='#fff';ctx.fillText('+',x+sw/2+5,y+32);
ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.fillText(val,x+sw/2+30,y+8);
return{minusBtn:{x:x-sw/2-5,y:y+16,w:30,h:22},plusBtn:{x:x+sw/2-10,y:y+16,w:30,h:22}}}
function drawBubble(b){
if(!b)return;
const wobX=Math.sin(b.wobble)*b.r*0.08;
const wobY=Math.cos(b.wobble*1.3)*b.r*0.05;
const grad=ctx.createRadialGradient(b.x+wobX-b.r*0.3,b.y+wobY-b.r*0.3,b.r*0.1,b.x+wobX,b.y+wobY,b.r);
grad.addColorStop(0,'rgba(255,255,255,0.3)');grad.addColorStop(0.3,'rgba(96,165,250,0.15)');
grad.addColorStop(0.6,'rgba(192,132,252,0.1)');grad.addColorStop(1,'rgba(96,165,250,0.05)');
ctx.fillStyle=grad;ctx.beginPath();ctx.arc(b.x+wobX,b.y+wobY,b.r,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='rgba(192,132,252,0.4)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(b.x+wobX,b.y+wobY,b.r,0,Math.PI*2);ctx.stroke();
const rainbowGrad=ctx.createLinearGradient(b.x-b.r,b.y-b.r,b.x+b.r,b.y+b.r);
rainbowGrad.addColorStop(0,'rgba(255,107,157,0.15)');rainbowGrad.addColorStop(0.25,'rgba(251,191,36,0.15)');
rainbowGrad.addColorStop(0.5,'rgba(52,211,153,0.15)');rainbowGrad.addColorStop(0.75,'rgba(96,165,250,0.15)');
rainbowGrad.addColorStop(1,'rgba(192,132,252,0.15)');
ctx.strokeStyle=rainbowGrad;ctx.lineWidth=3;ctx.beginPath();ctx.arc(b.x+wobX,b.y+wobY,b.r-2,0,Math.PI*2);ctx.stroke();
ctx.fillStyle='rgba(255,255,255,0.5)';ctx.beginPath();ctx.ellipse(b.x+wobX-b.r*0.3,b.y+wobY-b.r*0.3,b.r*0.15,b.r*0.1,-0.5,0,Math.PI*2);ctx.fill()}
let btnRects={};
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🫧 Baloncuk Kimyası',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Doğru karışımla baloncuk üfle!',W/2,225);ctx.font='50px Segoe UI';ctx.fillText('🧪',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,382);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Baloncuk Ustası! 🎉',W/2,180);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,230);ctx.font='50px Segoe UI';ctx.fillText('🏆',W/2,310);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,350,160,50,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,382);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
if(target){ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.fillText('Hedef: '+target.name+' baloncuk',W/2,55);
ctx.fillStyle='#a78bfa40';ctx.font='12px Segoe UI';ctx.fillText('(çap: '+target.min+'—'+target.max+' piksel)',W/2,72);
ctx.strokeStyle='#fbbf2440';ctx.setLineDash([4,4]);ctx.lineWidth=1;
ctx.beginPath();ctx.arc(W/2+230,160,target.min,0,Math.PI*2);ctx.stroke();
ctx.beginPath();ctx.arc(W/2+230,160,target.max,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#fbbf2440';ctx.font='10px Segoe UI';ctx.fillText('Hedef boyut',W/2+230,160+target.max+15)}
drawBowl(W/2,340);
btnRects.water=drawSlider(W/2-180,480,'Su','💧',water,5);
btnRects.soap=drawSlider(W/2,480,'Sabun','🧴',soap,5);
btnRects.blow=drawSlider(W/2+180,480,'Üfleme','🌬️',blow,5);
if(!bubble&&bubblePhase==='idle'){ctx.fillStyle='#34d399';ctx.beginPath();ctx.roundRect(W/2-65,560,130,45,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Üfle! 🫧',W/2,590)}
if(bubble)drawBubble(bubble);
if(resultMsg&&resultTimer>0){ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(resultMsg,W/2,140)}
droplets.forEach(d=>{ctx.globalAlpha=d.life;ctx.fillStyle=d.clr;ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,Math.PI*2);ctx.fill()});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){
if(bubble){
bubble.wobble+=bubble.wobbleSpd;
if(bubble.growing){bubble.r+=0.8;if(bubble.r>=bubble.targetR){bubble.growing=false;checkBubble()}}
else{bubble.vy-=0.015;bubble.y+=bubble.vy;bubble.x+=Math.sin(bubble.wobble)*0.5;
bubble.life-=0.016;
if(bubble.life<=0||bubble.y+bubble.r<-20){
if(bubble.y+bubble.r>=0)addDroplets(bubble.x,bubble.y,bubble.r);
popBubble()}}}
if(resultTimer>0)resultTimer-=0.016;
droplets.forEach(d=>{d.x+=d.vx;d.y+=d.vy;d.vy+=0.15;d.life-=0.02});droplets=droplets.filter(d=>d.life>0);
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
function hitBtn(m,btn){return m.x>=btn.x&&m.x<=btn.x+btn.w&&m.y>=btn.y&&m.y<=btn.y+btn.h}
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>350&&m.y<400){state='play';score=0;round=1;setup()}return}
if(state!=='play')return;
if(!bubble&&bubblePhase==='idle'){
if(m.x>W/2-65&&m.x<W/2+65&&m.y>560&&m.y<605){blowBubble();return}
if(btnRects.water){
if(hitBtn(m,btnRects.water.minusBtn)){water=Math.max(0,water-1);return}
if(hitBtn(m,btnRects.water.plusBtn)){water=Math.min(5,water+1);return}}
if(btnRects.soap){
if(hitBtn(m,btnRects.soap.minusBtn)){soap=Math.max(0,soap-1);return}
if(hitBtn(m,btnRects.soap.plusBtn)){soap=Math.min(5,soap+1);return}}
if(btnRects.blow){
if(hitBtn(m,btnRects.blow.minusBtn)){blow=Math.max(0,blow-1);return}
if(hitBtn(m,btnRects.blow.plusBtn)){blow=Math.min(5,blow+1);return}}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""
