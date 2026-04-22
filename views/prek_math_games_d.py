# -*- coding: utf-8 -*-
"""Okul Öncesi Matematik Oyunları 16-20."""


def _build_prek_math_yon_bul_html():
    """Yön Bul Macerası — Karakteri hazineye yönlendir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let px=0,py=0,tx=0,ty=0,grid=5,level=1,maxL=10,score=0,state='start',particles=[],moves=0,maxMoves=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#fbbf24',r:3+Math.random()*4})}
function gen(){grid=Math.min(4+Math.floor(level/3),7);px=0;py=0;
tx=1+Math.floor(Math.random()*(grid-1));ty=1+Math.floor(Math.random()*(grid-1));
moves=0;maxMoves=Math.abs(tx-px)+Math.abs(ty-py)+3}
function cellXY(gx,gy){const sz=Math.min(60,400/grid);const ox=(W-grid*sz)/2,oy=120;return{x:ox+gx*sz,y:oy+gy*sz,sz}}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🧭 Yön Bul Macerası',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Karakteri hazineye götür!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Kaşif! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Seviye: '+level+'/'+maxL+'  Puan: '+score+'  Hamle: '+moves+'/'+maxMoves,W/2,35);
// grid
for(let gx=0;gx<grid;gx++)for(let gy=0;gy<grid;gy++){const c=cellXY(gx,gy);
ctx.fillStyle=(gx+gy)%2===0?'#1e1b4b':'#1e1b4b80';ctx.strokeStyle='#a78bfa30';ctx.lineWidth=1;
ctx.fillRect(c.x,c.y,c.sz,c.sz);ctx.strokeRect(c.x,c.y,c.sz,c.sz)}
// treasure
const tc=cellXY(tx,ty);ctx.font=(tc.sz*0.6)+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('💎',tc.x+tc.sz/2,tc.y+tc.sz/2);
// player
const pc=cellXY(px,py);ctx.font=(pc.sz*0.6)+'px Segoe UI';ctx.fillText('🧒',pc.x+pc.sz/2,pc.y+pc.sz/2);
ctx.textBaseline='alphabetic';
// direction hint
const dx=tx-px,dy=ty-py;let hint='';
if(dx>0)hint+='➡️ Sağ  ';if(dx<0)hint+='⬅️ Sol  ';if(dy>0)hint+='⬇️ Aşağı  ';if(dy<0)hint+='⬆️ Yukarı';
ctx.fillStyle='#fbbf2480';ctx.font='18px Segoe UI';ctx.textAlign='center';ctx.fillText('İpucu: '+hint,W/2,H-140);
// arrow buttons
const bx=W/2,by=H-80,bs=50;
ctx.fillStyle='#7c3aed';
ctx.beginPath();ctx.roundRect(bx-bs/2,by-bs*1.5,bs,bs,8);ctx.fill();ctx.fillStyle='#fff';ctx.font='24px Segoe UI';ctx.fillText('⬆️',bx,by-bs);
ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(bx-bs/2,by+bs*.5,bs,bs,8);ctx.fill();ctx.fillStyle='#fff';ctx.fillText('⬇️',bx,by+bs);
ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(bx-bs*1.5,by-bs/2,bs,bs,8);ctx.fill();ctx.fillStyle='#fff';ctx.fillText('⬅️',bx-bs,by);
ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(bx+bs*.5,by-bs/2,bs,bs,8);ctx.fill();ctx.fillStyle='#fff';ctx.fillText('➡️',bx+bs,by);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function move(ddx,ddy){const nx=px+ddx,ny=py+ddy;if(nx<0||nx>=grid||ny<0||ny>=grid)return;
px=nx;py=ny;moves++;
if(px===tx&&py===ty){score+=Math.max(1,(maxMoves-moves+1)*5);snd(true);const c=cellXY(tx,ty);addP(c.x+30,c.y+30);
level++;if(level>maxL)state='win';else setTimeout(gen,500)}
else if(moves>=maxMoves){snd(false);moves=0;px=0;py=0}}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;level=1;gen()}return}
if(state!=='play')return;
const bx=W/2,by=H-80,bs=50;
if(mx>bx-bs/2&&mx<bx+bs/2&&my>by-bs*1.5&&my<by-bs*.5)move(0,-1);
if(mx>bx-bs/2&&mx<bx+bs/2&&my>by+bs*.5&&my<by+bs*1.5)move(0,1);
if(mx>bx-bs*1.5&&mx<bx-bs*.5&&my>by-bs/2&&my<by+bs/2)move(-1,0);
if(mx>bx+bs*.5&&mx<bx+bs*1.5&&my>by-bs/2&&my<by+bs/2)move(1,0)});
document.addEventListener('keydown',e=>{if(state!=='play')return;
if(e.key==='ArrowUp')move(0,-1);if(e.key==='ArrowDown')move(0,1);
if(e.key==='ArrowLeft')move(-1,0);if(e.key==='ArrowRight')move(1,0)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_math_parca_butun_html():
    """Parça-Bütün Yapboz — Şekil parçalarını birleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const CLRS=['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#ec4899'];
