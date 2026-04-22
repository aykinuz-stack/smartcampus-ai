# -*- coding: utf-8 -*-
"""Okul Öncesi Genel Yetenek Oyunları — 20 Premium HTML5 Oyun (Bölüm D: 16-20)."""


def _build_prek_ab_ayni_yone_cevir_html():
    """Aynı Yöne Çevir — Referans okun yönünü eşle."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let round=1,maxRound=10,score=0,state='start',particles=[];
let refDir=0,options=[],correctIdx=0,shake=0,shakeIdx=-1,feedback='',feedbackTimer=0;
let animTimer=0,timeLeft=0,timerActive=false;
const DIR4=[0,90,180,270];
const DIR8=[0,45,90,135,180,225,270,315];
const DIR_NAMES={0:'Sağ',45:'Sağ Yukarı',90:'Yukarı',135:'Sol Yukarı',180:'Sol',225:'Sol Aşağı',270:'Aşağı',315:'Sağ Aşağı'};
const ARROW_CLRS=['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#ec4899','#06b6d4','#f97316'];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function shuffle(arr){for(let i=arr.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}return arr}
function genRound(){
let pool;
if(round<=4)pool=DIR4.slice();
else if(round<=7)pool=DIR8.slice();
else pool=DIR8.slice();
refDir=pool[Math.floor(Math.random()*pool.length)];
let optDirs=[refDir];
let avail=pool.filter(d=>d!==refDir);
shuffle(avail);
let needed=3;
for(let i=0;i<needed&&i<avail.length;i++)optDirs.push(avail[i]);
while(optDirs.length<4){optDirs.push(pool[Math.floor(Math.random()*pool.length)])}
shuffle(optDirs);
correctIdx=optDirs.indexOf(refDir);
options=optDirs.map((d,i)=>({dir:d,x:110+i*160,y:420,clr:ARROW_CLRS[i%ARROW_CLRS.length]}));
shake=0;shakeIdx=-1;feedback='';feedbackTimer=0;
timeLeft=round>=8?8:0;timerActive=round>=8;animTimer=0}
function drawArrow(cx,cy,angle,size,clr,lineW){
ctx.save();ctx.translate(cx,cy);ctx.rotate(-angle*Math.PI/180);
ctx.fillStyle=clr;ctx.strokeStyle=clr;ctx.lineWidth=lineW||4;ctx.lineCap='round';ctx.lineJoin='round';
const s=size;
ctx.beginPath();ctx.moveTo(s*0.5,0);ctx.lineTo(s*0.15,-s*0.25);ctx.lineTo(s*0.15,-s*0.1);
ctx.lineTo(-s*0.5,-s*0.1);ctx.lineTo(-s*0.5,s*0.1);ctx.lineTo(s*0.15,s*0.1);
ctx.lineTo(s*0.15,s*0.25);ctx.closePath();ctx.fill();ctx.stroke();ctx.restore()}
function drawRoundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🏹 Aynı Yöne Çevir',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Referans okla aynı yönü gösteren oku bul!',W/2,230);
ctx.fillText('Ok yönünü eşle ve puan kazan!',W/2,260);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,300,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Harika! 🎉',W/2,180);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,230);ctx.font='20px Segoe UI';ctx.fillText('Tüm yönleri doğru buldun!',W/2,270);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'  Puan: '+score,W/2,30);
if(timerActive&&timeLeft>0){ctx.fillStyle=timeLeft<=3?'#ef4444':'#fbbf24';ctx.font='bold 18px Segoe UI';
ctx.fillText('Süre: '+Math.ceil(timeLeft)+'s',W/2,55)}
ctx.fillStyle='#a78bfa40';ctx.font='16px Segoe UI';ctx.fillText('Referans Ok',W/2,85);
let refAngle=refDir;
if(round>=8){animTimer+=0.02;refAngle=refDir}
drawArrow(W/2,170,refAngle,120,'#fbbf24',5);
ctx.fillStyle='#fbbf2480';ctx.font='bold 16px Segoe UI';
ctx.fillText(DIR_NAMES[refDir]||'',W/2,240);
ctx.fillStyle='#a78bfa40';ctx.font='16px Segoe UI';ctx.fillText('Doğru yönü seç:',W/2,280);
for(let i=0;i<options.length;i++){const o=options[i];
let ox=o.x,oy=o.y;
if(shakeIdx===i&&shake>0){ox+=Math.sin(shake*10)*8;shake-=0.05;if(shake<=0){shake=0;shakeIdx=-1}}
ctx.fillStyle='#1e1b4b';ctx.strokeStyle=o.clr+'80';ctx.lineWidth=3;
drawRoundRect(ox-55,oy-55,110,130,15);ctx.fill();ctx.stroke();
drawArrow(ox,oy,o.dir,70,o.clr,3);
ctx.fillStyle='#e9d5ff80';ctx.font='13px Segoe UI';ctx.textAlign='center';
ctx.fillText(DIR_NAMES[o.dir]||'',ox,oy+65)}
if(feedbackTimer>0){ctx.fillStyle=feedback.startsWith('D')?'#10b981':'#ef4444';
ctx.font='bold 26px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=Math.min(1,feedbackTimer);
ctx.fillText(feedback,W/2,560);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastTime=0;
function upd(t){const dt=lastTime?Math.min((t-lastTime)/1000,0.1):0.016;lastTime=t;
if(state==='play'&&timerActive&&timeLeft>0){timeLeft-=dt;if(timeLeft<=0){timeLeft=0;snd(false);feedback='Süre doldu!';feedbackTimer=2;setTimeout(()=>{genRound()},1500)}}
if(feedbackTimer>0)feedbackTimer-=dt;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function handleClick(mx,my){
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=1;genRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;genRound()}return}
if(state!=='play'||feedbackTimer>0.5)return;
for(let i=0;i<options.length;i++){const o=options[i];
if(mx>o.x-55&&mx<o.x+55&&my>o.y-55&&my<o.y+75){
if(i===correctIdx){score+=10;snd(true);addP(o.x,o.y,o.clr);feedback='Doğru! +10';feedbackTimer=1.5;
round++;if(round>maxRound){setTimeout(()=>{state='win'},800)}else{setTimeout(()=>{genRound()},1000)}}
else{snd(false);shake=1;shakeIdx=i;feedback='Tekrar dene!';feedbackTimer=1.2}
break}}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);handleClick(mx,my)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);handleClick(mx,my)});
genRound();requestAnimationFrame(upd);
</script></body></html>"""


