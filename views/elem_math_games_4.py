# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Matematik Oyunları 16-20 (L1→L4 zorluk)."""


def _build_elem_math_asal_cift_tek_html():
    """Asal/Çift/Tek Arenası — Sınıflandırma oyunu."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=20,num=0,categories=[],correctCat='',state='start',particles=[],showRes=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function isPrime(n){if(n<2)return false;for(let i=2;i*i<=n;i++)if(n%i===0)return false;return true}
function gen(){if(level===1){num=1+Math.floor(Math.random()*20);categories=['Çift','Tek'];correctCat=num%2===0?'Çift':'Tek'}
else if(level===2){num=1+Math.floor(Math.random()*50);categories=['Çift','Tek'];correctCat=num%2===0?'Çift':'Tek'}
else if(level===3){num=2+Math.floor(Math.random()*30);categories=['Asal','Asal Değil'];correctCat=isPrime(num)?'Asal':'Asal Değil'}
else{num=2+Math.floor(Math.random()*50);if(Math.random()>.5){categories=['Asal','Asal Değil'];correctCat=isPrime(num)?'Asal':'Asal Değil'}else{categories=['Çift','Tek'];correctCat=num%2===0?'Çift':'Tek'}}
showRes=0}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🏟️ Asal/Çift/Tek Arenası',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Sayıları doğru sınıflandır!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏟️ Şampiyon!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
// number ball
ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.arc(W/2,180,60,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 40px Segoe UI';ctx.fillText(num,W/2,195);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText('Bu sayı nedir?',W/2,280);
// category buttons
categories.forEach((cat,i)=>{const bx=W/2-150+i*200,by=320;
ctx.fillStyle=i===0?'#3b82f6':'#ef4444';ctx.beginPath();ctx.roundRect(bx,by,120,60,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText(cat,bx+60,by+38)});
if(showRes>0){ctx.fillStyle=showRes===1?'#10b981':'#ef4444';ctx.font='bold 24px Segoe UI';ctx.fillText(showRes===1?'✓ Doğru!':'✗ Yanlış! → '+correctCat,W/2,440)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(showRes>0&&Date.now()-resTime>800){showRes=0;round++;if(round>maxR)state='end';else gen()}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
let resTime=0;
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
if(showRes>0)return;
categories.forEach((cat,i)=>{const bx=W/2-150+i*200,by=320;if(mx>bx&&mx<bx+120&&my>by&&my<by+60){
if(cat===correctCat){score+=level*5;snd(true);addP(bx+60,by+30,'#10b981');showRes=1;
if(score>=30&&level<2)level=2;if(score>=60&&level<3)level=3;if(score>=100&&level<4)level=4}
else{snd(false);addP(bx+60,by+30,'#ef4444');showRes=2}
resTime=Date.now()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_veri_grafigi_html():
    """Veri Grafiği Atölyesi — Resim grafiği → sütun grafiği → yorumlama."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const CATS=[['🍎','🍊','🍇','🍌'],['🐱','🐶','🐰','🐸'],['⚽','🏀','🎾','🏐']];
