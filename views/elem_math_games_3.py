# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Matematik Oyunları 11-15 (L1→L4 zorluk)."""


def _build_elem_math_sayi_cizgisi_yarisi_html():
    """Sayı Çizgisi Yarışı — 0–10000 arası sayı çizgisinde hız/konum."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,target=0,rangeMin=0,rangeMax=10,state='start',particles=[],clickX=-1;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function gen(){if(level===1){rangeMin=0;rangeMax=10;target=Math.floor(Math.random()*11)}
else if(level===2){rangeMin=0;rangeMax=100;target=Math.floor(Math.random()*101)}
else if(level===3){rangeMin=0;rangeMax=1000;target=Math.round(Math.random()*100)*10}
else{rangeMin=0;rangeMax=10000;target=Math.round(Math.random()*1000)*10}
clickX=-1}
function numToX(n){return 60+(n-rangeMin)/(rangeMax-rangeMin)*(W-120)}
function xToNum(x){return Math.round((x-60)/(W-120)*(rangeMax-rangeMin)+rangeMin)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🏁 Sayı Çizgisi Yarışı',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Sayının yerini bul!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏁 Yarış Bitti!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.fillText(target+' nerede?',W/2,90);
// number line
const ly=300;ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(50,ly);ctx.lineTo(W-50,ly);ctx.stroke();
const ticks=level<=2?10:level===3?10:10;
for(let i=0;i<=ticks;i++){const val=rangeMin+i*(rangeMax-rangeMin)/ticks;const x=numToX(val);
ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,ly-12);ctx.lineTo(x,ly+12);ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='14px Segoe UI';ctx.textAlign='center';ctx.fillText(Math.round(val),x,ly+30)}
// click marker
if(clickX>=0){ctx.fillStyle='#ef4444';ctx.beginPath();ctx.moveTo(clickX,ly-20);ctx.lineTo(clickX-8,ly-35);ctx.lineTo(clickX+8,ly-35);ctx.closePath();ctx.fill();
ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.fillText(xToNum(clickX),clickX,ly-42)}
// confirm button
if(clickX>=0){ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-55,400,110,45,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Onayla ✓',W/2,428)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
if(state!=='play')return;
if(my>260&&my<340&&mx>50&&mx<W-50){clickX=mx}
if(clickX>=0&&mx>W/2-55&&mx<W/2+55&&my>400&&my<445){
const guess=xToNum(clickX);const range=rangeMax-rangeMin;const tolerance=range*0.08;
if(Math.abs(guess-target)<=tolerance){score+=level*10;snd(true);addP(numToX(target),300,'#10b981');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(clickX,300,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_hata_avcisi_html():
    """Hata Avcısı — Yanlış işlemi yakala."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,eqs=[],wrongIdx=-1,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function makeEq(correct){let a,b,op,res;