def _build_prek_ab_siniflandirma_html():
    """Sınıflandırma Kutuları — Nesneleri doğru kategoriye sürükle."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let round=1,maxRound=10,score=0,state='start',particles=[];
let categories=[],currentItem=null,itemQueue=[],feedback='',feedbackTimer=0;
let flyAnim=null,glowBox=-1,glowTimer=0,correctInRound=0,totalInRound=0;
const CAT_DATA=[
{name:'Hayvanlar',icon:'\uD83D\uDC3E',clr:'#ef4444',items:['\uD83D\uDC31','\uD83D\uDC36','\uD83D\uDC30','\uD83D\uDC3B','\uD83E\uDD81','\uD83D\uDC18','\uD83D\uDC35','\uD83D\uDC27','\uD83E\uDD8A','\uD83D\uDC3A']},
{name:'Meyveler',icon:'\uD83C\uDF4E',clr:'#10b981',items:['\uD83C\uDF4E','\uD83C\uDF4C','\uD83C\uDF4A','\uD83C\uDF47','\uD83C\uDF53','\uD83C\uDF51','\uD83C\uDF52','\uD83E\uDD5D','\uD83C\uDF49','\uD83C\uDF4D']},
{name:'Araçlar',icon:'\uD83D\uDE97',clr:'#3b82f6',items:['\uD83D\uDE97','\uD83D\uDE8C','\uD83D\uDEB2','\uD83D\uDE81','\u2708\uFE0F','\uD83D\uDE82','\uD83D\uDE95','\uD83D\uDEF5','\uD83D\uDE92','\uD83D\uDE91']},
{name:'Giysiler',icon:'\uD83D\uDC55',clr:'#f59e0b',items:['\uD83D\uDC55','\uD83D\uDC57','\uD83E\uDDE3','\uD83E\uDDE4','\uD83D\uDC5F','\uD83E\uDDE5','\uD83D\uDC52','\uD83D\uDC56','\uD83E\uDD7E','\uD83D\uDC5E']},
{name:'Eşyalar',icon:'\uD83C\uDFE0',clr:'#8b5cf6',items:['\uD83D\uDCFA','\uD83D\uDCBB','\u260E\uFE0F','\uD83D\uDD11','\uD83D\uDCDA','\uD83D\uDD70\uFE0F','\uD83D\uDCA1','\uD83D\uDECB\uFE0F','\uD83E\uDDF9','\uD83C\uDF21\uFE0F']}
];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function drawRoundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function setupRound(){
let numCats=round<=6?3:(round<=8?4:5);
let activeCats=CAT_DATA.slice(0,numCats);
categories=activeCats.map((c,i)=>({name:c.name,icon:c.icon,clr:c.clr,items:c.items.slice(),count:0,
x:0,y:0,w:0,h:0}));
let spacing=W/(categories.length+1);
categories.forEach((c,i)=>{c.w=120;c.h=100;c.x=spacing*(i+1)-c.w/2;c.y=H-140});
let pool=[];
categories.forEach((cat,ci)=>{
let used=shuffle(cat.items.slice()).slice(0,2);
used.forEach(item=>pool.push({emoji:item,catIdx:ci}))});
shuffle(pool);
let itemCount=Math.min(pool.length,round<=5?3:4);
itemQueue=pool.slice(0,itemCount);
totalInRound=itemQueue.length;correctInRound=0;
nextItem()}
function nextItem(){if(itemQueue.length===0){
if(correctInRound>=totalInRound){score+=10;snd(true);feedback='Doğru! +10';feedbackTimer=1.5;
round++;if(round>maxRound){setTimeout(()=>{state='win'},800)}else{setTimeout(setupRound,1200)}}
currentItem=null;return}
let it=itemQueue.shift();
currentItem={emoji:it.emoji,catIdx:it.catIdx,x:W/2,y:100,baseX:W/2,baseY:100,scale:1}}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('📦 Sınıflandırma Kutuları',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Nesneleri doğru kutuya koy!',W/2,230);
ctx.fillText('Hayvanlar, meyveler ve araçları ayır.',W/2,260);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,300,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Süper! 🎉',W/2,180);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,230);ctx.font='20px Segoe UI';ctx.fillText('Hepsini doğru sınıflandırdın!',W/2,270);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'  Puan: '+score,W/2,30);
for(let i=0;i<categories.length;i++){const c=categories[i];
let glow=(glowBox===i&&glowTimer>0);
ctx.fillStyle=glow?c.clr+'60':c.clr+'25';ctx.strokeStyle=glow?c.clr:c.clr+'80';ctx.lineWidth=glow?4:2;
drawRoundRect(c.x,c.y,c.w,c.h,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='28px Segoe UI';ctx.textAlign='center';
ctx.fillText(c.icon,c.x+c.w/2,c.y+40);
ctx.font='bold 13px Segoe UI';ctx.fillText(c.name,c.x+c.w/2,c.y+65);
ctx.fillStyle=c.clr+'80';ctx.font='12px Segoe UI';
ctx.fillText(c.count+' nesne',c.x+c.w/2,c.y+85)}
if(currentItem&&!flyAnim){ctx.font='50px Segoe UI';ctx.textAlign='center';
ctx.fillText(currentItem.emoji,currentItem.x,currentItem.y+20);
ctx.fillStyle='#a78bfa60';ctx.font='14px Segoe UI';
ctx.fillText('Kutuya tıkla veya sürükle',W/2,160)}
if(flyAnim){let p=flyAnim.progress;
let fx=flyAnim.sx+(flyAnim.tx-flyAnim.sx)*p;
let fy=flyAnim.sy+(flyAnim.ty-flyAnim.sy)*p-Math.sin(p*Math.PI)*60;
ctx.font=(50*(1-p*0.3))+'px Segoe UI';ctx.textAlign='center';
ctx.globalAlpha=1-p*0.3;ctx.fillText(flyAnim.emoji,fx,fy+20);ctx.globalAlpha=1}
if(feedbackTimer>0){ctx.fillStyle=feedback.startsWith('D')?'#10b981':'#ef4444';
ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=Math.min(1,feedbackTimer);
ctx.fillText(feedback,W/2,220);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(feedbackTimer>0)feedbackTimer-=dt;
if(glowTimer>0)glowTimer-=dt;
if(flyAnim){flyAnim.progress+=dt*2.5;if(flyAnim.progress>=1){flyAnim=null;nextItem()}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function checkCategory(ci){
if(!currentItem||flyAnim)return;
if(ci===currentItem.catIdx){
let c=categories[ci];c.count++;
flyAnim={emoji:currentItem.emoji,sx:currentItem.x,sy:currentItem.y,tx:c.x+c.w/2,ty:c.y+30,progress:0};
snd(true);addP(c.x+c.w/2,c.y+50,c.clr);correctInRound++;
currentItem=null}
else{snd(false);feedback='Yanlış kutu!';feedbackTimer=1.2;
glowBox=currentItem.catIdx;glowTimer=1.5}}
function handleClick(mx,my){
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=1;setupRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;setupRound()}return}
if(state!=='play')return;
for(let i=0;i<categories.length;i++){const c=categories[i];
if(mx>=c.x&&mx<=c.x+c.w&&my>=c.y&&my<=c.y+c.h){checkCategory(i);return}}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);handleClick(mx,my)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);handleClick(mx,my)});
setupRound();requestAnimationFrame(upd);
</script></body></html>"""


