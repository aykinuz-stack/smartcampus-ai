# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Matematik Oyunları 1-5 (L1→L4 zorluk)."""


def _build_elem_math_islem_kosusu_html():
    """İşlem Koşusu — Runner: toplama/çıkarma → çarpma/bölme."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,lives=3,question='',answer=0,opts=[],runnerX=80,groundY=480,obstacles=[],dist=0,spd=2,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function genQ(){let a,b,op;
if(level===1){a=1+Math.floor(Math.random()*20);b=1+Math.floor(Math.random()*20);op='+';answer=a+b}
else if(level===2){if(Math.random()>.4){a=1+Math.floor(Math.random()*50);b=1+Math.floor(Math.random()*50);op='+';answer=a+b}else{a=10+Math.floor(Math.random()*50);b=1+Math.floor(Math.random()*a);op='-';answer=a-b}}
else if(level===3){if(Math.random()>.5){a=2+Math.floor(Math.random()*10);b=2+Math.floor(Math.random()*10);op='×';answer=a*b}else{a=1+Math.floor(Math.random()*100);b=1+Math.floor(Math.random()*100);op=Math.random()>.5?'+':'-';answer=op==='+'?a+b:Math.abs(a-b);if(op==='-'&&a<b){const t=a;a=b;b=t;answer=a-b}}}
else{const r=Math.random();if(r<.3){a=2+Math.floor(Math.random()*12);b=2+Math.floor(Math.random()*12);op='×';answer=a*b}else if(r<.6){b=2+Math.floor(Math.random()*10);answer=1+Math.floor(Math.random()*12);a=b*answer;op='÷'}else{a=10+Math.floor(Math.random()*500);b=10+Math.floor(Math.random()*500);op=Math.random()>.5?'+':'-';answer=op==='+'?a+b:Math.abs(a-b);if(op==='-'&&a<b){const t=a;a=b;b=t;answer=a-b}}}
question=a+' '+op+' '+b+' = ?';
opts=[answer];while(opts.length<4){const r=Math.max(0,answer+Math.floor(Math.random()*11)-5);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5);
obstacles=opts.map((o,i)=>({x:300+i*100,y:groundY-30,val:o,hit:false}))}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🏃 İşlem Koşusu',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Doğru cevabı seçerek koş!',W/2,230);ctx.fillText('L1: Toplama → L4: Çarpma/Bölme',W/2,260);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,300,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,330);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText(lives>0?'🏆 Tebrikler!':'💔 Bitti!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  Seviye: L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,300,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,330);return}
// HUD
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('❤️'.repeat(lives),15,30);
ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 20px Segoe UI';ctx.fillText('L'+level,W/2,30);
ctx.fillStyle='#e9d5ff';ctx.textAlign='right';ctx.font='18px Segoe UI';ctx.fillText('Puan: '+score,W-15,30);
// ground
ctx.fillStyle='#166534';ctx.fillRect(0,groundY,W,H-groundY);
for(let x=(-dist*3)%40-40;x<W;x+=40){ctx.strokeStyle='#15803d';ctx.beginPath();ctx.moveTo(x,groundY);ctx.lineTo(x+20,groundY+20);ctx.stroke()}
// question
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2-140,50,280,50,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText(question,W/2,83);
// runner
ctx.font='40px Segoe UI';ctx.fillText('🏃',runnerX,groundY-5);
// obstacles (answer blocks)
obstacles.forEach(o=>{if(o.hit)return;
ctx.fillStyle='#7c3aed';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(o.x-30,o.y-25,60,50,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(o.val,o.x,o.y+8)});
// progress
const prog=Math.min(score/200,1);ctx.fillStyle='#1e1b4b';ctx.fillRect(50,H-30,W-100,12);
ctx.fillStyle='#10b981';ctx.fillRect(50,H-30,(W-100)*prog,12);
ctx.fillStyle='#e9d5ff';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText('İlerleme: '+Math.round(prog*100)+'%',W/2,H-20);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(state==='play'){dist+=spd;
obstacles.forEach(o=>{if(!o.hit)o.x-=spd});
if(obstacles.every(o=>o.hit||o.x<-50))genQ()}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>300&&my<350){state='play';score=0;lives=3;level=1;dist=0;genQ()}return}
obstacles.forEach(o=>{if(!o.hit&&Math.abs(mx-o.x)<35&&Math.abs(my-o.y)<30){o.hit=true;
if(o.val===answer){score+=level*10;snd(true);addP(o.x,o.y,'#10b981');
if(score>=50&&level<2)level=2;if(score>=120&&level<3)level=3;if(score>=200&&level<4)level=4;if(score>=300){state='end';lives=99}}
else{lives--;snd(false);addP(o.x,o.y,'#ef4444');if(lives<=0)state='end'}}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_toplama_cikarma_savasi_html():
    """Toplama-Çıkarma Savaşı — Doğru sonucu seç, kalkan kazan."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,shields=0,round=1,maxR=20,q='',ans=0,opts=[],timer=0,maxTime=8,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function gen(){let a,b,op;