if(level<=2){a=1+Math.floor(Math.random()*(level===1?20:50));b=1+Math.floor(Math.random()*(level===1?20:50));op=Math.random()>.5?'+':'-';if(op==='-'&&a<b){const t=a;a=b;b=t}res=op==='+'?a+b:a-b}
else if(level===3){const r=Math.random();if(r<.5){a=2+Math.floor(Math.random()*10);b=2+Math.floor(Math.random()*10);op='×';res=a*b}else{a=10+Math.floor(Math.random()*100);b=10+Math.floor(Math.random()*100);op=Math.random()>.5?'+':'-';if(op==='-'&&a<b){const t=a;a=b;b=t}res=op==='+'?a+b:a-b}}
else{const r=Math.random();if(r<.3){a=3+Math.floor(Math.random()*12);b=3+Math.floor(Math.random()*12);op='×';res=a*b}else if(r<.6){b=2+Math.floor(Math.random()*9);res=2+Math.floor(Math.random()*12);a=b*res;op='÷'}else{a=50+Math.floor(Math.random()*200);b=50+Math.floor(Math.random()*200);op=Math.random()>.5?'+':'-';if(op==='-'&&a<b){const t=a;a=b;b=t}res=op==='+'?a+b:a-b}}
if(!correct){let wrong=res;while(wrong===res){wrong=res+Math.floor(Math.random()*7)-3;if(wrong<0)wrong=res+Math.floor(Math.random()*5)+1}res=wrong}
return{text:a+' '+op+' '+b+' = '+res,correct}}
function gen(){const cnt=level<=2?3:4;wrongIdx=Math.floor(Math.random()*cnt);
eqs=[];for(let i=0;i<cnt;i++)eqs.push(makeEq(i!==wrongIdx))}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔍 Hata Avcısı',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Yanlış işlemi bul!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🔍 Süper Dedektif!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText('Hangisi YANLIŞ? 🐛',W/2,80);
eqs.forEach((eq,i)=>{const ey=130+i*100;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(W/2-180,ey,360,70,12);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 26px Segoe UI';ctx.textAlign='center';ctx.fillText(eq.text,W/2,ey+45)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
eqs.forEach((eq,i)=>{const ey=130+i*100;if(mx>W/2-180&&mx<W/2+180&&my>ey&&my<ey+70){
if(i===wrongIdx){score+=level*10;snd(true);addP(W/2,ey+35,'#10b981');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(W/2,ey+35,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_oruntu_dedektifi_html():
    """Örüntü Dedektifi — Artış/azalış → karma örüntüler."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,seq=[],ans=0,opts=[],state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function gen(){seq=[];const start=1+Math.floor(Math.random()*10);
if(level===1){const step=1+Math.floor(Math.random()*3);for(let i=0;i<5;i++)seq.push(start+i*step);ans=start+5*step}
else if(level===2){const step=2+Math.floor(Math.random()*5);if(Math.random()>.5){for(let i=0;i<5;i++)seq.push(start+i*step);ans=start+5*step}else{const s=start+5*step;for(let i=0;i<5;i++)seq.push(s-i*step);ans=s-5*step}}
else if(level===3){const step=2+Math.floor(Math.random()*4);if(Math.random()>.5){for(let i=0;i<5;i++)seq.push(start*Math.pow(2,i));ans=start*Math.pow(2,5)}else{for(let i=0;i<5;i++)seq.push(start+i*step);ans=start+5*step}}
else{const r=Math.random();if(r<.3){for(let i=0;i<5;i++)seq.push(start+i*i);ans=start+25}
else if(r<.6){const step=3+Math.floor(Math.random()*5);for(let i=0;i<5;i++)seq.push(start+i*step);ans=start+5*step}
else{const a1=2,d=3;for(let i=0;i<5;i++)seq.push(a1+i*d);ans=a1+5*d}}
opts=[ans];while(opts.length<4){const r=ans+Math.floor(Math.random()*11)-5;if(r>=0&&!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔎 Örüntü Dedektifi',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Sayı dizisini çöz!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🔎 Dedektif!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText('Sıradaki sayı ne?',W/2,80);
const tw=(seq.length+1)*80;const sx=(W-tw)/2;
seq.forEach((n,i)=>{const x=sx+i*80;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(x,120,70,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.fillText(n,x+35,158)});
const qx=sx+seq.length*80;ctx.fillStyle='#7c3aed50';ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(qx,120,70,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.font='bold 30px Segoe UI';ctx.fillText('?',qx+35,158);
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=260;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.fillText(o,ox+55,oy+38)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=260;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+60){
if(o===ans){score+=level*10;snd(true);addP(ox+55,oy+30,'#10b981');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(ox+55,oy+30,'#ef4444')}round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_zeka_kapilari_html():
    """Çoktan Seçmeli Zeka Kapıları — Doğru cevapla kapı aç."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,q='',ans=0,opts=[],openDoor=-1,showRes=0,state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function gen(){let a,b;
if(level===1){a=1+Math.floor(Math.random()*20);b=1+Math.floor(Math.random()*20);q=a+' + '+b;ans=a+b}
else if(level===2){a=10+Math.floor(Math.random()*50);b=10+Math.floor(Math.random()*50);const op=Math.random()>.5?'+':'-';if(op==='-'&&a<b){const t=a;a=b;b=t}q=a+' '+op+' '+b;ans=op==='+'?a+b:a-b}
else if(level===3){a=2+Math.floor(Math.random()*10);b=2+Math.floor(Math.random()*10);q=a+' × '+b;ans=a*b}
else{const r=Math.random();if(r<.4){a=2+Math.floor(Math.random()*12);b=2+Math.floor(Math.random()*12);q=a+' × '+b;ans=a*b}else{b=2+Math.floor(Math.random()*10);ans=2+Math.floor(Math.random()*12);a=b*ans;q=a+' ÷ '+b}}
opts=[ans];while(opts.length<3){const r=Math.max(0,ans+Math.floor(Math.random()*11)-5);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5);openDoor=-1;showRes=0}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🚪 Zeka Kapıları',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Doğru cevapla kapıyı aç!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🚪 Tüm Kapılar Açıldı!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.fillText(q+' = ?',W/2,90);
opts.forEach((o,i)=>{const dx=120+i*220,dy=280;
ctx.fillStyle=openDoor===i?(opts[i]===ans?'#10b98160':'#ef444460'):'#7c3aed';
ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(dx-55,dy-90,110,190,12);ctx.fill();ctx.stroke();
ctx.beginPath();ctx.arc(dx,dy-90,55,Math.PI,0);ctx.strokeStyle='#a78bfa80';ctx.lineWidth=2;ctx.stroke();
ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(dx+35,dy+20,7,0,Math.PI*2);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';ctx.fillText(o,dx,dy+5);
if(openDoor===i){ctx.font='40px Segoe UI';ctx.fillText(opts[i]===ans?'💎':'💨',dx,dy-50)}});
if(showRes>0){ctx.fillStyle=openDoor>=0&&opts[openDoor]===ans?'#10b981':'#ef4444';ctx.font='bold 24px Segoe UI';ctx.fillText(openDoor>=0&&opts[openDoor]===ans?'Doğru!':'Yanlış!',W/2,520)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){if(showRes>0){showRes--;if(showRes===0){round++;if(round>maxR)state='end';else gen()}}
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
if(showRes>0)return;
opts.forEach((o,i)=>{const dx=120+i*220,dy=280;if(Math.abs(mx-dx)<60&&my>dy-90&&my<dy+100){
openDoor=i;if(o===ans){score+=level*10;snd(true);addP(dx,dy,'#fbbf24');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else snd(false);showRes=50}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_carpan_avi_html():
    """Çarpan Avı — Çarpan-bölen bulma."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,target=0,nums=[],state='start',particles=[],found=new Set();
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function getFactors(n){const f=[];for(let i=1;i<=n;i++)if(n%i===0)f.push(i);return f}
function gen(){if(level<=2)target=4+Math.floor(Math.random()*13);
else target=10+Math.floor(Math.random()*40);
const factors=getFactors(target);found=new Set();
nums=[];factors.forEach(f=>nums.push({val:f,isFactor:true}));
while(nums.length<8){const r=2+Math.floor(Math.random()*target);if(!nums.some(n=>n.val===r))nums.push({val:r,isFactor:target%r===0})}
nums.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🎯 Çarpan Avı',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Sayının çarpanlarını bul!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎯 Çarpan Ustası!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.fillText(target+' sayısının çarpanlarını bul!',W/2,80);
const totalFactors=nums.filter(n=>n.isFactor).length;
ctx.fillStyle='#e9d5ff';ctx.font='18px Segoe UI';ctx.fillText('Bulunan: '+found.size+'/'+totalFactors,W/2,110);
nums.forEach((n,i)=>{const col=i%4,row=Math.floor(i/4);const x=140+col*140,y=150+row*100;
ctx.fillStyle=found.has(i)?'#10b98140':'#1e1b4b';ctx.strokeStyle=found.has(i)?'#10b981':'#a78bfa';ctx.lineWidth=2;
ctx.beginPath();ctx.roundRect(x,y,110,70,10);ctx.fill();ctx.stroke();
ctx.fillStyle=found.has(i)?'#10b981':'#e9d5ff';ctx.font='bold 26px Segoe UI';ctx.textAlign='center';ctx.fillText(n.val,x+55,y+45)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
nums.forEach((n,i)=>{if(found.has(i))return;const col=i%4,row=Math.floor(i/4);const x=140+col*140,y=150+row*100;
if(mx>x&&mx<x+110&&my>y&&my<y+70){if(n.isFactor){found.add(i);score+=level*5;snd(true);addP(x+55,y+35,'#10b981');
const totalFactors=nums.filter(nn=>nn.isFactor).length;
if(found.size>=totalFactors){if(score>=30&&level<2)level=2;if(score>=80&&level<3)level=3;if(score>=140&&level<4)level=4;
round++;if(round>maxR)state='end';else gen()}}
else{snd(false);addP(x+55,y+35,'#ef4444')}}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""