def _build_prek_ab_gizli_nesne_html():
    """Gizli Nesne — Sahnede gizlenen nesneyi bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let round=1,maxRound=10,score=0,state='start',particles=[];
let hiddenObj=null,sceneObjs=[],feedback='',feedbackTimer=0,found=false;
let timeLeft=10,hintShown=false,flashTimer=0,revealCircle=null,revealTimer=0;
const SCENES=[
{name:'Park',bg1:'#87ceeb',bg2:'#228b22',ground:'#2d5016',
objs:[{e:'\uD83C\uDF33',x:80,y:280,s:50},{e:'\uD83C\uDF33',x:600,y:270,s:55},{e:'\uD83C\uDF38',x:180,y:420,s:25},{e:'\uD83C\uDF38',x:350,y:440,s:22},
{e:'\uD83C\uDF38',x:520,y:430,s:28},{e:'\uD83C\uDF3B',x:260,y:400,s:30},{e:'\uD83C\uDF3B',x:450,y:410,s:26},{e:'\u2601\uFE0F',x:200,y:120,s:40},{e:'\u2601\uFE0F',x:500,y:100,s:45},
{e:'\uD83C\uDFE0',x:400,y:230,s:60},{e:'\uD83D\uDC26',x:150,y:180,s:25},{e:'\uD83E\uDDA4',x:340,y:350,s:20}],
targets:[{e:'\uD83C\uDFBE',name:'Topu',hx:310,hy:390},{e:'\uD83E\uDD8B',name:'Kelebeği',hx:230,hy:300},{e:'\uD83D\uDC1E',name:'Uğurböceğini',hx:480,hy:400}]},
{name:'Oda',bg1:'#ddd6fe',bg2:'#c4b5fd',ground:'#8b7355',
objs:[{e:'\uD83D\uDECB\uFE0F',x:150,y:350,s:60},{e:'\uD83D\uDCFA',x:400,y:250,s:50},{e:'\uD83D\uDDBC\uFE0F',x:300,y:150,s:40},{e:'\uD83D\uDCDA',x:550,y:300,s:35},
{e:'\uD83E\uDDF8',x:200,y:400,s:30},{e:'\uD83D\uDD6F\uFE0F',x:500,y:200,s:28},{e:'\u23F0',x:600,y:160,s:25},{e:'\uD83C\uDF05',x:120,y:130,s:45},
{e:'\uD83E\uDDF9',x:620,y:380,s:35},{e:'\uD83C\uDF3A',x:350,y:380,s:22}],
targets:[{e:'\uD83D\uDD11',name:'Anahtarı',hx:420,hy:370},{e:'\uD83D\uDC31',name:'Kediyi',hx:180,hy:330},{e:'\u2702\uFE0F',name:'Makası',hx:560,hy:350}]},
{name:'Bahçe',bg1:'#86efac',bg2:'#22c55e',ground:'#92400e',
objs:[{e:'\uD83C\uDF3F',x:100,y:300,s:40},{e:'\uD83C\uDF3F',x:250,y:310,s:35},{e:'\uD83C\uDF3F',x:500,y:290,s:42},{e:'\uD83C\uDF3B',x:180,y:380,s:30},
{e:'\uD83C\uDF39',x:400,y:370,s:28},{e:'\uD83E\uDEB4',x:600,y:300,s:45},{e:'\uD83C\uDF33',x:80,y:230,s:55},{e:'\uD83C\uDF33',x:580,y:220,s:50},
{e:'\u2600\uFE0F',x:350,y:100,s:50},{e:'\uD83E\uDD94',x:300,y:350,s:25},{e:'\uD83D\uDC1B',x:450,y:390,s:20}],
targets:[{e:'\uD83D\uDC0C',name:'Salyangozu',hx:340,hy:380},{e:'\uD83C\uDF44',name:'Mantarı',hx:520,hy:370},{e:'\uD83E\uDD5A',name:'Yumurtayı',hx:150,hy:350}]}
];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function drawRoundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function genScene(){
let si=round%SCENES.length;let scene=SCENES[si];
let ti=Math.floor((round-1)/SCENES.length)%scene.targets.length;
if(ti>=scene.targets.length)ti=0;
let tgt=scene.targets[ti];
let jitterX=(Math.random()-0.5)*40;let jitterY=(Math.random()-0.5)*30;
hiddenObj={emoji:tgt.e,name:tgt.name,x:Math.max(50,Math.min(W-50,tgt.hx+jitterX)),y:Math.max(280,Math.min(H-100,tgt.hy+jitterY)),found:false};
sceneObjs=scene.objs.map(o=>({...o}));
found=false;timeLeft=10;hintShown=false;flashTimer=0;revealCircle=null;revealTimer=0;
feedback='';feedbackTimer=0}
function drawScene(){
let si=round%SCENES.length;let scene=SCENES[si];
let skyG=ctx.createLinearGradient(0,60,0,H);skyG.addColorStop(0,scene.bg1);skyG.addColorStop(0.6,scene.bg2);skyG.addColorStop(1,scene.ground);
ctx.fillStyle=skyG;ctx.fillRect(20,60,W-40,H-120);
ctx.strokeStyle='#a78bfa40';ctx.lineWidth=2;drawRoundRect(20,60,W-40,H-120,12);ctx.stroke();
sceneObjs.forEach(o=>{ctx.font=o.s+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(o.e,o.x,o.y)});
if(hiddenObj&&!hiddenObj.found){
let show=true;
if(hintShown){flashTimer+=0.1;if(Math.sin(flashTimer*5)>0.3)show=true;else show=false}
if(show){ctx.globalAlpha=0.65;ctx.font='20px Segoe UI';ctx.fillText(hiddenObj.emoji,hiddenObj.x,hiddenObj.y);ctx.globalAlpha=1}}
if(hiddenObj&&hiddenObj.found){ctx.font='30px Segoe UI';ctx.fillText(hiddenObj.emoji,hiddenObj.x,hiddenObj.y)}
if(revealCircle&&revealTimer>0){ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;
let rad=40*(1-revealTimer/1.5)+10;
ctx.beginPath();ctx.arc(revealCircle.x,revealCircle.y,rad,0,Math.PI*2);ctx.stroke();
ctx.fillStyle='#fbbf2420';ctx.fill()}
ctx.textBaseline='alphabetic'}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🔍 Gizli Nesne',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Sahnede gizlenen nesneyi bul!',W/2,230);
ctx.fillText('Dikkatli bak ve tıkla!',W/2,260);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,300,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Dedektif! 🎉',W/2,180);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,230);ctx.font='20px Segoe UI';ctx.fillText('Tüm gizli nesneleri buldun!',W/2,270);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'  Puan: '+score,W/2,22);
if(hiddenObj){ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';
ctx.fillText(hiddenObj.emoji+' '+hiddenObj.name+' Bul!',W/2,50)}
ctx.fillStyle=timeLeft<=3?'#ef4444':'#a78bfa';ctx.font='16px Segoe UI';
let barW=200;let barX=W/2-barW/2;
ctx.fillRect(barX,H-45,barW*(timeLeft/10),12);ctx.strokeStyle='#a78bfa60';ctx.lineWidth=1;ctx.strokeRect(barX,H-45,barW,12);
ctx.fillStyle='#e9d5ff';ctx.fillText(Math.ceil(timeLeft)+'s',W/2,H-20);
drawScene();
if(feedbackTimer>0){let fc=feedback.includes('Buldun')?'#10b981':(feedback.includes('Yakın')?'#f59e0b':'#ef4444');
ctx.fillStyle=fc;ctx.font='bold 24px Segoe UI';ctx.textAlign='center';
ctx.globalAlpha=Math.min(1,feedbackTimer);ctx.fillText(feedback,W/2,H-65);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(state==='play'&&!found){timeLeft-=dt;
if(timeLeft<=5&&!hintShown){hintShown=true}
if(timeLeft<=0){timeLeft=0;snd(false);feedback='Süre doldu!';feedbackTimer=2;found=true;
if(hiddenObj)hiddenObj.found=true;
setTimeout(()=>{round++;if(round>maxRound)state='win';else genScene()},2000)}}
if(feedbackTimer>0)feedbackTimer-=dt;
if(revealTimer>0)revealTimer-=dt;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function handleClick(mx,my){
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=1;genScene()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;genScene()}return}
if(state!=='play'||found)return;
if(!hiddenObj)return;
let dist=Math.hypot(mx-hiddenObj.x,my-hiddenObj.y);
if(dist<45){found=true;hiddenObj.found=true;score+=10;snd(true);
addP(hiddenObj.x,hiddenObj.y,'#fbbf24');feedback='Buldun! +10';feedbackTimer=2;
revealCircle={x:hiddenObj.x,y:hiddenObj.y};revealTimer=1.5;
setTimeout(()=>{round++;if(round>maxRound)state='win';else genScene()},1800)}
else if(dist<120){feedback='Yakın! Biraz daha...';feedbackTimer=1.2}
else{feedback='Uzak, başka yere bak!';feedbackTimer=1}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);handleClick(mx,my)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);handleClick(mx,my)});
genScene();requestAnimationFrame(upd);
</script></body></html>"""


