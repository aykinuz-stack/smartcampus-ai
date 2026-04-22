# -*- coding: utf-8 -*-
"""İlkokul Genel Yetenek Oyunları — Bölüm C: 11-15 (Görsel Dönüşüm, Kesir Puzzle, Hızlı Matematik, Kategorize Et, Hata Avcısı)."""


def _build_elem_ab_gorsel_donusum_html():
    """Görsel Dönüşüm — Şekli döndür/aynala, doğru versiyonu seç."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

const SHAPES=[
  // Each shape: array of [x,y] relative points forming a polygon, centered around 0,0
  {name:'Ok',pts:[[-20,-30],[0,-50],[20,-30],[10,-30],[10,30],[-10,30],[-10,-30]],color:'#3b82f6'},
  {name:'L',pts:[[-25,-30],[-5,-30],[-5,0],[25,0],[25,20],[-25,20]],color:'#ef4444'},
  {name:'T',pts:[[-30,-25],[30,-25],[30,-5],[10,-5],[10,25],[-10,25],[-10,-5],[-30,-5]],color:'#10b981'},
  {name:'Artı',pts:[[-10,-30],[10,-30],[10,-10],[30,-10],[30,10],[10,10],[10,30],[-10,30],[-10,10],[-30,10],[-30,-10],[-10,-10]],color:'#f59e0b'},
  {name:'Üçgen',pts:[[0,-35],[30,25],[-30,25]],color:'#8b5cf6'},
  {name:'Bayrak',pts:[[-20,-30],[-20,30],[-10,30],[-10,-10],[20,-20],[20,-30]],color:'#ec4899'},
  {name:'Merdiven',pts:[[-25,-25],[-5,-25],[-5,-5],[15,-5],[15,15],[25,15],[25,30],[-25,30]],color:'#06b6d4'},
  {name:'Kare-Çıkıntı',pts:[[-25,-25],[25,-25],[25,0],[15,0],[15,25],[-15,25],[-15,0],[-25,0]],color:'#f97316'},
  {name:'Yıldız',pts:[[0,-35],[8,-12],[33,-10],[14,5],[20,30],[0,16],[-20,30],[-14,5],[-33,-10],[-8,-12]],color:'#eab308'},
  {name:'Ev',pts:[[0,-35],[30,0],[30,30],[-30,30],[-30,0]],color:'#14b8a6'}
];

const TRANSFORMS=[
  {name:'Saat yönünde 90° döndür',fn:(pts)=>pts.map(([x,y])=>[y,-x])},
  {name:'Saat yönünde 180° döndür',fn:(pts)=>pts.map(([x,y])=>[-x,-y])},
  {name:'Yatay aynala',fn:(pts)=>pts.map(([x,y])=>[-x,y])},
  {name:'Dikey aynala',fn:(pts)=>pts.map(([x,y])=>[x,-y])}
];

let curShape,curTransform,options,correctIdx,selected,feedback,feedTimer;

function drawShape(cx,cy,pts,color,scale){
  scale=scale||1;
  ctx.beginPath();
  ctx.moveTo(cx+pts[0][0]*scale,cy+pts[0][1]*scale);
  for(let i=1;i<pts.length;i++) ctx.lineTo(cx+pts[i][0]*scale,cy+pts[i][1]*scale);
  ctx.closePath();
  ctx.fillStyle=color;ctx.fill();
  ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
}

function wrongTransform(pts){
  const t=TRANSFORMS[Math.floor(Math.random()*TRANSFORMS.length)];
  const extra=Math.random()>.5?
    pts.map(([x,y])=>[x+(Math.random()>.5?8:-8),y+(Math.random()>.5?5:-5)]):
    t.fn(pts);
  return extra;
}

function initRound(){
  const si=Math.floor(Math.random()*SHAPES.length);
  curShape=SHAPES[si];
  const ti=Math.floor(Math.random()*TRANSFORMS.length);
  curTransform=TRANSFORMS[ti];
  const correctPts=curTransform.fn(curShape.pts);
  correctIdx=Math.floor(Math.random()*4);
  options=[];
  for(let i=0;i<4;i++){
    if(i===correctIdx){options.push(correctPts)}
    else{
      // generate wrong option: apply a different transform or distort
      let wrong;
      let attempts=0;
      do{
        const wti=(ti+1+Math.floor(Math.random()*3))%TRANSFORMS.length;
        wrong=TRANSFORMS[wti].fn(curShape.pts);
        // sometimes flip additionally
        if(Math.random()>.6) wrong=wrong.map(([x,y])=>[x+(Math.random()>.5?6:-6),y]);
        attempts++;
      }while(attempts<5&&JSON.stringify(wrong)===JSON.stringify(correctPts));
      options.push(wrong);
    }
  }
  selected=-1;feedback='';feedTimer=0;
}

function draw(){
  ctx.clearRect(0,0,W,H);
  const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);

  if(state==='start'){
    ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🔄 Görsel Dönüşüm',W/2,180);
    ctx.font='20px Segoe UI';ctx.fillText('Şekli döndür veya aynala!',W/2,225);
    ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Doğru dönüşümü 4 seçenekten bul.',W/2,260);
    ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,331);
    return;
  }
  if(state==='win'){
    ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';
    ctx.fillText('TEBRİKLER!',W/2,200);
    ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';
    ctx.fillText('Toplam Puan: '+score,W/2,260);
    ctx.font='18px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Harika gözlem yeteneği!',W/2,300);
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
    return;
  }

  // HUD
  ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Tur: '+round+'/'+maxR,15,30);
  ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,30);

  // Instruction
  ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 17px Segoe UI';
  ctx.fillText('İşlem: '+curTransform.name,W/2,60);

  // Reference shape box
  ctx.strokeStyle='#3b82f6';ctx.lineWidth=3;
  ctx.strokeRect(W/2-60,75,120,120);
  ctx.fillStyle='rgba(59,130,246,0.1)';ctx.fillRect(W/2-60,75,120,120);
  ctx.fillStyle='#94a3b8';ctx.font='13px Segoe UI';
  ctx.fillText('Orijinal Şekil',W/2,210);
  drawShape(W/2,135,curShape.pts,curShape.color,1);

  // Options
  const optW=140,optH=130,gap=15;
  const totalW=4*optW+3*gap;
  const startX=(W-totalW)/2;
  const optY=250;

  for(let i=0;i<4;i++){
    const ox=startX+i*(optW+gap);
    let borderClr='#475569';
    if(selected===i){
      borderClr=i===correctIdx?'#10b981':'#ef4444';
    }else if(feedback&&i===correctIdx){
      borderClr='#10b981';
    }
    ctx.strokeStyle=borderClr;ctx.lineWidth=selected===i?4:2;
    ctx.fillStyle='rgba(255,255,255,0.05)';
    ctx.fillRect(ox,optY,optW,optH);
    ctx.strokeRect(ox,optY,optW,optH);
    drawShape(ox+optW/2,optY+optH/2,options[i],curShape.color,0.85);
    // label
    ctx.fillStyle='#94a3b8';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
    ctx.fillText(String.fromCharCode(65+i),ox+optW/2,optY+optH+22);
  }

  // Feedback
  if(feedback){
    ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
    ctx.fillStyle=feedback==='Doğru! +10 puan'?'#10b981':'#ef4444';
    ctx.fillText(feedback,W/2,440);
  }

  // Particles
  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function update(){
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.08});
  particles=particles.filter(p=>p.life>0);
  if(feedTimer>0){feedTimer--;if(feedTimer===0){round++;if(round>maxR){state='win';for(let i=0;i<40;i++)addP(W/2+Math.random()*200-100,H/2+Math.random()*100-50,['#fbbf24','#10b981','#6366f1','#ec4899'][i%4])}else initRound()}}
  draw();requestAnimationFrame(update);
}

canvas.addEventListener('click',e=>{
  const rect=canvas.getBoundingClientRect();
  const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
  if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return;}
  if(state==='win') return;
  if(feedTimer>0) return;
  // Check option clicks
  const optW2=140,optH2=130,gap2=15;
  const totalW2=4*optW2+3*gap2;
  const startX2=(W-totalW2)/2;
  const optY2=250;
  for(let i=0;i<4;i++){
    const ox=startX2+i*(optW2+gap2);
    if(mx>=ox&&mx<=ox+optW2&&my>=optY2&&my<=optY2+optH2){
      selected=i;
      if(i===correctIdx){score+=10;feedback='Doğru! +10 puan';beep(523,0.15);addP(ox+optW2/2,optY2+optH2/2,'#10b981')}
      else{feedback='Yanlış! Doğru: '+String.fromCharCode(65+correctIdx);beep(180,0.3)}
      feedTimer=50;
      break;
    }
  }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_kesir_puzzle_html():
    """Parça Bütün – Kesir Puzzle — Şekli doğru kesir kadar doldur."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

