# -*- coding: utf-8 -*-
"""İlkokul (1-4) Genel Yetenek Oyunları — 5 Premium HTML5 Oyun."""


def _build_elem_ab_dikkat_bas_html():
    """Hızlı Dikkat: Doğruya Bas — Kurala uygun seçeneği hızlıca bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c'),ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
let timer=0,timerMax=300,options=[],rule={},answered=false,feedback='',feedbackT=0;
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,c,r:2+Math.random()*4})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function isPrime(n){if(n<2)return false;for(let i=2;i*i<=n;i++)if(n%i===0)return false;return true}
const vowels='AEIİOÖUÜ';
const RULES=[
{text:'Sadece ASAL sayıya bas!',gen:function(){let ops=[];const primes=[2,3,5,7,11,13];const nonp=[4,6,8,9,10,12,14,15];const p=primes[Math.floor(Math.random()*primes.length)];ops.push({label:String(p),correct:true});const used=new Set([p]);while(ops.length<6){const pool=Math.random()<0.3?primes:nonp;let v=pool[Math.floor(Math.random()*pool.length)];if(!used.has(v)){used.add(v);ops.push({label:String(v),correct:isPrime(v)})}}return shuffle(ops)}},
{text:'Sadece ÇİFT sayıya bas!',gen:function(){let ops=[];const evens=[2,4,6,8,10,12,14,16,18,20];const odds=[1,3,5,7,9,11,13,15,17,19];const e=evens[Math.floor(Math.random()*evens.length)];ops.push({label:String(e),correct:true});const used=new Set([e]);while(ops.length<6){const pool=Math.random()<0.4?evens:odds;let v=pool[Math.floor(Math.random()*pool.length)];if(!used.has(v)){used.add(v);ops.push({label:String(v),correct:v%2===0})}}return shuffle(ops)}},
{text:'Sadece TEK sayıya bas!',gen:function(){let ops=[];const odds=[1,3,5,7,9,11,13,15];const evens=[2,4,6,8,10,12,14,16];const o=odds[Math.floor(Math.random()*odds.length)];ops.push({label:String(o),correct:true});const used=new Set([o]);while(ops.length<6){const pool=Math.random()<0.4?odds:evens;let v=pool[Math.floor(Math.random()*pool.length)];if(!used.has(v)){used.add(v);ops.push({label:String(v),correct:v%2===1})}}return shuffle(ops)}},
{text:'Sadece BÜYÜK harfe bas!',gen:function(){let ops=[];const upper='ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ';const lower='abcçdefgğhıijklmnoöprsştuüvyz';const u=upper[Math.floor(Math.random()*upper.length)];ops.push({label:u,correct:true});const used=new Set([u]);while(ops.length<6){const pool=Math.random()<0.4?upper:lower;let v=pool[Math.floor(Math.random()*pool.length)];if(!used.has(v)){used.add(v);ops.push({label:v,correct:upper.includes(v)})}}return shuffle(ops)}},
{text:'Sadece SESLİ harfe bas!',gen:function(){let ops=[];const v='AEIİOÖUÜaeıioöuü';const c='BCÇDFGĞHJKLMNPRSŞTVYZbcçdfgğhjklmnprsştvyz';const vl=v[Math.floor(Math.random()*v.length)];ops.push({label:vl,correct:true});const used=new Set([vl]);while(ops.length<6){const pool=Math.random()<0.4?v:c;let ch=pool[Math.floor(Math.random()*pool.length)];if(!used.has(ch)){used.add(ch);ops.push({label:ch,correct:v.includes(ch)})}}return shuffle(ops)}},
{text:'Sadece 5\\'e bölünen sayıya bas!',gen:function(){let ops=[];const div5=[5,10,15,20,25,30,35,40];const notd=[1,2,3,4,6,7,8,9,11,12,13,14];const d=div5[Math.floor(Math.random()*div5.length)];ops.push({label:String(d),correct:true});const used=new Set([d]);while(ops.length<6){const pool=Math.random()<0.35?div5:notd;let v=pool[Math.floor(Math.random()*pool.length)];if(!used.has(v)){used.add(v);ops.push({label:String(v),correct:v%5===0})}}return shuffle(ops)}},
{text:'Sadece 10\\'dan BÜYÜK sayıya bas!',gen:function(){let ops=[];const big=[11,12,13,14,15,16,17,18,19,20,25,30];const small=[1,2,3,4,5,6,7,8,9,10];const b=big[Math.floor(Math.random()*big.length)];ops.push({label:String(b),correct:true});const used=new Set([b]);while(ops.length<6){const pool=Math.random()<0.4?big:small;let v=pool[Math.floor(Math.random()*pool.length)];if(!used.has(v)){used.add(v);ops.push({label:String(v),correct:v>10})}}return shuffle(ops)}},
{text:'Sadece SESSİZ harfe bas!',gen:function(){let ops=[];const c='BCÇDFGĞHJKLMNPRSŞTVYZbcçdfgğhjklmnprsştvyz';const v='AEIİOÖUÜaeıioöuü';const cl=c[Math.floor(Math.random()*c.length)];ops.push({label:cl,correct:true});const used=new Set([cl]);while(ops.length<6){const pool=Math.random()<0.4?c:v;let ch=pool[Math.floor(Math.random()*pool.length)];if(!used.has(ch)){used.add(ch);ops.push({label:ch,correct:c.includes(ch)})}}return shuffle(ops)}}
];
function initRound(){rule=RULES[(round-1)%RULES.length];options=rule.gen();timer=timerMax;answered=false;feedback='';feedbackT=0}
function drawBox(x,y,w,h,clr,txt,hover){ctx.save();ctx.shadowColor=clr;ctx.shadowBlur=hover?15:5;ctx.beginPath();ctx.moveTo(x+10,y);ctx.lineTo(x+w-10,y);ctx.quadraticCurveTo(x+w,y,x+w,y+10);ctx.lineTo(x+w,y+h-10);ctx.quadraticCurveTo(x+w,y+h,x+w-10,y+h);ctx.lineTo(x+10,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-10);ctx.lineTo(x,y+10);ctx.quadraticCurveTo(x,y,x+10,y);ctx.closePath();ctx.fillStyle=clr;ctx.globalAlpha=0.25;ctx.fill();ctx.globalAlpha=1;ctx.strokeStyle=clr;ctx.lineWidth=2;ctx.stroke();ctx.fillStyle='#fff';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(txt,x+w/2,y+h/2);ctx.restore()}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('⚡ Hızlı Dikkat: Doğruya Bas ⚡',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Kurala uygun seçeneğe hızla tıkla!',W/2,230);ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Her turda farklı kural, 5 saniye süren!',W/2,265);ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,327);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';ctx.fillText('Toplam Puan: '+score,W/2,260);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,327);return}
ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,20,30);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
const pct=timer/timerMax;ctx.fillStyle='#334155';ctx.fillRect(150,15,W-300,14);ctx.fillStyle=pct>0.4?'#22c55e':(pct>0.15?'#f59e0b':'#ef4444');ctx.fillRect(150,15,(W-300)*pct,14);
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(rule.text,W/2,75);
const bw=170,bh=80,gap=20,cols=3,rows=2;const totalW=cols*bw+(cols-1)*gap;const startX=(W-totalW)/2;const startY=120;
for(let i=0;i<options.length;i++){const col=i%cols,row=Math.floor(i/cols);const bx=startX+col*(bw+gap),by=startY+row*(bh+gap);let clr=options[i].hit===true?'#22c55e':(options[i].hit===false?'#ef4444':'#6366f1');drawBox(bx,by,bw,bh,clr,options[i].label,false)}
if(feedbackT>0){ctx.globalAlpha=Math.min(1,feedbackT/20);ctx.fillStyle=feedback==='Doğru! +10'?'#22c55e':'#ef4444';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,350);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function nextRound(){round++;if(round>maxR){state='win'}else{initRound()}}
function update(){if(state==='play'&&!answered){timer--;if(timer<=0){answered=true;feedback='Süre doldu!';feedbackT=60;beep(180,0.3);setTimeout(nextRound,1200)}}
if(feedbackT>0)feedbackT--;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.12});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',function(e){const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return}
if(state==='win'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='start';round=1;score=0}return}
if(answered)return;
const bw=170,bh=80,gap=20,cols=3;const totalW=cols*bw+(cols-1)*gap;const startX=(W-totalW)/2;const startY=120;
for(let i=0;i<options.length;i++){const col=i%cols,row=Math.floor(i/cols);const bx=startX+col*(bw+gap),by=startY+row*(bh+gap);
if(mx>=bx&&mx<=bx+bw&&my>=by&&my<=by+bh){answered=true;options[i].hit=options[i].correct;
if(options[i].correct){score+=10;feedback='Doğru! +10';beep(523,0.15);addP(bx+bw/2,by+bh/2,'#22c55e')}
else{score=Math.max(0,score-5);feedback='Yanlış! -5';beep(180,0.3)}
feedbackT=60;setTimeout(nextRound,1200);return}}});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_kelime_resim_html():
    """Kelime–Resim Hafıza — Kelime ve resim kartlarını eşleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c'),ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