def _build_prek_ab_ritim_taklidi_html():
    """Ritim Taklidi — Bilgisayarın çaldığı ritmi tekrarla."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let round=1,maxRound=10,score=0,state='start',particles=[];
let phase='listen',pattern=[],playerTaps=[],patternIdx=0;
let beatTimer=0,listenTimer=0,feedback='',feedbackTimer=0;
let drumGlow=0,drumScale=1,playbackDone=false,playerDone=false;
let showBeatIdx=-1,replayCount=0,maxReplay=2;
let tempo=600,tolerance=300;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function drumSnd(){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=200;o.type='triangle';g.gain.value=0.4;o.start();o.frequency.exponentialRampToValueAtTime(60,a.currentTime+0.15);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.3);o.stop(a.currentTime+0.3)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function drawRoundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function genPattern(){
let numBeats=round<=3?2:(round<=7?3:4);
tempo=round<=3?700:(round<=7?550:450);
tolerance=round<=5?350:250;
pattern=[];
for(let i=0;i<numBeats;i++){
let gap=i===0?0:(tempo+Math.floor(Math.random()*200));
pattern.push({time:i===0?0:pattern[i-1].time+gap})}
playerTaps=[];patternIdx=0;playbackDone=false;playerDone=false;
showBeatIdx=-1;replayCount=0;
phase='listen';listenTimer=0;
playPattern()}
function playPattern(){
phase='listen';showBeatIdx=-1;
let baseTime=performance.now()+500;
pattern.forEach((b,i)=>{
setTimeout(()=>{drumSnd();drumGlow=1;drumScale=1.15;showBeatIdx=i},500+b.time)});
setTimeout(()=>{playbackDone=true;phase='play';playerTaps=[];
listenTimer=pattern[pattern.length-1].time+tempo*2},500+pattern[pattern.length-1].time+600)}
function checkRhythm(){
if(playerTaps.length!==pattern.length){return false}
if(pattern.length<=1)return true;
let pIntervals=[];let uIntervals=[];
for(let i=1;i<pattern.length;i++)pIntervals.push(pattern[i].time-pattern[i-1].time);
for(let i=1;i<playerTaps.length;i++)uIntervals.push(playerTaps[i]-playerTaps[i-1]);
for(let i=0;i<pIntervals.length;i++){
if(Math.abs(pIntervals[i]-uIntervals[i])>tolerance)return false}
return true}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🥁 Ritim Taklidi',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Ritmi dinle ve tekrarla!',W/2,230);
ctx.fillText('Davula doğru zamanda vur.',W/2,260);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,300,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Ritim Ustası! 🎉',W/2,180);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,230);ctx.font='20px Segoe UI';ctx.fillText('Harika ritim duygun var!',W/2,270);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'  Puan: '+score,W/2,25);
let phaseText=phase==='listen'?'🎵 Dinle...':'🎯 Sıra sende!';
ctx.fillStyle=phase==='listen'?'#fbbf24':'#10b981';ctx.font='bold 22px Segoe UI';
ctx.fillText(phaseText,W/2,60);
let totalT=pattern.length>0?pattern[pattern.length-1].time+tempo:tempo*3;
let tlX=100,tlY=110,tlW=W-200;
ctx.fillStyle='#1e1b4b';drawRoundRect(tlX-10,tlY-25,tlW+20,50,10);ctx.fill();
ctx.strokeStyle='#a78bfa40';ctx.lineWidth=1;ctx.strokeRect(tlX,tlY,tlW,2);
for(let i=0;i<pattern.length;i++){
let bx=tlX+(pattern[i].time/totalT)*tlW;
let filled=(phase==='listen'&&showBeatIdx>=i)||(phase==='play');
ctx.fillStyle=filled?'#fbbf24':'#a78bfa40';
ctx.beginPath();ctx.arc(bx,tlY,12,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#1a0533';ctx.font='bold 10px Segoe UI';ctx.fillText(i+1,bx,tlY+4)}
if(phase==='play'&&playerTaps.length>0){
for(let i=0;i<playerTaps.length;i++){
let relT=playerTaps[i]-playerTaps[0];
if(pattern.length>1){let patTotal=pattern[pattern.length-1].time;
let bx=tlX+(relT/Math.max(patTotal,totalT))*tlW;
ctx.fillStyle='#10b981';ctx.beginPath();ctx.arc(bx,tlY+25,8,0,Math.PI*2);ctx.fill()}}
ctx.fillStyle='#10b98180';ctx.font='12px Segoe UI';ctx.fillText('Senin vuruşların',W/2,tlY+50)}
let drumX=W/2,drumY=340,drumR=90*drumScale;
let dg=ctx.createRadialGradient(drumX,drumY,drumR*0.2,drumX,drumY,drumR);
dg.addColorStop(0,drumGlow>0.3?'#fbbf24':'#7c3aed');dg.addColorStop(0.6,drumGlow>0.3?'#f59e0b':'#6d28d9');
dg.addColorStop(1,drumGlow>0.3?'#dc2626':'#4c1d95');
ctx.fillStyle=dg;ctx.beginPath();ctx.arc(drumX,drumY,drumR,0,Math.PI*2);ctx.fill();
ctx.strokeStyle='#fbbf2480';ctx.lineWidth=4;ctx.beginPath();ctx.arc(drumX,drumY,drumR,0,Math.PI*2);ctx.stroke();
ctx.strokeStyle='#fbbf2440';ctx.lineWidth=2;ctx.beginPath();ctx.arc(drumX,drumY,drumR*0.6,0,Math.PI*2);ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 28px Segoe UI';ctx.fillText('🥁',drumX,drumY+10);
if(phase==='play'){ctx.fillStyle='#e9d5ff80';ctx.font='14px Segoe UI';
ctx.fillText('Davula tıkla! ('+playerTaps.length+'/'+pattern.length+')',W/2,drumY+drumR+30)}
if(phase==='listen'){ctx.fillStyle='#a78bfa60';ctx.font='14px Segoe UI';
ctx.fillText('Ritmi dinliyorsun...',W/2,drumY+drumR+30)}
ctx.fillStyle='#a78bfa40';ctx.font='13px Segoe UI';
let beatText=pattern.length+' vuruş'+(round>=8?' - Hızlı!':'');
ctx.fillText(beatText,W/2,drumY+drumR+55);
if(phase==='play'&&replayCount<maxReplay){
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-60,H-80,120,35,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.fillText('Tekrar Dinle',W/2,H-58)}
if(feedbackTimer>0){let fc=feedback.includes('Harika')||feedback.includes('+')?'#10b981':'#ef4444';
ctx.fillStyle=fc;ctx.font='bold 24px Segoe UI';ctx.textAlign='center';
ctx.globalAlpha=Math.min(1,feedbackTimer);ctx.fillText(feedback,W/2,H-110);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(drumGlow>0){drumGlow-=dt*3;if(drumGlow<0)drumGlow=0}
if(drumScale>1){drumScale-=dt*2;if(drumScale<1)drumScale=1}
if(feedbackTimer>0)feedbackTimer-=dt;
if(state==='play'&&phase==='play'&&!playerDone){
listenTimer-=dt*1000;
if(listenTimer<=0&&playerTaps.length<pattern.length){
playerDone=true;snd(false);feedback='Süre doldu! Tekrar dene.';feedbackTimer=2;
setTimeout(()=>{genPattern()},2000)}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function tapDrum(){
if(phase!=='play'||playerDone)return;
drumSnd();drumGlow=1;drumScale=1.15;addP(W/2+(Math.random()-0.5)*60,340+(Math.random()-0.5)*60,'#fbbf24');
playerTaps.push(performance.now());
if(playerTaps.length>=pattern.length){
playerDone=true;
setTimeout(()=>{
if(checkRhythm()){score+=10;snd(true);addP(W/2,340,'#10b981');
feedback='Harika! +10';feedbackTimer=2;
round++;if(round>maxRound){setTimeout(()=>{state='win'},1000)}else{setTimeout(genPattern,1500)}}
else{snd(false);feedback='Ritim uyuşmadı, tekrar!';feedbackTimer=2;
setTimeout(genPattern,2000)}},300)}}
function handleClick(mx,my){
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=1;genPattern()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;genPattern()}return}
if(state!=='play')return;
let drumDist=Math.hypot(mx-W/2,my-340);
if(drumDist<100&&phase==='play'){tapDrum();return}
if(phase==='play'&&replayCount<maxReplay&&mx>W/2-60&&mx<W/2+60&&my>H-80&&my<H-45){
replayCount++;playerTaps=[];playerDone=false;playPattern();return}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);handleClick(mx,my)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);handleClick(mx,my)});
document.addEventListener('keydown',e=>{if(e.code==='Space'&&state==='play'&&phase==='play'){e.preventDefault();tapDrum()}});
genPattern();requestAnimationFrame(upd);
</script></body></html>"""