// Fractions available: [numerator, denominator]
const FRACTIONS=[[1,2],[1,3],[2,3],[1,4],[2,4],[3,4]];
let fracNum,fracDen,shapeType,sections,filledPre,playerFilled,targetFill,feedback,feedTimer;

function initRound(){
  const fi=Math.floor(Math.random()*FRACTIONS.length);
  fracNum=FRACTIONS[fi][0];fracDen=FRACTIONS[fi][1];
  shapeType=Math.random()>0.5?'circle':'rect';
  sections=[];
  filledPre=0;playerFilled=[];
  // We need fracDen total sections, fracNum of them must end up filled
  // Pre-fill 0 sections, player must fill fracNum
  // For variety, sometimes pre-fill some and ask to complete
  let preFill=0;
  if(fracNum>1&&Math.random()>0.5){preFill=Math.floor(Math.random()*fracNum);if(preFill>=fracNum)preFill=0}
  filledPre=preFill;
  targetFill=fracNum-preFill;

  if(shapeType==='circle'){
    const cx=W/2,cy=280,r=100;
    const angleStep=Math.PI*2/fracDen;
    for(let i=0;i<fracDen;i++){
      sections.push({idx:i,filled:i<preFill,playerFill:false,startAngle:-Math.PI/2+i*angleStep,endAngle:-Math.PI/2+(i+1)*angleStep,cx,cy,r});
    }
  }else{
    // Rectangle grid
    const cols=fracDen<=4?fracDen:Math.ceil(fracDen/2);
    const rows=fracDen<=4?1:2;
    const cellW=Math.min(80,300/cols);
    const cellH=80;
    const totalW2=cols*cellW;const totalH=rows*cellH;
    const startX2=(W-totalW2)/2;const startY=240;
    let idx2=0;
    for(let r2=0;r2<rows;r2++){
      for(let c=0;c<cols;c++){
        if(idx2>=fracDen)break;
        sections.push({idx:idx2,filled:idx2<preFill,playerFill:false,x:startX2+c*cellW,y:startY+r2*cellH,w:cellW,h:cellH});
        idx2++;
      }
    }
  }
  // Shuffle sections so pre-filled aren't always first
  const indices=[...Array(fracDen).keys()];
  for(let i=indices.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[indices[i],indices[j]]=[indices[j],indices[i]]}
  const preSet=new Set(indices.slice(0,preFill));
  sections.forEach((s,i)=>{s.filled=preSet.has(i);s.playerFill=false});

  playerFilled=[];
  feedback='';feedTimer=0;
}

function getPlayerFilledCount(){return sections.filter(s=>s.playerFill).length}

function draw(){
  ctx.clearRect(0,0,W,H);
  const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);

  if(state==='start'){
    ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🧩 Kesir Puzzle',W/2,180);
    ctx.font='20px Segoe UI';ctx.fillText('Şekli doğru kesir kadar doldur!',W/2,225);
    ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Boş parçalara tıklayarak tamamla.',W/2,260);
    ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,331);
    return;
  }
  if(state==='win'){
    ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';
    ctx.fillText('TEBRİKLER!',W/2,200);
    ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';
    ctx.fillText('Toplam Puan: '+score,W/2,260);
    ctx.font='18px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Kesir ustası oldun!',W/2,300);
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
    return;
  }

  // HUD
  ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Tur: '+round+'/'+maxR,15,30);
  ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,30);

  // Instruction
  ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';
  const instrText=filledPre>0?
    'Bu şeklin '+fracNum+'/'+fracDen+"'"+(['ü','i','u','ı'][fracDen%4]||'ü')+'nü tamamla! ('+targetFill+' parça daha)':
    'Bu şeklin '+fracNum+'/'+fracDen+"'"+(['ü','i','u','ı'][fracDen%4]||'ü')+'nü boya!';
  ctx.fillText(instrText,W/2,70);

  // Counter
  ctx.fillStyle='#94a3b8';ctx.font='16px Segoe UI';
  ctx.fillText('Boyanan: '+(filledPre+getPlayerFilledCount())+'/'+fracNum+'  (Toplam: '+fracDen+' parça)',W/2,100);

  // Draw shape
  if(shapeType==='circle'){
    const s0=sections[0];
    // Draw each section
    sections.forEach(s=>{
      ctx.beginPath();
      ctx.moveTo(s.cx,s.cy);
      ctx.arc(s.cx,s.cy,s.r,s.startAngle,s.endAngle);
      ctx.closePath();
      if(s.filled){ctx.fillStyle='#3b82f6';ctx.fill()}
      else if(s.playerFill){ctx.fillStyle='#10b981';ctx.fill()}
      else{ctx.fillStyle='rgba(203,213,225,0.15)';ctx.fill()}
      ctx.strokeStyle='#e2e8f0';ctx.lineWidth=2;ctx.stroke();
    });
    // outer ring
    ctx.beginPath();ctx.arc(s0.cx,s0.cy,s0.r,0,Math.PI*2);
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=3;ctx.stroke();
  }else{
    sections.forEach(s=>{
      if(s.filled){ctx.fillStyle='#3b82f6'}
      else if(s.playerFill){ctx.fillStyle='#10b981'}
      else{ctx.fillStyle='rgba(203,213,225,0.15)'}
      ctx.fillRect(s.x,s.y,s.w,s.h);
      ctx.strokeStyle='#e2e8f0';ctx.lineWidth=2;ctx.strokeRect(s.x,s.y,s.w,s.h);
    });
  }

  // Legend
  const ly=shapeType==='circle'?430:400;
  ctx.fillStyle='#3b82f6';ctx.fillRect(W/2-150,ly,20,20);
  ctx.fillStyle='#94a3b8';ctx.font='14px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Önceden dolu',W/2-120,ly+15);
  ctx.fillStyle='#10b981';ctx.fillRect(W/2+20,ly,20,20);
  ctx.fillStyle='#94a3b8';ctx.fillText('Senin boyadığın',W/2+50,ly+15);

  // Feedback
  if(feedback){
    ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
    ctx.fillStyle=feedback.includes('Doğru')?'#10b981':'#ef4444';
    ctx.fillText(feedback,W/2,ly+65);
  }

  // Fraction visual
  ctx.fillStyle='#e0e7ff';ctx.font='bold 50px Segoe UI';ctx.textAlign='center';
  const fracX=W/2,fracY=550;
  ctx.fillText(fracNum,fracX,fracY-10);
  ctx.fillRect(fracX-30,fracY,60,3);
  ctx.fillText(fracDen,fracX,fracY+45);

  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function checkComplete(){
  const total=filledPre+getPlayerFilledCount();
  if(total===fracNum){
    score+=10;feedback='Doğru! +10 puan';beep(523,0.15);
    addP(W/2,280,'#10b981');
    feedTimer=50;
  }else if(total>fracNum){
    // Too many filled - undo last
    const last=sections.filter(s=>s.playerFill);
    if(last.length>0){last[last.length-1].playerFill=false}
    feedback='Çok fazla! Bir parça fazla boyadın.';beep(180,0.3);
    feedTimer=30;
  }
}

