# -*- coding: utf-8 -*-
"""Okul Öncesi Matematik Oyunları 11-15."""


def _build_prek_math_golge_eslestirme_html():
    """Gölge Eşleştirme (Sayılı) — Sayılı nesneleri gölgeleriyle eşleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const OBJ=['🚗','🏠','⭐','🌙','🎈','🐱','🐶','🍎','🌸','✈️'];
let items=[],shadows=[],dragging=null,dx=0,dy=0,round=1,maxR=10,score=0,matched=0,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#a78bfa',r:3+Math.random()*3})}
function setup(){const cnt=Math.min(3+Math.floor(round/3),5);matched=0;
const pool=[...OBJ].sort(()=>Math.random()-.5).slice(0,cnt);
items=pool.map((e,i)=>({emoji:e,num:i+1,x:60+Math.random()*200,y:130+i*90,matched:false}));
shadows=pool.map((e,i)=>({emoji:e,num:i+1,x:430+Math.random()*180,y:130+i*90,matched:false}));
shadows.sort(()=>Math.random()-.5);shadows.forEach((s,i)=>s.y=130+i*90)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('👤 Gölge Eşleştirme',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Nesneleri gölgeleriyle eşleştir!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Harika! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
ctx.fillStyle='#a78bfa60';ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText('Nesneler',150,100);ctx.fillText('Gölgeler',530,100);
// shadows (dark silhouettes)
shadows.forEach(s=>{ctx.fillStyle=s.matched?'#10b98140':'#00000080';ctx.beginPath();ctx.roundRect(s.x-30,s.y-30,60,60,10);ctx.fill();
ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=0.3;ctx.fillText(s.emoji,s.x,s.y+12);ctx.globalAlpha=1;
ctx.fillStyle='#e9d5ff60';ctx.font='bold 16px Segoe UI';ctx.fillText(s.num,s.x,s.y-20)});
// items
items.forEach(it=>{if(it.matched)return;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(it.x-30,it.y-30,60,60,10);ctx.fill();ctx.stroke();
ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.fillText(it.emoji,it.x,it.y+12);
ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.fillText(it.num,it.x,it.y-20)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play')return;
for(let i=items.length-1;i>=0;i--){const it=items[i];if(!it.matched&&Math.hypot(m.x-it.x,m.y-it.y)<35){dragging=it;dx=m.x-it.x;dy=m.y-it.y;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);dragging.x=m.x-dx;dragging.y=m.y-dy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;
shadows.forEach(s=>{if(!s.matched&&s.emoji===dragging.emoji&&Math.hypot(dragging.x-s.x,dragging.y-s.y)<60){
s.matched=true;dragging.matched=true;dragging.x=s.x;dragging.y=s.y;matched++;score+=15;snd(true);addP(s.x,s.y);
if(matched>=items.length){round++;if(round>maxR)state='win';else setTimeout(setup,600)}}});dragging=null});
cv.addEventListener('click',e=>{const m=gp(e);if(state==='start'||state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setup()}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_math_aynisinibul_html():
    """Aynısını Bul (Hızlı Göz) — 5 seviyeli hafıza kartları eşleştirme."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const SYMBOLS=['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','🌸','💎'];