if(level===1){a=1+Math.floor(Math.random()*20);b=1+Math.floor(Math.random()*20);op=Math.random()>.5?'+':'-';if(op==='-'&&a<b){const t=a;a=b;b=t}ans=op==='+'?a+b:a-b}
else if(level===2){a=10+Math.floor(Math.random()*90);b=10+Math.floor(Math.random()*90);op=Math.random()>.5?'+':'-';if(op==='-'&&a<b){const t=a;a=b;b=t}ans=op==='+'?a+b:a-b}
else if(level===3){a=2+Math.floor(Math.random()*12);b=2+Math.floor(Math.random()*12);op=Math.random()>.5?'×':Math.random()>.5?'+':'-';if(op==='×')ans=a*b;else{a=10+Math.floor(Math.random()*200);b=10+Math.floor(Math.random()*200);if(op==='-'&&a<b){const t=a;a=b;b=t}ans=op==='+'?a+b:a-b}}
else{const r=Math.random();if(r<.3){a=2+Math.floor(Math.random()*12);b=2+Math.floor(Math.random()*12);op='×';ans=a*b}else if(r<.5){b=2+Math.floor(Math.random()*10);ans=2+Math.floor(Math.random()*12);a=b*ans;op='÷'}else{a=100+Math.floor(Math.random()*900);b=100+Math.floor(Math.random()*900);op=Math.random()>.5?'+':'-';if(op==='-'&&a<b){const t=a;a=b;b=t}ans=op==='+'?a+b:a-b}}
q=a+' '+op+' '+b;opts=[ans];while(opts.length<4){const r=ans+Math.floor(Math.random()*21)-10;if(r>=0&&!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5);
maxTime=level===1?10:level===2?8:level===3?7:5;timer=maxTime}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('⚔️ Toplama-Çıkarma Savaşı',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Hızlı çöz, kalkan kazan!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏆 Savaş Bitti!',W/2,180);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  Kalkan: 🛡️×'+shields,W/2,230);ctx.fillText('Seviye: L'+level,W/2,270);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
// HUD
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('🛡️×'+shields,15,30);
ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR,W/2,30);
ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,30);
// timer bar
const tp=timer/maxTime;ctx.fillStyle='#1e1b4b';ctx.fillRect(100,50,W-200,16);
ctx.fillStyle=tp>.5?'#10b981':tp>.25?'#f59e0b':'#ef4444';ctx.fillRect(100,50,(W-200)*tp,16);
// question
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2-160,90,320,70,15);ctx.fill();ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 30px Segoe UI';ctx.textAlign='center';ctx.fillText(q+' = ?',W/2,135);
// options as shields
opts.forEach((o,i)=>{const ox=90+i*160,oy=250;
ctx.fillStyle='#7c3aed';ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();
ctx.moveTo(ox,oy-40);ctx.lineTo(ox+55,oy-25);ctx.lineTo(ox+55,oy+25);ctx.lineTo(ox,oy+45);ctx.lineTo(ox-55,oy+25);ctx.lineTo(ox-55,oy-25);ctx.closePath();ctx.fill();ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 24px Segoe UI';ctx.fillText(o,ox,oy+8)});
// warrior
ctx.font='60px Segoe UI';ctx.textAlign='center';ctx.fillText('⚔️',W/2,430);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;function upd(t){const dt=(t-lastT)/1000;lastT=t;
if(state==='play'){timer-=dt;if(timer<=0){timer=0;round++;if(round>maxR)state='end';else gen()}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;shields=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=90+i*160,oy=250;if(Math.hypot(mx-ox,my-oy)<55){
if(o===ans){const bonus=Math.ceil(timer);score+=level*10+bonus;shields++;snd(true);addP(ox,oy,'#10b981');
if(shields>=5&&level<2)level=2;if(shields>=12&&level<3)level=3;if(shields>=18&&level<4)level=4}
else{snd(false);addP(ox,oy,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
requestAnimationFrame(upd);
</script></body></html>"""


def _build_elem_math_carpim_kartlari_html():
    """Çarpım Kartları Koleksiyonu — Çarpım tablosu kart biriktirme."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,cards=[],collection=new Set(),a=0,b=0,ans=0,opts=[],round=1,maxR=20,state='start',particles=[];
const CARD_CLRS=['#ef4444','#f59e0b','#10b981','#3b82f6','#8b5cf6','#ec4899','#06b6d4','#f97316','#84cc16'];
function snd(ok){try{const ac=new AudioContext(),o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,ac.currentTime+.4);o.stop(ac.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function gen(){const maxN=level===1?5:level===2?7:level===3?9:12;
a=2+Math.floor(Math.random()*(maxN-1));b=2+Math.floor(Math.random()*(maxN-1));ans=a*b;
opts=[ans];while(opts.length<4){const r=Math.max(1,ans+Math.floor(Math.random()*21)-10);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🃏 Çarpım Kartları',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Çarpım tablosunu öğren, kart biriktir!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🃏 Koleksiyon!',W/2,150);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  Kart: '+collection.size,W/2,190);
// show collection grid
let ci=0;collection.forEach(key=>{const col=ci%8,row=Math.floor(ci/8);const x=80+col*72,y=220+row*50;
ctx.fillStyle=CARD_CLRS[ci%CARD_CLRS.length];ctx.beginPath();ctx.roundRect(x,y,65,40,6);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';ctx.fillText(key,x+32,y+26);ci++});
ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,H-80,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,H-50);return}
// HUD
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('🃏 '+collection.size+' kart',15,30);
ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR,W/2,30);
ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,30);
// card being offered
ctx.save();ctx.translate(W/2,200);ctx.rotate(Math.sin(Date.now()/500)*.05);
ctx.fillStyle=CARD_CLRS[(a+b)%CARD_CLRS.length];ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;
ctx.beginPath();ctx.roundRect(-70,-80,140,160,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#fff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText(a+' × '+b,0,-15);
ctx.fillStyle='#fbbf2480';ctx.font='bold 22px Segoe UI';ctx.fillText('= ?',0,25);ctx.restore();
// options
opts.forEach((o,i)=>{const ox=W/2-180+i*120,oy=400;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,100,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 26px Segoe UI';ctx.textAlign='center';ctx.fillText(o,ox+50,oy+40)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<340){state='play';score=0;collection=new Set();round=1;level=1;gen()}return}
if(state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>H-80&&my<H-30){state='play';score=0;collection=new Set();round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-180+i*120,oy=400;if(mx>ox&&mx<ox+100&&my>oy&&my<oy+60){
if(o===ans){score+=level*10;collection.add(a+'×'+b+'='+ans);snd(true);addP(W/2,200,'#fbbf24');
if(collection.size>=6&&level<2)level=2;if(collection.size>=15&&level<3)level=3;if(collection.size>=18&&level<4)level=4}
else{snd(false);addP(ox+50,oy+30,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_bolme_korsani_html():
    """Bölme Korsanı — Eşit paylaştırma → kalanlı bölme."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,total=0,divisor=0,ans=0,remainder=0,opts=[],state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function gen(){if(level<=2){divisor=2+Math.floor(Math.random()*(level===1?3:5));ans=1+Math.floor(Math.random()*(level===1?5:10));total=divisor*ans;remainder=0}
else if(level===3){divisor=2+Math.floor(Math.random()*8);total=divisor*(1+Math.floor(Math.random()*12))+Math.floor(Math.random()*divisor);ans=Math.floor(total/divisor);remainder=total%divisor}
else{divisor=3+Math.floor(Math.random()*10);total=divisor*(5+Math.floor(Math.random()*20))+Math.floor(Math.random()*divisor);ans=Math.floor(total/divisor);remainder=total%divisor}
opts=[ans];while(opts.length<4){const r=Math.max(0,ans+Math.floor(Math.random()*7)-3);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🏴‍☠️ Bölme Korsanı',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Hazineyi eşit paylaştır!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏴‍☠️ Korsan Tamamladı!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
// pirate scene
ctx.font='50px Segoe UI';ctx.fillText('🏴‍☠️',W/2,100);
// treasure items
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2-200,130,400,100,15);ctx.fill();ctx.stroke();
const gem='🪙';const perRow=Math.min(total,15);const startX=W/2-perRow*14;
for(let i=0;i<Math.min(total,30);i++){const col=i%15,row=Math.floor(i/15);
ctx.font='22px Segoe UI';ctx.fillText(gem,startX+col*28,165+row*30)}
// question
ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';
ctx.fillText(total+' ÷ '+divisor+' = ?'+(remainder>0?' (kalan: '+remainder+')':''),W/2,280);
// pirates waiting
for(let i=0;i<divisor&&i<8;i++){ctx.font='30px Segoe UI';ctx.fillText('🏴‍☠️',100+i*80,340)}
ctx.fillStyle='#e9d5ff80';ctx.font='16px Segoe UI';ctx.fillText(divisor+' korsan eşit paylaşacak',W/2,380);
// options
opts.forEach((o,i)=>{const ox=W/2-180+i*120,oy=420;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,100,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 26px Segoe UI';ctx.fillText(o,ox+50,oy+40)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-180+i*120,oy=420;if(mx>ox&&mx<ox+100&&my>oy&&my<oy+60){
if(o===ans){score+=level*10;snd(true);addP(W/2,200,'#fbbf24');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(ox+50,oy+30,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_kesir_pizza_html():
    """Kesir Pizza Ustası — 1/2, 1/4 → denk kesir → basit işlemler."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,targetNum=1,targetDen=2,opts=[],state='start',particles=[];
const PIZZA_CLRS=['#ef4444','#f59e0b','#10b981','#3b82f6','#8b5cf6','#ec4899'];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function drawPizza(cx,cy,r,num,den,highlight){
ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
for(let i=0;i<den;i++){const a1=i*Math.PI*2/den-Math.PI/2,a2=(i+1)*Math.PI*2/den-Math.PI/2;
ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,a1,a2);ctx.closePath();
ctx.fillStyle=i<num?PIZZA_CLRS[i%PIZZA_CLRS.length]+'cc':'#1e1b4b';ctx.fill();ctx.stroke()}}
function gen(){if(level===1){const dens=[2,4];targetDen=dens[Math.floor(Math.random()*dens.length)];targetNum=1+Math.floor(Math.random()*(targetDen-1));
opts=[{n:targetNum,d:targetDen}];while(opts.length<3){const d=dens[Math.floor(Math.random()*dens.length)];const n=1+Math.floor(Math.random()*(d-1));if(!opts.some(o=>o.n===n&&o.d===d))opts.push({n,d})}}
else if(level===2){const dens=[2,3,4,6];targetDen=dens[Math.floor(Math.random()*dens.length)];targetNum=1+Math.floor(Math.random()*(targetDen-1));
opts=[{n:targetNum,d:targetDen}];while(opts.length<3){const d=dens[Math.floor(Math.random()*dens.length)];const n=1+Math.floor(Math.random()*(d-1));if(!opts.some(o=>o.n===n&&o.d===d))opts.push({n,d})}}
else if(level===3){const dens=[2,3,4,6,8];targetDen=dens[Math.floor(Math.random()*dens.length)];targetNum=1+Math.floor(Math.random()*(targetDen-1));
const equiv={n:targetNum*(level===3?2:1),d:targetDen*(level===3?2:1)};
opts=[{n:targetNum,d:targetDen}];if(equiv.d<=12)opts[0]=equiv;
while(opts.length<3){const d=dens[Math.floor(Math.random()*dens.length)];const n=1+Math.floor(Math.random()*(d-1));if(!opts.some(o=>o.n*d===n*o.d))opts.push({n,d})}}
else{const dens=[2,3,4,5,6,8,10];targetDen=dens[Math.floor(Math.random()*dens.length)];targetNum=1+Math.floor(Math.random()*(targetDen-1));
opts=[{n:targetNum,d:targetDen}];while(opts.length<4){const d=dens[Math.floor(Math.random()*dens.length)];const n=1+Math.floor(Math.random()*(d-1));if(!opts.some(o=>o.n===n&&o.d===d))opts.push({n,d})}}
opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🍕 Kesir Pizza Ustası',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Pizzayı doğru kesir kadar dilimle!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🍕 Pizza Ustası!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
// target pizza
drawPizza(W/2,180,90,targetNum,targetDen,true);
ctx.fillStyle='#fbbf24';ctx.font='bold 26px Segoe UI';ctx.fillText(targetNum+'/'+targetDen,W/2,300);
ctx.fillStyle='#e9d5ff';ctx.font='18px Segoe UI';ctx.fillText('Bu pizza kaç dilim boyalı?',W/2,330);
// option pizzas
opts.forEach((o,i)=>{const ox=100+i*(W-200)/(opts.length-1||1),oy=450;
drawPizza(ox,oy,50,o.n,o.d,false);
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.fillText(o.n+'/'+o.d,ox,oy+70)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=100+i*(W-200)/(opts.length-1||1),oy=450;
if(Math.hypot(mx-ox,my-oy)<60){
if(o.n*targetDen===targetNum*o.d||( o.n===targetNum&&o.d===targetDen)){score+=level*10;snd(true);addP(ox,oy,'#fbbf24');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(ox,oy,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""