let cards=[],firstPick=null,secondPick=null,lockBoard=false,matchedCount=0,totalPairs=0,flipTimer=0;
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,c,r:2+Math.random()*4})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
const PAIR_SETS=[
[{w:'Kedi',e:'🐱'},{w:'Köpek',e:'🐶'},{w:'Kuş',e:'🐦'},{w:'Balık',e:'🐟'},{w:'Tavşan',e:'🐰'},{w:'Kaplumbağa',e:'🐢'},{w:'Kelebek',e:'🦋'},{w:'Arı',e:'🐝'}],
[{w:'Elma',e:'🍎'},{w:'Muz',e:'🍌'},{w:'Üzüm',e:'🍇'},{w:'Çilek',e:'🍓'},{w:'Portakal',e:'🍊'},{w:'Karpuz',e:'🍉'},{w:'Armut',e:'🍐'},{w:'Kiraz',e:'🍒'}],
[{w:'Araba',e:'🚗'},{w:'Otobüs',e:'🚌'},{w:'Uçak',e:'✈️'},{w:'Gemi',e:'🚢'},{w:'Bisiklet',e:'🚲'},{w:'Tren',e:'🚆'},{w:'Helikopter',e:'🚁'},{w:'Roket',e:'🚀'}],
[{w:'Güneş',e:'☀️'},{w:'Ay',e:'🌙'},{w:'Yıldız',e:'⭐'},{w:'Bulut',e:'☁️'},{w:'Yağmur',e:'🌧️'},{w:'Gökkuşağı',e:'🌈'},{w:'Kar',e:'❄️'},{w:'Şimşek',e:'⚡'}],
[{w:'Ev',e:'🏠'},{w:'Okul',e:'🏫'},{w:'Hastane',e:'🏥'},{w:'Cami',e:'🕌'},{w:'Kale',e:'🏰'},{w:'Köprü',e:'🌉'},{w:'Çadır',e:'⛺'},{w:'Kule',e:'🗼'}],
[{w:'Çiçek',e:'🌸'},{w:'Ağaç',e:'🌳'},{w:'Yaprak',e:'🍃'},{w:'Mantar',e:'🍄'},{w:'Kaktüs',e:'🌵'},{w:'Gül',e:'🌹'},{w:'Lale',e:'🌷'},{w:'Papatya',e:'🌼'}],
[{w:'Futbol',e:'⚽'},{w:'Basketbol',e:'🏀'},{w:'Tenis',e:'🎾'},{w:'Yüzme',e:'🏊'},{w:'Kayak',e:'⛷️'},{w:'Voleybol',e:'🏐'},{w:'Boks',e:'🥊'},{w:'Okçuluk',e:'🏹'}],
[{w:'Kitap',e:'📖'},{w:'Kalem',e:'✏️'},{w:'Saat',e:'⏰'},{w:'Anahtar',e:'🔑'},{w:'Şemsiye',e:'☂️'},{w:'Gözlük',e:'👓'},{w:'Çanta',e:'🎒'},{w:'Mum',e:'🕯️'}],
[{w:'Pizza',e:'🍕'},{w:'Dondurma',e:'🍦'},{w:'Kek',e:'🎂'},{w:'Hamburger',e:'🍔'},{w:'Simit',e:'🥯'},{w:'Çay',e:'🍵'},{w:'Makarna',e:'🍝'},{w:'Ekmek',e:'🍞'}],
[{w:'Aslan',e:'🦁'},{w:'Fil',e:'🐘'},{w:'Zürafa',e:'🦒'},{w:'Penguen',e:'🐧'},{w:'Panda',e:'🐼'},{w:'Yunus',e:'🐬'},{w:'Kartal',e:'🦅'},{w:'Timsah',e:'🐊'}]
];
function getPairCount(){if(round<=3)return 4;if(round<=6)return 6;return 8}
function initRound(){const cnt=getPairCount();const setIdx=(round-1)%PAIR_SETS.length;
const pairs=shuffle([...PAIR_SETS[setIdx]]).slice(0,cnt);totalPairs=cnt;matchedCount=0;
let deck=[];pairs.forEach(function(p){deck.push({type:'word',text:p.w,pairId:p.w,faceUp:false,matched:false,flipScale:1});deck.push({type:'emoji',text:p.e,pairId:p.w,faceUp:false,matched:false,flipScale:1})});
shuffle(deck);
const cols=cnt<=4?4:(cnt<=6?4:4),rows=Math.ceil(deck.length/cols);
const cw=Math.min(140,Math.floor((W-60)/cols)-10),ch=Math.min(100,Math.floor((H-160)/rows)-10);
const tw=cols*(cw+10)-10,th=rows*(ch+10)-10;const sx=(W-tw)/2,sy=(H-th)/2+30;
cards=[];for(let i=0;i<deck.length;i++){const col=i%cols,row=Math.floor(i/cols);
cards.push(Object.assign(deck[i],{x:sx+col*(cw+10),y:sy+row*(ch+10),w:cw,h:ch}))}
firstPick=null;secondPick=null;lockBoard=false;flipTimer=0}
function drawCard(cd){ctx.save();const cx=cd.x+cd.w/2,cy=cd.y+cd.h/2;ctx.translate(cx,cy);ctx.scale(cd.flipScale,1);ctx.translate(-cx,-cy);
if(cd.faceUp||cd.matched){ctx.beginPath();ctx.moveTo(cd.x+8,cd.y);ctx.lineTo(cd.x+cd.w-8,cd.y);ctx.quadraticCurveTo(cd.x+cd.w,cd.y,cd.x+cd.w,cd.y+8);ctx.lineTo(cd.x+cd.w,cd.y+cd.h-8);ctx.quadraticCurveTo(cd.x+cd.w,cd.y+cd.h,cd.x+cd.w-8,cd.y+cd.h);ctx.lineTo(cd.x+8,cd.y+cd.h);ctx.quadraticCurveTo(cd.x,cd.y+cd.h,cd.x,cd.y+cd.h-8);ctx.lineTo(cd.x,cd.y+8);ctx.quadraticCurveTo(cd.x,cd.y,cd.x+8,cd.y);ctx.closePath();
ctx.fillStyle=cd.matched?'#14532d':'#1e1b4b';ctx.fill();ctx.strokeStyle=cd.matched?'#4ade80':'#818cf8';ctx.lineWidth=2;ctx.stroke();
if(cd.type==='emoji'){ctx.font=Math.min(cd.w,cd.h)*0.45+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(cd.text,cx,cy)}
else{ctx.fillStyle='#e0e7ff';ctx.font='bold '+Math.min(18,cd.w*0.15)+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(cd.text,cx,cy)}}
else{ctx.beginPath();ctx.moveTo(cd.x+8,cd.y);ctx.lineTo(cd.x+cd.w-8,cd.y);ctx.quadraticCurveTo(cd.x+cd.w,cd.y,cd.x+cd.w,cd.y+8);ctx.lineTo(cd.x+cd.w,cd.y+cd.h-8);ctx.quadraticCurveTo(cd.x+cd.w,cd.y+cd.h,cd.x+cd.w-8,cd.y+cd.h);ctx.lineTo(cd.x+8,cd.y+cd.h);ctx.quadraticCurveTo(cd.x,cd.y+cd.h,cd.x,cd.y+cd.h-8);ctx.lineTo(cd.x,cd.y+8);ctx.quadraticCurveTo(cd.x,cd.y,cd.x+8,cd.y);ctx.closePath();
const bg=ctx.createLinearGradient(cd.x,cd.y,cd.x+cd.w,cd.y+cd.h);bg.addColorStop(0,'#4338ca');bg.addColorStop(1,'#6366f1');ctx.fillStyle=bg;ctx.fill();ctx.strokeStyle='#818cf8';ctx.lineWidth=2;ctx.stroke();
ctx.fillStyle='#c7d2fe';ctx.font='bold '+Math.min(cd.w,cd.h)*0.3+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('?',cx,cy)}
ctx.restore()}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🧠 Kelime–Resim Hafıza 🧠',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Kelimeyi resmiyle eşleştir!',W/2,230);ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Aynı anlama gelen iki kartı çevir',W/2,265);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,327);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';ctx.fillText('Toplam Puan: '+score,W/2,260);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,327);return}
ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,20,30);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.fillText('Eşleşen: '+matchedCount+'/'+totalPairs,W/2,30);
cards.forEach(function(c){drawCard(c)});
particles.forEach(function(p){ctx.globalAlpha=p.life;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let flipAnims=[];
function update(){particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(function(p){return p.life>0});
flipAnims=flipAnims.filter(function(fa){fa.card.flipScale+=fa.dir*0.12;
if(fa.dir<0&&fa.card.flipScale<=0){fa.card.flipScale=0;fa.card.faceUp=fa.target;fa.dir=1;return true}
if(fa.dir>0&&fa.card.flipScale>=1){fa.card.flipScale=1;return false}return true});
if(flipTimer>0){flipTimer--;if(flipTimer===0&&firstPick&&secondPick){
flipAnims.push({card:firstPick,dir:-0.12,target:false});flipAnims.push({card:secondPick,dir:-0.12,target:false});
setTimeout(function(){firstPick=null;secondPick=null;lockBoard=false},350)}}
draw();requestAnimationFrame(update)}
function flipCard(card){if(lockBoard||card.faceUp||card.matched)return;
flipAnims.push({card:card,dir:-0.12,target:true});
if(!firstPick){firstPick=card}else{secondPick=card;lockBoard=true;
setTimeout(function(){if(firstPick.pairId===secondPick.pairId&&firstPick!==secondPick){firstPick.matched=true;secondPick.matched=true;score+=10;matchedCount++;
addP(firstPick.x+firstPick.w/2,firstPick.y+firstPick.h/2,'#4ade80');addP(secondPick.x+secondPick.w/2,secondPick.y+secondPick.h/2,'#4ade80');beep(523,0.15);
firstPick=null;secondPick=null;lockBoard=false;
if(matchedCount>=totalPairs){round++;if(round>maxR){setTimeout(function(){state='win'},600)}else{setTimeout(initRound,800)}}}
else{beep(180,0.3);flipTimer=35}},500)}}
canvas.addEventListener('click',function(e){const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return}
if(state==='win'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){round=1;score=0;state='start'}return}
for(let i=0;i<cards.length;i++){const c=cards[i];if(mx>=c.x&&mx<=c.x+c.w&&my>=c.y&&my<=c.y+c.h){flipCard(c);return}}});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_sudoku_mini_html():
    """Sudoku Mini (4x4) — 4x4 Sudoku bulmaca oyunu."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c'),ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
let grid=[],fixed=[],solution=[],selR=-1,selC=-1,complete=false,errCells=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,c,r:2+Math.random()*4})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function genSolved(){const base=[[1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]];
const perm=shuffle([1,2,3,4]);const map={};for(let i=0;i<4;i++)map[i+1]=perm[i];
const g=[];for(let r=0;r<4;r++){g[r]=[];for(let c=0;c<4;c++)g[r][c]=map[base[r][c]]}
const rows=[[0,1],[2,3]];for(let band of rows){if(Math.random()>0.5){const tmp=g[band[0]];g[band[0]]=g[band[1]];g[band[1]]=tmp}}
const cols=[[0,1],[2,3]];for(let band of cols){if(Math.random()>0.5){for(let r=0;r<4;r++){const tmp=g[r][band[0]];g[r][band[0]]=g[r][band[1]];g[r][band[1]]=tmp}}}
return g}
function isValid(g,r,c,v){for(let i=0;i<4;i++){if(i!==c&&g[r][i]===v)return false;if(i!==r&&g[i][c]===v)return false}
const br=Math.floor(r/2)*2,bc=Math.floor(c/2)*2;
for(let dr=0;dr<2;dr++)for(let dc=0;dc<2;dc++){if(br+dr!==r||bc+dc!==c){if(g[br+dr][bc+dc]===v)return false}}return true}
function initRound(){solution=genSolved();grid=[];fixed=[];errCells=[];selR=-1;selC=-1;complete=false;
const difficulty=Math.min(10,4+round);const empties=Math.min(12,difficulty);
for(let r=0;r<4;r++){grid[r]=[];fixed[r]=[];for(let c=0;c<4;c++){grid[r][c]=solution[r][c];fixed[r][c]=true}}
let positions=[];for(let r=0;r<4;r++)for(let c=0;c<4;c++)positions.push([r,c]);
shuffle(positions);for(let i=0;i<empties&&i<positions.length;i++){const p=positions[i];grid[p[0]][p[1]]=0;fixed[p[0]][p[1]]=false}}
function checkComplete(){for(let r=0;r<4;r++)for(let c=0;c<4;c++)if(grid[r][c]===0)return false;
for(let r=0;r<4;r++)for(let c=0;c<4;c++){if(!isValid(grid,r,c,grid[r][c]))return false}return true}
const GS=100,GP=6,GX=(W-4*GS-3*GP)/2,GY=80;
function cellXY(r,c){return{x:GX+c*(GS+GP)-(c>=2?0:0)+Math.floor(c/2)*8,y:GY+r*(GS+GP)+Math.floor(r/2)*8}}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔢 Sudoku Mini (4×4) 🔢',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Her satır, sütun ve 2×2 kutuda',W/2,225);ctx.fillText('1-2-3-4 sayıları birer kez olmalı!',W/2,255);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,327);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';ctx.fillText('Toplam Puan: '+score,W/2,260);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,327);return}
ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,20,30);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
ctx.textAlign='center';ctx.fillStyle='#94a3b8';ctx.font='16px Segoe UI';ctx.fillText('Bir hücreye tıkla, sonra aşağıdan sayı seç',W/2,60);
for(let r=0;r<4;r++){for(let c=0;c<4;c++){const p=cellXY(r,c);const isErr=errCells.some(function(e){return e[0]===r&&e[1]===c});
const isSel=r===selR&&c===selC;
ctx.fillStyle=isErr?'#7f1d1d':(isSel?'#312e81':(fixed[r][c]?'#94A3B8':'#0B0F19'));
ctx.strokeStyle=isErr?'#ef4444':(isSel?'#818cf8':'#334155');ctx.lineWidth=isSel?3:1;
ctx.fillRect(p.x,p.y,GS,GS);ctx.strokeRect(p.x,p.y,GS,GS);
if(grid[r][c]>0){ctx.fillStyle=fixed[r][c]?'#e2e8f0':'#67e8f9';ctx.font=(fixed[r][c]?'bold ':'')+'36px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(String(grid[r][c]),p.x+GS/2,p.y+GS/2)}}}
for(let br=0;br<2;br++){for(let bc=0;bc<2;bc++){const p1=cellXY(br*2,bc*2);const p2=cellXY(br*2+1,bc*2+1);
ctx.strokeStyle='#6366f1';ctx.lineWidth=3;ctx.strokeRect(p1.x-2,p1.y-2,2*(GS+GP)+4+8,2*(GS+GP)+4+8)}}
const btnY=GY+4*(GS+GP)+4*8+30;const btnW=80,btnH=60,btnGap=20;const totalBtnW=4*btnW+3*btnGap;const btnX=(W-totalBtnW)/2;
for(let n=1;n<=4;n++){const bx=btnX+(n-1)*(btnW+btnGap);
ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#6366f1';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(bx+10,btnY);ctx.lineTo(bx+btnW-10,btnY);ctx.quadraticCurveTo(bx+btnW,btnY,bx+btnW,btnY+10);ctx.lineTo(bx+btnW,btnY+btnH-10);ctx.quadraticCurveTo(bx+btnW,btnY+btnH,bx+btnW-10,btnY+btnH);ctx.lineTo(bx+10,btnY+btnH);ctx.quadraticCurveTo(bx,btnY+btnH,bx,btnY+btnH-10);ctx.lineTo(bx,btnY+10);ctx.quadraticCurveTo(bx,btnY,bx+10,btnY);ctx.closePath();
ctx.fill();ctx.stroke();ctx.fillStyle='#c7d2fe';ctx.font='bold 30px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(String(n),bx+btnW/2,btnY+btnH/2)}
const clrX=btnX+4*(btnW+btnGap)+10,clrY=btnY;
ctx.fillStyle='#7f1d1d';ctx.strokeStyle='#ef4444';ctx.lineWidth=2;ctx.fillRect(clrX,clrY,btnW,btnH);ctx.strokeRect(clrX,clrY,btnW,btnH);
ctx.fillStyle='#fca5a5';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('Sil',clrX+btnW/2,clrY+btnH/2);
particles.forEach(function(p){ctx.globalAlpha=p.life;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(function(p){return p.life>0});
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',function(e){const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return}
if(state==='win'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){round=1;score=0;state='start'}return}
if(complete)return;
for(let r=0;r<4;r++){for(let c=0;c<4;c++){const p=cellXY(r,c);if(mx>=p.x&&mx<=p.x+GS&&my>=p.y&&my<=p.y+GS){if(!fixed[r][c]){selR=r;selC=c;errCells=[]}return}}}
const btnY2=GY+4*(GS+GP)+4*8+30;const btnW2=80,btnH2=60,btnGap2=20;const totalBtnW2=4*btnW2+3*btnGap2;const btnX2=(W-totalBtnW2)/2;
for(let n=1;n<=4;n++){const bx=btnX2+(n-1)*(btnW2+btnGap2);
if(mx>=bx&&mx<=bx+btnW2&&my>=btnY2&&my<=btnY2+btnH2){if(selR>=0&&selC>=0&&!fixed[selR][selC]){
if(isValid(grid,selR,selC,n)){grid[selR][selC]=n;beep(523,0.15);const p=cellXY(selR,selC);addP(p.x+GS/2,p.y+GS/2,'#22c55e');errCells=[];
if(checkComplete()){complete=true;score+=10;setTimeout(function(){round++;if(round>maxR){state='win'}else{initRound()}},1000)}}
else{grid[selR][selC]=n;errCells=[[selR,selC]];beep(180,0.3)}}return}}
const clrX2=btnX2+4*(btnW2+btnGap2)+10;
if(mx>=clrX2&&mx<=clrX2+btnW2&&my>=btnY2&&my<=btnY2+btnH2){if(selR>=0&&selC>=0&&!fixed[selR][selC]){grid[selR][selC]=0;errCells=[]}}});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_tangram_html():
    """Tangram Zeka — Geometrik parçaları yerleştirerek şekil oluştur."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c'),ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
