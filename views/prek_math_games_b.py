# -*- coding: utf-8 -*-
"""Okul Öncesi Matematik Oyunları 6-10."""


def _build_prek_math_buyuk_kucuk_html():
    """Büyük-Küçük Sıralama — Nesneleri boyutuna göre sırala."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const EMOJIS=['🐱','🐶','🐻','🐸','🦊','🐰','🍎','🍊','🍇','🚗','🏠','⭐'];
let items=[],slots=[],dragging=null,dx=0,dy=0,round=1,maxRound=10,score=0,state='start',particles=[],ascending=true;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#fbbf24',r:3+Math.random()*3})}
function setup(){const cnt=Math.min(3+Math.floor(round/3),5);const emoji=EMOJIS[Math.floor(Math.random()*EMOJIS.length)];ascending=Math.random()>.5;
const sizes=[];for(let i=0;i<cnt;i++)sizes.push(24+i*12);
items=sizes.map((sz,i)=>({emoji,sz,order:i,placed:-1,x:80+Math.random()*(W-160),y:150+Math.random()*200}));
items.sort(()=>Math.random()-.5);slots=[];for(let i=0;i<cnt;i++)slots.push({x:W/(cnt+1)*(i+1),y:500,filled:false})}
function check(){const p=items.filter(it=>it.placed>=0);if(p.length<items.length)return false;
const s=[...p].sort((a,b)=>a.placed-b.placed);
return ascending?s.every((it,i)=>it.order===i):s.every((it,i)=>it.order===items.length-1-i)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('📏 Büyük-Küçük Sıralama',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Nesneleri boyutuna göre sırala!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Mükemmel! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxRound+'  Puan: '+score,W/2,35);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText(ascending?'Küçükten → Büyüğe Sırala':'Büyükten → Küçüğe Sırala',W/2,70);
slots.forEach((s,i)=>{ctx.strokeStyle='#a78bfa60';ctx.lineWidth=2;ctx.setLineDash([5,5]);ctx.beginPath();ctx.roundRect(s.x-35,s.y-35,70,70,10);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#a78bfa40';ctx.font='16px Segoe UI';ctx.fillText((i+1)+'.',s.x,s.y+55)});
items.forEach(it=>{const px=it.placed>=0?slots[it.placed].x:it.x,py=it.placed>=0?slots[it.placed].y:it.y;ctx.font=it.sz+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(it.emoji,px,py)});
if(items.every(it=>it.placed>=0)){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-60,590,120,45,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.fillText('Kontrol',W/2,618)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play')return;for(let i=items.length-1;i>=0;i--){const it=items[i];const px=it.placed>=0?slots[it.placed].x:it.x,py=it.placed>=0?slots[it.placed].y:it.y;if(Math.hypot(m.x-px,m.y-py)<it.sz){if(it.placed>=0){slots[it.placed].filled=false;it.placed=-1}dragging=it;dx=m.x-px;dy=m.y-py;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);dragging.x=m.x-dx;dragging.y=m.y-dy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;slots.forEach((s,i)=>{if(!s.filled&&Math.hypot(dragging.x-s.x,dragging.y-s.y)<50){dragging.placed=i;s.filled=true}});dragging=null});
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'||state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setup()}return}
if(items.every(it=>it.placed>=0)&&m.x>W/2-60&&m.x<W/2+60&&m.y>590&&m.y<635){if(check()){score+=round*10;snd(true);slots.forEach(s=>addP(s.x,s.y));round++;if(round>maxRound)state='win';else setTimeout(setup,800)}else snd(false)}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_math_eksik_sayi_html():
    """Eksik Sayı Bul — Dizideki eksik sayıyı bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const ANI=['🐱','🐶','🐻','🐸','🦊','🐰','🐧','🦁','🐮','🐷'];
