# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Matematik Oyunları 6-10 (L1→L4 zorluk)."""


def _build_elem_math_saat_ustasi_html():
    """Saat Ustası — Tam/yarım → çeyrek → dakika → süre problemleri."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=15,tgtH=0,tgtM=0,opts=[],state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function pad(n){return n<10?'0'+n:''+n}
function gen(){tgtH=1+Math.floor(Math.random()*12);
if(level===1)tgtM=[0,30][Math.floor(Math.random()*2)];
else if(level===2)tgtM=[0,15,30,45][Math.floor(Math.random()*4)];
else if(level===3)tgtM=Math.floor(Math.random()*12)*5;
else tgtM=Math.floor(Math.random()*60);
const ans=pad(tgtH)+':'+pad(tgtM);opts=[ans];
while(opts.length<4){const h=1+Math.floor(Math.random()*12),m=level<=2?[0,15,30,45][Math.floor(Math.random()*4)]:Math.floor(Math.random()*60);
const s=pad(h)+':'+pad(m);if(!opts.includes(s))opts.push(s)}opts.sort(()=>Math.random()-.5)}
function drawClock(cx,cy,r,h,m){
ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.fillStyle='#1e1b4b';ctx.fill();ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.stroke();
for(let i=1;i<=12;i++){const a=i*Math.PI/6-Math.PI/2;ctx.fillStyle='#e9d5ff';ctx.font='bold '+(r*.18)+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(i,cx+Math.cos(a)*r*.78,cy+Math.sin(a)*r*.78)}
for(let i=0;i<60;i++){const a=i*Math.PI/30;const len=i%5===0?r*.12:r*.05;
ctx.strokeStyle=i%5===0?'#a78bfa':'#a78bfa40';ctx.lineWidth=i%5===0?2:1;
ctx.beginPath();ctx.moveTo(cx+Math.cos(a)*(r-.8),cy+Math.sin(a)*(r-.8));ctx.lineTo(cx+Math.cos(a)*(r-len),cy+Math.sin(a)*(r-len));ctx.stroke()}
// hour hand
const ha=(h%12+m/60)*Math.PI/6-Math.PI/2;ctx.strokeStyle='#fbbf24';ctx.lineWidth=4;ctx.lineCap='round';
ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+Math.cos(ha)*r*.5,cy+Math.sin(ha)*r*.5);ctx.stroke();
// minute hand
const ma=m*Math.PI/30-Math.PI/2;ctx.strokeStyle='#e9d5ff';ctx.lineWidth=3;
ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+Math.cos(ma)*r*.7,cy+Math.sin(ma)*r*.7);ctx.stroke();
ctx.beginPath();ctx.arc(cx,cy,5,0,Math.PI*2);ctx.fillStyle='#fbbf24';ctx.fill()}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🕐 Saat Ustası',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Saati oku, doğru zamanı bul!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🕐 Saat Ustası!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
drawClock(W/2,220,120,tgtH,tgtM);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText('Saat kaç?',W/2,380);
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=410;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,55,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.fillText(o,ox+55,oy+35)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
const ans=pad(tgtH)+':'+pad(tgtM);
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=410;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+55){
if(o===ans){score+=level*10;snd(true);addP(ox+55,oy+27,'#10b981');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(ox+55,oy+27,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_para_marketi_html():
    """Para Marketi — Ödeme/para üstü → bütçe → çoklu ürün."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const ITEMS=[['🍎','Elma'],['🍞','Ekmek'],['🥛','Süt'],['🧀','Peynir'],['🍫','Çikolata'],['📒','Defter'],['✏️','Kalem'],['🧃','Meyve Suyu']];