function update(){
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.08});
  particles=particles.filter(p=>p.life>0);
  if(feedTimer>0){feedTimer--;if(feedTimer===0&&feedback.includes('Doğru')){round++;if(round>maxR){state='win';for(let i=0;i<40;i++)addP(W/2+Math.random()*200-100,H/2+Math.random()*100-50,['#fbbf24','#10b981','#6366f1'][i%3])}else initRound()}}
  draw();requestAnimationFrame(update);
}

canvas.addEventListener('click',e=>{
  const rect=canvas.getBoundingClientRect();
  const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
  if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return;}
  if(state==='win') return;
  if(feedTimer>0) return;
  // Click on sections
  if(shapeType==='circle'){
    sections.forEach(s=>{
      if(s.filled) return;
      // Check if click is in the pie sector
      const dx=mx-s.cx,dy=my-s.cy;
      const dist=Math.sqrt(dx*dx+dy*dy);
      if(dist>s.r) return;
      let angle=Math.atan2(dy,dx);
      // Normalize angles
      let sa=s.startAngle,ea=s.endAngle;
      while(angle<sa) angle+=Math.PI*2;
      while(angle>sa+Math.PI*2) angle-=Math.PI*2;
      if(angle>=sa&&angle<=ea){
        s.playerFill=!s.playerFill;
        checkComplete();
      }
    });
  }else{
    sections.forEach(s=>{
      if(s.filled) return;
      if(mx>=s.x&&mx<=s.x+s.w&&my>=s.y&&my<=s.y+s.h){
        s.playerFill=!s.playerFill;
        checkComplete();
      }
    });
  }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_hizli_mat_html():
    """Hızlı Matematik Reaksiyon — Zamana karşı matematik soruları çöz."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

let question,answer,opts,timerStart,timeLeft,maxTime=4,streak=0,bestStreak=0;
let feedback,feedTimer,answered,earnedPts;

function genQuestion(){
  let a,b,op,ans;
  const r=Math.random();
  if(r<0.3){
    a=1+Math.floor(Math.random()*50);b=1+Math.floor(Math.random()*50);
    op='+';ans=a+b;
  }else if(r<0.55){
    a=10+Math.floor(Math.random()*50);b=1+Math.floor(Math.random()*a);
    op='-';ans=a-b;
  }else if(r<0.85){
    a=2+Math.floor(Math.random()*11);b=2+Math.floor(Math.random()*11);
    op='×';ans=a*b;
  }else{
    b=2+Math.floor(Math.random()*10);ans=1+Math.floor(Math.random()*11);
    a=b*ans;op='÷';
  }
  question=a+' '+op+' '+b+' = ?';
  answer=ans;
  opts=[ans];
  while(opts.length<4){
    let wrong=ans+Math.floor(Math.random()*21)-10;
    if(wrong<0) wrong=Math.abs(wrong)+1;
    if(!opts.includes(wrong)&&wrong!==ans) opts.push(wrong);
  }
  // Shuffle
  for(let i=opts.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[opts[i],opts[j]]=[opts[j],opts[i]]}
  timerStart=Date.now();timeLeft=maxTime;answered=false;feedback='';feedTimer=0;earnedPts=0;
}

function draw(){
  ctx.clearRect(0,0,W,H);
  const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);

  if(state==='start'){
    ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
    ctx.fillText('⚡ Hızlı Matematik',W/2,170);
    ctx.font='20px Segoe UI';ctx.fillText('Zamana karşı matematik yarışı!',W/2,215);
    ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Her soru için 4 saniye! Hızlı cevap = bonus puan!',W/2,250);
    ctx.fillText('<1sn: +15  |  <2sn: +12  |  <3sn: +10',W/2,275);
    ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,331);
    return;
  }
  if(state==='win'){
    ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';
    ctx.fillText('TEBRİKLER!',W/2,180);
    ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';
    ctx.fillText('Toplam Puan: '+score,W/2,240);
    ctx.font='20px Segoe UI';ctx.fillStyle='#f59e0b';
    ctx.fillText('En iyi seri: '+bestStreak+' 🔥',W/2,280);
    ctx.font='18px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Matematik reflekslerin süper!',W/2,320);
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
    return;
  }

  // HUD
  ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Tur: '+round+'/'+maxR,15,30);
  ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,30);
  // Streak
  if(streak>0){
    ctx.textAlign='center';ctx.fillStyle='#f59e0b';ctx.font='bold 16px Segoe UI';
    ctx.fillText('🔥 Seri: '+streak,W/2,30);
  }

  // Timer bar
  if(!answered){
    const elapsed=(Date.now()-timerStart)/1000;
    timeLeft=Math.max(0,maxTime-elapsed);
    const ratio=timeLeft/maxTime;
    // Bar bg
    ctx.fillStyle='#94A3B8';ctx.fillRect(50,55,W-100,18);
    // Bar fill
    let barClr='#10b981';
    if(ratio<0.5) barClr='#f59e0b';
    if(ratio<0.25) barClr='#ef4444';
    const barGrd=ctx.createLinearGradient(50,0,50+(W-100)*ratio,0);
    barGrd.addColorStop(0,barClr);barGrd.addColorStop(1,barClr+'99');
    ctx.fillStyle=barGrd;ctx.fillRect(50,55,(W-100)*ratio,18);
    ctx.strokeStyle='#475569';ctx.lineWidth=1;ctx.strokeRect(50,55,W-100,18);
    // Timer text
    ctx.fillStyle='#e0e7ff';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';
    ctx.fillText(timeLeft.toFixed(1)+'s',W/2,69);
    // Auto-timeout
    if(timeLeft<=0){
      answered=true;feedback='Süre doldu! Doğru: '+answer;beep(180,0.3);
      streak=0;feedTimer=60;
    }
  }else{
    ctx.fillStyle='#94A3B8';ctx.fillRect(50,55,W-100,18);
  }

  // Question
  ctx.fillStyle='#0B0F19';
  ctx.beginPath();
  const qx=W/2-160,qy=95,qw=320,qh=80;
  ctx.moveTo(qx+15,qy);ctx.lineTo(qx+qw-15,qy);ctx.quadraticCurveTo(qx+qw,qy,qx+qw,qy+15);
  ctx.lineTo(qx+qw,qy+qh-15);ctx.quadraticCurveTo(qx+qw,qy+qh,qx+qw-15,qy+qh);
  ctx.lineTo(qx+15,qy+qh);ctx.quadraticCurveTo(qx,qy+qh,qx,qy+qh-15);
  ctx.lineTo(qx,qy+15);ctx.quadraticCurveTo(qx,qy,qx+15,qy);ctx.fill();
  ctx.strokeStyle='#6366f1';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='#fbbf24';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
  ctx.fillText(question,W/2,148);

  // Options (2x2 grid)
  const btnW=260,btnH=70,gapX=30,gapY=20;
  const gridStartX=(W-2*btnW-gapX)/2;
  const gridStartY=210;
  const optColors=['#6366f1','#ec4899','#f59e0b','#10b981'];

  for(let i=0;i<4;i++){
    const col=i%2,row=Math.floor(i/2);
    const bx=gridStartX+col*(btnW+gapX);
    const by=gridStartY+row*(btnH+gapY);
    let bgClr=optColors[i];
    if(answered){
      if(opts[i]===answer) bgClr='#10b981';
      else bgClr='#94A3B8';
    }
    ctx.fillStyle=bgClr;
    ctx.beginPath();
    ctx.moveTo(bx+12,by);ctx.lineTo(bx+btnW-12,by);ctx.quadraticCurveTo(bx+btnW,by,bx+btnW,by+12);
    ctx.lineTo(bx+btnW,by+btnH-12);ctx.quadraticCurveTo(bx+btnW,by+btnH,bx+btnW-12,by+btnH);
    ctx.lineTo(bx+12,by+btnH);ctx.quadraticCurveTo(bx,by+btnH,bx,by+btnH-12);
    ctx.lineTo(bx,by+12);ctx.quadraticCurveTo(bx,by,bx+12,by);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';
    ctx.fillText(opts[i],bx+btnW/2,by+btnH/2+10);
  }

  // Feedback
  if(feedback){
    ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
    ctx.fillStyle=feedback.includes('+')?'#10b981':'#ef4444';
    ctx.fillText(feedback,W/2,430);
    if(earnedPts>0){
      ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';
      ctx.fillText('+'+earnedPts+' puan!',W/2,460);
    }
  }

  // Bonus info
  ctx.fillStyle='#475569';ctx.font='14px Segoe UI';ctx.textAlign='center';
  ctx.fillText('Hız Bonusu:  <1s → +15  |  <2s → +12  |  <3s → +10  |  <4s → +8',W/2,500);

  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function update(){
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.08});
  particles=particles.filter(p=>p.life>0);
  if(feedTimer>0){feedTimer--;if(feedTimer===0){round++;if(round>maxR){state='win';if(streak>bestStreak)bestStreak=streak;for(let i=0;i<40;i++)addP(W/2+Math.random()*200-100,H/2+Math.random()*100-50,['#fbbf24','#10b981','#6366f1','#ec4899'][i%4])}else genQuestion()}}
  draw();requestAnimationFrame(update);
}

canvas.addEventListener('click',e=>{
  const rect=canvas.getBoundingClientRect();
  const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
  if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';streak=0;bestStreak=0;genQuestion()}return;}
  if(state==='win') return;
  if(answered) return;
  // Check option clicks
  const btnW2=260,btnH2=70,gapX2=30,gapY2=20;
  const gridStartX2=(W-2*btnW2-gapX2)/2;
  const gridStartY2=210;
  for(let i=0;i<4;i++){
    const col=i%2,row=Math.floor(i/2);
    const bx=gridStartX2+col*(btnW2+gapX2);
    const by=gridStartY2+row*(btnH2+gapY2);
    if(mx>=bx&&mx<=bx+btnW2&&my>=by&&my<=by+btnH2){
      answered=true;
      const elapsed=(Date.now()-timerStart)/1000;
      if(opts[i]===answer){
        if(elapsed<1){earnedPts=15}else if(elapsed<2){earnedPts=12}else if(elapsed<3){earnedPts=10}else{earnedPts=8}
        score+=earnedPts;streak++;
        if(streak>bestStreak) bestStreak=streak;
        feedback='Doğru! ('+elapsed.toFixed(1)+'s)';
        beep(523,0.15);addP(bx+btnW2/2,by+btnH2/2,'#10b981');
      }else{
        earnedPts=0;streak=0;
        feedback='Yanlış! Doğru: '+answer;
        beep(180,0.3);
      }
      feedTimer=50;
      break;
    }
  }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_kategorize_html():
    """Kategorize Et — Öğeleri doğru kategorilere yerleştir."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

const CATEGORY_SETS=[
  {cats:['Meyve','Sebze'],items:[
    {text:'🍎 Elma',cat:'Meyve'},{text:'🥕 Havuç',cat:'Sebze'},{text:'🍌 Muz',cat:'Meyve'},
    {text:'🥒 Salatalık',cat:'Sebze'},{text:'🍊 Portakal',cat:'Meyve'},{text:'🍅 Domates',cat:'Sebze'},
    {text:'🍇 Üzüm',cat:'Meyve'},{text:'🥦 Brokoli',cat:'Sebze'}
  ]},
  {cats:['Kara Hayvanı','Deniz Hayvanı'],items:[
    {text:'🐱 Kedi',cat:'Kara Hayvanı'},{text:'🐟 Balık',cat:'Deniz Hayvanı'},{text:'🐶 Köpek',cat:'Kara Hayvanı'},
    {text:'🐙 Ahtapot',cat:'Deniz Hayvanı'},{text:'🐴 At',cat:'Kara Hayvanı'},{text:'🐬 Yunus',cat:'Deniz Hayvanı'},
    {text:'🐘 Fil',cat:'Kara Hayvanı'},{text:'🦈 Köpekbalığı',cat:'Deniz Hayvanı'}
  ]},
  {cats:['Canlı','Cansız'],items:[
    {text:'🌳 Ağaç',cat:'Canlı'},{text:'🪨 Taş',cat:'Cansız'},{text:'🐦 Kuş',cat:'Canlı'},
    {text:'💎 Elmas',cat:'Cansız'},{text:'🌺 Çiçek',cat:'Canlı'},{text:'🔑 Anahtar',cat:'Cansız'},
    {text:'🐛 Tırtıl',cat:'Canlı'},{text:'📚 Kitap',cat:'Cansız'}
  ]},
  {cats:['Sıcak','Soğuk'],items:[
    {text:'☀️ Güneş',cat:'Sıcak'},{text:'❄️ Kar',cat:'Soğuk'},{text:'🔥 Ateş',cat:'Sıcak'},
    {text:'🧊 Buz',cat:'Soğuk'},{text:'🌋 Yanardağ',cat:'Sıcak'},{text:'🐧 Penguen',cat:'Soğuk'},
    {text:'🏜️ Çöl',cat:'Sıcak'},{text:'🏔️ Dağ',cat:'Soğuk'}
  ]},
  {cats:['Ulaşım','Yiyecek','Hayvan'],items:[
    {text:'🚗 Araba',cat:'Ulaşım'},{text:'🍕 Pizza',cat:'Yiyecek'},{text:'🐱 Kedi',cat:'Hayvan'},
    {text:'✈️ Uçak',cat:'Ulaşım'},{text:'🍔 Hamburger',cat:'Yiyecek'},{text:'🐶 Köpek',cat:'Hayvan'},
    {text:'🚲 Bisiklet',cat:'Ulaşım'},{text:'🍦 Dondurma',cat:'Yiyecek'}
  ]},
  {cats:['Okul','Ev','Park'],items:[
    {text:'📚 Kitap',cat:'Okul'},{text:'🛋️ Kanepe',cat:'Ev'},{text:'🎡 Dönme Dolap',cat:'Park'},
    {text:'✏️ Kalem',cat:'Okul'},{text:'🛏️ Yatak',cat:'Ev'},{text:'🌳 Ağaç',cat:'Park'},
    {text:'📐 Cetvel',cat:'Okul'},{text:'🍳 Tava',cat:'Ev'}
  ]},
  {cats:['Gökyüzü','Yer'],items:[
    {text:'⭐ Yıldız',cat:'Gökyüzü'},{text:'🌊 Deniz',cat:'Yer'},{text:'🌙 Ay',cat:'Gökyüzü'},
    {text:'🏔️ Dağ',cat:'Yer'},{text:'☁️ Bulut',cat:'Gökyüzü'},{text:'🌻 Çiçek',cat:'Yer'},
    {text:'🌈 Gökkuşağı',cat:'Gökyüzü'},{text:'🏠 Ev',cat:'Yer'}
  ]},
  {cats:['Müzik','Spor'],items:[
    {text:'🎸 Gitar',cat:'Müzik'},{text:'⚽ Futbol',cat:'Spor'},{text:'🎹 Piyano',cat:'Müzik'},
    {text:'🏀 Basketbol',cat:'Spor'},{text:'🥁 Davul',cat:'Müzik'},{text:'🎾 Tenis',cat:'Spor'},
    {text:'🎵 Nota',cat:'Müzik'},{text:'🏊 Yüzme',cat:'Spor'}
  ]},
  {cats:['Büyük','Küçük'],items:[
    {text:'🐘 Fil',cat:'Büyük'},{text:'🐜 Karınca',cat:'Küçük'},{text:'🐋 Balina',cat:'Büyük'},
    {text:'🐁 Fare',cat:'Küçük'},{text:'🦒 Zürafa',cat:'Büyük'},{text:'🐝 Arı',cat:'Küçük'},
    {text:'🏔️ Dağ',cat:'Büyük'},{text:'🍒 Kiraz',cat:'Küçük'}
  ]},
  {cats:['Yazılı','Sözlü'],items:[
    {text:'📖 Kitap',cat:'Yazılı'},{text:'🗣️ Konuşma',cat:'Sözlü'},{text:'📰 Gazete',cat:'Yazılı'},
    {text:'🎤 Şarkı',cat:'Sözlü'},{text:'✉️ Mektup',cat:'Yazılı'},{text:'📞 Telefon',cat:'Sözlü'},
    {text:'📝 Not',cat:'Yazılı'},{text:'🎭 Tiyatro',cat:'Sözlü'}
  ]}
];

let categories,items,selectedItem,placed,animItem,animTimer,feedback,feedTimer;
const catColors=['#6366f1','#ec4899','#f59e0b'];

function initRound(){
  const si=(round-1)%CATEGORY_SETS.length;
  const set=CATEGORY_SETS[si];
  categories=set.cats;
  // Shuffle items
  const arr=[...set.items];
  for(let i=arr.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}
  items=arr.map((it,i)=>({...it,placed:false,idx:i}));
  selectedItem=-1;placed=0;animItem=null;animTimer=0;feedback='';feedTimer=0;
}

function getItemPos(idx){
  const cols=4,rw=Math.floor(idx/cols),cl=idx%cols;
  const iw=150,ih=45,gap=10;
  const totalW2=cols*(iw+gap)-gap;
  const sx=(W-totalW2)/2;
  return{x:sx+cl*(iw+gap),y:80+rw*(ih+gap),w:iw,h:ih};
}

function getCatBox(ci){
  const catCount=categories.length;
  const bw=Math.min(200,Math.floor((W-40)/catCount)-10);
  const totalW2=catCount*(bw+10)-10;
  const sx=(W-totalW2)/2;
  return{x:sx+ci*(bw+10),y:420,w:bw,h:180};
}

function draw(){
  ctx.clearRect(0,0,W,H);
  const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);

  if(state==='start'){
    ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
    ctx.fillText('📦 Kategorize Et',W/2,180);
    ctx.font='20px Segoe UI';ctx.fillText('Öğeleri doğru kutulara yerleştir!',W/2,225);
    ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Önce öğeye, sonra kategoriye tıkla.',W/2,260);
    ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,331);
    return;
  }
  if(state==='win'){
    ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';
    ctx.fillText('TEBRİKLER!',W/2,200);
    ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';
    ctx.fillText('Toplam Puan: '+score,W/2,260);
    ctx.font='18px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Sınıflandırma uzmanısın!',W/2,300);
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
    return;
  }

  // HUD
  ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Tur: '+round+'/'+maxR,15,30);
  ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,30);
  ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='16px Segoe UI';
  ctx.fillText('Yerleştirilen: '+placed+'/'+items.length,W/2,30);

  // Instruction
  ctx.fillStyle='#94a3b8';ctx.font='16px Segoe UI';ctx.textAlign='center';
  ctx.fillText(selectedItem>=0?'Şimdi bir kategori kutusuna tıkla!':'Bir öğe seç, sonra kategoriye yerleştir.',W/2,55);

  // Items
  items.forEach((it,i)=>{
    if(it.placed) return;
    const p=getItemPos(i);
    const isSelected=(selectedItem===i);
    ctx.fillStyle=isSelected?'#4c1d95':'#94A3B8';
    ctx.strokeStyle=isSelected?'#fbbf24':'#475569';
    ctx.lineWidth=isSelected?3:1;
    ctx.beginPath();
    ctx.moveTo(p.x+8,p.y);ctx.lineTo(p.x+p.w-8,p.y);ctx.quadraticCurveTo(p.x+p.w,p.y,p.x+p.w,p.y+8);
    ctx.lineTo(p.x+p.w,p.y+p.h-8);ctx.quadraticCurveTo(p.x+p.w,p.y+p.h,p.x+p.w-8,p.y+p.h);
    ctx.lineTo(p.x+8,p.y+p.h);ctx.quadraticCurveTo(p.x,p.y+p.h,p.x,p.y+p.h-8);
    ctx.lineTo(p.x,p.y+8);ctx.quadraticCurveTo(p.x,p.y,p.x+8,p.y);ctx.fill();ctx.stroke();
    ctx.fillStyle='#e0e7ff';ctx.font='15px Segoe UI';ctx.textAlign='center';
    ctx.fillText(it.text,p.x+p.w/2,p.y+p.h/2+5);
  });

  // Divider line
  ctx.strokeStyle='#475569';ctx.lineWidth=1;ctx.setLineDash([5,5]);
  ctx.beginPath();ctx.moveTo(30,400);ctx.lineTo(W-30,400);ctx.stroke();
  ctx.setLineDash([]);

  // Category boxes
  categories.forEach((cat,ci)=>{
    const b=getCatBox(ci);
    const clr=catColors[ci%catColors.length];
    ctx.fillStyle=clr+'20';
    ctx.strokeStyle=clr;ctx.lineWidth=2;
    ctx.fillRect(b.x,b.y,b.w,b.h);ctx.strokeRect(b.x,b.y,b.w,b.h);
    // Label
    ctx.fillStyle=clr;ctx.font='bold 17px Segoe UI';ctx.textAlign='center';
    ctx.fillText(cat,b.x+b.w/2,b.y+25);
    // Show placed items inside
    let yy=b.y+45;
    items.forEach(it=>{
      if(it.placed&&it.placedCat===cat){
        ctx.fillStyle='#e0e7ff';ctx.font='13px Segoe UI';
        ctx.fillText(it.text,b.x+b.w/2,yy);
        yy+=18;
      }
    });
  });

  // Feedback
  if(feedback){
    ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
    ctx.fillStyle=feedback.includes('Doğru')?'#10b981':'#ef4444';
    ctx.fillText(feedback,W/2,390);
  }

  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function update(){
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.08});
  particles=particles.filter(p=>p.life>0);
  if(feedTimer>0){feedTimer--;if(feedTimer===0){feedback='';
    if(placed>=items.length){round++;if(round>maxR){state='win';for(let i=0;i<40;i++)addP(W/2+Math.random()*200-100,H/2+Math.random()*100-50,['#fbbf24','#10b981','#6366f1'][i%3])}else initRound()}
  }}
  draw();requestAnimationFrame(update);
}