let pieces=[],targets=[],dragging=null,dx=0,dy=0,round=1,maxR=10,score=0,matched=0,state='start',particles=[],puzzleType=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#a78bfa',r:3+Math.random()*3})}
function setup(){matched=0;puzzleType=round%5;const clr=CLRS[round%CLRS.length];
pieces=[];targets=[];
if(puzzleType===0){// circle halves
targets=[{x:W/2-40,y:250,type:'half_l',clr,matched:false},{x:W/2+40,y:250,type:'half_r',clr,matched:false}];
pieces=[{x:100+Math.random()*150,y:400+Math.random()*100,type:'half_l',clr,matched:false},{x:450+Math.random()*150,y:400+Math.random()*100,type:'half_r',clr,matched:false}]}
else if(puzzleType===1){// square quarters
for(let i=0;i<4;i++){const col=i%2,row=Math.floor(i/2);targets.push({x:W/2-30+col*60,y:220+row*60,type:'q'+i,clr,matched:false});
pieces.push({x:80+Math.random()*(W-160),y:420+Math.random()*120,type:'q'+i,clr,matched:false})}}
else if(puzzleType===2){// triangle 2 pieces
targets=[{x:W/2,y:210,type:'tri_t',clr,matched:false},{x:W/2,y:280,type:'tri_b',clr,matched:false}];
pieces=[{x:100+Math.random()*200,y:420+Math.random()*100,type:'tri_t',clr,matched:false},{x:400+Math.random()*200,y:420+Math.random()*100,type:'tri_b',clr,matched:false}]}
else{// 3 horizontal strips
for(let i=0;i<3;i++){targets.push({x:W/2,y:200+i*50,type:'strip'+i,clr,matched:false});
pieces.push({x:80+Math.random()*(W-160),y:400+Math.random()*130,type:'strip'+i,clr,matched:false})}}
pieces.sort(()=>Math.random()-.5)}
function drawPiece(x,y,type,clr,alpha){ctx.globalAlpha=alpha||1;ctx.fillStyle=clr;
if(type==='half_l'){ctx.beginPath();ctx.arc(x+20,y,35,Math.PI/2,Math.PI*1.5);ctx.fill()}
else if(type==='half_r'){ctx.beginPath();ctx.arc(x-20,y,35,Math.PI*1.5,Math.PI/2);ctx.fill()}
else if(type.startsWith('q')){const i=parseInt(type[1]);ctx.fillRect(x-25,y-25,50,50)}
else if(type==='tri_t'){ctx.beginPath();ctx.moveTo(x,y-25);ctx.lineTo(x+30,y+10);ctx.lineTo(x-30,y+10);ctx.closePath();ctx.fill()}
else if(type==='tri_b'){ctx.beginPath();ctx.moveTo(x-30,y-10);ctx.lineTo(x+30,y-10);ctx.lineTo(x,y+25);ctx.closePath();ctx.fill()}
else if(type.startsWith('strip')){ctx.fillRect(x-50,y-15,100,30)}
ctx.globalAlpha=1}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🧩 Parça-Bütün Yapboz',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Parçaları birleştir!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Yapboz Ustası! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
ctx.fillStyle='#a78bfa40';ctx.font='16px Segoe UI';ctx.fillText('Hedef şekil',W/2,80);
// target outlines
targets.forEach(t=>{drawPiece(t.x,t.y,t.type,t.matched?t.clr+'80':t.clr+'30',t.matched?.8:.3)});
// movable pieces
pieces.forEach(p=>{if(!p.matched)drawPiece(p.x,p.y,p.type,p.clr,1)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play')return;
for(let i=pieces.length-1;i>=0;i--){if(!pieces[i].matched&&Math.hypot(m.x-pieces[i].x,m.y-pieces[i].y)<45){dragging=pieces[i];dx=m.x-pieces[i].x;dy=m.y-pieces[i].y;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);dragging.x=m.x-dx;dragging.y=m.y-dy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;
targets.forEach(t=>{if(!t.matched&&t.type===dragging.type&&Math.hypot(dragging.x-t.x,dragging.y-t.y)<55){
t.matched=true;dragging.matched=true;dragging.x=t.x;dragging.y=t.y;matched++;score+=15;snd(true);addP(t.x,t.y);
if(matched>=targets.length){round++;if(round>maxR)state='win';else setTimeout(setup,600)}}});dragging=null});
cv.addEventListener('click',e=>{const m=gp(e);if(state==='start'||state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setup()}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_math_zaman_rutini_html():
    """Zaman Rutini — Günlük aktiviteleri sırala."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const ACTS=[
{e:'🌅',n:'Uyanma',t:'07:00'},{e:'🪥',n:'Diş Fırçalama',t:'07:15'},{e:'🥣',n:'Kahvaltı',t:'07:30'},
{e:'🎒',n:'Okula Gitme',t:'08:00'},{e:'📚',n:'Ders',t:'09:00'},{e:'🍎',n:'Ara Öğün',t:'10:30'},
{e:'🎨',n:'Etkinlik',t:'11:00'},{e:'🍝',n:'Öğle Yemeği',t:'12:00'},{e:'😴',n:'Uyku Saati',t:'13:00'},
{e:'🏃',n:'Oyun',t:'15:00'},{e:'🍪',n:'Atıştırma',t:'16:00'},{e:'🛁',n:'Banyo',t:'18:00'},
{e:'🍽️',n:'Akşam Yemeği',t:'19:00'},{e:'📖',n:'Kitap Okuma',t:'20:00'},{e:'🌙',n:'Uyuma',t:'21:00'}];
let cards=[],slots=[],dragging=null,dx=0,dy=0,level=1,maxL=10,score=0,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#fbbf24',r:3+Math.random()*3})}
function setup(){const cnt=Math.min(3+level,13);
const pool=[...ACTS].slice(0,cnt);
cards=pool.map((a,i)=>({...a,order:i,placed:-1,x:50+Math.random()*(W/2-100),y:120+i*(H-200)/cnt}));
cards.sort(()=>Math.random()-.5);cards.forEach((c,i)=>c.y=120+i*(H-200)/cnt);
slots=[];for(let i=0;i<cnt;i++)slots.push({x:W/2+120,y:120+i*(H-200)/cnt,filled:false})}
function check(){const p=cards.filter(c=>c.placed>=0).sort((a,b)=>a.placed-b.placed);
return p.length===cards.length&&p.every((c,i)=>c.order===i)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🕐 Zaman Rutini',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Günlük aktiviteleri sıraya koy!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Zaman Ustası! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Seviye: '+level+'/'+maxL+'  Puan: '+score,W/2,35);
ctx.fillStyle='#fbbf24';ctx.font='18px Segoe UI';ctx.fillText('Aktiviteleri sabahtan akşama sırala!',W/2,65);
// slot areas
slots.forEach((s,i)=>{ctx.strokeStyle='#a78bfa40';ctx.lineWidth=2;ctx.setLineDash([4,4]);ctx.beginPath();ctx.roundRect(s.x-80,s.y-20,160,45,8);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#a78bfa30';ctx.font='14px Segoe UI';ctx.textAlign='center';ctx.fillText((i+1)+'.',s.x-65,s.y+5)});
// cards
cards.forEach(c=>{const cx=c.placed>=0?slots[c.placed].x:c.x,cy=c.placed>=0?slots[c.placed].y:c.y;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(cx-75,cy-18,150,40,8);ctx.fill();ctx.stroke();
ctx.font='22px Segoe UI';ctx.textAlign='center';ctx.fillText(c.e,cx-50,cy+8);
ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.fillText(c.n,cx+15,cy+7)});
if(cards.every(c=>c.placed>=0)){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-55,H-60,110,42,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Kontrol',W/2,H-34)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play')return;
for(let i=cards.length-1;i>=0;i--){const c=cards[i],cx=c.placed>=0?slots[c.placed].x:c.x,cy=c.placed>=0?slots[c.placed].y:c.y;
if(Math.abs(m.x-cx)<80&&Math.abs(m.y-cy)<25){if(c.placed>=0){slots[c.placed].filled=false;c.placed=-1}dragging=c;dx=m.x-cx;dy=m.y-cy;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);dragging.x=m.x-dx;dragging.y=m.y-dy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;slots.forEach((s,i)=>{if(!s.filled&&Math.hypot(dragging.x-s.x,dragging.y-s.y)<60){dragging.placed=i;s.filled=true}});dragging=null});
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'||state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;level=1;setup()}return}
if(cards.every(c=>c.placed>=0)&&m.x>W/2-55&&m.x<W/2+55&&m.y>H-60&&m.y<H-18){
if(check()){score+=level*20;snd(true);cards.forEach(c=>{if(c.placed>=0)addP(slots[c.placed].x,slots[c.placed].y)});
level++;if(level>maxL)state='win';else setTimeout(setup,800)}else snd(false)}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_math_karistir_sirala_html():
    """Karıştır-Sırala (Boyut) — Nesneleri boyutuna göre sırala."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const SETS=[['🐘','🐕','🐱','🐭','🐜'],['🚌','🚗','🏍️','🛴','🛹'],['🏢','🏠','🏕️','📦','🎁'],['🌳','🌿','🌱','🍀','🌾']];
let items=[],slots=[],dragging=null,dx=0,dy=0,round=1,maxR=10,score=0,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#fbbf24',r:3+Math.random()*3})}
function setup(){const cnt=Math.min(3+Math.floor(round/3),5);
const set=SETS[round%SETS.length].slice(0,cnt);
items=set.map((e,i)=>({emoji:e,sz:20+i*10,order:i,placed:-1,x:60+Math.random()*(W-120),y:150+Math.random()*200}));
items.sort(()=>Math.random()-.5);
slots=[];for(let i=0;i<cnt;i++)slots.push({x:W/(cnt+1)*(i+1),y:500,filled:false})}
function check(){const p=items.filter(it=>it.placed>=0).sort((a,b)=>a.placed-b.placed);
return p.length===items.length&&p.every((it,i)=>it.order===i)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('📐 Karıştır-Sırala',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Nesneleri büyükten küçüğe sırala!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Sıralama Ustası! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';ctx.fillText('Büyükten → Küçüğe Sırala',W/2,70);
slots.forEach((s,i)=>{ctx.strokeStyle='#a78bfa50';ctx.lineWidth=2;ctx.setLineDash([5,5]);ctx.beginPath();ctx.roundRect(s.x-35,s.y-35,70,70,10);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#a78bfa30';ctx.font='14px Segoe UI';ctx.textAlign='center';ctx.fillText((i+1),s.x,s.y+52)});
items.forEach(it=>{const px=it.placed>=0?slots[it.placed].x:it.x,py=it.placed>=0?slots[it.placed].y:it.y;
ctx.font=it.sz+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(it.emoji,px,py)});
ctx.textBaseline='alphabetic';
if(items.every(it=>it.placed>=0)){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-55,590,110,42,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Kontrol',W/2,616)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play')return;
for(let i=items.length-1;i>=0;i--){const it=items[i],px=it.placed>=0?slots[it.placed].x:it.x,py=it.placed>=0?slots[it.placed].y:it.y;
if(Math.hypot(m.x-px,m.y-py)<it.sz){if(it.placed>=0){slots[it.placed].filled=false;it.placed=-1}dragging=it;dx=m.x-px;dy=m.y-py;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);dragging.x=m.x-dx;dragging.y=m.y-dy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;slots.forEach((s,i)=>{if(!s.filled&&Math.hypot(dragging.x-s.x,dragging.y-s.y)<50){dragging.placed=i;s.filled=true}});dragging=null});
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'||state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setup()}return}
if(items.every(it=>it.placed>=0)&&m.x>W/2-55&&m.x<W/2+55&&m.y>590&&m.y<632){
if(check()){score+=round*10;snd(true);slots.forEach(s=>addP(s.x,s.y));round++;if(round>maxR)state='win';else setTimeout(setup,800)}else snd(false)}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_math_sihirli_kapilar_html():
    """Sihirli Kapılar (Kural Oyunu) — Kurala göre doğru kapıyı seç."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const RULES=[
{q:'Çift sayının kapısını aç!',test:n=>n%2===0},
{q:'Tek sayının kapısını aç!',test:n=>n%2===1},
{q:'5ten büyük sayının kapısını aç!',test:n=>n>5},
{q:'3ten küçük sayının kapısını aç!',test:n=>n<3},
{q:'En büyük sayının kapısını aç!',test:null,type:'max'},
{q:'En küçük sayının kapısını aç!',test:null,type:'min'}];
let doors=[],rule=null,correctDoor=-1,round=1,maxR=10,score=0,state='start',particles=[],openDoor=-1,showResult=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<20;i++)particles.push({x,y,vx:(Math.random()-.5)*8,vy:(Math.random()-.5)*8,life:1,clr:'#fbbf24',r:3+Math.random()*5})}
function gen(){rule=RULES[Math.floor(Math.random()*RULES.length)];
let nums;
if(rule.type==='max'||rule.type==='min'){
nums=new Set();while(nums.size<3){nums.add(1+Math.floor(Math.random()*10))}
doors=[...nums].map((n,i)=>({num:n,x:120+i*220,y:280}));
if(rule.type==='max'){const mx=Math.max(...doors.map(d=>d.num));correctDoor=doors.findIndex(d=>d.num===mx)}
else{const mn=Math.min(...doors.map(d=>d.num));correctDoor=doors.findIndex(d=>d.num===mn)}}
else{// Ensure exactly one door matches
const ci=Math.floor(Math.random()*3);const good=rule.q.includes('Çift')?[2,4,6,8,10]:rule.q.includes('Tek')?[1,3,5,7,9]:rule.q.includes('büyük')?[6,7,8,9,10]:[1,2];
const bad=rule.q.includes('Çift')?[1,3,5,7,9]:rule.q.includes('Tek')?[2,4,6,8,10]:rule.q.includes('büyük')?[1,2,3,4,5]:[3,4,5,6,7,8,9,10];
const gv=good[Math.floor(Math.random()*good.length)];
const bv=[];while(bv.length<2){const r=bad[Math.floor(Math.random()*bad.length)];if(!bv.includes(r)&&r!==gv)bv.push(r)}
const dn=[];for(let i=0;i<3;i++)dn.push(i===ci?gv:bv[i<ci?i:i-1]);
doors=dn.map((n,i)=>({num:n,x:120+i*220,y:280}));correctDoor=ci}
openDoor=-1;showResult=0}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🚪 Sihirli Kapılar',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Kurala göre doğru kapıyı aç!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Kural Ustası! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
// rule
ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.fillText(rule.q,W/2,100);
// doors
doors.forEach((d,i)=>{const dx=d.x,dy=d.y;
// door frame
ctx.fillStyle=openDoor===i?(i===correctDoor?'#10b98180':'#ef444480'):'#7c3aed';
ctx.beginPath();ctx.roundRect(dx-50,dy-80,100,180,12);ctx.fill();
ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(dx-50,dy-80,100,180,12);ctx.stroke();
// doorknob
ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(dx+30,dy+20,8,0,Math.PI*2);ctx.fill();
// arch
ctx.strokeStyle='#a78bfa80';ctx.lineWidth=2;ctx.beginPath();ctx.arc(dx,dy-80,50,Math.PI,0);ctx.stroke();
// number
ctx.fillStyle='#fff';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';ctx.fillText(d.num,dx,dy+10);
// result
if(openDoor===i){ctx.font='40px Segoe UI';ctx.fillText(i===correctDoor?'💎':'💨',dx,dy-40)}});
// result message
if(showResult>0){ctx.fillStyle=openDoor===correctDoor?'#10b981':'#ef4444';ctx.font='bold 28px Segoe UI';
ctx.fillText(openDoor===correctDoor?'Doğru! 🎉':'Yanlış kapı! 😢',W/2,520)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(showResult>0){showResult--;if(showResult===0){if(openDoor===correctDoor){round++;if(round>maxR)state='win';else gen()}else gen()}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;gen()}return}
if(state!=='play'||showResult>0)return;
doors.forEach((d,i)=>{if(Math.abs(mx-d.x)<55&&my>d.y-85&&my<d.y+105){openDoor=i;
if(i===correctDoor){score+=15;snd(true);addP(d.x,d.y)}else snd(false);showResult=60}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""