let level=1,score=0,round=1,maxR=12,product='',pName='',price=0,paid=0,change=0,opts=[],state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function gen(){const it=ITEMS[Math.floor(Math.random()*ITEMS.length)];product=it[0];pName=it[1];
if(level===1){price=[1,2,3,5][Math.floor(Math.random()*4)];paid=[5,10][Math.floor(Math.random()*2)];if(paid<=price)paid=10}
else if(level===2){price=1+Math.floor(Math.random()*15);paid=[10,20,50][Math.floor(Math.random()*3)];if(paid<=price)paid=50}
else if(level===3){price=5+Math.floor(Math.random()*45);paid=[20,50,100][Math.floor(Math.random()*3)];if(paid<=price)paid=100}
else{price=10+Math.floor(Math.random()*90);paid=[50,100,200][Math.floor(Math.random()*3)];if(paid<=price)paid=200}
change=paid-price;opts=[change];while(opts.length<4){const r=Math.max(0,change+Math.floor(Math.random()*21)-10);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🏪 Para Marketi',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Alışveriş yap, para üstünü hesapla!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏪 Market Ustası!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
// product
ctx.font='60px Segoe UI';ctx.fillText(product,W/2,120);
ctx.fillStyle='#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.fillText(pName,W/2,160);
// price tag
ctx.fillStyle='#ef4444';ctx.beginPath();ctx.roundRect(W/2-60,170,120,40,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText(price+' ₺',W/2,196);
// payment
ctx.fillStyle='#10b981';ctx.beginPath();ctx.roundRect(W/2-80,230,160,45,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Ödeme: '+paid+' ₺',W/2,258);
// question
ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.fillText('Para üstü kaç ₺?',W/2,330);
// options
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=370;
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.fillText(o+' ₺',ox+55,oy+38)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=370;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+60){
if(o===change){score+=level*10;snd(true);addP(ox+55,oy+30,'#10b981');
if(score>=40&&level<2)level=2;if(score>=90&&level<3)level=3;if(score>=140&&level<4)level=4}
else{snd(false);addP(ox+55,oy+30,'#ef4444')}
round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_geometri_insa_html():
    """Geometri İnşa — Kenar/köşe → çevre → alan → açı türleri."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const SHAPES=[{n:'Üçgen',s:3},{n:'Kare',s:4},{n:'Dikdörtgen',s:4,rect:true},{n:'Beşgen',s:5},{n:'Altıgen',s:6}];
let level=1,score=0,round=1,maxR=15,q='',ans=0,opts=[],shape=null,dims=[],state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function drawPoly(cx,cy,r,sides,clr){ctx.beginPath();for(let i=0;i<sides;i++){const a=i*Math.PI*2/sides-Math.PI/2;ctx.lineTo(cx+Math.cos(a)*r,cy+Math.sin(a)*r)}ctx.closePath();ctx.fillStyle=clr+'40';ctx.fill();ctx.strokeStyle=clr;ctx.lineWidth=3;ctx.stroke()}
function gen(){shape=SHAPES[Math.floor(Math.random()*SHAPES.length)];
if(level===1){q='Bu şeklin kaç kenarı var?';ans=shape.s;dims=[]}
else if(level===2){q='Bu şeklin kaç köşesi var?';ans=shape.s;dims=[]}
else if(level===3){if(shape.rect){const a=3+Math.floor(Math.random()*8),b=3+Math.floor(Math.random()*8);dims=[a,b];ans=2*(a+b);q='Çevresi kaç cm? ('+a+'cm × '+b+'cm)'}else{const s=2+Math.floor(Math.random()*8);dims=[s];ans=shape.s*s;q='Çevresi kaç cm? (kenar: '+s+'cm)'}}
else{if(shape.n==='Kare'){const s=2+Math.floor(Math.random()*10);dims=[s];ans=s*s;q='Alanı kaç cm²? (kenar: '+s+'cm)'}
else if(shape.rect){const a=2+Math.floor(Math.random()*8),b=2+Math.floor(Math.random()*8);dims=[a,b];ans=a*b;q='Alanı kaç cm²? ('+a+'×'+b+')'}
else{q='Bu şeklin kaç kenarı var?';ans=shape.s;dims=[]}}
opts=[ans];while(opts.length<4){const r=Math.max(1,ans+Math.floor(Math.random()*11)-5);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('📐 Geometri İnşa',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Şekilleri tanı, ölç, hesapla!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('📐 Geometri Ustası!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
if(shape.rect){ctx.fillStyle='#3b82f640';ctx.strokeStyle='#3b82f6';ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(W/2-70,100,140,90,4);ctx.fill();ctx.stroke()}
else drawPoly(W/2,170,80,shape.s,'#3b82f6');
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.fillText(shape.n,W/2,290);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText(q,W/2,330);
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=370;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.fillText(o,ox+55,oy+38)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=370;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+60){
if(o===ans){score+=level*10;snd(true);addP(ox+55,oy+30,'#10b981');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(ox+55,oy+30,'#ef4444')}round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_olcme_lab_html():
    """Ölçme Laboratuvarı — cm-m, g-kg, l-ml dönüşümleri."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const UNITS=[{from:'cm',to:'m',factor:100,emoji:'📏'},{from:'m',to:'cm',factor:0.01,emoji:'📏'},{from:'g',to:'kg',factor:1000,emoji:'⚖️'},{from:'kg',to:'g',factor:0.001,emoji:'⚖️'},{from:'ml',to:'l',factor:1000,emoji:'🧪'},{from:'l',to:'ml',factor:0.001,emoji:'🧪'}];
let level=1,score=0,round=1,maxR=15,q='',ans=0,opts=[],emoji='',state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function gen(){const u=UNITS[Math.floor(Math.random()*UNITS.length)];emoji=u.emoji;
let val;
if(level===1){if(u.factor>=100){val=u.factor*[1,2,3][Math.floor(Math.random()*3)];ans=val/u.factor}else{val=[1,2,5][Math.floor(Math.random()*3)];ans=val*Math.round(1/u.factor)}}
else if(level===2){if(u.factor>=100){val=u.factor*[1,2,3,5,10][Math.floor(Math.random()*5)];ans=val/u.factor}else{val=[1,2,5,10][Math.floor(Math.random()*4)];ans=val*Math.round(1/u.factor)}}
else if(level===3){if(u.factor>=100){val=u.factor*(2+Math.floor(Math.random()*15));ans=val/u.factor}else{val=1+Math.floor(Math.random()*5);ans=val*Math.round(1/u.factor)}}
else{if(u.factor>=100){val=u.factor*(5+Math.floor(Math.random()*25));ans=val/u.factor}else{val=5+Math.floor(Math.random()*20);ans=val*Math.round(1/u.factor)}}
q=val+' '+u.from+' = ? '+u.to;
opts=[ans];while(opts.length<4){const r=Math.max(0,Math.round(ans*(0.5+Math.random()*1.5)));if(!opts.includes(r)&&r!==ans)opts.push(r)}
if(opts.length<4){let c=1;while(opts.length<4){if(!opts.includes(ans+c))opts.push(ans+c);c++}}
opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔬 Ölçme Laboratuvarı',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Birimleri dönüştür!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🔬 Bilim İnsanı!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
ctx.font='70px Segoe UI';ctx.fillText(emoji,W/2,140);
ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.fillText(q,W/2,230);
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=300;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.fillText(o,ox+55,oy+38)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=300;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+60){
if(o===ans){score+=level*10;snd(true);addP(ox+55,oy+30,'#10b981');
if(score>=40&&level<2)level=2;if(score>=100&&level<3)level=3;if(score>=160&&level<4)level=4}
else{snd(false);addP(ox+55,oy+30,'#ef4444')}round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_elem_math_problem_tiyatrosu_html():
    """Problem Tiyatrosu — Sözel problemleri sahneyle canlandır, çöz."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let level=1,score=0,round=1,maxR=12,problem='',scene=[],ans=0,opts=[],state='start',particles=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:c||'#fbbf24',r:2+Math.random()*3})}
function gen(){let a,b;
if(level===1){a=2+Math.floor(Math.random()*10);b=1+Math.floor(Math.random()*10);const r=Math.random();
if(r<.5){problem='Ayşe\'nin '+a+' elması var. Annesi '+b+' tane daha verdi. Kaç elması oldu?';scene=['👧','🍎×'+a,'+','🍎×'+b];ans=a+b}
else{if(a<b){const t=a;a=b;b=t}problem='Ali\'nin '+a+' bilye si var. '+b+' tanesini verdi. Kaç kaldı?';scene=['👦','🔵×'+a,'-','🔵×'+b];ans=a-b}}
else if(level===2){a=5+Math.floor(Math.random()*30);b=5+Math.floor(Math.random()*30);const r=Math.random();
if(r<.5){problem='Bahçede '+a+' kırmızı ve '+b+' sarı çiçek var. Toplam kaç çiçek?';scene=['🌹×'+a,'+','🌻×'+b];ans=a+b}
else{if(a<b){const t=a;a=b;b=t}problem='Kutuda '+a+' kalem var. '+b+' tanesi kırıldı. Kaç sağlam kalem?';scene=['✏️×'+a,'-','❌×'+b];ans=a-b}}
else if(level===3){a=3+Math.floor(Math.random()*8);b=2+Math.floor(Math.random()*6);const r=Math.random();
if(r<.5){problem='Her rafa '+a+' kitap konuyor. '+b+' raf var. Toplam kaç kitap?';scene=['📚×'+a,'×','🗄️×'+b];ans=a*b}
else{problem=a*b+' çikolata '+b+' çocuğa eşit paylaştırılıyor. Herbirine kaç tane?';scene=['🍫×'+(a*b),'÷','👦×'+b];ans=a}}
else{const r=Math.random();if(r<.3){a=5+Math.floor(Math.random()*12);b=3+Math.floor(Math.random()*8);problem='Her paket '+a+' ₺. '+b+' paket aldık. '+a*b+' ₺ verdik, para üstü?';const paid=Math.ceil(a*b/10)*10;ans=paid-a*b;problem='Her paket '+a+' ₺. '+b+' paket aldık. '+paid+' ₺ verdik, para üstü?';scene=['📦×'+b,'=','💰'+paid]}
else if(r<.6){a=4+Math.floor(Math.random()*10);b=3+Math.floor(Math.random()*10);problem='Sınıfta '+a+' sıra var, her sırada '+b+' öğrenci. Toplam kaç öğrenci?';scene=['🪑×'+a,'×','👤×'+b];ans=a*b}
else{a=2+Math.floor(Math.random()*10);b=2+Math.floor(Math.random()*10);const c=1+Math.floor(Math.random()*10);problem=a+' kedi, '+b+' köpek ve '+c+' kuş var. Toplam kaç hayvan?';scene=['🐱×'+a,'🐶×'+b,'🐦×'+c];ans=a+b+c}}
opts=[ans];while(opts.length<4){const r=Math.max(0,ans+Math.floor(Math.random()*11)-5);if(!opts.includes(r))opts.push(r)}opts.sort(()=>Math.random()-.5)}
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🎭 Problem Tiyatrosu',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Problemleri çöz, sahneyi canlandır!',W/2,230);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,290,160,50);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,320);return}
if(state==='end'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎭 Bravo!',W/2,200);ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'  L'+level,W/2,250);ctx.fillStyle='#a78bfa';ctx.fillRect(W/2-80,310,160,50);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar',W/2,340);return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('L'+level+'  Tur: '+round+'/'+maxR+'  Puan: '+score,W/2,30);
// stage curtains
ctx.fillStyle='#7c3aed30';ctx.fillRect(30,60,W-60,200);ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.strokeRect(30,60,W-60,200);
// scene emojis
const scW=scene.length;ctx.font='28px Segoe UI';
scene.forEach((s,i)=>{ctx.fillText(s,W/(scW+1)*(i+1),170)});
// problem text
ctx.fillStyle='#e9d5ff';ctx.font='18px Segoe UI';
const words=problem.split(' ');let line='',ly=300;
words.forEach(w=>{if((line+w).length>45){ctx.fillText(line,W/2,ly);ly+=25;line=w+' '}else line+=w+' '});
ctx.fillText(line,W/2,ly);
// options
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=ly+40;ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(ox,oy,110,60,10);ctx.fill();ctx.stroke();
ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText(o,ox+55,oy+38)});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'||state==='end'){if(mx>W/2-80&&mx<W/2+80&&my>290&&my<350){state='play';score=0;round=1;level=1;gen()}return}
const words=problem.split(' ');let ly=300;let line='';
words.forEach(w=>{if((line+w).length>45){ly+=25;line=w+' '}else line+=w+' '});
opts.forEach((o,i)=>{const ox=W/2-200+i*130,oy=ly+40;if(mx>ox&&mx<ox+110&&my>oy&&my<oy+60){
if(o===ans){score+=level*10;snd(true);addP(ox+55,oy+30,'#10b981');
if(score>=40&&level<2)level=2;if(score>=90&&level<3)level=3;if(score>=140&&level<4)level=4}
else{snd(false);addP(ox+55,oy+30,'#ef4444')}round++;if(round>maxR)state='end';else gen()}})});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""