let slots=[],pieces=[],selectedPiece=-1,placedCount=0,totalSlots=0;
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,c,r:2+Math.random()*4})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
const SHAPES=[
{name:'Ev',slots:[
{id:'A',type:'triangle',x:0,y:-70,w:80,h:60,label:'Çatı',color:'#ef4444',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*30);ctx.lineTo(cx-s*40,cy+s*30);ctx.lineTo(cx+s*40,cy+s*30);ctx.closePath()}},
{id:'B',type:'rect',x:0,y:10,w:70,h:70,label:'Gövde',color:'#3b82f6',draw:function(cx,cy,s){ctx.fillRect(cx-s*35,cy-s*35,s*70,s*70)}},
{id:'C',type:'rect',x:0,y:30,w:25,h:35,label:'Kapı',color:'#a855f7',draw:function(cx,cy,s){ctx.fillRect(cx-s*12,cy-s*17,s*25,s*35)}},
{id:'D',type:'rect',x:-20,y:-10,w:20,h:20,label:'Pencere',color:'#f59e0b',draw:function(cx,cy,s){ctx.fillRect(cx-s*10,cy-s*10,s*20,s*20)}},
{id:'E',type:'rect',x:20,y:-10,w:20,h:20,label:'Pencere 2',color:'#22c55e',draw:function(cx,cy,s){ctx.fillRect(cx-s*10,cy-s*10,s*20,s*20)}}
]},
{name:'Tekne',slots:[
{id:'A',type:'trapezoid',x:0,y:20,w:100,h:40,label:'Gövde',color:'#3b82f6',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*50,cy-s*20);ctx.lineTo(cx+s*50,cy-s*20);ctx.lineTo(cx+s*35,cy+s*20);ctx.lineTo(cx-s*35,cy+s*20);ctx.closePath()}},
{id:'B',type:'triangle',x:0,y:-40,w:60,h:50,label:'Yelken',color:'#ef4444',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*25);ctx.lineTo(cx-s*30,cy+s*25);ctx.lineTo(cx+s*5,cy+s*25);ctx.closePath()}},
{id:'C',type:'rect',x:0,y:-15,w:5,h:50,label:'Direk',color:'#f59e0b',draw:function(cx,cy,s){ctx.fillRect(cx-s*2,cy-s*25,s*5,s*50)}},
{id:'D',type:'triangle',x:20,y:-35,w:40,h:35,label:'Küçük Yelken',color:'#22c55e',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*17);ctx.lineTo(cx+s*20,cy+s*17);ctx.lineTo(cx-s*5,cy+s*17);ctx.closePath()}},
{id:'E',type:'rect',x:0,y:45,w:80,h:8,label:'Su',color:'#06b6d4',draw:function(cx,cy,s){ctx.fillRect(cx-s*40,cy-s*4,s*80,s*8)}}
]},
{name:'Ağaç',slots:[
{id:'A',type:'triangle',x:0,y:-60,w:70,h:45,label:'Tepe',color:'#22c55e',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*22);ctx.lineTo(cx-s*35,cy+s*22);ctx.lineTo(cx+s*35,cy+s*22);ctx.closePath()}},
{id:'B',type:'triangle',x:0,y:-25,w:90,h:50,label:'Orta',color:'#16a34a',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*25);ctx.lineTo(cx-s*45,cy+s*25);ctx.lineTo(cx+s*45,cy+s*25);ctx.closePath()}},
{id:'C',type:'triangle',x:0,y:15,w:110,h:55,label:'Alt',color:'#15803d',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*27);ctx.lineTo(cx-s*55,cy+s*27);ctx.lineTo(cx+s*55,cy+s*27);ctx.closePath()}},
{id:'D',type:'rect',x:0,y:55,w:20,h:30,label:'Gövde',color:'#92400e',draw:function(cx,cy,s){ctx.fillRect(cx-s*10,cy-s*15,s*20,s*30)}}
]},
{name:'Roket',slots:[
{id:'A',type:'triangle',x:0,y:-70,w:40,h:40,label:'Burun',color:'#ef4444',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*20);ctx.lineTo(cx-s*20,cy+s*20);ctx.lineTo(cx+s*20,cy+s*20);ctx.closePath()}},
{id:'B',type:'rect',x:0,y:-15,w:40,h:70,label:'Gövde',color:'#6366f1',draw:function(cx,cy,s){ctx.fillRect(cx-s*20,cy-s*35,s*40,s*70)}},
{id:'C',type:'triangle',x:-30,y:30,w:25,h:35,label:'Sol Kanat',color:'#f59e0b',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx+s*12,cy-s*17);ctx.lineTo(cx-s*12,cy+s*17);ctx.lineTo(cx+s*12,cy+s*17);ctx.closePath()}},
{id:'D',type:'triangle',x:30,y:30,w:25,h:35,label:'Sağ Kanat',color:'#f59e0b',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*12,cy-s*17);ctx.lineTo(cx+s*12,cy+s*17);ctx.lineTo(cx-s*12,cy+s*17);ctx.closePath()}},
{id:'E',type:'rect',x:0,y:10,w:15,h:15,label:'Pencere',color:'#22d3ee',draw:function(cx,cy,s){ctx.beginPath();ctx.arc(cx,cy,s*7,0,Math.PI*2);ctx.closePath()}}
]},
{name:'Kedi',slots:[
{id:'A',type:'circle',x:0,y:-50,w:50,h:50,label:'Kafa',color:'#f59e0b',draw:function(cx,cy,s){ctx.beginPath();ctx.arc(cx,cy,s*25,0,Math.PI*2);ctx.closePath()}},
{id:'B',type:'triangle',x:-18,y:-78,w:18,h:20,label:'Sol Kulak',color:'#d97706',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*10);ctx.lineTo(cx-s*9,cy+s*10);ctx.lineTo(cx+s*9,cy+s*10);ctx.closePath()}},
{id:'C',type:'triangle',x:18,y:-78,w:18,h:20,label:'Sağ Kulak',color:'#d97706',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*10);ctx.lineTo(cx-s*9,cy+s*10);ctx.lineTo(cx+s*9,cy+s*10);ctx.closePath()}},
{id:'D',type:'oval',x:0,y:10,w:40,h:60,label:'Gövde',color:'#ea580c',draw:function(cx,cy,s){ctx.beginPath();ctx.ellipse(cx,cy,s*20,s*30,0,0,Math.PI*2);ctx.closePath()}},
{id:'E',type:'rect',x:0,y:55,w:50,h:8,label:'Kuyruk',color:'#c2410c',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*5,cy);ctx.quadraticCurveTo(cx+s*15,cy-s*10,cx+s*25,cy);ctx.quadraticCurveTo(cx+s*15,cy+s*10,cx-s*5,cy);ctx.closePath()}}
]},
{name:'Yıldız',slots:[
{id:'A',type:'triangle',x:0,y:-45,w:40,h:35,label:'Üst',color:'#fbbf24',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*17);ctx.lineTo(cx-s*20,cy+s*17);ctx.lineTo(cx+s*20,cy+s*17);ctx.closePath()}},
{id:'B',type:'triangle',x:-35,y:-10,w:40,h:35,label:'Sol Üst',color:'#f59e0b',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*20,cy);ctx.lineTo(cx+s*20,cy-s*10);ctx.lineTo(cx+s*20,cy+s*10);ctx.closePath()}},
{id:'C',type:'triangle',x:35,y:-10,w:40,h:35,label:'Sağ Üst',color:'#f59e0b',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx+s*20,cy);ctx.lineTo(cx-s*20,cy-s*10);ctx.lineTo(cx-s*20,cy+s*10);ctx.closePath()}},
{id:'D',type:'triangle',x:-20,y:30,w:40,h:35,label:'Sol Alt',color:'#d97706',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*15,cy+s*17);ctx.lineTo(cx,cy-s*17);ctx.lineTo(cx+s*15,cy+s*17);ctx.closePath()}},
{id:'E',type:'triangle',x:20,y:30,w:40,h:35,label:'Sağ Alt',color:'#d97706',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*15,cy+s*17);ctx.lineTo(cx,cy-s*17);ctx.lineTo(cx+s*15,cy+s*17);ctx.closePath()}}
]},
{name:'Balık',slots:[
{id:'A',type:'oval',x:0,y:0,w:70,h:40,label:'Gövde',color:'#3b82f6',draw:function(cx,cy,s){ctx.beginPath();ctx.ellipse(cx,cy,s*35,s*20,0,0,Math.PI*2);ctx.closePath()}},
{id:'B',type:'triangle',x:-50,y:0,w:35,h:40,label:'Kuyruk',color:'#6366f1',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx+s*17,cy);ctx.lineTo(cx-s*17,cy-s*20);ctx.lineTo(cx-s*17,cy+s*20);ctx.closePath()}},
{id:'C',type:'circle',x:25,y:-8,w:10,h:10,label:'Göz',color:'#fbbf24',draw:function(cx,cy,s){ctx.beginPath();ctx.arc(cx,cy,s*5,0,Math.PI*2);ctx.closePath()}},
{id:'D',type:'triangle',x:0,y:-25,w:30,h:20,label:'Üst Yüzgeç',color:'#22c55e',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*10);ctx.lineTo(cx-s*15,cy+s*10);ctx.lineTo(cx+s*15,cy+s*10);ctx.closePath()}}
]},
{name:'Araba',slots:[
{id:'A',type:'rect',x:0,y:0,w:100,h:35,label:'Gövde',color:'#ef4444',draw:function(cx,cy,s){ctx.fillRect(cx-s*50,cy-s*17,s*100,s*35)}},
{id:'B',type:'rect',x:10,y:-30,w:50,h:25,label:'Kabin',color:'#dc2626',draw:function(cx,cy,s){ctx.fillRect(cx-s*25,cy-s*12,s*50,s*25)}},
{id:'C',type:'circle',x:-30,y:25,w:20,h:20,label:'Sol Tekerlek',color:'#94A3B8',draw:function(cx,cy,s){ctx.beginPath();ctx.arc(cx,cy,s*10,0,Math.PI*2);ctx.closePath()}},
{id:'D',type:'circle',x:30,y:25,w:20,h:20,label:'Sağ Tekerlek',color:'#94A3B8',draw:function(cx,cy,s){ctx.beginPath();ctx.arc(cx,cy,s*10,0,Math.PI*2);ctx.closePath()}},
{id:'E',type:'rect',x:20,y:-28,w:15,h:15,label:'Pencere',color:'#7dd3fc',draw:function(cx,cy,s){ctx.fillRect(cx-s*7,cy-s*7,s*15,s*15)}}
]},
{name:'Uçak',slots:[
{id:'A',type:'rect',x:0,y:0,w:100,h:20,label:'Gövde',color:'#e2e8f0',draw:function(cx,cy,s){ctx.beginPath();ctx.ellipse(cx,cy,s*50,s*10,0,0,Math.PI*2);ctx.closePath()}},
{id:'B',type:'triangle',x:55,y:-5,w:20,h:25,label:'Burun',color:'#94a3b8',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx+s*10,cy);ctx.lineTo(cx-s*10,cy-s*8);ctx.lineTo(cx-s*10,cy+s*8);ctx.closePath()}},
{id:'C',type:'rect',x:0,y:-25,w:80,h:10,label:'Kanat',color:'#6366f1',draw:function(cx,cy,s){ctx.fillRect(cx-s*40,cy-s*5,s*80,s*10)}},
{id:'D',type:'triangle',x:-45,y:-18,w:20,h:20,label:'Kuyruk',color:'#f59e0b',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx,cy-s*10);ctx.lineTo(cx-s*10,cy+s*10);ctx.lineTo(cx+s*10,cy+s*10);ctx.closePath()}}
]},
{name:'Kale',slots:[
{id:'A',type:'rect',x:0,y:10,w:90,h:60,label:'Duvar',color:'#78716c',draw:function(cx,cy,s){ctx.fillRect(cx-s*45,cy-s*30,s*90,s*60)}},
{id:'B',type:'rect',x:-30,y:-30,w:15,h:30,label:'Sol Kule',color:'#57534e',draw:function(cx,cy,s){ctx.fillRect(cx-s*7,cy-s*15,s*15,s*30)}},
{id:'C',type:'rect',x:30,y:-30,w:15,h:30,label:'Sağ Kule',color:'#57534e',draw:function(cx,cy,s){ctx.fillRect(cx-s*7,cy-s*15,s*15,s*30)}},
{id:'D',type:'rect',x:0,y:25,w:20,h:30,label:'Kapı',color:'#44403c',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*10,cy+s*15);ctx.lineTo(cx-s*10,cy-s*5);ctx.arc(cx,cy-s*5,s*10,Math.PI,0);ctx.lineTo(cx+s*10,cy+s*15);ctx.closePath()}},
{id:'E',type:'triangle',x:0,y:-45,w:30,h:20,label:'Bayrak',color:'#ef4444',draw:function(cx,cy,s){ctx.beginPath();ctx.moveTo(cx-s*2,cy-s*10);ctx.lineTo(cx+s*15,cy);ctx.lineTo(cx-s*2,cy+s*10);ctx.closePath()}}
]}
];
function initRound(){const shape=SHAPES[(round-1)%SHAPES.length];
slots=[];pieces=[];placedCount=0;selectedPiece=-1;
const cx=W/2,cy=200;
for(let i=0;i<shape.slots.length;i++){const s=shape.slots[i];slots.push({id:s.id,label:s.label,color:s.color,cx:cx+s.x*1.5,cy:cy+s.y*1.5,draw:s.draw,filled:false})}
totalSlots=slots.length;
const pieceW=100,pieceH=70,gap=15;const totalW=totalSlots*pieceW+(totalSlots-1)*gap;const startX=Math.max(20,(W-totalW)/2);const pieceY=H-120;
const indices=shuffle(Array.from({length:totalSlots},function(_,i){return i}));
for(let i=0;i<totalSlots;i++){const si=indices[i];const s=slots[si];pieces.push({slotIdx:si,label:s.label,color:s.color,x:startX+i*(pieceW+gap),y:pieceY,w:pieceW,h:pieceH,placed:false,selected:false})}}
function drawShape(){ctx.save();ctx.globalAlpha=0.15;for(let i=0;i<slots.length;i++){const s=slots[i];if(!s.filled){ctx.fillStyle=s.color;s.draw(s.cx,s.cy,1.5);if(ctx.fill)ctx.fill()}}ctx.restore();
for(let i=0;i<slots.length;i++){const s=slots[i];if(s.filled){ctx.fillStyle=s.color;ctx.globalAlpha=0.9;s.draw(s.cx,s.cy,1.5);if(ctx.fill)ctx.fill();ctx.globalAlpha=1;ctx.strokeStyle='#4ade80';ctx.lineWidth=2;s.draw(s.cx,s.cy,1.5);ctx.stroke()}else{ctx.strokeStyle='#475569';ctx.lineWidth=1;ctx.setLineDash([4,4]);s.draw(s.cx,s.cy,1.5);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#94a3b8';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s.label,s.cx,s.cy)}}}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🔷 Tangram Zeka 🔷',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Parçaları seçip silüete yerleştir!',W/2,230);ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Önce parçayı tıkla, sonra yerine tıkla',W/2,265);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,327);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';ctx.fillText('Toplam Puan: '+score,W/2,260);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,327);return}
ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,20,30);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
const shape=SHAPES[(round-1)%SHAPES.length];ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.fillText('Şekil: '+shape.name,W/2,55);
drawShape();
ctx.fillStyle='#94a3b8';ctx.font='14px Segoe UI';ctx.textAlign='center';ctx.fillText('Parçalar — birini seçip yukarıdaki yerine tıkla:',W/2,H-160);
for(let i=0;i<pieces.length;i++){const p=pieces[i];if(p.placed)continue;
ctx.fillStyle=p.selected?'#312e81':'#94A3B8';ctx.strokeStyle=p.selected?'#818cf8':'#475569';ctx.lineWidth=p.selected?3:1;
ctx.beginPath();ctx.moveTo(p.x+8,p.y);ctx.lineTo(p.x+p.w-8,p.y);ctx.quadraticCurveTo(p.x+p.w,p.y,p.x+p.w,p.y+8);ctx.lineTo(p.x+p.w,p.y+p.h-8);ctx.quadraticCurveTo(p.x+p.w,p.y+p.h,p.x+p.w-8,p.y+p.h);ctx.lineTo(p.x+8,p.y+p.h);ctx.quadraticCurveTo(p.x,p.y+p.h,p.x,p.y+p.h-8);ctx.lineTo(p.x,p.y+8);ctx.quadraticCurveTo(p.x,p.y,p.x+8,p.y);ctx.closePath();ctx.fill();ctx.stroke();
ctx.save();const s=slots[p.slotIdx];ctx.fillStyle=p.color;ctx.globalAlpha=0.7;s.draw(p.x+p.w/2,p.y+p.h/2,0.5);if(ctx.fill)ctx.fill();ctx.restore();
ctx.fillStyle='#c7d2fe';ctx.font='11px Segoe UI';ctx.textAlign='center';ctx.fillText(p.label,p.x+p.w/2,p.y+p.h-6)}
particles.forEach(function(p){ctx.globalAlpha=p.life;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function update(){particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(function(p){return p.life>0});
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',function(e){const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return}
if(state==='win'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){round=1;score=0;state='start'}return}
for(let i=0;i<pieces.length;i++){const p=pieces[i];if(!p.placed&&mx>=p.x&&mx<=p.x+p.w&&my>=p.y&&my<=p.y+p.h){
pieces.forEach(function(pp){pp.selected=false});p.selected=true;selectedPiece=i;return}}
if(selectedPiece>=0){const piece=pieces[selectedPiece];const target=slots[piece.slotIdx];
const dist=Math.sqrt(Math.pow(mx-target.cx,2)+Math.pow(my-target.cy,2));
if(dist<60){piece.placed=true;piece.selected=false;target.filled=true;placedCount++;
beep(523,0.15);addP(target.cx,target.cy,'#4ade80');score+=10;selectedPiece=-1;
if(placedCount>=totalSlots){setTimeout(function(){round++;if(round>maxR){state='win'}else{initRound()}},1000)}}
else{let wrongSlot=false;for(let j=0;j<slots.length;j++){if(j!==piece.slotIdx&&!slots[j].filled){const s=slots[j];const d2=Math.sqrt(Math.pow(mx-s.cx,2)+Math.pow(my-s.cy,2));
if(d2<60){wrongSlot=true;break}}}
if(wrongSlot){beep(180,0.3)}}}});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_mantik_izgarasi_html():
    """Mantık Izgarası — Mantıksal çıkarım ile ipuçlarından çözüm bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}
</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c'),ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
let gridState=[],solution=[],clues=[],people=[],attrs=[],feedback='',feedbackT=0,checkAnim=0;
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,c,r:2+Math.random()*4})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
const PUZZLES=[
{people:['Ali','Ayşe','Can'],attrs:['Kırmızı','Mavi','Yeşil'],
sol:[[1,0,0],[0,0,1],[0,1,0]],
clues:['Ali kırmızı sever.','Ayşe yeşil sever.','Can mavi sever.']},
{people:['Elif','Mert','Zeynep'],attrs:['Futbol','Basket','Yüzme'],
sol:[[0,1,0],[0,0,1],[1,0,0]],
clues:['Elif basket oynar.','Zeynep futbol oynar.','Mert yüzme yapar.']},
{people:['Deniz','Berk','Sude'],attrs:['Kedi','Köpek','Kuş'],
sol:[[0,0,1],[1,0,0],[0,1,0]],
clues:['Deniz kuş besler.','Sude köpek besler.','Berk kedi besler.']},
{people:['Ece','Burak','Lale'],attrs:['Elma','Muz','Çilek'],
sol:[[0,1,0],[1,0,0],[0,0,1]],
clues:['Ece muz sever.','Burak elma sever.','Lale çilek sever.']},
{people:['Yusuf','Naz','Kaan'],attrs:['Resim','Müzik','Dans'],
sol:[[1,0,0],[0,0,1],[0,1,0]],
clues:['Yusuf resim yapar.','Kaan müzik çalar.','Naz dans eder.']},
{people:['Selin','Emre','Defne'],attrs:['Pizza','Makarna','Pilav'],
sol:[[0,0,1],[0,1,0],[1,0,0]],
clues:['Selin pilav sever.','Emre makarna sever.','Defne pizza sever.']},
{people:['Ahmet','Melis','Ozan'],attrs:['Bisiklet','Kaykay','Paten'],
sol:[[0,1,0],[1,0,0],[0,0,1]],
clues:['Ahmet kaykay sürer.','Melis bisiklet sürer.','Ozan paten yapar.']},
{people:['İrem','Barış','Ceren'],attrs:['Kitap','Oyun','Film'],
sol:[[1,0,0],[0,1,0],[0,0,1]],
clues:['İrem kitap okur.','Barış oyun oynar.','Ceren film izler.']},
{people:['Doruk','Nil','Kerem'],attrs:['Çizim','Yazma','Hesap'],
sol:[[0,0,1],[1,0,0],[0,1,0]],
clues:['Doruk hesap yapar.','Nil çizim yapar.','Kerem yazma sever.']},
{people:['Pınar','Umut','Asya'],attrs:['Kış','Yaz','Bahar'],
sol:[[0,1,0],[0,0,1],[1,0,0]],
clues:['Pınar yazı sever.','Umut baharı sever.','Asya kışı sever.']}
];
function initRound(){const pz=PUZZLES[(round-1)%PUZZLES.length];
people=pz.people;attrs=pz.attrs;solution=pz.sol;clues=pz.clues;
gridState=[];for(let r=0;r<3;r++){gridState[r]=[];for(let c=0;c<3;c++)gridState[r][c]=0}
feedback='';feedbackT=0;checkAnim=0}
const GS=70,GX=180,GY=240,LH=30,LY=100;
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🧩 Mantık Izgarası 🧩',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('İpuçlarını oku, tabloyu doldur!',W/2,230);ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Hücrelere tıklayarak ✓ veya ✗ koy',W/2,265);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,327);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';ctx.fillText('Toplam Puan: '+score,W/2,260);ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,327);return}
ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,20,30);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
ctx.textAlign='left';ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.fillText('İpuçları:',30,LY-10);
for(let i=0;i<clues.length;i++){ctx.fillStyle='#94A3B8';ctx.strokeStyle='#334155';ctx.lineWidth=1;
const cw=W-60,cy=LY+i*LH;
ctx.beginPath();ctx.moveTo(30+6,cy);ctx.lineTo(30+cw-6,cy);ctx.quadraticCurveTo(30+cw,cy,30+cw,cy+6);ctx.lineTo(30+cw,cy+LH-8);ctx.quadraticCurveTo(30+cw,cy+LH-2,30+cw-6,cy+LH-2);ctx.lineTo(36,cy+LH-2);ctx.quadraticCurveTo(30,cy+LH-2,30,cy+LH-8);ctx.lineTo(30,cy+6);ctx.quadraticCurveTo(30,cy,36,cy);ctx.closePath();ctx.fill();ctx.stroke();
ctx.fillStyle='#c7d2fe';ctx.font='14px Segoe UI';ctx.textAlign='left';ctx.fillText('💡 '+clues[i],42,cy+LH/2+4)}
const gridX=GX+80,gridY=GY;
ctx.fillStyle='#94a3b8';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
for(let c=0;c<3;c++){ctx.fillText(attrs[c],gridX+c*GS+GS/2,gridY-10)}
ctx.textAlign='right';
for(let r=0;r<3;r++){ctx.fillStyle='#94a3b8';ctx.font='bold 14px Segoe UI';ctx.fillText(people[r],gridX-12,gridY+r*GS+GS/2+5)}
for(let r=0;r<3;r++){for(let c=0;c<3;c++){const cx=gridX+c*GS,cy=gridY+r*GS;
const isCorrectCell=checkAnim>0&&solution[r][c]===1;
ctx.fillStyle=isCorrectCell?'#14532d':'#0B0F19';ctx.strokeStyle='#334155';ctx.lineWidth=1;ctx.fillRect(cx,cy,GS,GS);ctx.strokeRect(cx,cy,GS,GS);
if(gridState[r][c]===1){ctx.fillStyle='#22c55e';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('✓',cx+GS/2,cy+GS/2)}
else if(gridState[r][c]===-1){ctx.fillStyle='#ef4444';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('✗',cx+GS/2,cy+GS/2)}}}
ctx.strokeStyle='#6366f1';ctx.lineWidth=3;ctx.strokeRect(gridX,gridY,3*GS,3*GS);
const btnX=gridX+3*GS+30,btnY=gridY+40;
ctx.fillStyle='#166534';ctx.strokeStyle='#22c55e';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(btnX+8,btnY);ctx.lineTo(btnX+112,btnY);ctx.quadraticCurveTo(btnX+120,btnY,btnX+120,btnY+8);ctx.lineTo(btnX+120,btnY+42);ctx.quadraticCurveTo(btnX+120,btnY+50,btnX+112,btnY+50);ctx.lineTo(btnX+8,btnY+50);ctx.quadraticCurveTo(btnX,btnY+50,btnX,btnY+42);ctx.lineTo(btnX,btnY+8);ctx.quadraticCurveTo(btnX,btnY,btnX+8,btnY);ctx.closePath();
ctx.fill();ctx.stroke();ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('Kontrol Et',btnX+60,btnY+25);
const clrBtnY=btnY+70;
ctx.fillStyle='#7f1d1d';ctx.strokeStyle='#ef4444';ctx.lineWidth=2;
ctx.beginPath();ctx.moveTo(btnX+8,clrBtnY);ctx.lineTo(btnX+112,clrBtnY);ctx.quadraticCurveTo(btnX+120,clrBtnY,btnX+120,clrBtnY+8);ctx.lineTo(btnX+120,clrBtnY+42);ctx.quadraticCurveTo(btnX+120,clrBtnY+50,btnX+112,clrBtnY+50);ctx.lineTo(btnX+8,clrBtnY+50);ctx.quadraticCurveTo(btnX,clrBtnY+50,btnX,clrBtnY+42);ctx.lineTo(btnX,clrBtnY+8);ctx.quadraticCurveTo(btnX,clrBtnY,btnX+8,clrBtnY);ctx.closePath();
ctx.fill();ctx.stroke();ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('Temizle',btnX+60,clrBtnY+25);
if(feedbackT>0){ctx.globalAlpha=Math.min(1,feedbackT/30);ctx.fillStyle=feedback.indexOf('Doğru')>=0?'#22c55e':'#ef4444';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.textBaseline='top';ctx.fillText(feedback,W/2,gridY+3*GS+25);ctx.globalAlpha=1}
particles.forEach(function(p){ctx.globalAlpha=p.life;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function checkSolution(){for(let r=0;r<3;r++){for(let c=0;c<3;c++){const expected=solution[r][c];const actual=gridState[r][c];
if(expected===1&&actual!==1)return false;if(expected===0&&actual!==-1&&actual!==0)return false}}return true}
function update(){if(feedbackT>0)feedbackT--;if(checkAnim>0)checkAnim--;
particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(function(p){return p.life>0});
draw();requestAnimationFrame(update)}
canvas.addEventListener('click',function(e){const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return}
if(state==='win'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){round=1;score=0;state='start'}return}
const gridX2=GX+80,gridY2=GY;
for(let r=0;r<3;r++){for(let c=0;c<3;c++){const cx=gridX2+c*GS,cy=gridY2+r*GS;
if(mx>=cx&&mx<=cx+GS&&my>=cy&&my<=cy+GS){if(gridState[r][c]===0)gridState[r][c]=1;else if(gridState[r][c]===1)gridState[r][c]=-1;else gridState[r][c]=0;return}}}
const btnX2=gridX2+3*GS+30,btnY2=gridY2+40;
if(mx>=btnX2&&mx<=btnX2+120&&my>=btnY2&&my<=btnY2+50){
if(checkSolution()){score+=10;feedback='Doğru! +10 Puan!';feedbackT=80;checkAnim=60;beep(523,0.15);
addP(W/2,gridY2+3*GS+30,'#22c55e');addP(W/2-40,gridY2+3*GS+30,'#4ade80');addP(W/2+40,gridY2+3*GS+30,'#22c55e');
setTimeout(function(){round++;if(round>maxR){state='win'}else{initRound()}},1500)}
else{feedback='Yanlış! Tekrar dene.';feedbackT=80;beep(180,0.3)}return}
const clrBtnY2=btnY2+70;
if(mx>=btnX2&&mx<=btnX2+120&&my>=clrBtnY2&&my<=clrBtnY2+50){for(let r=0;r<3;r++)for(let c=0;c<3;c++)gridState[r][c]=0;feedback='';feedbackT=0}});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""