const LVL_PAIRS=[3,4,5,6,8],LVL_COLS=[3,4,5,4,4],LVL_TIME=[40,45,50,55,60];
let cards=[],flipped=[],matched=new Set(),score=0,moves=0,timer=60,state='start',particles=[],lockBoard=false,level=1,maxLevel=5,lvlMsg=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#a78bfa',r:3+Math.random()*3})}
function setup(){const pc=LVL_PAIRS[Math.min(level-1,4)];const pairs=[...SYMBOLS].slice(0,pc);
cards=[...pairs,...pairs].sort(()=>Math.random()-.5).map((s,i)=>({sym:s,idx:i}));
flipped=[];matched=new Set();moves=0;timer=LVL_TIME[Math.min(level-1,4)];lockBoard=false}
function cardPos(i){const cols=LVL_COLS[Math.min(level-1,4)];const col=i%cols,row=Math.floor(i/cols);
const cw=Math.min(85,Math.floor((W-120)/cols-10));const rows=Math.ceil(cards.length/cols);
const ox=(W-cols*(cw+10))/2+5,oy=100+(400-rows*(cw+10))/2;
return{x:ox+col*(cw+10),y:oy+row*(cw+10),w:cw,h:cw}}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('👀 Aynısını Bul',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('5 seviyede kartları eşleştir!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Tüm Seviyeler Tamam! 🏆',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Toplam Puan: '+score+'  Hamle: '+moves,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('⏰ Süre Bitti!',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score+'  Seviye: '+level+'/'+maxLevel,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
const pc=LVL_PAIRS[Math.min(level-1,4)];
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Seviye: '+level+'/'+maxLevel+'  ⏱️'+Math.ceil(timer)+'s  Hamle:'+moves+'  Puan:'+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='16px Segoe UI';ctx.fillText('Eşleşen: '+matched.size/2+'/'+pc,W/2,55);
if(lvlMsg>0){ctx.fillStyle='#fbbf24';ctx.font='bold 32px Segoe UI';ctx.globalAlpha=lvlMsg/60;ctx.fillText('⬆️ Seviye '+level+'!',W/2,85);ctx.globalAlpha=1}
cards.forEach((c,i)=>{const p=cardPos(i);const isFlipped=flipped.includes(i)||matched.has(i);
ctx.fillStyle=matched.has(i)?'#10b98130':isFlipped?'#1e1b4b':'#7c3aed';
ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(p.x,p.y,p.w,p.h,10);ctx.fill();ctx.stroke();
const fs=Math.min(32,p.w-16);
if(isFlipped){ctx.font=fs+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(c.sym,p.x+p.w/2,p.y+p.h/2)}
else{ctx.fillStyle='#a78bfa';ctx.font='bold '+fs+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('?',p.x+p.w/2,p.y+p.h/2)}});
ctx.textBaseline='alphabetic';
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;function upd(t){const dt=(t-lastT)/1000;lastT=t;
if(state==='play'){timer-=dt;if(lvlMsg>0)lvlMsg--;if(timer<=0){timer=0;state='end'}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;level=1;setup()}return}
if(state!=='play'||lockBoard)return;
cards.forEach((c,i)=>{const p=cardPos(i);if(mx>p.x&&mx<p.x+p.w&&my>p.y&&my<p.y+p.h&&!flipped.includes(i)&&!matched.has(i)){
flipped.push(i);if(flipped.length===2){moves++;lockBoard=true;
const[a,b]=flipped;if(cards[a].sym===cards[b].sym){matched.add(a);matched.add(b);score+=20;snd(true);
const pa=cardPos(a),pb=cardPos(b);addP(pa.x+pa.w/2,pa.y+pa.h/2);addP(pb.x+pb.w/2,pb.y+pb.h/2);
flipped=[];lockBoard=false;if(matched.size===cards.length){level++;if(level>maxLevel){state='win'}else{lvlMsg=60;setTimeout(setup,800)}}}
else{snd(false);setTimeout(()=>{flipped=[];lockBoard=false},800)}}}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
requestAnimationFrame(upd);
</script></body></html>"""


def _build_prek_math_kutulari_doldur_html():
    """Kutuları Doldur (Miktar) — Kutuya doğru sayıda nesne ekle."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const ITEMS=['⭐','🍎','🌸','💎','🎈','🔵'];
let target=0,count=0,item='',boxItems=[],round=1,maxR=10,score=0,state='start',particles=[],dropAnim=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#fbbf24',r:3+Math.random()*3})}
function gen(){target=2+Math.floor(Math.random()*8);count=0;item=ITEMS[Math.floor(Math.random()*ITEMS.length)];boxItems=[]}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('📦 Kutuları Doldur',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Kutuya doğru sayıda nesne ekle!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Muhteşem! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
ctx.fillStyle='#fbbf24';ctx.font='bold 26px Segoe UI';ctx.fillText(target+' tane '+item+' koy!',W/2,80);
// box
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(150,130,400,280,15);ctx.fill();ctx.stroke();
// items in box
boxItems.forEach((bi,i)=>{const col=i%8,row=Math.floor(i/8);ctx.font='32px Segoe UI';ctx.textAlign='center';ctx.fillText(item,185+col*48,180+row*50)});
// counter
ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.fillText(count+' / '+target,W/2,440);
// add button
ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(W/2-100,460,90,55,12);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText('+ Ekle',W/2-55,493);
// remove button
ctx.fillStyle='#ef4444';ctx.beginPath();ctx.roundRect(W/2+10,460,90,55,12);ctx.fill();ctx.fillStyle='#fff';ctx.fillText('- Çıkar',W/2+55,493);
// confirm
if(count>0){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-60,540,120,45,10);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Tamam ✓',W/2,568)}
// drop animations
dropAnim.forEach(d=>{ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=d.life;ctx.fillText(item,d.x,d.y);ctx.globalAlpha=1});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){dropAnim.forEach(d=>{d.y+=3;d.life-=.03});dropAnim=dropAnim.filter(d=>d.life>0);
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;gen()}return}
if(state!=='play')return;
// add
if(mx>W/2-100&&mx<W/2-10&&my>460&&my<515){count++;boxItems.push(1);dropAnim.push({x:W/2,y:120,life:1});snd(true)}
// remove
if(mx>W/2+10&&mx<W/2+100&&my>460&&my<515&&count>0){count--;boxItems.pop();snd(false)}
// confirm
if(count>0&&mx>W/2-60&&mx<W/2+60&&my>540&&my<585){
if(count===target){score+=15;snd(true);addP(W/2,300);round++;if(round>maxR)state='win';else setTimeout(gen,600)}else{snd(false);count=0;boxItems=[]}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_math_mini_toplama_html():
    """Mini Toplama (Görselli) — Görsel toplama işlemi."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const EMOJI=[['🐱','kedi'],['🐶','köpek'],['🐸','kurbağa'],['🍎','elma'],['🌸','çiçek'],['⭐','yıldız'],['🎈','balon'],['🐰','tavşan']];
let a=0,b=0,answer=0,opts=[],emoji='',eName='',round=1,maxR=10,score=0,state='start',particles=[];
function snd(ok){try{const ac=new AudioContext(),o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,ac.currentTime+.4);o.stop(ac.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#10b981',r:3+Math.random()*3})}
function gen(){const e=EMOJI[Math.floor(Math.random()*EMOJI.length)];emoji=e[0];eName=e[1];
const mx=Math.min(4+round,10);a=1+Math.floor(Math.random()*mx);b=1+Math.floor(Math.random()*Math.max(1,mx-a));answer=a+b;
opts=[answer];while(opts.length<3){const r=Math.max(1,answer+Math.floor(Math.random()*5)-2);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('➕ Mini Toplama',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Resimleri say ve topla!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Matematik Dahisi! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
// group A
const startA=W/2-(a*40+30+b*40)/2;
for(let i=0;i<a;i++){ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.fillText(emoji,startA+i*40+20,200)}
// plus sign
ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.fillText('+',startA+a*40+15,200);
// group B
for(let i=0;i<b;i++){ctx.font='36px Segoe UI';ctx.fillText(emoji,startA+a*40+30+i*40+20,200)}
// equals
ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.fillText('= ?',W/2,280);
// text
ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.fillText(a+' '+eName+' + '+b+' '+eName+' = ?',W/2,340);
// options
opts.forEach((o,i)=>{const ox=W/2-130+i*100;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,380,80,70,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 30px Segoe UI';ctx.textAlign='center';ctx.fillText(o,ox+40,425)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-130+i*100;if(mx>ox&&mx<ox+80&&my>380&&my<450){
if(o===answer){score+=10;snd(true);addP(ox+40,415);round++;if(round>maxR)state='win';else gen()}else snd(false)}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_math_mini_cikarma_html():
    """Mini Çıkarma (Görselli) — Görsel çıkarma işlemi."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const EMOJI=[['🎈','balon'],['🍎','elma'],['⭐','yıldız'],['🌸','çiçek'],['🐱','kedi'],['🍊','portakal']];
let total=0,sub=0,answer=0,opts=[],emoji='',eName='',round=1,maxR=10,score=0,state='start',particles=[];
let flyAway=[],showTime=0;
function snd(ok){try{const ac=new AudioContext(),o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,ac.currentTime+.4);o.stop(ac.currentTime+.4)}catch(e){}}
function addP(x,y){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#ef4444',r:3+Math.random()*3})}
function gen(){const e=EMOJI[Math.floor(Math.random()*EMOJI.length)];emoji=e[0];eName=e[1];
const mxT=Math.min(3+round,12);total=3+Math.floor(Math.random()*mxT);sub=1+Math.floor(Math.random()*Math.min(total-1,Math.min(3+round,8)));answer=total-sub;
opts=[answer];while(opts.length<3){const r=Math.max(0,answer+Math.floor(Math.random()*5)-2);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5);
flyAway=[];for(let i=0;i<sub;i++)flyAway.push({x:W/2-((total-1)*20)+((total-sub+i)*40),y:180,vy:-2-Math.random()*2,vx:(Math.random()-.5)*3,life:1});showTime=60}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('➖ Mini Çıkarma',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Kalanları say!',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,340);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Çıkarma Ustası! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,35);
// remaining items
const sx=W/2-((answer-1)*20);
for(let i=0;i<answer;i++){ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.fillText(emoji,sx+i*40,200)}
// crossed out positions
if(showTime>0){for(let i=0;i<sub;i++){ctx.globalAlpha=.3;ctx.font='36px Segoe UI';ctx.fillText(emoji,sx+answer*40+i*40,200);
ctx.strokeStyle='#ef4444';ctx.lineWidth=3;const xx=sx+answer*40+i*40;ctx.beginPath();ctx.moveTo(xx-15,180);ctx.lineTo(xx+15,210);ctx.stroke();ctx.beginPath();ctx.moveTo(xx+15,180);ctx.lineTo(xx-15,210);ctx.stroke();ctx.globalAlpha=1}}
// flying away
flyAway.forEach(f=>{if(f.life>0){ctx.globalAlpha=f.life;ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText(emoji,f.x,f.y);ctx.globalAlpha=1}});
// text
ctx.fillStyle='#fbbf24';ctx.font='bold 26px Segoe UI';ctx.textAlign='center';
ctx.fillText(total+' '+eName+' - '+sub+' '+eName+' = ?',W/2,290);
// options
opts.forEach((o,i)=>{const ox=W/2-130+i*100;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,340,80,70,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 30px Segoe UI';ctx.textAlign='center';ctx.fillText(o,ox+40,385)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(showTime>0)showTime--;flyAway.forEach(f=>{f.x+=f.vx;f.y+=f.vy;f.life-=.015});
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>310&&my<360){state='play';score=0;round=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-130+i*100;if(mx>ox&&mx<ox+80&&my>340&&my<410){
if(o===answer){score+=10;snd(true);addP(ox+40,375);round++;if(round>maxR)state='win';else gen()}else snd(false)}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""