canvas.addEventListener('click',e=>{
  const rect=canvas.getBoundingClientRect();
  const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
  if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return;}
  if(state==='win') return;
  if(feedTimer>0) return;

  // Check item click
  let clickedItem=false;
  items.forEach((it,i)=>{
    if(it.placed) return;
    const p=getItemPos(i);
    if(mx>=p.x&&mx<=p.x+p.w&&my>=p.y&&my<=p.y+p.h){
      selectedItem=i;clickedItem=true;
    }
  });
  if(clickedItem) return;

  // Check category click
  if(selectedItem<0) return;
  categories.forEach((cat,ci)=>{
    const b=getCatBox(ci);
    if(mx>=b.x&&mx<=b.x+b.w&&my>=b.y&&my<=b.y+b.h){
      const it=items[selectedItem];
      if(it.cat===cat){
        it.placed=true;it.placedCat=cat;placed++;
        score+=10;feedback='Doğru! ✓';beep(523,0.15);
        addP(b.x+b.w/2,b.y+b.h/2,'#10b981');
        feedTimer=20;
      }else{
        feedback='Yanlış! '+it.text+' → '+it.cat;beep(180,0.3);
        feedTimer=35;
      }
      selectedItem=-1;
    }
  });
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""


def _build_elem_ab_hata_avcisi_html():
    """Hata Avcısı — Metindeki hataları bul ve işaretle."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c" width="700" height="650"></canvas>
<script>
const W=700,H=650,canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

const TEXTS=[
  {
    correct:'Bugün hava çok güzel. Parkta arkadaşlarımla oyun oynadık. Sonra eve geldik ve ödevlerimizi yaptık. Anneannem bize kurabiye yaptı.',
    broken: 'Bugün hava çok güzle. parkta arkadaşlarımla oyun oynadık. Sonra eve geldik  ve ödevlerimizi yaptık. Anneannem bize kurabiy yaptı.',
    errors:[{pos:19,len:5,wrong:'güzle',right:'güzel',type:'harf'},{pos:26,len:1,wrong:'p',right:'P',type:'büyük harf'},{pos:82,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:110,len:7,wrong:'kurabiy',right:'kurabiye',type:'eksik harf'},{pos:106,len:4,wrong:'bize',hint:'nokta eksik — cümle sonu'}]
  },
  {
    correct:'Okulumuzun bahçesi çok büyük. Her gün teneffüste koşuyoruz. Öğretmenimiz bize yeni bir şarkı öğretti. Çok eğlenceli bir gündü.',
    broken: 'Okulumuzun bahçesi çok büyük. Her gün tenefüste koşuyoruz. öğretmenimiz bize yeni bir şarkı ögretti. Çok eğlenceli  bir gündü.',
    errors:[{pos:40,len:8,wrong:'tenefüst',right:'teneffüs',type:'harf'},{pos:60,len:1,wrong:'ö',right:'Ö',type:'büyük harf'},{pos:93,len:7,wrong:'ögretti',right:'öğretti',type:'harf'},{pos:110,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:121,len:5,wrong:'gündü',right:'gündü.',type:'nokta eksik'}]
  },
  {
    correct:'Kedimizin adı Pamuk. Beyaz ve çok tatlı. Her sabah süt içer. Akşamları kucağımda uyur. Onu çok seviyorum.',
    broken: 'Kedimizin adı pamuk. Beyaz ve çok tatli. Her sabah süt içer. akşamları kucağımda uyur. Onu  çok seviyorum.',
    errors:[{pos:14,len:5,wrong:'pamuk',right:'Pamuk',type:'büyük harf'},{pos:35,len:5,wrong:'tatli',right:'tatlı',type:'harf'},{pos:61,len:1,wrong:'a',right:'A',type:'büyük harf'},{pos:90,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:60,len:5,wrong:'içer.',hint:'virgül eksik'}]
  },
  {
    correct:'Yazın denize gittik. Kumda kale yaptık. Dalgalarla oynadık. Babam bana yüzme öğretti. Çok güzel bir tatildi.',
    broken: 'Yazın denize gittik. Kumda kale yaptik. Dalgalarla oynadık. babam bana yüzme öğretti. Çok güzel  bir tatildi.',
    errors:[{pos:35,len:6,wrong:'yaptik',right:'yaptık',type:'harf'},{pos:60,len:1,wrong:'b',right:'B',type:'büyük harf'},{pos:94,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:26,len:4,wrong:'kale',hint:'nokta eksik'},{pos:103,len:7,wrong:'tatildi',right:'tatildi.',type:'nokta eksik'}]
  },
  {
    correct:'Müzik dersini çok seviyorum. Flüt çalmayı öğreniyoruz. Öğretmenimiz çok sabırlı. Her hafta yeni notalar çalışıyoruz.',
    broken: 'Müzik dersini çok seviyorum. Flüt çalmayı öğreniyoruz. öğretmenimiz çok sabirli. Her hafta yeni  notalar çalışıyoruz.',
    errors:[{pos:55,len:1,wrong:'ö',right:'Ö',type:'büyük harf'},{pos:73,len:7,wrong:'sabirli',right:'sabırlı',type:'harf'},{pos:95,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:0,len:5,wrong:'Müzik',hint:'eksik noktalama'},{pos:110,len:12,wrong:'çalışıyoruz.',right:'çalışıyoruz.',type:'doğru'}]
  },
  {
    correct:'Kütüphanede sessiz olmak lazım. Kitap okumak çok güzel. Ben hayvan hikâyeleri seviyorum. Kedi ve köpek kitapları en sevdiklerim.',
    broken: 'Kütüphanede sesiz olmak lazım. Kitap okumak çok güzel. ben hayvan hikâyeleri seviyorum. Kedi ve köpek kitaplari en sevdiklerim.',
    errors:[{pos:14,len:5,wrong:'sesiz',right:'sessiz',type:'harf'},{pos:55,len:1,wrong:'b',right:'B',type:'büyük harf'},{pos:99,len:9,wrong:'kitaplari',right:'kitapları',type:'harf'},{pos:31,len:5,wrong:'lazım',hint:'nokta eksik'},{pos:52,len:5,wrong:'güzel',hint:'virgül eksik'}]
  },
  {
    correct:'Resim yapmayı çok seviyorum. En çok mavi rengi kullanıyorum. Deniz ve gökyüzü resmi yaptım. Öğretmenim beğendi.',
    broken: 'Resim yapmayı çok seviyorum. En çok mavi rengi kullaniyorum. deniz ve gökyüzü resmi yaptım. Öğretmenim  beğendi.',
    errors:[{pos:47,len:12,wrong:'kullaniyorum',right:'kullanıyorum',type:'harf'},{pos:61,len:1,wrong:'d',right:'D',type:'büyük harf'},{pos:100,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:90,len:6,wrong:'yaptım',hint:'nokta eksik'},{pos:38,len:5,wrong:'rengi',hint:'eksik virgül'}]
  },
  {
    correct:'Matematik dersinde toplama öğrendik. İki sayıyı topluyoruz. Çıkarma da kolay. Öğretmenimiz çok iyi anlatıyor.',
    broken: 'Matematik dersinde toplama öğrendik. iki sayıyı topluyoruz. Çıkarma da koaly. öğretmenimiz çok iyi  anlatıyor.',
    errors:[{pos:37,len:1,wrong:'i',right:'İ',type:'büyük harf'},{pos:72,len:5,wrong:'koaly',right:'kolay',type:'harf'},{pos:79,len:1,wrong:'ö',right:'Ö',type:'büyük harf'},{pos:99,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:104,len:10,wrong:'anlatıyor.',right:'anlatıyor.',type:'doğru'}]
  },
  {
    correct:'Bahçemizde bir elma ağacı var. Sonbaharda elmalar kızarır. Onları toplarız. Annem elma kompostosu yapar.',
    broken: 'Bahçemizde bir elma agacı var. Sonbaharda elmalar kızarır. onları toplarız. Annem elma  kompostosu yapar.',
    errors:[{pos:20,len:5,wrong:'agacı',right:'ağacı',type:'harf'},{pos:59,len:1,wrong:'o',right:'O',type:'büyük harf'},{pos:85,len:2,wrong:'  ',right:' ',type:'fazla boşluk'},{pos:30,len:10,wrong:'Sonbaharda',hint:'virgül eksik'},{pos:98,len:5,wrong:'yapar',right:'yapar.',type:'nokta eksik'}]
  },
  {
    correct:'Spor yapmak sağlığa iyi gelir. Her gün koşuyorum. Futbol da oynuyorum. Takımımız çok güçlü.',
    broken: 'Spor yapmak sağlığa iyi gelir. Her gün koşuyorun. futbol da oynuyorum. Takımımız çok güclü.',
    errors:[{pos:42,len:9,wrong:'koşuyorun',right:'koşuyorum',type:'harf'},{pos:52,len:1,wrong:'f',right:'F',type:'büyük harf'},{pos:84,len:5,wrong:'güclü',right:'güçlü',type:'harf'},{pos:50,len:1,wrong:'.',hint:'virgül olmalı'},{pos:88,len:1,wrong:'.',hint:'nokta eksik'}]
  }
];

let curText,words,foundErrors,totalErrors,timer,maxTimer=30,timerStart,feedback,feedTimer;

function splitToWords(text){
  // Split text keeping spaces as separate tokens for double-space detection
  const result=[];
  let current='',x=0,lineY=0;
  const lineH=32,startX=60,maxW=W-120;
  let cx=startX,cy=175;

  // Tokenize: each word and each space separately
  const tokens=[];
  let t='';
  for(let i=0;i<text.length;i++){
    if(text[i]===' '){
      if(t.length>0){tokens.push({text:t,isSpace:false});t=''}
      tokens.push({text:' ',isSpace:true});
    }else{t+=text[i]}
  }
  if(t.length>0) tokens.push({text:t,isSpace:false});

  // Measure and layout
  ctx.font='18px Segoe UI';
  const laid=[];
  tokens.forEach(tk=>{
    const w=ctx.measureText(tk.text).width;
    if(cx+w>startX+maxW&&!tk.isSpace){cx=startX;cy+=lineH}
    laid.push({text:tk.text,x:cx,y:cy,w,isSpace:tk.isSpace});
    cx+=w;
  });
  return laid;
}

function initRound(){
  const ti=(round-1)%TEXTS.length;
  curText=TEXTS[ti];
  foundErrors=0;totalErrors=5;
  timerStart=Date.now();
  feedback='';feedTimer=0;

  // Build clickable word regions from broken text
  // We mark error zones by character position
  const brk=curText.broken;
  const errZones=curText.errors.map(e=>({...e,found:false}));

  // Tokenize broken text into clickable segments
  ctx.font='18px Segoe UI';
  const tokens2=[];
  let tk2='',charIdx2=0;
  for(let i=0;i<brk.length;i++){
    if(brk[i]===' '){
      if(tk2.length>0){tokens2.push({text:tk2,startIdx:charIdx2,endIdx:i-1,isSpace:false});charIdx2=i;tk2=''}
      // Check for double space
      if(i+1<brk.length&&brk[i+1]===' '){
        tokens2.push({text:'  ',startIdx:i,endIdx:i+1,isSpace:true,isDoubleSpace:true});
        i++;charIdx2=i+1;
      }else{
        tokens2.push({text:' ',startIdx:i,endIdx:i,isSpace:true,isDoubleSpace:false});
        charIdx2=i+1;
      }
    }else{tk2+=brk[i]}
  }
  if(tk2.length>0) tokens2.push({text:tk2,startIdx:charIdx2,endIdx:charIdx2+tk2.length-1,isSpace:false});

  // Layout
  const lineH2=36,startX2=55,maxW2=W-110;
  let cx2=startX2,cy2=185;
  words=[];
  tokens2.forEach(tk=>{
    ctx.font='18px Segoe UI';
    const w2=ctx.measureText(tk.text).width;
    if(cx2+w2>startX2+maxW2&&!tk.isSpace){cx2=startX2;cy2+=lineH2}
    // Check if this token overlaps any error zone
    let isError=false;let errIdx2=-1;
    errZones.forEach((ez,ei)=>{
      if(tk.startIdx<=ez.pos+ez.len-1&&tk.endIdx>=ez.pos){isError=true;errIdx2=ei}
    });
    words.push({text:tk.text,x:cx2,y:cy2,w:w2,h:28,isError,errIdx:errIdx2,found:false,isSpace:tk.isSpace,isDoubleSpace:tk.isDoubleSpace||false});
    cx2+=w2;
  });
}

function draw(){
  ctx.clearRect(0,0,W,H);
  const grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);

  if(state==='start'){
    ctx.fillStyle='#e0e7ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
    ctx.fillText('🔍 Hata Avcısı',W/2,180);
    ctx.font='20px Segoe UI';ctx.fillText('Metindeki hataları bul!',W/2,225);
    ctx.font='16px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Yanlış kelimelere tıkla. 30 saniye süren var!',W/2,260);
    ctx.fillStyle='#6366f1';ctx.fillRect(W/2-80,305,160,40);
    ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,331);
    return;
  }
  if(state==='win'){
    ctx.fillStyle='#fbbf24';ctx.font='bold 40px Segoe UI';ctx.textAlign='center';
    ctx.fillText('TEBRİKLER!',W/2,200);
    ctx.fillStyle='#e0e7ff';ctx.font='24px Segoe UI';
    ctx.fillText('Toplam Puan: '+score,W/2,260);
    ctx.font='18px Segoe UI';ctx.fillStyle='#94a3b8';
    ctx.fillText('Harika bir dedektifsin!',W/2,300);
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
    return;
  }

  // HUD
  ctx.fillStyle='#e0e7ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='left';
  ctx.fillText('Tur: '+round+'/'+maxR,15,30);
  ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,30);

  // Timer
  const elapsed2=(Date.now()-timerStart)/1000;
  const timeRem=Math.max(0,maxTimer-elapsed2);
  ctx.textAlign='center';
  ctx.fillStyle=timeRem<10?'#ef4444':'#fbbf24';
  ctx.font='bold 18px Segoe UI';
  ctx.fillText('⏱ '+Math.ceil(timeRem)+'s',W/2,30);

  // Timer bar
  const ratio2=timeRem/maxTimer;
  ctx.fillStyle='#94A3B8';ctx.fillRect(50,45,W-100,10);
  ctx.fillStyle=timeRem<10?'#ef4444':'#10b981';
  ctx.fillRect(50,45,(W-100)*ratio2,10);

  // Error counter
  ctx.fillStyle='#e0e7ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
  ctx.fillText(totalErrors+' hatadan '+foundErrors+' bulundu',W/2,75);

  // Notebook paper background
  ctx.fillStyle='#fefce8';
  ctx.fillRect(40,100,W-80,280);
  ctx.strokeStyle='#d4a373';ctx.lineWidth=2;ctx.strokeRect(40,100,W-80,280);
  // Lines
  ctx.strokeStyle='#d4d4d4';ctx.lineWidth=0.5;
  for(let ly=136;ly<380;ly+=36){ctx.beginPath();ctx.moveTo(50,ly);ctx.lineTo(W-50,ly);ctx.stroke()}
  // Red margin line
  ctx.strokeStyle='#fca5a5';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(80,100);ctx.lineTo(80,380);ctx.stroke();

  // Draw words
  words.forEach(wd=>{
    if(wd.isSpace&&!wd.isDoubleSpace) return;
    ctx.font='18px Segoe UI';
    if(wd.found){
      // Strikethrough in red
      ctx.fillStyle='#ef4444';ctx.globalAlpha=0.3;
      ctx.fillRect(wd.x,wd.y-8,wd.w,wd.h);ctx.globalAlpha=1;
      ctx.fillStyle='#ef4444';
      ctx.fillText(wd.text,wd.x,wd.y+12);
      // Strikethrough line
      ctx.strokeStyle='#ef4444';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(wd.x,wd.y+5);ctx.lineTo(wd.x+wd.w,wd.y+5);ctx.stroke();
    }else{
      ctx.fillStyle='#1a1a2e';
      ctx.fillText(wd.text,wd.x,wd.y+12);
    }
  });

  // Feedback
  if(feedback){
    ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
    ctx.fillStyle=feedback.includes('Hata')?'#10b981':'#ef4444';
    ctx.fillText(feedback,W/2,420);
  }

  // Hint area
  ctx.fillStyle='#475569';ctx.font='14px Segoe UI';ctx.textAlign='center';
  ctx.fillText('İpucu: Yanlış harf, eksik noktalama, fazla boşluk veya büyük/küçük harf hataları ara!',W/2,460);

  // Timeout check
  if(timeRem<=0&&feedTimer===0){
    feedback='Süre doldu!';feedTimer=60;beep(180,0.3);
  }

  particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function update(){
  particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.08});
  particles=particles.filter(p=>p.life>0);
  if(feedTimer>0){feedTimer--;if(feedTimer===0){
    if(feedback==='Süre doldu!'||foundErrors>=totalErrors){
      round++;
      if(round>maxR){state='win';for(let i=0;i<40;i++)addP(W/2+Math.random()*200-100,H/2+Math.random()*100-50,['#fbbf24','#10b981','#6366f1'][i%3])}
      else initRound();
    }
    feedback='';
  }}
  draw();requestAnimationFrame(update);
}

canvas.addEventListener('click',e=>{
  const rect=canvas.getBoundingClientRect();
  const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
  if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';initRound()}return;}
  if(state==='win') return;
  if(feedTimer>0) return;

  // Check word clicks
  words.forEach(wd=>{
    if(wd.found) return;
    if(mx>=wd.x&&mx<=wd.x+wd.w&&my>=wd.y-12&&my<=wd.y+wd.h){
      if(wd.isError){
        wd.found=true;foundErrors++;
        score+=10;feedback='Hata bulundu! +10';beep(523,0.15);
        addP(wd.x+wd.w/2,wd.y,'#10b981');
        // Mark all words with same errIdx as found
        words.forEach(w2=>{if(w2.errIdx===wd.errIdx) w2.found=true});
        if(foundErrors>=totalErrors){feedback='Tüm hatalar bulundu! Harika!';feedTimer=60}
        else{feedTimer=15}
      }else{
        feedback='Burada hata yok!';beep(180,0.3);feedTimer=20;
      }
    }
  });
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
update();
</script></body></html>"""
