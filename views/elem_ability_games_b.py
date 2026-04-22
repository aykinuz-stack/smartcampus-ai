# -*- coding: utf-8 -*-
"""İlkokul Genel Yetenek Oyunları — 5 Premium HTML5 Oyun (Bölüm B: 6-10)."""


def _build_elem_ab_sifre_cozme_html():
    """Şifre Çözme (Basit Kripto) — Caesar cipher ile şifrelenmiş kelimeyi çöz."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c'),ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
const ALP='ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ';
const WORDS=['KALEM','OKUL','SINIF','KITAP','DEFTER','MASA','TAHTA','SILGI','CETVEL','BOYA','ATLAS','HARITA','RESIM','OYUN','BILGI','DERS','KARNE','ODEV','SANAT','MUZIK'];
let shift=1,targetWord='',encodedWord='',decoded=[],curPos=0,feedback='',feedTimer=0,roundDone=false,roundCorrect=false;
function encode(w,s){let r='';for(let i=0;i<w.length;i++){let idx=ALP.indexOf(w[i]);if(idx>=0){r+=ALP[(idx+s)%ALP.length]}else r+=w[i]}return r}
function decode(ch,s){let idx=ALP.indexOf(ch);if(idx>=0)return ALP[(idx-s+ALP.length)%ALP.length];return ch}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
function initRound(){shift=1+Math.floor(Math.random()*5);targetWord=WORDS[(round-1+Math.floor(Math.random()*WORDS.length))%WORDS.length];encodedWord=encode(targetWord,shift);decoded=new Array(targetWord.length).fill('');curPos=0;feedback='';feedTimer=0;roundDone=false;roundCorrect=false}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🔐 Şifre Çözme',W/2,160);ctx.font='20px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Caesar şifresini çöz, gizli kelimeyi bul!',W/2,210);ctx.fillText('Anahtar sayısı kadar harf geri say.',W/2,240);ctx.font='16px Segoe UI';ctx.fillStyle='#64748b';ctx.fillText('Örnek: Anahtar +2 → C harfi aslında A\\'dır',W/2,275);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,332);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e2e8f0';ctx.font='24px Segoe UI';ctx.fillText('Şifre Çözme Tamamlandı!',W/2,250);ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,290);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,330,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,357);return}
/* HUD */
ctx.fillStyle='#e2e8f0';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,15,30);ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Alphabet reference */
ctx.fillStyle='rgba(30,30,60,0.7)';ctx.fillRect(15,50,W-30,40);ctx.fillStyle='#94a3b8';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';let alpStr='';for(let i=0;i<ALP.length;i++)alpStr+=ALP[i]+' ';ctx.fillText(alpStr.trim(),W/2,75);
/* Shift key display */
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText('🔑 Anahtar: +'+shift,W/2,125);
/* Encoded word display */
ctx.fillStyle='#e2e8f0';ctx.font='16px Segoe UI';ctx.fillText('Şifreli Kelime:',W/2,160);
const boxW=50,boxH=55,gap=8;const totalW=encodedWord.length*(boxW+gap)-gap;const startX=W/2-totalW/2;
for(let i=0;i<encodedWord.length;i++){const bx=startX+i*(boxW+gap);ctx.fillStyle=i===curPos&&!roundDone?'rgba(124,58,237,0.5)':'rgba(30,30,60,0.7)';ctx.strokeStyle=i===curPos&&!roundDone?'#a78bfa':'#475569';ctx.lineWidth=2;ctx.fillRect(bx,175,boxW,boxH);ctx.strokeRect(bx,175,boxW,boxH);ctx.fillStyle='#f472b6';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText(encodedWord[i],bx+boxW/2,207)}
/* Decoded word display */
ctx.fillStyle='#e2e8f0';ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText('Çözülen Kelime:',W/2,260);
for(let i=0;i<targetWord.length;i++){const bx=startX+i*(boxW+gap);ctx.fillStyle=decoded[i]?'rgba(52,211,153,0.3)':'rgba(15,15,35,0.7)';ctx.strokeStyle=decoded[i]?'#34d399':'#334155';ctx.lineWidth=2;ctx.fillRect(bx,275,boxW,boxH);ctx.strokeRect(bx,275,boxW,boxH);if(decoded[i]){ctx.fillStyle='#34d399';ctx.font='bold 24px Segoe UI';ctx.fillText(decoded[i],bx+boxW/2,307)}else{ctx.fillStyle='#475569';ctx.font='bold 24px Segoe UI';ctx.fillText('?',bx+boxW/2,307)}}
/* Arrow from encoded to decoded for current pos */
if(!roundDone&&curPos<encodedWord.length){const ax=startX+curPos*(boxW+gap)+boxW/2;ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(ax,232);ctx.lineTo(ax,272);ctx.stroke();ctx.beginPath();ctx.moveTo(ax-6,265);ctx.lineTo(ax,275);ctx.lineTo(ax+6,265);ctx.fill()}
/* Feedback message */
if(feedTimer>0){ctx.fillStyle=roundCorrect?'#34d399':'#ef4444';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,365)}
/* Letter buttons (A-Z Turkish) */
if(!roundDone){const bSize=42,bGap=4,cols=10;const rows=Math.ceil(ALP.length/cols);const gridW=cols*(bSize+bGap)-bGap;const gridStartX=W/2-gridW/2;const gridStartY=390;
for(let i=0;i<ALP.length;i++){const col=i%cols,row=Math.floor(i/cols);const bx=gridStartX+col*(bSize+bGap),by=gridStartY+row*(bSize+bGap);ctx.fillStyle='rgba(51,65,85,0.8)';ctx.strokeStyle='#64748b';ctx.lineWidth=1;ctx.fillRect(bx,by,bSize,bSize);ctx.strokeRect(bx,by,bSize,bSize);ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(ALP[i],bx+bSize/2,by+bSize/2+6)}}
/* Hint text */
ctx.fillStyle='#64748b';ctx.font='14px Segoe UI';ctx.textAlign='center';if(!roundDone){ctx.fillText('İpucu: "'+encodedWord[curPos]+'" harfinden '+shift+' geri say → ?',W/2,585)}
/* Next button when done */
if(roundDone){ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-70,580,140,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Sonraki ▶',W/2,607)}}
function update(){if(feedTimer>0)feedTimer--;particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(update)}
function handleLetterClick(letter){if(roundDone||curPos>=targetWord.length)return;const correct=targetWord[curPos];if(letter===correct){decoded[curPos]=letter;curPos++;beep(523,0.15);addP(W/2,300,'#34d399');if(curPos>=targetWord.length){roundDone=true;roundCorrect=true;score+=10;feedback='Doğru! Kelime: '+targetWord;feedTimer=120}}else{beep(180,0.3);feedback='Yanlış! Tekrar dene.';feedTimer=60}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(my>305&&my<345&&mx>W/2-80&&mx<W/2+80){state='play';round=1;score=0;initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<370){state='start'}return}
if(state==='play'){
/* Next button */
if(roundDone&&my>580&&my<620&&mx>W/2-70&&mx<W/2+70){round++;if(round>maxR){state='win'}else{initRound()}return}
/* Letter buttons */
if(!roundDone){const bSize=42,bGap=4,cols=10;const gridW=cols*(bSize+bGap)-bGap;const gridStartX=W/2-gridW/2;const gridStartY=390;
for(let i=0;i<ALP.length;i++){const col=i%cols,row=Math.floor(i/cols);const bx=gridStartX+col*(bSize+bGap),by=gridStartY+row*(bSize+bGap);if(mx>bx&&mx<bx+bSize&&my>by&&my<by+bSize){handleLetterClick(ALP[i]);return}}}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_elem_ab_siralama_html():
    """Sıralama Oyunu — Farklı türde öğeleri doğru sıraya diz."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c'),ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