def _build_prek_ab_hikaye_siralama_html():
    """Hikâye Sıralama (3 Kart) — Kartları doğru sıraya koy."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let round=1,maxRound=10,score=0,state='start',particles=[];
let cards=[],selectedOrder=[],feedback='',feedbackTimer=0;
let animPhase='',animTimer=0,storyPlaying=false;
const STORIES3=[
{title:'Çiçek Büyüyor',cards:[
{emoji:'\uD83C\uDF31',label:'Tohum',bg:'#92400e',desc:'Tohum ekildi'},
{emoji:'\uD83C\uDF3F',label:'Filiz',bg:'#16a34a',desc:'Filiz çıktı'},
{emoji:'\uD83C\uDF38',label:'Çiçek',bg:'#ec4899',desc:'Çiçek açtı'}]},
{title:'Tavuk Doğuyor',cards:[
{emoji:'\uD83E\uDD5A',label:'Yumurta',bg:'#fbbf24',desc:'Yumurta var'},
{emoji:'\uD83D\uDC23',label:'Civciv',bg:'#facc15',desc:'Civciv çıktı'},
{emoji:'\uD83D\uDC14',label:'Tavuk',bg:'#dc2626',desc:'Tavuk oldu'}]},
{title:'Gökkuşağı',cards:[
{emoji:'\u2600\uFE0F',label:'Güneş',bg:'#f59e0b',desc:'Güneş parlıyor'},
{emoji:'\uD83C\uDF27\uFE0F',label:'Yağmur',bg:'#3b82f6',desc:'Yağmur yağdı'},
{emoji:'\uD83C\uDF08',label:'Gökkuşağı',bg:'#a855f7',desc:'Gökkuşağı çıktı'}]},
{title:'Buz Erir',cards:[
{emoji:'\uD83E\uDDCA',label:'Buz',bg:'#67e8f9',desc:'Buz var'},
{emoji:'\uD83D\uDCA7',label:'Su',bg:'#2563eb',desc:'Buz eridi'},
{emoji:'\u2601\uFE0F',label:'Buhar',bg:'#9ca3af',desc:'Su buharlaştı'}]},
{title:'Gece ve Gündüz',cards:[
{emoji:'\uD83C\uDF19',label:'Gece',bg:'#1e1b4b',desc:'Gece karanlık'},
{emoji:'\uD83C\uDF05',label:'Şafak',bg:'#f97316',desc:'Güneş doğuyor'},
{emoji:'\u2600\uFE0F',label:'Gündüz',bg:'#fbbf24',desc:'Gündüz oldu'}]},
{title:'Kek Yapımı',cards:[
{emoji:'\uD83E\uDD5A\uD83C\uDF5E',label:'Malzeme',bg:'#92400e',desc:'Malzemeleri hazırla'},
{emoji:'\uD83C\uDF75',label:'Pişir',bg:'#dc2626',desc:'Fırına koy'},
{emoji:'\uD83C\uDF82',label:'Kek',bg:'#ec4899',desc:'Kek hazır!'}]},
{title:'Ağaç Mevsimi',cards:[
{emoji:'\uD83C\uDF3E',label:'Sonbahar',bg:'#b45309',desc:'Yapraklar döküldü'},
{emoji:'\u2744\uFE0F',label:'Kış',bg:'#bfdbfe',desc:'Kar yağdı'},
{emoji:'\uD83C\uDF3C',label:'İlkbahar',bg:'#16a34a',desc:'Çiçekler açtı'}]}
];
const STORIES4=[
{title:'Kurbağa Büyür',cards:[
{emoji:'\uD83D\uDCA7',label:'Yumurta',bg:'#3b82f6',desc:'Suda yumurta'},
{emoji:'\uD83D\uDC1B',label:'Larva',bg:'#65a30d',desc:'Larva çıktı'},
{emoji:'\uD83E\uDD8E',label:'Küçük',bg:'#16a34a',desc:'Kuyruklu'},
{emoji:'\uD83D\uDC38',label:'Kurbağa',bg:'#15803d',desc:'Kurbağa oldu'}]},
{title:'Pasta Yap',cards:[
{emoji:'\uD83D\uDED2',label:'Alışveriş',bg:'#6366f1',desc:'Market'},
{emoji:'\uD83E\uDD5A',label:'Hazırla',bg:'#f59e0b',desc:'Karıştır'},
{emoji:'\uD83C\uDF75',label:'Pişir',bg:'#dc2626',desc:'Fırında'},
{emoji:'\uD83C\uDF70',label:'Ye!',bg:'#ec4899',desc:'Afiyet olsun'}]},
{title:'Yağmur Döngüsü',cards:[
{emoji:'\u2600\uFE0F',label:'Güneş',bg:'#fbbf24',desc:'Isıtır'},
{emoji:'\uD83D\uDCA8',label:'Buhar',bg:'#94a3b8',desc:'Buharlaşır'},
{emoji:'\u2601\uFE0F',label:'Bulut',bg:'#64748b',desc:'Bulut olur'},
{emoji:'\uD83C\uDF27\uFE0F',label:'Yağmur',bg:'#2563eb',desc:'Yağar'}]}
];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function drawRoundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function genRound(){
let use4=round>=8;
let pool=use4?STORIES4:STORIES3;
let si=(round-1)%pool.length;
let story=pool[si];
let numCards=story.cards.length;
let cw=use4?130:160,ch=200,gap=20;
let totalW=numCards*cw+(numCards-1)*gap;
let startX=(W-totalW)/2;
let correctCards=story.cards.map((c,i)=>({...c,correctIdx:i}));
let shuffled=shuffle(correctCards.slice());
let tries=0;
while(tries<20){let ok=false;for(let i=0;i<shuffled.length;i++){if(shuffled[i].correctIdx!==i){ok=true;break}}
if(ok)break;shuffle(shuffled);tries++}
cards=shuffled.map((c,i)=>({...c,x:startX+i*(cw+gap),y:240,w:cw,h:ch,selected:false,orderNum:-1,displayIdx:i}));
selectedOrder=[];feedback='';feedbackTimer=0;animPhase='';storyPlaying=false}
function drawCard(c,idx){
let x=c.x,y=c.y,w=c.w,h=c.h;
ctx.fillStyle=c.bg+'40';ctx.strokeStyle=c.selected?'#fbbf24':c.bg;ctx.lineWidth=c.selected?4:2;
drawRoundRect(x,y,w,h,15);ctx.fill();ctx.stroke();
if(c.selected){ctx.fillStyle=c.bg+'20';drawRoundRect(x,y,w,h,15);ctx.fill()}
ctx.fillStyle='#fff';ctx.font=(w>140?'50':'40')+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(c.emoji,x+w/2,y+h*0.35);
ctx.font='bold 16px Segoe UI';ctx.textBaseline='alphabetic';ctx.fillStyle='#e9d5ff';
ctx.fillText(c.label,x+w/2,y+h*0.65);
ctx.font='13px Segoe UI';ctx.fillStyle='#a78bfa';
ctx.fillText(c.desc,x+w/2,y+h*0.8);
if(c.orderNum>=0){
ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(x+w-15,y+15,18,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#1a0533';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(c.orderNum+1,x+w-15,y+16);ctx.textBaseline='alphabetic'}}
function playStoryAnim(){
storyPlaying=true;animTimer=0;
let sorted=cards.slice().sort((a,b)=>a.correctIdx-b.correctIdx);
let delay=0;
sorted.forEach((c,i)=>{
setTimeout(()=>{c.selected=true;addP(c.x+c.w/2,c.y+c.h/2,c.bg)},delay);
delay+=600});
setTimeout(()=>{
storyPlaying=false;
round++;if(round>maxRound){state='win'}else{genRound()}
},delay+800)}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('📖 Hikâye Sıralama',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Kartları doğru sıraya koy!',W/2,230);
ctx.fillText('Hikâyeyi baştan sona sırala.',W/2,260);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,300,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎉 Hikâye Ustası! 🎉',W/2,180);ctx.font='24px Segoe UI';
ctx.fillText('Puan: '+score,W/2,230);ctx.font='20px Segoe UI';ctx.fillText('Tüm hikayeleri doğru sıraladın!',W/2,270);
ctx.fillStyle='#a78bfa';drawRoundRect(W/2-80,310,160,50,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'  Puan: '+score,W/2,25);
let use4=round>=8;let pool=use4?STORIES4:STORIES3;
let si=(round-1)%pool.length;let story=pool[si];
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';
ctx.fillText('📖 '+story.title,W/2,65);
ctx.fillStyle='#a78bfa80';ctx.font='16px Segoe UI';
ctx.fillText('Kartlara sırasıyla tıkla: 1., 2., 3.'+(cards.length>3?', 4.':''),W/2,95);
ctx.fillStyle='#e9d5ff60';ctx.font='14px Segoe UI';
let instText='Önce ne oldu? Sonra? En son?';
ctx.fillText(instText,W/2,120);
for(let i=0;i<cards.length;i++){drawCard(cards[i],i)}
let numSel=selectedOrder.length;
ctx.fillStyle='#a78bfa';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
let progress='Seçilen: '+numSel+'/'+cards.length;
ctx.fillText(progress,W/2,490);
if(numSel>0&&numSel<cards.length){
ctx.fillStyle='#ef444480';drawRoundRect(W/2-50,510,100,30,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 13px Segoe UI';ctx.fillText('Sıfırla',W/2,530)}
if(feedbackTimer>0){let fc=feedback.includes('Doğru')||feedback.includes('Bravo')?'#10b981':'#ef4444';
ctx.fillStyle=fc;ctx.font='bold 26px Segoe UI';ctx.textAlign='center';
ctx.globalAlpha=Math.min(1,feedbackTimer);ctx.fillText(feedback,W/2,580);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(feedbackTimer>0)feedbackTimer-=dt;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function resetSelection(){
selectedOrder=[];cards.forEach(c=>{c.selected=false;c.orderNum=-1});feedback='';feedbackTimer=0}
function handleClick(mx,my){
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;round=1;genRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;genRound()}return}
if(state!=='play'||storyPlaying)return;
if(selectedOrder.length>0&&selectedOrder.length<cards.length){
if(mx>W/2-50&&mx<W/2+50&&my>510&&my<540){resetSelection();return}}
for(let i=0;i<cards.length;i++){const c=cards[i];
if(mx>=c.x&&mx<=c.x+c.w&&my>=c.y&&my<=c.y+c.h&&!c.selected){
c.selected=true;c.orderNum=selectedOrder.length;
selectedOrder.push(i);
addP(c.x+c.w/2,c.y+c.h/2,'#a78bfa');
if(selectedOrder.length===cards.length){
let correct=true;
for(let j=0;j<selectedOrder.length;j++){
if(cards[selectedOrder[j]].correctIdx!==j){correct=false;break}}
if(correct){score+=10;snd(true);feedback='Doğru sıra! Bravo! +10';feedbackTimer=2;
setTimeout(()=>{playStoryAnim()},500)}
else{snd(false);feedback='Tekrar dene! Sıra yanlış.';feedbackTimer=2;
setTimeout(()=>{resetSelection()},1800)}}
return}}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);handleClick(mx,my)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);handleClick(mx,my)});
genRound();requestAnimationFrame(upd);
</script></body></html>"""