let seq=[],mIdx=0,mVal=0,opts=[],round=1,maxR=10,score=0,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#fbbf24',r:3+Math.random()*3})}
function gen(){const len=Math.min(5+Math.floor(round/3),8);const st=Math.floor(Math.random()*5)+1;seq=[];for(let i=0;i<len;i++)seq.push(st+i);mIdx=1+Math.floor(Math.random()*(len-2));mVal=seq[mIdx];opts=[mVal];while(opts.length<4){const r=1+Math.floor(Math.random()*15);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔢 Eksik Sayı Bul',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Dizideki eksik sayıyı bul!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Harika! 🏆',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
const cw=70,gap=10,tw=seq.length*(cw+gap)-gap,sx=(W-tw)/2;
seq.forEach((num,i)=>{const x=sx+i*(cw+gap);ctx.fillStyle=i===mIdx?'#7c3aed50':'#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(x,180,cw,90,10);ctx.fill();ctx.stroke();
if(i===mIdx){ctx.fillStyle='#fbbf24';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('?',x+cw/2,235)}else{ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.fillText(ANI[(num-1)%ANI.length],x+cw/2,215);ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.fillText(num,x+cw/2,255)}});
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText('Eksik sayı hangisi?',W/2,340);
opts.forEach((o,i)=>{const ox=W/2-150+i*85;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,370,70,70,12);ctx.fill();ctx.stroke();ctx.fillStyle='#e9d5ff';ctx.font='bold 28px Segoe UI';ctx.fillText(o,ox+35,415)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-150+i*85;if(mx>ox&&mx<ox+70&&my>370&&my<440){if(o===mVal){score+=10;snd(true);addP(ox+35,405);round++;if(round>maxR)state='win';else gen()}else snd(false)}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_math_sayi_cizgisi_html():
    """Sayı Çizgisi Zıplama — Kurbağa sayı çizgisinde zıplar."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let fPos=0,tPos=0,jAmt=0,dir='',round=1,maxR=10,score=0,state='start',jumping=false,jStart=0,fAnimY=0,particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#10b981',r:3+Math.random()*3})}
function gen(){jAmt=1+Math.floor(Math.random()*4);if(Math.random()>.3&&fPos+jAmt<=10){dir='ileri';tPos=fPos+jAmt}else if(fPos-jAmt>=0){dir='geri';tPos=fPos-jAmt}else{dir='ileri';jAmt=Math.min(10-fPos,3);tPos=fPos+jAmt}}
function nx(n){return 50+n*(W-100)/10}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🐸 Sayı Çizgisi Zıplama',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Kurbağayı doğru sayıya zıplat!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Süper! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
ctx.fillStyle='#fbbf24';ctx.font='bold 26px Segoe UI';ctx.fillText(jAmt+' '+(dir==='ileri'?'ileri ➡️':'⬅️ geri')+' zıpla!',W/2,90);
ctx.fillStyle='#e9d5ff80';ctx.font='18px Segoe UI';ctx.fillText('Kurbağa: '+fPos,W/2,120);
const ly=380;ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(40,ly);ctx.lineTo(W-40,ly);ctx.stroke();
for(let i=0;i<=10;i++){const x=nx(i);ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,ly-15);ctx.lineTo(x,ly+15);ctx.stroke();
ctx.fillStyle='#1e1b4b80';ctx.beginPath();ctx.arc(x,ly,20,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(i,x,ly+45)}
ctx.font='40px Segoe UI';ctx.fillText('🐸',nx(fPos),ly-30+fAnimY);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(jumping){fAnimY=Math.sin(Date.now()/100)*-20;if(Date.now()-jStart>500){jumping=false;fAnimY=0}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;fPos=Math.floor(Math.random()*5)+2;gen()}return}
if(state!=='play'||jumping)return;
for(let i=0;i<=10;i++){if(Math.hypot(mx-nx(i),my-380)<25){if(i===tPos){score+=10;snd(true);fPos=tPos;jumping=true;jStart=Date.now();addP(nx(tPos),350);round++;if(round>maxR)state='win';else setTimeout(gen,600)}else snd(false);break}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_math_topla_besle_html():
    """Topla ve Besle — Hayvanı doğru sayıda meyve ile besle."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const ANIM=['🐱','🐶','🐻','🐰','🐸','🦊','🐧','🐷'];
const FRUIT=['🍎','🍊','🍇','🍌','🍓','🍑'];
let animal='',fruit='',target=0,collected=0,fPos=[],round=1,maxR=10,score=0,state='start',particles=[],happy=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#fbbf24',r:3+Math.random()*3})}
function gen(){animal=ANIM[Math.floor(Math.random()*ANIM.length)];fruit=FRUIT[Math.floor(Math.random()*FRUIT.length)];target=2+Math.floor(Math.random()*8);collected=0;fPos=[];for(let i=0;i<target+4;i++)fPos.push({x:40+Math.random()*(W-80),y:220+Math.random()*250,alive:true,w:Math.random()*Math.PI*2})}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🍎 Topla ve Besle',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Hayvanı doğru sayıda meyve ile besle!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Hayvanlar Tok! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
ctx.font='55px Segoe UI';ctx.fillText(happy>0?animal+'😋':animal,W/2,115);
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2+40,55,180,40,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText(target+' tane '+fruit+' topla!',W/2+50,80);
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Toplanan: '+collected+'/'+target,W/2,175);
ctx.fillStyle='#1e1b4b';ctx.fillRect(W/2-100,185,200,12);ctx.fillStyle=collected<=target?'#10b981':'#ef4444';ctx.fillRect(W/2-100,185,Math.min(collected/target,1)*200,12);
fPos.forEach(f=>{if(!f.alive)return;f.w+=.03;ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText(fruit,f.x+Math.sin(f.w)*3,f.y)});
if(collected===target){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-65,540,130,45,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Besle! 🍽️',W/2,568)}
else if(collected>target){ctx.fillStyle='#ef4444';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Çok fazla! Tekrar dene.',W/2,555);ctx.fillStyle='#f59e0b';ctx.beginPath();ctx.roundRect(W/2-45,570,90,35,8);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('Sıfırla',W/2,593)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(happy>0)happy--;particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;gen()}return}
if(state!=='play')return;
if(collected>target&&mx>W/2-45&&mx<W/2+45&&my>570&&my<605){fPos.forEach(f=>f.alive=true);collected=0;return}
if(collected===target&&mx>W/2-65&&mx<W/2+65&&my>540&&my<585){score+=10;snd(true);happy=60;addP(W/2,100);round++;if(round>maxR)state='win';else setTimeout(gen,800);return}
fPos.forEach(f=>{if(!f.alive)return;if(Math.hypot(mx-f.x,my-f.y)<25){f.alive=false;collected++;addP(f.x,f.y);if(collected<=target)snd(true);else snd(false)}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_math_hazine_sayaci_html():
    """Hazine Sayacı — Hazinedeki mücevherleri say."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const GEMS=['💎','🪙','💰','👑','🔮','⭐'];
let gems=[],correct=0,opts=[],round=1,maxR=10,score=0,state='start',mapProg=0,sel=-1,particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#fbbf24',r:3+Math.random()*4})}
function gen(){correct=2+Math.floor(Math.random()*(round>5?16:10));const gem=GEMS[Math.floor(Math.random()*GEMS.length)];gems=[];for(let i=0;i<correct;i++)gems.push({e:gem,x:180+Math.random()*340,y:160+Math.random()*180,w:Math.random()*Math.PI*2});opts=[correct];while(opts.length<4){const r=Math.max(1,correct+Math.floor(Math.random()*5)-2);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5);sel=-1}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('💎 Hazine Sayacı',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Mücevherleri say, haritayı tamamla!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🗺️ Harita Tamamlandı!',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
ctx.fillStyle='#1e1b4b';ctx.fillRect(50,55,W-100,18);ctx.fillStyle='#fbbf24';ctx.fillRect(50,55,(W-100)*mapProg/maxR,18);
ctx.fillStyle='#e9d5ff';ctx.font='14px Segoe UI';ctx.fillText('🗺️ %'+Math.round(mapProg/maxR*100),W/2,68);
ctx.fillStyle='#1e1b4b40';ctx.strokeStyle='#a78bfa40';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(150,100,400,260,15);ctx.fill();ctx.stroke();
ctx.font='45px Segoe UI';ctx.textAlign='center';ctx.fillText('📦',W/2,130);
gems.forEach(ge=>{ge.w+=.02;ctx.font='28px Segoe UI';ctx.fillText(ge.e,ge.x+Math.sin(ge.w)*3,ge.y)});
ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.fillText('Kaç tane var?',W/2,400);
opts.forEach((o,i)=>{const ox=W/2-170+i*95;ctx.fillStyle=sel===i?'#7c3aed':'#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,420,80,65,12);ctx.fill();ctx.stroke();ctx.fillStyle='#e9d5ff';ctx.font='bold 28px Segoe UI';ctx.fillText(o,ox+40,462)});
if(sel>=0){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-55,510,110,42,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Onayla ✓',W/2,536)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;mapProg=0;gen()}return}
if(state!=='play')return;
opts.forEach((o,i)=>{const ox=W/2-170+i*95;if(mx>ox&&mx<ox+80&&my>420&&my<485)sel=i});
if(sel>=0&&mx>W/2-55&&mx<W/2+55&&my>510&&my<552){if(opts[sel]===correct){score+=10;snd(true);mapProg++;addP(W/2,470);round++;if(round>maxR)state='win';else setTimeout(gen,600)}else{snd(false);sel=-1}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""