const COLORS=['#f472b6','#a78bfa','#fbbf24','#34d399','#60a5fa','#fb923c'];
const TYPES=['numbers','words','lengths','weights'];
const NUM_SETS=[[38,12,55,7,91,23],[4,67,19,83,41,56],[9,34,72,15,48,88],[27,63,5,81,44,16],[3,58,21,76,39,92]];
const WORD_SETS=[['Fil','Arı','Ceylan','Balık','Deve','Aslan'],['Elma','Çilek','Armut','Dut','Fındık','Böğürtlen'],['Kalem','Ağaç','Bulut','Defter','Ev','Fare'],['Güneş','Ay','Dünya','Bulut','Deniz','Ateş'],['Ada','Bayrak','Cam','Dağ','Eczane','Fener']];
const LEN_SETS=[['at','kedi','papağan','su','kalem','fil'],['ok','masa','bilgisayar','göl','araba','diz'],['el','ayak','telefon','top','bisiklet','kuş'],['ip','köy','otobüs','dal','uçak','gül'],['un','park','helikopter','yol','kitap','bal']];
const WGT_SETS=[[['Tüy','5g'],['Kalem','20g'],['Elma','150g'],['Kitap','400g'],['Laptop','2kg'],['Sandalye','5kg']],[['Toz','1g'],['Silgi','15g'],['Portakal','200g'],['Ayakkabı','500g'],['Çanta','3kg'],['Masa','8kg']],[['Yaprak','2g'],['Anahtar','25g'],['Muz','120g'],['Şişe','350g'],['Karpuz','4kg'],['Bisiklet','12kg']],[['İğne','1g'],['Bozuk Para','8g'],['Yumurta','60g'],['Telefon','200g'],['Sözlük','1kg'],['Televizyon','10kg']],[['Tüy','3g'],['Düğme','5g'],['Limon','80g'],['Bardak','250g'],['Sırt Çantası','2kg'],['Buzdolabı','50kg']]];
let items=[],slots=[],selected=-1,taskType='',taskLabel='',roundDone=false,checkTimer=0;
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function initRound(){selected=-1;roundDone=false;checkTimer=0;
const tIdx=(round-1)%TYPES.length;taskType=TYPES[tIdx];
const setIdx=(round-1)%5;
if(taskType==='numbers'){const nums=[...NUM_SETS[setIdx]];const sorted=[...nums].sort((a,b)=>a-b);items=shuffle(nums.map((n,i)=>({label:''+n,val:n,color:COLORS[i%6]})));taskLabel='Küçükten Büyüğe Sırala';slots=sorted.map((n,i)=>({target:''+n,filled:null,idx:i}))}
else if(taskType==='words'){const ws=[...WORD_SETS[setIdx]];const sorted=[...ws].sort((a,b)=>a.localeCompare(b,'tr'));items=shuffle(ws.map((w,i)=>({label:w,val:w,color:COLORS[i%6]})));taskLabel='Alfabetik Sıraya Diz';slots=sorted.map((w,i)=>({target:w,filled:null,idx:i}))}
else if(taskType==='lengths'){const ls=[...LEN_SETS[setIdx]];const sorted=[...ls].sort((a,b)=>a.length-b.length);items=shuffle(ls.map((w,i)=>({label:w,val:w,color:COLORS[i%6]})));taskLabel='Kısadan Uzuna Sırala (Harf Sayısı)';slots=sorted.map((w,i)=>({target:w,filled:null,idx:i}))}
else{const wt=[...WGT_SETS[setIdx]];const sorted=[...wt].sort((a,b)=>{const pa=parseFloat(a[1]),pb=parseFloat(b[1]);const ua=a[1].includes('kg')?1000:1,ub=b[1].includes('kg')?1000:1;return pa*ua-pb*ub});items=shuffle(wt.map((w,i)=>({label:w[0]+' ('+w[1]+')',val:w[0],color:COLORS[i%6]})));taskLabel='Hafiften Ağıra Sırala';slots=sorted.map((w,i)=>({target:w[0],filled:null,idx:i}))}}
function checkComplete(){const allFilled=slots.every(s=>s.filled!==null);if(!allFilled)return;let allCorrect=true;for(let i=0;i<slots.length;i++){let match=false;if(taskType==='weights'){if(slots[i].filled&&slots[i].filled.val===slots[i].target)match=true}else{if(slots[i].filled&&slots[i].filled.label===''+slots[i].target)match=true}if(!match)allCorrect=false}
if(allCorrect){roundDone=true;score+=10;beep(523,0.15);addP(W/2,400,'#34d399');checkTimer=90}else{beep(180,0.3);/* Reset all slots */
items.forEach(it=>it.placed=false);slots.forEach(s=>s.filled=null);selected=-1;checkTimer=0}}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('📊 Sıralama Oyunu',W/2,160);ctx.font='20px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Öğeleri doğru sıraya yerleştir!',W/2,210);ctx.fillText('Sayılar, kelimeler, uzunluklar, ağırlıklar...',W/2,240);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,332);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e2e8f0';ctx.font='24px Segoe UI';ctx.fillText('Sıralama Ustası!',W/2,250);ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,290);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,330,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,357);return}
/* HUD */
ctx.fillStyle='#e2e8f0';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,15,30);ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Task label */
ctx.fillStyle='#a78bfa';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(taskLabel,W/2,65);
/* Items row */
const iW=95,iH=55,iGap=10;const totalIW=6*(iW+iGap)-iGap;const iStartX=W/2-totalIW/2;
for(let i=0;i<items.length;i++){if(items[i].placed)continue;const ix=iStartX+i*(iW+iGap),iy=100;ctx.fillStyle=i===selected?'rgba(124,58,237,0.8)':items[i].color+'33';ctx.strokeStyle=i===selected?'#fbbf24':items[i].color;ctx.lineWidth=i===selected?3:2;ctx.fillRect(ix,iy,iW,iH);ctx.strokeRect(ix,iy,iW,iH);ctx.fillStyle='#e2e8f0';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';const lbl=items[i].label;if(lbl.length>10){ctx.font='bold 11px Segoe UI'}ctx.fillText(lbl,ix+iW/2,iy+iH/2+5)}
/* Slots row */
ctx.fillStyle='#94a3b8';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('Sıralama Kutuları (1 → 6):',W/2,210);
const sW=95,sH=70,sGap=10;const totalSW=6*(sW+sGap)-sGap;const sStartX=W/2-totalSW/2;
for(let i=0;i<6;i++){const sx=sStartX+i*(sW+sGap),sy=230;if(slots[i].filled){ctx.fillStyle=slots[i].filled.color+'55';ctx.strokeStyle=slots[i].filled.color;ctx.lineWidth=2;ctx.fillRect(sx,sy,sW,sH);ctx.strokeRect(sx,sy,sW,sH);ctx.fillStyle='#e2e8f0';ctx.font='bold 13px Segoe UI';const fl=slots[i].filled.label;if(fl.length>10)ctx.font='bold 10px Segoe UI';ctx.fillText(fl,sx+sW/2,sy+sH/2+5)}else{ctx.strokeStyle='#475569';ctx.lineWidth=2;ctx.setLineDash([5,5]);ctx.strokeRect(sx,sy,sW,sH);ctx.setLineDash([]);ctx.fillStyle='#475569';ctx.font='bold 24px Segoe UI';ctx.fillText(''+(i+1),sx+sW/2,sy+sH/2+8)}}
/* Status */
if(roundDone){ctx.fillStyle='#34d399';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText('✓ Mükemmel! Doğru sıralama!',W/2,360);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-70,380,140,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Sonraki ▶',W/2,407)}
if(selected>=0&&!roundDone){ctx.fillStyle='#fbbf24';ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText('Şimdi bir kutuya tıkla!',W/2,360)}
/* Instruction */
if(!roundDone&&selected<0){ctx.fillStyle='#64748b';ctx.font='16px Segoe UI';ctx.textAlign='center';ctx.fillText('Bir öğeye tıkla, sonra hedef kutuya yerleştir.',W/2,360)}}
function update(){if(checkTimer>0)checkTimer--;particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(update)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(my>305&&my<345&&mx>W/2-80&&mx<W/2+80){state='play';round=1;score=0;initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<370){state='start'}return}
if(state==='play'){
if(roundDone&&my>380&&my<420&&mx>W/2-70&&mx<W/2+70){round++;if(round>maxR){state='win'}else{initRound()}return}
if(roundDone)return;
/* Check items click */
const iW=95,iH=55,iGap=10;const totalIW=6*(iW+iGap)-iGap;const iStartX=W/2-totalIW/2;
for(let i=0;i<items.length;i++){if(items[i].placed)continue;const ix=iStartX+i*(iW+iGap),iy=100;if(mx>ix&&mx<ix+iW&&my>iy&&my<iy+iH){selected=i;return}}
/* Check slots click */
if(selected>=0){const sW=95,sH=70,sGap=10;const totalSW=6*(sW+sGap)-sGap;const sStartX=W/2-totalSW/2;
for(let i=0;i<6;i++){const sx=sStartX+i*(sW+sGap),sy=230;if(mx>sx&&mx<sx+sW&&my>sy&&my<sy+sH){if(slots[i].filled){/* swap: put old item back */
slots[i].filled.placed=false}slots[i].filled=items[selected];items[selected].placed=true;selected=-1;checkComplete();return}}}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_elem_ab_desen_kural_html():
    """Desen ve Kural Bulma — Sayı/şekil dizisindeki kuralı bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c'),ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
const COLORS=['#f472b6','#a78bfa','#fbbf24','#34d399','#60a5fa','#fb923c'];
let seqItems=[],options=[],correctIdx=0,feedback='',feedTimer=0,shakeTimer=0,shakeIdx=-1,pulseTimer=0,pulseIdx=-1,roundDone=false,ruleText='';
function genPatterns(){
const pType=Math.floor(Math.random()*6);let seq=[],ans,rule,opts=[];
if(pType===0){/* +N arithmetic */
const step=2+Math.floor(Math.random()*4);const start=1+Math.floor(Math.random()*10);seq=[];for(let i=0;i<5;i++)seq.push(start+step*i);ans=start+step*5;rule='+'+step+' artarak gidiyor';opts=[ans,ans+step,ans-1,ans+step*2]}
else if(pType===1){/* *2 geometric */
const start=1+Math.floor(Math.random()*3);seq=[start];for(let i=1;i<5;i++)seq.push(seq[i-1]*2);ans=seq[4]*2;rule='Her sayı 2 katına çıkıyor';opts=[ans,ans+2,ans/2,ans-1]}
else if(pType===2){/* -N descending */
const step=2+Math.floor(Math.random()*3);const start=50+Math.floor(Math.random()*20);seq=[];for(let i=0;i<5;i++)seq.push(start-step*i);ans=start-step*5;rule='-'+step+' azalarak gidiyor';opts=[ans,ans+step,ans-step,ans+1]}
else if(pType===3){/* alternating +a +b */
const a=2,b=3+Math.floor(Math.random()*3);const start=1+Math.floor(Math.random()*5);seq=[start];for(let i=1;i<5;i++){seq.push(seq[i-1]+(i%2===1?a:b))}ans=seq[4]+(5%2===1?a:b);rule='+'+a+', +'+b+' sırayla ekleniyor';opts=[ans,ans+1,ans-1,ans+a+b]}
else if(pType===4){/* square numbers */
const off=Math.floor(Math.random()*3);seq=[];for(let i=1;i<=5;i++)seq.push((i+off)*(i+off));ans=(6+off)*(6+off);rule='Kare sayılar dizisi';opts=[ans,ans+1,ans-1,(5+off)*(5+off)+1]}
else{/* fibonacci-like */
const a=1+Math.floor(Math.random()*3),b=1+Math.floor(Math.random()*3);seq=[a,b];for(let i=2;i<5;i++)seq.push(seq[i-1]+seq[i-2]);ans=seq[4]+seq[3];rule='Her sayı önceki ikisinin toplamı';opts=[ans,ans+1,ans-2,seq[4]+1]}
/* Shuffle options */
const correct=opts[0];opts=opts.sort(()=>Math.random()-.5);correctIdx=opts.indexOf(correct);seqItems=seq.map(v=>''+v);options=opts.map(v=>''+v);ruleText=rule;return correct}
function initRound(){feedback='';feedTimer=0;shakeTimer=0;shakeIdx=-1;pulseTimer=0;pulseIdx=-1;roundDone=false;genPatterns()}
function drawCircle(x,y,r,text,color,shake,pulse){ctx.save();let ox=0;if(shake>0)ox=Math.sin(shake*1.5)*5;if(pulse>0){const sc=1+Math.sin(pulse*0.3)*0.1;ctx.translate(x+ox,y);ctx.scale(sc,sc);ctx.translate(-(x+ox),-y)}
ctx.fillStyle=color+'44';ctx.strokeStyle=color;ctx.lineWidth=3;ctx.beginPath();ctx.arc(x+ox,y,r,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle='#e2e8f0';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,x+ox,y);ctx.restore()}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🔢 Desen ve Kural Bulma',W/2,160);ctx.font='20px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Sayı dizisindeki kuralı keşfet!',W/2,210);ctx.fillText('Sıradaki sayıyı tahmin et.',W/2,240);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,332);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e2e8f0';ctx.font='24px Segoe UI';ctx.fillText('Desen Ustası Oldun!',W/2,250);ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,290);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,330,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,357);return}
/* HUD */
ctx.fillStyle='#e2e8f0';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,15,30);ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Title */
ctx.fillStyle='#a78bfa';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText('Sıradaki sayı ne?',W/2,65);
/* Sequence circles */
const totalItems=seqItems.length+1;const gap=90;const seqStartX=W/2-(totalItems*gap)/2+gap/2;const seqY=170;
for(let i=0;i<seqItems.length;i++){drawCircle(seqStartX+i*gap,seqY,35,seqItems[i],COLORS[i%COLORS.length],0,0);
/* Arrow between */
if(i<seqItems.length-1){ctx.fillStyle='#475569';ctx.font='20px Segoe UI';ctx.textAlign='center';ctx.fillText('→',seqStartX+i*gap+gap/2,seqY)}}
/* Question mark circle */
const qx=seqStartX+seqItems.length*gap;ctx.fillStyle='#475569';ctx.font='20px Segoe UI';ctx.textAlign='center';ctx.fillText('→',qx-gap/2,seqY);
if(roundDone&&pulseIdx>=0){drawCircle(qx,seqY,35,options[correctIdx],'#34d399',0,pulseTimer)}else{ctx.fillStyle='rgba(71,85,105,0.4)';ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;ctx.setLineDash([8,4]);ctx.beginPath();ctx.arc(qx,seqY,35,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#fbbf24';ctx.font='bold 32px Segoe UI';ctx.fillText('?',qx,seqY+2)}
/* Options */
ctx.fillStyle='#e2e8f0';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Cevabını Seç:',W/2,280);
const optW=130,optH=60,optGap=20;const totalOptW=4*(optW+optGap)-optGap;const optStartX=W/2-totalOptW/2;const optY=310;
for(let i=0;i<options.length;i++){const ox=optStartX+i*(optW+optGap);let sh=0;if(i===shakeIdx&&shakeTimer>0)sh=shakeTimer;let pl=0;if(i===pulseIdx&&pulseTimer>0)pl=pulseTimer;
ctx.save();let offx=0;if(sh>0)offx=Math.sin(sh*1.5)*5;
let bgColor='rgba(51,65,85,0.7)';let borderColor='#64748b';if(roundDone&&i===correctIdx){bgColor='rgba(52,211,153,0.3)';borderColor='#34d399'}else if(i===shakeIdx&&shakeTimer>0){bgColor='rgba(239,68,68,0.3)';borderColor='#ef4444'}
if(pl>0){const sc=1+Math.sin(pl*0.3)*0.05;ctx.translate(ox+optW/2+offx,optY+optH/2);ctx.scale(sc,sc);ctx.translate(-(ox+optW/2+offx),-(optY+optH/2))}
ctx.fillStyle=bgColor;ctx.strokeStyle=borderColor;ctx.lineWidth=2;ctx.fillRect(ox+offx,optY,optW,optH);ctx.strokeRect(ox+offx,optY,optW,optH);
ctx.fillStyle='#e2e8f0';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText(options[i],ox+optW/2+offx,optY+optH/2+8);
ctx.fillStyle='#64748b';ctx.font='bold 14px Segoe UI';ctx.fillText(String.fromCharCode(65+i),ox+offx+15,optY+18);ctx.restore()}
/* Feedback */
if(feedTimer>0){ctx.fillStyle=feedback.includes('Doğru')?'#34d399':'#ef4444';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,420)}
/* Rule reveal */
if(roundDone){ctx.fillStyle='rgba(30,30,60,0.8)';ctx.fillRect(W/2-200,440,400,40);ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('Kural: '+ruleText,W/2,465);
ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-70,500,140,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Sonraki ▶',W/2,527)}}
function update(){if(feedTimer>0)feedTimer--;if(shakeTimer>0)shakeTimer--;if(pulseTimer>0)pulseTimer--;particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(update)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(my>305&&my<345&&mx>W/2-80&&mx<W/2+80){state='play';round=1;score=0;initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<370){state='start'}return}
if(state==='play'){
if(roundDone&&my>500&&my<540&&mx>W/2-70&&mx<W/2+70){round++;if(round>maxR){state='win'}else{initRound()}return}
if(roundDone)return;
/* Options click */
const optW=130,optH=60,optGap=20;const totalOptW=4*(optW+optGap)-optGap;const optStartX=W/2-totalOptW/2;const optY=310;
for(let i=0;i<options.length;i++){const ox=optStartX+i*(optW+optGap);if(mx>ox&&mx<ox+optW&&my>optY&&my<optY+optH){if(i===correctIdx){score+=10;feedback='✓ Doğru! +10 Puan';feedTimer=120;pulseIdx=i;pulseTimer=60;roundDone=true;beep(523,0.15);addP(W/2,350,'#34d399')}else{feedback='✗ Yanlış! Tekrar dene.';feedTimer=60;shakeIdx=i;shakeTimer=30;beep(180,0.3)}return}}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_elem_ab_labirent_engel_html():
    """Labirent + Engeller — Kısıtlı hamle sayısıyla labirentten çık."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c'),ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
const GS=8;let grid=[],px=0,py=0,moves=0,maxMoves=25,keys=0,totalKeys=0,roundDone=false,roundFail=false,failMsg='';
/* 0=path,1=wall,2=trap,3=key,4=door,5=exit */
function carve(g,x,y){g[y][x]=0;const dirs=[[0,-2],[0,2],[-2,0],[2,0]].sort(()=>Math.random()-.5);for(const[dx,dy]of dirs){const nx=x+dx,ny=y+dy;if(nx>=0&&nx<GS&&ny>=0&&ny<GS&&g[ny][nx]===1){g[y+dy/2][x+dx/2]=0;carve(g,nx,ny)}}}
function genMaze(){grid=[];for(let y=0;y<GS;y++){grid[y]=[];for(let x=0;x<GS;x++)grid[y][x]=1}
carve(grid,0,0);grid[0][0]=0;grid[GS-1][GS-1]=5;
/* Ensure more open paths for smaller grid */
for(let i=0;i<GS*2;i++){const rx=Math.floor(Math.random()*(GS-2))+1;const ry=Math.floor(Math.random()*(GS-2))+1;if(grid[ry][rx]===1){let adj=0;if(ry>0&&grid[ry-1][rx]!==1)adj++;if(ry<GS-1&&grid[ry+1][rx]!==1)adj++;if(rx>0&&grid[ry][rx-1]!==1)adj++;if(rx<GS-1&&grid[ry][rx+1]!==1)adj++;if(adj>=1)grid[ry][rx]=0}}
/* Place traps and keys */
let freeCells=[];for(let y=0;y<GS;y++)for(let x=0;x<GS;x++){if(grid[y][x]===0&&!(x===0&&y===0)&&!(x===GS-1&&y===GS-1))freeCells.push([x,y])}
freeCells.sort(()=>Math.random()-.5);
const numTraps=Math.min(2+Math.floor(round/3),freeCells.length-2);const numKeys=Math.min(1+Math.floor(round/4),3);totalKeys=0;
for(let i=0;i<numTraps&&i<freeCells.length;i++){const[fx,fy]=freeCells[i];grid[fy][fx]=2}
for(let i=numTraps;i<numTraps+numKeys&&i<freeCells.length;i++){const[fx,fy]=freeCells[i];grid[fy][fx]=3;totalKeys++}
/* Place door near exit if keys exist */
if(totalKeys>0){const doorCands=[[GS-2,GS-1],[GS-1,GS-2]];for(const[dx,dy]of doorCands){if(dx>=0&&dy>=0&&dx<GS&&dy<GS&&grid[dy][dx]===0){grid[dy][dx]=4;break}}}}
function initRound(){px=0;py=0;moves=0;maxMoves=18+round*2;keys=0;roundDone=false;roundFail=false;failMsg='';genMaze()}
function tryMove(dx,dy){if(roundDone||roundFail)return;const nx=px+dx,ny=py+dy;if(nx<0||nx>=GS||ny<0||ny>=GS)return;const cell=grid[ny][nx];if(cell===1)return;if(cell===4&&keys<totalKeys){beep(180,0.3);failMsg='Kapı kilitli! Anahtar topla.';return}
moves++;failMsg='';
if(cell===2){moves+=2;beep(180,0.15);addP(350,300,'#ef4444')}
if(cell===3){keys++;grid[ny][nx]=0;beep(523,0.1);addP(350,300,'#fbbf24')}
if(cell===4){grid[ny][nx]=0}
px=nx;py=ny;
if(cell===5){roundDone=true;score+=10;beep(523,0.15);addP(350,300,'#34d399')}
if(moves>=maxMoves&&!roundDone){roundFail=true;beep(180,0.3)}}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🏰 Labirent + Engeller',W/2,160);ctx.font='20px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Labirentte yolunu bul!',W/2,210);ctx.fillText('Tuzaklara dikkat et, anahtarları topla!',W/2,240);ctx.font='16px Segoe UI';ctx.fillStyle='#64748b';ctx.fillText('⬛ Duvar  🔴 Tuzak(-2 hamle)  🔑 Anahtar  🚪 Kapı',W/2,275);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,332);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e2e8f0';ctx.font='24px Segoe UI';ctx.fillText('Labirent Ustası!',W/2,250);ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,290);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,330,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,357);return}
/* HUD */
ctx.fillStyle='#e2e8f0';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,15,30);ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Move counter */
ctx.textAlign='center';const moveColor=moves>maxMoves*0.7?'#ef4444':'#34d399';ctx.fillStyle=moveColor;ctx.font='bold 18px Segoe UI';ctx.fillText('Hamle: '+moves+' / '+maxMoves,W/2,30);
/* Key counter */
if(totalKeys>0){ctx.fillStyle='#fbbf24';ctx.textAlign='left';ctx.fillText('🔑 '+keys+'/'+totalKeys,15,55)}
/* Grid */
const cellSize=Math.min(50,Math.floor(440/GS));const gridW=GS*cellSize,gridH=GS*cellSize;const gx=W/2-gridW/2,gy=75;
for(let y=0;y<GS;y++){for(let x=0;x<GS;x++){const cx=gx+x*cellSize,cy=gy+y*cellSize;const cell=grid[y][x];
if(cell===1){ctx.fillStyle='#94A3B8';ctx.fillRect(cx,cy,cellSize,cellSize);ctx.strokeStyle='#334155';ctx.lineWidth=1;ctx.strokeRect(cx,cy,cellSize,cellSize)}
else{ctx.fillStyle='#0B0F19';ctx.fillRect(cx,cy,cellSize,cellSize);ctx.strokeStyle='#94A3B8';ctx.lineWidth=1;ctx.strokeRect(cx,cy,cellSize,cellSize)}
if(cell===2){ctx.fillStyle='#ef4444';ctx.font=Math.floor(cellSize*0.5)+'px Segoe UI';ctx.textAlign='center';ctx.fillText('💀',cx+cellSize/2,cy+cellSize*0.65)}
if(cell===3){ctx.fillStyle='#fbbf24';ctx.font=Math.floor(cellSize*0.5)+'px Segoe UI';ctx.textAlign='center';ctx.fillText('🔑',cx+cellSize/2,cy+cellSize*0.65)}
if(cell===4){ctx.fillStyle='#a78bfa';ctx.font=Math.floor(cellSize*0.5)+'px Segoe UI';ctx.textAlign='center';ctx.fillText('🚪',cx+cellSize/2,cy+cellSize*0.65)}
if(cell===5){ctx.fillStyle='#34d399';ctx.font=Math.floor(cellSize*0.5)+'px Segoe UI';ctx.textAlign='center';ctx.fillText('🏁',cx+cellSize/2,cy+cellSize*0.65)}
/* Player */
if(x===px&&y===py){ctx.fillStyle='#60a5fa';ctx.beginPath();ctx.arc(cx+cellSize/2,cy+cellSize/2,cellSize*0.35,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold '+Math.floor(cellSize*0.35)+'px Segoe UI';ctx.textAlign='center';ctx.fillText('😊',cx+cellSize/2,cy+cellSize*0.65)}}}
/* Arrow buttons */
const btnSize=55,btnGap=5,btnBaseX=W/2,btnBaseY=gy+gridH+50;
/* Up */
ctx.fillStyle='rgba(71,85,105,0.7)';ctx.fillRect(btnBaseX-btnSize/2,btnBaseY-btnSize-btnGap,btnSize,btnSize);ctx.fillStyle='#e2e8f0';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';ctx.fillText('↑',btnBaseX,btnBaseY-btnSize/2-btnGap+3);
/* Down */
ctx.fillStyle='rgba(71,85,105,0.7)';ctx.fillRect(btnBaseX-btnSize/2,btnBaseY+btnGap,btnSize,btnSize);ctx.fillStyle='#e2e8f0';ctx.fillText('↓',btnBaseX,btnBaseY+btnGap+btnSize/2+3);
/* Left */
ctx.fillStyle='rgba(71,85,105,0.7)';ctx.fillRect(btnBaseX-btnSize*1.5-btnGap,btnBaseY-btnSize/2,btnSize,btnSize);ctx.fillStyle='#e2e8f0';ctx.fillText('←',btnBaseX-btnSize-btnGap,btnBaseY+3);
/* Right */
ctx.fillStyle='rgba(71,85,105,0.7)';ctx.fillRect(btnBaseX+btnSize/2+btnGap,btnBaseY-btnSize/2,btnSize,btnSize);ctx.fillStyle='#e2e8f0';ctx.fillText('→',btnBaseX+btnSize+btnGap,btnBaseY+3);
/* Fail message */
if(failMsg){ctx.fillStyle='#ef4444';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(failMsg,W/2,gy+gridH+15)}
/* Round done */
if(roundDone){ctx.fillStyle='rgba(0,0,0,0.5)';ctx.fillRect(0,0,W,H);ctx.fillStyle='#34d399';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.fillText('Çıkışı Buldun! +10 Puan',W/2,H/2-30);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-70,H/2,140,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Sonraki ▶',W/2,H/2+27)}
if(roundFail){ctx.fillStyle='rgba(0,0,0,0.5)';ctx.fillRect(0,0,W,H);ctx.fillStyle='#ef4444';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.fillText('Hamle Hakkın Bitti!',W/2,H/2-30);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-70,H/2,140,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.fillText('Tekrar Dene',W/2,H/2+27)}}
function update(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(update)}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(my>305&&my<345&&mx>W/2-80&&mx<W/2+80){state='play';round=1;score=0;initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<370){state='start'}return}
if(state==='play'){
/* Round done next */
if(roundDone&&mx>W/2-70&&mx<W/2+70&&my>H/2&&my<H/2+40){round++;if(round>maxR){state='win'}else{initRound()}return}
/* Round fail retry */
if(roundFail&&mx>W/2-70&&mx<W/2+70&&my>H/2&&my<H/2+40){initRound();return}
if(roundDone||roundFail)return;
/* Arrow buttons */
const cellSize=Math.min(50,Math.floor(440/GS));const gridH2=GS*cellSize;const gy2=75;const btnSize=55,btnGap=5,btnBaseX=W/2,btnBaseY=gy2+gridH2+50;
/* Up */
if(mx>btnBaseX-btnSize/2&&mx<btnBaseX+btnSize/2&&my>btnBaseY-btnSize-btnGap&&my<btnBaseY-btnGap){tryMove(0,-1);return}
/* Down */
if(mx>btnBaseX-btnSize/2&&mx<btnBaseX+btnSize/2&&my>btnBaseY+btnGap&&my<btnBaseY+btnGap+btnSize){tryMove(0,1);return}
/* Left */
if(mx>btnBaseX-btnSize*1.5-btnGap&&mx<btnBaseX-btnSize/2-btnGap&&my>btnBaseY-btnSize/2&&my<btnBaseY+btnSize/2){tryMove(-1,0);return}
/* Right */
if(mx>btnBaseX+btnSize/2+btnGap&&mx<btnBaseX+btnSize*1.5+btnGap&&my>btnBaseY-btnSize/2&&my<btnBaseY+btnSize/2){tryMove(1,0);return}
/* Click on adjacent cell to move */
const gx2=W/2-(GS*cellSize)/2;if(mx>gx2&&mx<gx2+GS*cellSize&&my>gy2&&my<gy2+GS*cellSize){const cx=Math.floor((mx-gx2)/cellSize),cy=Math.floor((my-gy2)/cellSize);const ddx=cx-px,ddy=cy-py;if(Math.abs(ddx)+Math.abs(ddy)===1){tryMove(ddx,ddy)}}}});
/* Keyboard support */
document.addEventListener('keydown',e=>{if(state!=='play'||roundDone||roundFail)return;if(e.key==='ArrowUp')tryMove(0,-1);else if(e.key==='ArrowDown')tryMove(0,1);else if(e.key==='ArrowLeft')tryMove(-1,0);else if(e.key==='ArrowRight')tryMove(1,0)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""


def _build_elem_ab_koordinat_html():
    """Hedefi Bul (Koordinat) — Koordinat düzleminde noktayı bul."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c'),ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}
const GRIDMAX=7,CELL=65;
const GRIDX=85,GRIDY=100,GRIDW=GRIDMAX*CELL,GRIDH=GRIDMAX*CELL;
let targetX=0,targetY=0,targetX2=-1,targetY2=-1,midpointMode=false;
let placed=[],feedback='',feedTimer=0,roundDone=false,needPoints=1,hoverCX=-1,hoverCY=-1;
function initRound(){placed=[];feedback='';feedTimer=0;roundDone=false;hoverCX=-1;hoverCY=-1;targetX2=-1;targetY2=-1;midpointMode=false;
targetX=Math.floor(Math.random()*GRIDMAX);targetY=Math.floor(Math.random()*GRIDMAX);
if(round>=7){/* Two-point or midpoint mode */
if(round>=9){midpointMode=true;/* Ask midpoint of two given points */
targetX=Math.floor(Math.random()*(GRIDMAX-1));targetY=Math.floor(Math.random()*(GRIDMAX-1));
targetX2=targetX+2*Math.floor(Math.random()*2);if(targetX2>=GRIDMAX)targetX2=targetX;targetY2=targetY+2*Math.floor(Math.random()*2);if(targetY2>=GRIDMAX)targetY2=targetY;
if(targetX2===targetX&&targetY2===targetY){targetX2=Math.min(targetX+2,GRIDMAX-1)}
needPoints=1}else{/* Two separate points */
targetX2=Math.floor(Math.random()*GRIDMAX);targetY2=Math.floor(Math.random()*GRIDMAX);while(targetX2===targetX&&targetY2===targetY){targetX2=Math.floor(Math.random()*GRIDMAX);targetY2=Math.floor(Math.random()*GRIDMAX)}needPoints=2}}else{needPoints=1}}
function getTask(){if(midpointMode){return 'Orta Noktayı Bul: ('+targetX+','+targetY+') ve ('+targetX2+','+targetY2+')'}
if(targetX2>=0&&!midpointMode){return 'İki Noktayı Bul: ('+targetX+','+targetY+') ve ('+targetX2+','+targetY2+')'}
return 'Noktayı Bul: ('+targetX+', '+targetY+')'}
function checkPlacement(cx,cy){if(roundDone)return;
if(midpointMode){const mx=(targetX+targetX2)/2,my2=(targetY+targetY2)/2;if(cx===mx&&cy===my2){placed.push({x:cx,y:cy,correct:true});roundDone=true;score+=10;feedback='Doğru! Orta nokta: ('+mx+','+my2+')';feedTimer=120;beep(523,0.15);addP(GRIDX+cx*CELL+CELL/2,GRIDY+(GRIDMAX-1-cy)*CELL+CELL/2,'#34d399')}else{feedback='Yanlış konum! Tekrar dene.';feedTimer=60;beep(180,0.3);placed.push({x:cx,y:cy,correct:false})}return}
if(needPoints===2){/* Two points mode */
const isT1=(cx===targetX&&cy===targetY);const isT2=(cx===targetX2&&cy===targetY2);const alreadyT1=placed.some(p=>p.x===targetX&&p.y===targetY&&p.correct);const alreadyT2=placed.some(p=>p.x===targetX2&&p.y===targetY2&&p.correct);
if(isT1&&!alreadyT1){placed.push({x:cx,y:cy,correct:true});beep(523,0.1);addP(GRIDX+cx*CELL+CELL/2,GRIDY+(GRIDMAX-1-cy)*CELL+CELL/2,'#34d399');if(alreadyT2){roundDone=true;score+=10;feedback='İki noktayı da buldun! +10 Puan';feedTimer=120;beep(523,0.15)}else{feedback='Birinci nokta doğru! İkincisini bul.';feedTimer=60}}else if(isT2&&!alreadyT2){placed.push({x:cx,y:cy,correct:true});beep(523,0.1);addP(GRIDX+cx*CELL+CELL/2,GRIDY+(GRIDMAX-1-cy)*CELL+CELL/2,'#34d399');if(alreadyT1){roundDone=true;score+=10;feedback='İki noktayı da buldun! +10 Puan';feedTimer=120;beep(523,0.15)}else{feedback='Bir nokta doğru! Diğerini bul.';feedTimer=60}}else{feedback='Yanlış konum! Tekrar dene.';feedTimer=60;beep(180,0.3);placed.push({x:cx,y:cy,correct:false})}return}
/* Single point */
if(cx===targetX&&cy===targetY){placed.push({x:cx,y:cy,correct:true});roundDone=true;score+=10;feedback='Doğru! +10 Puan';feedTimer=120;beep(523,0.15);addP(GRIDX+cx*CELL+CELL/2,GRIDY+(GRIDMAX-1-cy)*CELL+CELL/2,'#34d399')}else{placed.push({x:cx,y:cy,correct:false});feedback='Yanlış! ('+cx+','+cy+') değil. Tekrar dene.';feedTimer=80;beep(180,0.3)}}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('📍 Hedefi Bul (Koordinat)',W/2,160);ctx.font='20px Segoe UI';ctx.fillStyle='#94a3b8';ctx.fillText('Koordinat düzleminde noktayı bul!',W/2,210);ctx.fillText('X ve Y eksenlerini kullanarak tıkla.',W/2,240);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,305,160,40);ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,332);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('TEBRİKLER!',W/2,200);ctx.fillStyle='#e2e8f0';ctx.font='24px Segoe UI';ctx.fillText('Koordinat Ustası!',W/2,250);ctx.fillText('Puan: '+score+' / '+(maxR*10),W/2,290);ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-80,330,160,40);ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,357);return}
/* HUD */
ctx.fillStyle='#e2e8f0';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';ctx.fillText('Tur: '+round+'/'+maxR,15,30);ctx.textAlign='right';ctx.fillStyle='#fbbf24';ctx.fillText('Puan: '+score,W-15,30);
/* Task */
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText(getTask(),W/2,65);
/* Draw grid */
ctx.strokeStyle='#334155';ctx.lineWidth=1;
for(let i=0;i<=GRIDMAX;i++){/* Vertical */
ctx.beginPath();ctx.moveTo(GRIDX+i*CELL,GRIDY);ctx.lineTo(GRIDX+i*CELL,GRIDY+GRIDH);ctx.stroke();
/* Horizontal */
ctx.beginPath();ctx.moveTo(GRIDX,GRIDY+i*CELL);ctx.lineTo(GRIDX+GRIDW,GRIDY+i*CELL);ctx.stroke()}
/* Axis labels */
ctx.fillStyle='#94a3b8';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
for(let i=0;i<GRIDMAX;i++){/* X labels (bottom) */
ctx.fillText(''+i,GRIDX+i*CELL+CELL/2,GRIDY+GRIDH+25);
/* Y labels (left) */
ctx.textAlign='right';ctx.fillText(''+(GRIDMAX-1-i),GRIDX-12,GRIDY+i*CELL+CELL/2+5);ctx.textAlign='center'}
/* Axis arrows and labels */
ctx.fillStyle='#60a5fa';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('X',GRIDX+GRIDW+20,GRIDY+GRIDH+25);ctx.fillText('Y',GRIDX-12,GRIDY-10);
/* Draw grid cell fills for hover */
if(hoverCX>=0&&hoverCY>=0&&!roundDone){const hx=GRIDX+hoverCX*CELL,hy=GRIDY+(GRIDMAX-1-hoverCY)*CELL;ctx.fillStyle='rgba(124,58,237,0.2)';ctx.fillRect(hx,hy,CELL,CELL);
/* Crosshair lines */
ctx.strokeStyle='rgba(124,58,237,0.3)';ctx.lineWidth=1;ctx.setLineDash([4,4]);ctx.beginPath();ctx.moveTo(hx+CELL/2,GRIDY);ctx.lineTo(hx+CELL/2,GRIDY+GRIDH);ctx.stroke();ctx.beginPath();ctx.moveTo(GRIDX,hy+CELL/2);ctx.lineTo(GRIDX+GRIDW,hy+CELL/2);ctx.stroke();ctx.setLineDash([]);
/* Coordinate tooltip */
ctx.fillStyle='rgba(15,23,42,0.9)';ctx.fillRect(hx+CELL+5,hy-5,70,25);ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';ctx.fillText('('+hoverCX+','+hoverCY+')',hx+CELL+10,hy+13)}
/* Given points for midpoint mode */
if(midpointMode){const ax=GRIDX+targetX*CELL+CELL/2,ay=GRIDY+(GRIDMAX-1-targetY)*CELL+CELL/2;const bx=GRIDX+targetX2*CELL+CELL/2,by=GRIDY+(GRIDMAX-1-targetY2)*CELL+CELL/2;
ctx.fillStyle='#f472b6';ctx.beginPath();ctx.arc(ax,ay,10,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 11px Segoe UI';ctx.textAlign='center';ctx.fillText('A',ax,ay+4);
ctx.fillStyle='#60a5fa';ctx.beginPath();ctx.arc(bx,by,10,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.fillText('B',bx,by+4);
/* Dashed line between */
ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;ctx.setLineDash([6,4]);ctx.beginPath();ctx.moveTo(ax,ay);ctx.lineTo(bx,by);ctx.stroke();ctx.setLineDash([])}
/* Placed markers */
placed.forEach(p=>{const px2=GRIDX+p.x*CELL+CELL/2,py2=GRIDY+(GRIDMAX-1-p.y)*CELL+CELL/2;if(p.correct){ctx.fillStyle='#34d399';ctx.beginPath();ctx.arc(px2,py2,12,0,Math.PI*2);ctx.fill();/* Star */
ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText('★',px2,py2+6)}else{ctx.strokeStyle='#ef4444';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(px2-8,py2-8);ctx.lineTo(px2+8,py2+8);ctx.stroke();ctx.beginPath();ctx.moveTo(px2+8,py2-8);ctx.lineTo(px2-8,py2+8);ctx.stroke()}});
/* Feedback */
if(feedTimer>0){ctx.fillStyle=feedback.includes('Doğru')||feedback.includes('buldun')?'#34d399':'#ef4444';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,GRIDY+GRIDH+55)}
/* Next button */
if(roundDone){ctx.fillStyle='#7c3aed';ctx.fillRect(W/2-70,GRIDY+GRIDH+70,140,40);ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Sonraki ▶',W/2,GRIDY+GRIDH+97)}
/* Info panel on right */
const infoX=GRIDX+GRIDW+25,infoY=GRIDY+20;
ctx.fillStyle='rgba(15,23,42,0.7)';ctx.fillRect(infoX,infoY,170,120);ctx.fillStyle='#94a3b8';ctx.font='14px Segoe UI';ctx.textAlign='left';
ctx.fillText('Koordinat Sistemi:',infoX+10,infoY+20);ctx.fillStyle='#60a5fa';ctx.fillText('X → Sağa doğru',infoX+10,infoY+45);ctx.fillText('Y → Yukarı doğru',infoX+10,infoY+65);ctx.fillStyle='#fbbf24';ctx.fillText('(X, Y) şeklinde oku',infoX+10,infoY+90);
if(round>=7&&!midpointMode){ctx.fillStyle='#f472b6';ctx.fillText('İki nokta bul!',infoX+10,infoY+110)}
if(midpointMode){ctx.fillStyle='#f472b6';ctx.fillText('Orta noktayı bul!',infoX+10,infoY+110)}}
function update(){if(feedTimer>0)feedTimer--;particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.02;p.vy+=.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(update)}
cv.addEventListener('mousemove',e=>{if(state!=='play'||roundDone)return;const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(mx>GRIDX&&mx<GRIDX+GRIDW&&my>GRIDY&&my<GRIDY+GRIDH){const cx=Math.floor((mx-GRIDX)/CELL);const cy=GRIDMAX-1-Math.floor((my-GRIDY)/CELL);hoverCX=cx;hoverCY=cy}else{hoverCX=-1;hoverCY=-1}});
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
if(state==='start'){if(my>305&&my<345&&mx>W/2-80&&mx<W/2+80){state='play';round=1;score=0;initRound()}return}
if(state==='win'){if(mx>W/2-80&&mx<W/2+80&&my>330&&my<370){state='start'}return}
if(state==='play'){
/* Next button */
if(roundDone){const btnY=GRIDY+GRIDH+70;if(mx>W/2-70&&mx<W/2+70&&my>btnY&&my<btnY+40){round++;if(round>maxR){state='win'}else{initRound()}return}}
if(roundDone)return;
/* Grid click */
if(mx>GRIDX&&mx<GRIDX+GRIDW&&my>GRIDY&&my<GRIDY+GRIDH){const cx=Math.floor((mx-GRIDX)/CELL);const cy=GRIDMAX-1-Math.floor((my-GRIDY)/CELL);if(cx>=0&&cx<GRIDMAX&&cy>=0&&cy<GRIDMAX){checkPlacement(cx,cy)}}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
update();
</script></body></html>"""