const NAMES=[['Elma','Portakal','Üzüm','Muz'],['Kedi','Köpek','Tavşan','Kurbağa'],['Futbol','Basket','Tenis','Voleybol']];
let level=1,score=0,round=1,maxR=10,data=[],labels=[],emojis=[],q='',ans=0,opts=[],state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function gen(){const ci=Math.floor(Math.random()*CATS.length);emojis=CATS[ci];labels=NAMES[ci];
const cnt=level<=2?3:4;data=[];for(let i=0;i<cnt;i++)data.push(1+Math.floor(Math.random()*(level<=2?8:15)));
const r=Math.random();if(level<=2){if(r<.5){const idx=Math.floor(Math.random()*cnt);q=labels[idx]+' kaç tane?';ans=data[idx]}else{q='Toplam kaç tane?';ans=data.reduce((a,b)=>a+b,0)}}
else{if(r<.3){q='En çok hangisinden var?';const mx=Math.max(...data);ans=mx;const idx=data.indexOf(mx);q='En çok olan kaç tane?'}
else if(r<.6){q='Toplam kaç tane?';ans=data.reduce((a,b)=>a+b,0)}
else{const i1=Math.floor(Math.random()*cnt);let i2=i1;while(i2===i1)i2=Math.floor(Math.random()*cnt);
q=labels[i1]+' ile '+labels[i2]+' farkı kaç?';ans=Math.abs(data[i1]-data[i2])}}
opts=[ans];while(opts.length<4){const rr=Math.max(0,ans+Math.floor(Math.random()*9)-4);if(!opts.includes(rr))opts.push(rr)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('📊 Veri Grafiği Atölyesi',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Grafikleri oku ve yorumla!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('📊 Veri Uzmanı!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
// bar chart
const maxD=Math.max(...data);const bw=80,gap=30,totalW=data.length*(bw+gap)-gap;const sx=(W-totalW)/2;
const chartH=200,chartY=350;
const BCLRS=['#ef4444','#3b82f6','#10b981','#f59e0b'];
data.forEach((d,i)=>{const x=sx+i*(bw+gap);const bh=d/maxD*chartH;
ctx.fillStyle=BCLRS[i%BCLRS.length];ctx.beginPath();ctx.roundRect(x,chartY-bh,bw,bh,6);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(d,x+bw/2,chartY-bh-8);
ctx.font='24px Segoe UI';ctx.fillText(emojis[i],x+bw/2,chartY+25);
ctx.fillStyle='#e9d5ff';ctx.font='12px Segoe UI';ctx.fillText(labels[i],x+bw/2,chartY+42)});
ctx.strokeStyle='#a78bfa40';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(sx-10,chartY);ctx.lineTo(sx+totalW+10,chartY);ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(q,W/2,420);
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=450;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,55,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.fillText(o,ox+55,oy+35)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=450;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+55){
if(o===ans){score+=level*10;snd(true);addP(ox+55,oy+27,'#10b981');
if(score>=30&&level<2)level=2;if(score>=70&&level<3)level=3;if(score>=120&&level<4)level=4}
else{snd(false);addP(ox+55,oy+27,'#ef4444')}round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_koordinat_hazine_html():
    """Koordinat Hazinesi — Basit ızgara/koordinat."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=12,gridSz=5,tx=0,ty=0,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function gen(){gridSz=level<=2?5:level===3?7:10;tx=Math.floor(Math.random()*gridSz);ty=Math.floor(Math.random()*gridSz)}
function cellXY(gx,gy){const margin=60,sz=Math.min((W-2*margin)/gridSz,(H-200)/gridSz);const ox=margin+(W-2*margin-gridSz*sz)/2;const oy=100;return{x:ox+gx*sz,y:oy+(gridSz-1-gy)*sz,sz}}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🗺️ Koordinat Hazinesi',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Koordinatı bul, hazineyi al!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🗺️ Harita Ustası!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText('Hazine: ('+tx+', '+ty+')',W/2,70);
// grid
for(let gx=0;gx<gridSz;gx++)for(let gy=0;gy<gridSz;gy++){const c=cellXY(gx,gy);
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa30';ctx.lineWidth=1;ctx.fillRect(c.x,c.y,c.sz,c.sz);ctx.strokeRect(c.x,c.y,c.sz,c.sz)}
// axis labels
for(let i=0;i<gridSz;i++){const c=cellXY(i,0);ctx.fillStyle='#a78bfa';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText(i,c.x+c.sz/2,c.y+c.sz+15);
const c2=cellXY(0,i);ctx.textAlign='right';ctx.fillText(i,c2.x-5,c2.y+c.sz/2+4)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
for(let gx=0;gx<gridSz;gx++)for(let gy=0;gy<gridSz;gy++){const c=cellXY(gx,gy);
if(mx>c.x&&mx<c.x+c.sz&&my>c.y&&my<c.y+c.sz){
if(gx===tx&&gy===ty){score+=level*10;snd(true);addP(c.x+c.sz/2,c.y+c.sz/2,'#fbbf24');
if(score>=40&&level<2)level=2;if(score>=80&&level<3)level=3;if(score>=130&&level<4)level=4;
round++;if(round>maxR)state='end';else gen()}
else{snd(false);addP(c.x+c.sz/2,c.y+c.sz/2,'#ef4444')}return}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_kesir_duello_html():
    """Kesir Karşılaştırma Duellosu — Hangisi büyük?"""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,fA={n:0,d:0},fB={n:0,d:0},ans='',state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function drawBar(cx,cy,w,h,num,den,clr){ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(cx-w/2,cy,w,h,6);ctx.fill();ctx.stroke();
const filled=num/den*w;ctx.fillStyle=clr;ctx.beginPath();ctx.roundRect(cx-w/2,cy,filled,h,6);ctx.fill()}
function gen(){const dens=level===1?[2,4]:level===2?[2,3,4,6]:level===3?[2,3,4,5,6,8]:[2,3,4,5,6,8,10,12];
if(level<=2){const d=dens[Math.floor(Math.random()*dens.length)];fA={n:1+Math.floor(Math.random()*(d-1)),d};fB={n:1+Math.floor(Math.random()*(d-1)),d};while(fA.n===fB.n)fB.n=1+Math.floor(Math.random()*(d-1))}
else{fA={d:dens[Math.floor(Math.random()*dens.length)]};fA.n=1+Math.floor(Math.random()*(fA.d-1));
fB={d:dens[Math.floor(Math.random()*dens.length)]};fB.n=1+Math.floor(Math.random()*(fB.d-1));
while(fA.n/fA.d===fB.n/fB.d){fB.d=dens[Math.floor(Math.random()*dens.length)];fB.n=1+Math.floor(Math.random()*(fB.d-1))}}
const vA=fA.n/fA.d,vB=fB.n/fB.d;ans=vA>vB?'A':vA<vB?'B':'='}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('⚔️ Kesir Duellosu',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Hangisi büyük?',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('⚔️ Kesir Şampiyonu!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
// fraction A
ctx.fillStyle='#3b82f6';ctx.font='bold 50px Segoe UI';ctx.textAlign='center';
ctx.fillText(fA.n,180,170);ctx.fillRect(155,180,50,4);ctx.fillText(fA.d,180,235);
drawBar(180,260,140,25,fA.n,fA.d,'#3b82f6');
// VS
ctx.fillStyle='#fbbf24';ctx.font='bold 30px Segoe UI';ctx.fillText('VS',W/2,200);
// fraction B
ctx.fillStyle='#ef4444';ctx.font='bold 50px Segoe UI';
ctx.fillText(fB.n,520,170);ctx.fillRect(495,180,50,4);ctx.fillText(fB.d,520,235);
drawBar(520,260,140,25,fB.n,fB.d,'#ef4444');
// choice buttons
const btns=[{lbl:'◀ Sol Büyük',val:'A',x:100,clr:'#3b82f6'},{lbl:'Eşit =',val:'=',x:W/2-55,clr:'#f59e0b'},{lbl:'Sağ Büyük ▶',val:'B',x:W-210,clr:'#ef4444'}];
btns.forEach(b=>{ctx.fillStyle=b.clr;ctx.beginPath();ctx.roundRect(b.x,370,110,55,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(b.lbl,b.x+55,403)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
const btns=[{val:'A',x:100},{val:'=',x:W/2-55},{val:'B',x:W-210}];
btns.forEach(b=>{if(mx>b.x&&mx<b.x+110&&my>370&&my<425){
if(b.val===ans){score+=level*10;snd(true);addP(b.x+55,395,'#10b981');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(b.x+55,395,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_escape_room_html():
    """Mini Matematik Escape Room — 4-6 bulmaca ile odadan çık."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,puzzles=[],pIdx=0,q='',ans=0,opts=[],solved=0,total=5,state='start',particles=[],timer=120;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function makeP(){let a,b,op,res;const r=Math.random();const d=level;
if(r<.25){a=5*d+Math.floor(Math.random()*50*d);b=5*d+Math.floor(Math.random()*50*d);op='+';res=a+b}
else if(r<.5){a=20*d+Math.floor(Math.random()*80*d);b=5+Math.floor(Math.random()*a);op='-';res=a-b}
else if(r<.75){a=2+Math.floor(Math.random()*(8+d*2));b=2+Math.floor(Math.random()*(8+d*2));op='×';res=a*b}
else{b=2+Math.floor(Math.random()*(7+d*2));res=2+Math.floor(Math.random()*(8+d*2));a=b*res;op='÷'}
return{q:a+' '+op+' '+b,ans:res}}
function genRoom(){total=4+level;puzzles=[];for(let i=0;i<total;i++)puzzles.push(makeP());pIdx=0;solved=0;loadPuzzle();timer=130-level*10}
function loadPuzzle(){if(pIdx>=total)return;q=puzzles[pIdx].q;ans=puzzles[pIdx].ans;
opts=[ans];while(opts.length<4){const r=Math.max(0,ans+Math.floor(Math.random()*11)-5);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔐 Matematik Escape Room',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('5 bulmacayı çöz, odadan kaç!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='escaped'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Kaçtın! 🎉',W/2,180);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  Süre: '+Math.ceil(timer)+'s kaldı',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,320);return}
if(state==='trapped'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('⏰ Süre Bitti!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
// room
ctx.fillStyle='#1e1b4b40';ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(40,50,W-80,H-100,15);ctx.fill();ctx.stroke();
// HUD
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  ⏱️ '+Math.ceil(timer)+'s  Puan: '+score,W/2,30);
// locks
for(let i=0;i<total;i++){ctx.font='30px Segoe UI';ctx.fillText(i<solved?'🔓':'🔒',100+i*120,100)}
// door
ctx.font='50px Segoe UI';ctx.fillText(solved>=total?'🚪✨':'🚪🔒',W/2,H-80);
// current puzzle
if(solved<total){ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.fillText('Bulmaca '+(pIdx+1)+'/'+total,W/2,170);
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2-140,190,280,60,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.fillText(q+' = ?',W/2,228);
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=290;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.fillText(o,ox+55,oy+38)})}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;function upd(t){const dt=(t-lastT)/1000;lastT=t;
if(state==='play'){timer-=dt;if(timer<=0){timer=0;state='trapped'}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='escaped'||state==='trapped'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;genRoom()}return}
if(solved>=total)return;
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=290;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+60){
if(o===ans){score+=20;solved++;snd(true);addP(100+solved*120-120,100,'#10b981');pIdx++;
if(solved>=total){level=Math.min(level+1,4);state='escaped';score+=Math.ceil(timer)*2}}
else{snd(false);addP(ox+55,oy+30,'#ef4444');timer-=5}
if(pIdx<total)loadPuzzle()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
requestAnimationFrame(upd);
</script></body></html>"""