# -*- coding: utf-8 -*-
"""Okul Öncesi Genel Yetenek Oyunları — 20 Premium HTML5 Oyun (Bölüm B: 6-10)."""


def _build_prek_ab_desen_tamamla_html() -> str:
    """Desen Tamamla (ABAB / AABB) — Pattern completion game."""
    return '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Desen Tamamla</title><style>body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}canvas{display:block;margin:20px auto;border-radius:18px;box-shadow:0 0 40px rgba(168,85,247,.4)}</style></head><body><canvas id="c"></canvas><script>
const W=700,H=650,canvas=document.getElementById('c');canvas.width=W;canvas.height=H;const ctx=canvas.getContext('2d');
let state='start',round=1,maxRound=10,score=0;
let particles=[];
let patternShapes=[],missingIdx=-1,options=[],correctOption=-1,feedback='',feedbackTimer=0;
let shakeIdx=-1,shakeTimer=0;
let flyAnim=null;

const COLORS=['#ef4444','#3b82f6','#22c55e','#f59e0b','#a855f7','#ec4899','#06b6d4','#f97316'];
const SHAPE_TYPES=['circle','square','triangle','star','heart'];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}

function drawShape(type,cx,cy,sz,color){
    ctx.fillStyle=color;ctx.strokeStyle='rgba(255,255,255,0.3)';ctx.lineWidth=2;
    if(type==='circle'){ctx.beginPath();ctx.arc(cx,cy,sz,0,Math.PI*2);ctx.fill();ctx.stroke()}
    else if(type==='square'){ctx.beginPath();ctx.rect(cx-sz,cy-sz,sz*2,sz*2);ctx.fill();ctx.stroke()}
    else if(type==='triangle'){ctx.beginPath();ctx.moveTo(cx,cy-sz);ctx.lineTo(cx+sz,cy+sz);ctx.lineTo(cx-sz,cy+sz);ctx.closePath();ctx.fill();ctx.stroke()}
    else if(type==='star'){ctx.beginPath();for(let i=0;i<5;i++){let a=Math.PI/2+i*Math.PI*2/5;ctx.lineTo(cx+Math.cos(a)*sz,cy-Math.sin(a)*sz);a+=Math.PI*2/10;ctx.lineTo(cx+Math.cos(a)*sz*0.45,cy-Math.sin(a)*sz*0.45)}ctx.closePath();ctx.fill();ctx.stroke()}
    else if(type==='heart'){ctx.beginPath();ctx.moveTo(cx,cy+sz*0.7);ctx.bezierCurveTo(cx-sz*1.2,cy-sz*0.3,cx-sz*0.5,cy-sz*1.1,cx,cy-sz*0.4);ctx.bezierCurveTo(cx+sz*0.5,cy-sz*1.1,cx+sz*1.2,cy-sz*0.3,cx,cy+sz*0.7);ctx.fill();ctx.stroke()}
}

function generatePattern(){
    patternShapes=[];options=[];
    let pLen=5+Math.min(round-1,3);
    let usedShapes=[];let usedColors=[];
    let numDistinct=round<=3?2:round<=6?3:4;
    for(let i=0;i<numDistinct;i++){usedShapes.push(SHAPE_TYPES[i]);usedColors.push(COLORS[i])}
    let seq=[];
    if(round<=3){for(let i=0;i<pLen;i++)seq.push(i%2)}
    else if(round<=5){for(let i=0;i<pLen;i++)seq.push(Math.floor(i/2)%2)}
    else if(round<=7){for(let i=0;i<pLen;i++)seq.push(i%3)}
    else{let base=[0,1,1,0];for(let i=0;i<pLen;i++)seq.push(base[i%base.length])}
    for(let i=0;i<pLen;i++){patternShapes.push({type:usedShapes[seq[i]],color:usedColors[seq[i]],idx:seq[i]})}
    missingIdx=pLen-1;
    let correctShape=patternShapes[missingIdx];
    let opts=[{type:correctShape.type,color:correctShape.color,idx:correctShape.idx,correct:true}];
    for(let i=0;i<numDistinct;i++){
        if(i!==correctShape.idx)opts.push({type:usedShapes[i],color:usedColors[i],idx:i,correct:false});
    }
    while(opts.length<4){let ri=Math.floor(Math.random()*SHAPE_TYPES.length);let ci=Math.floor(Math.random()*COLORS.length);opts.push({type:SHAPE_TYPES[ri],color:COLORS[ci],idx:-1,correct:false})}
    opts.sort(()=>Math.random()-0.5);
    options=opts.slice(0,4);
    correctOption=options.findIndex(o=>o.correct);
    feedback='';flyAnim=null;
}

generatePattern();

function draw(){
    ctx.clearRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,W,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    particles.forEach((p,i)=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.r*=0.98;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}});
    particles=particles.filter(p=>p.life>0);

    if(state==='start'){
        ctx.fillStyle='#f0abfc';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('🧩 Desen Tamamla',W/2,180);
        ctx.fillStyle='#c4b5fd';ctx.font='22px Segoe UI';ctx.fillText('Deseni tamamlayan şekli bul!',W/2,230);
        ctx.fillStyle='#c084fc';ctx.font='18px Segoe UI';ctx.fillText('ABAB, AABB gibi desenleri tanı',W/2,265);
        roundRect(W/2-90,300,180,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);
    } else if(state==='play'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 24px Segoe UI';ctx.textAlign='center';
        ctx.fillText('Tur '+round+'/'+maxRound+'  ⭐ '+score,W/2,40);
        ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';ctx.fillText('Deseni tamamla!',W/2,70);
        let pLen=patternShapes.length;
        let startX=W/2-(pLen*55)/2;
        for(let i=0;i<pLen;i++){
            let px=startX+i*55+25,py=160;
            if(i===missingIdx&&!flyAnim){
                ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;ctx.setLineDash([6,4]);
                ctx.beginPath();ctx.arc(px,py,22,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);
                ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.fillText('?',px,py+9);
            } else if(i===missingIdx&&flyAnim&&flyAnim.done){
                drawShape(patternShapes[i].type,px,py,20,patternShapes[i].color);
            } else if(i!==missingIdx){
                drawShape(patternShapes[i].type,px,py,20,patternShapes[i].color);
            }
        }
        let optStartX=W/2-((options.length*120)-20)/2;
        for(let i=0;i<options.length;i++){
            let ox=optStartX+i*120,oy=400;
            let shake=0;if(shakeIdx===i&&shakeTimer>0){shake=Math.sin(shakeTimer*0.5)*8;shakeTimer--;if(shakeTimer<=0)shakeIdx=-1}
            roundRect(ox+shake,oy,100,100,16);ctx.fillStyle='rgba(139,92,246,0.25)';ctx.fill();ctx.strokeStyle='rgba(196,181,253,0.5)';ctx.lineWidth=2;ctx.stroke();
            drawShape(options[i].type,ox+50+shake,oy+50,28,options[i].color);
        }
        if(flyAnim&&!flyAnim.done){
            flyAnim.t+=0.04;if(flyAnim.t>=1){flyAnim.done=true;flyAnim.t=1}
            let fx=flyAnim.sx+(flyAnim.ex-flyAnim.sx)*flyAnim.t;
            let fy=flyAnim.sy+(flyAnim.ey-flyAnim.sy)*flyAnim.t-Math.sin(flyAnim.t*Math.PI)*60;
            drawShape(flyAnim.type,fx,fy,20,flyAnim.color);
            if(flyAnim.done){addP(flyAnim.ex,flyAnim.ey,flyAnim.color);feedbackTimer=50}
        }
        if(feedback){ctx.fillStyle=feedback==='Doğru! ✨'?'#4ade80':'#f87171';ctx.font='bold 28px Segoe UI';ctx.fillText(feedback,W/2,340)}
        if(feedbackTimer>0){feedbackTimer--;if(feedbackTimer<=0&&feedback==='Doğru! ✨'){round++;if(round>maxRound){state='win'}else{generatePattern()}}}
    } else if(state==='win'){
        ctx.fillStyle='#fbbf24';ctx.font='bold 46px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler!',W/2,180);
        ctx.fillStyle='#e9d5ff';ctx.font='28px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxRound*10),W/2,240);
        ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';ctx.fillText('Tüm desenleri tamamladın!',W/2,280);
        roundRect(W/2-100,310,200,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);
        if(Math.random()<0.08)addP(Math.random()*W,Math.random()*H,COLORS[Math.floor(Math.random()*COLORS.length)]);
    }
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',function(e){
    const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state==='start'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';generatePattern()}}
    else if(state==='play'&&!flyAnim){
        let optStartX=W/2-((options.length*120)-20)/2;
        for(let i=0;i<options.length;i++){
            let ox=optStartX+i*120,oy=400;
            if(mx>ox&&mx<ox+100&&my>oy&&my<oy+100){
                if(options[i].correct){
                    snd(true);score+=10;feedback='Doğru! ✨';
                    let pLen=patternShapes.length;let startX2=W/2-(pLen*55)/2;
                    let targetX=startX2+missingIdx*55+25,targetY=160;
                    flyAnim={sx:ox+50,sy:oy+50,ex:targetX,ey:targetY,t:0,done:false,type:options[i].type,color:options[i].color};
                } else {
                    snd(false);feedback='Tekrar dene!';shakeIdx=i;shakeTimer=20;
                }
                break;
            }
        }
    }
    else if(state==='win'){if(mx>W/2-100&&mx<W/2+100&&my>310&&my<360){state='play';round=1;score=0;generatePattern()}}
});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
draw();
</script></body></html>'''


def _build_prek_ab_sira_bende_html() -> str:
    """Sıra Bende (Hafıza Sırası / Simon Says) — Memory sequence game."""
    return '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Sıra Bende</title><style>body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}canvas{display:block;margin:20px auto;border-radius:18px;box-shadow:0 0 40px rgba(168,85,247,.4)}</style></head><body><canvas id="c"></canvas><script>
const W=700,H=650,canvas=document.getElementById('c');canvas.width=W;canvas.height=H;const ctx=canvas.getContext('2d');
let state='start',round=1,maxRound=10,score=0;
let particles=[];
let sequence=[],playerIdx=0,showingSeq=false,showIdx=0,showTimer=0;
let quadrants=[
    {x:100,y:130,w:220,h:200,color:'#ef4444',bright:'#fca5a5',freq:262,label:'Kırmızı'},
    {x:380,y:130,w:220,h:200,color:'#3b82f6',bright:'#93c5fd',freq:330,label:'Mavi'},
    {x:100,y:370,w:220,h:200,color:'#22c55e',bright:'#86efac',freq:392,label:'Yeşil'},
    {x:380,y:370,w:220,h:200,color:'#eab308',bright:'#fde047',freq:523,label:'Sarı'}
];
let activeQuad=-1,activeTimer=0;
let feedback='',feedbackTimer=0;
let seqLen=2;
let clickable=false;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function playTone(freq){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=freq;o.type='sine';g.gain.value=0.3;o.start();g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.35);o.stop(a.currentTime+0.35)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}

function generateSequence(){
    sequence=[];
    seqLen=round+1;
    for(let i=0;i<seqLen;i++)sequence.push(Math.floor(Math.random()*4));
    playerIdx=0;clickable=false;
    showingSeq=true;showIdx=0;showTimer=60;
}

function startShowSequence(){showingSeq=true;showIdx=0;showTimer=40;activeQuad=-1}

generateSequence();

let frameCnt=0;
function draw(){
    frameCnt++;
    ctx.clearRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,W,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    particles.forEach((p)=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.r*=0.98;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}});
    particles=particles.filter(p=>p.life>0);

    if(state==='start'){
        ctx.fillStyle='#f0abfc';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('🎵 Sıra Bende',W/2,180);
        ctx.fillStyle='#c4b5fd';ctx.font='22px Segoe UI';ctx.fillText('Renk sırasını hatırla ve tekrarla!',W/2,230);
        ctx.fillStyle='#c084fc';ctx.font='18px Segoe UI';ctx.fillText('Her turda sıra uzar',W/2,265);
        roundRect(W/2-90,300,180,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);
    } else if(state==='play'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
        ctx.fillText('Tur '+round+'/'+maxRound+'  ⭐ '+score,W/2,40);
        ctx.fillStyle='#c4b5fd';ctx.font='18px Segoe UI';
        if(showingSeq)ctx.fillText('İzle ve hatırla... ('+seqLen+' renk)',W/2,70);
        else ctx.fillText('Sırayı tekrarla! ('+playerIdx+'/'+seqLen+')',W/2,70);

        if(showingSeq){
            showTimer--;
            if(showTimer<=0){
                if(showIdx<sequence.length){
                    activeQuad=sequence[showIdx];activeTimer=25;
                    playTone(quadrants[activeQuad].freq);
                    showIdx++;showTimer=35;
                } else {
                    showingSeq=false;clickable=true;activeQuad=-1;
                }
            }
            if(activeTimer>0){activeTimer--; if(activeTimer<=0)activeQuad=-1}
        } else {
            if(activeTimer>0){activeTimer--;if(activeTimer<=0)activeQuad=-1}
        }

        for(let i=0;i<4;i++){
            let q=quadrants[i];
            roundRect(q.x,q.y,q.w,q.h,20);
            ctx.fillStyle=(activeQuad===i)?q.bright:q.color;ctx.fill();
            if(activeQuad===i){ctx.shadowColor=q.bright;ctx.shadowBlur=30;ctx.fill();ctx.shadowBlur=0}
            ctx.strokeStyle='rgba(255,255,255,0.2)';ctx.lineWidth=2;ctx.stroke();
        }
        if(feedback){
            ctx.fillStyle=feedback==='Harika! ✨'?'#4ade80':'#f87171';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,610);
        }
        if(feedbackTimer>0){feedbackTimer--;if(feedbackTimer<=0){feedback='';
            if(feedback!==''){/*handled below*/}
        }}
    } else if(state==='win'){
        ctx.fillStyle='#fbbf24';ctx.font='bold 46px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler!',W/2,180);
        ctx.fillStyle='#e9d5ff';ctx.font='28px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxRound*10),W/2,240);
        ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';ctx.fillText('Harika bir hafızan var!',W/2,280);
        roundRect(W/2-100,310,200,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);
        if(Math.random()<0.08)addP(Math.random()*W,Math.random()*H,['#ef4444','#3b82f6','#22c55e','#eab308'][Math.floor(Math.random()*4)]);
    }
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',function(e){
    const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state==='start'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';generateSequence();startShowSequence()}}
    else if(state==='play'&&clickable&&!showingSeq){
        for(let i=0;i<4;i++){
            let q=quadrants[i];
            if(mx>q.x&&mx<q.x+q.w&&my>q.y&&my<q.y+q.h){
                activeQuad=i;activeTimer=15;playTone(q.freq);
                if(sequence[playerIdx]===i){
                    playerIdx++;
                    if(playerIdx>=seqLen){
                        clickable=false;score+=10;feedback='Harika! ✨';feedbackTimer=50;snd(true);
                        addP(W/2,H/2,q.bright);
                        setTimeout(()=>{round++;if(round>maxRound){state='win'}else{generateSequence();startShowSequence();feedback=''}},1200);
                    }
                } else {
                    snd(false);feedback='Yanlış!';feedbackTimer=40;clickable=false;
                    setTimeout(()=>{activeQuad=sequence[playerIdx];activeTimer=30;playTone(quadrants[sequence[playerIdx]].freq)},500);
                    setTimeout(()=>{playerIdx=0;startShowSequence();feedback='';clickable=false},1500);
                }
                break;
            }
        }
    }
    else if(state==='win'){if(mx>W/2-100&&mx<W/2+100&&my>310&&my<360){state='play';round=1;score=0;generateSequence();startShowSequence()}}
});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
draw();
</script></body></html>'''


def _build_prek_ab_hangisi_fazla_html() -> str:
    """Hangisi Fazla? (Odd One Out) — Find the item that doesn't belong."""
    return '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Hangisi Fazla?</title><style>body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}canvas{display:block;margin:20px auto;border-radius:18px;box-shadow:0 0 40px rgba(168,85,247,.4)}</style></head><body><canvas id="c"></canvas><script>
const W=700,H=650,canvas=document.getElementById('c');canvas.width=W;canvas.height=H;const ctx=canvas.getContext('2d');
let state='start',round=1,maxRound=10,score=0;
let particles=[];
let items=[],oddIdx=-1,feedback='',feedbackTimer=0;
let shakeIdx=-1,shakeTimer=0;
let flyOutAnim=null;
let groupLabel='';

const CATEGORIES=[
    {name:'Hayvanlar',items:['🐱','🐶','🐰','🐻','🐸','🐵','🦁','🐧'],odd_from:'Meyveler',odds:['🍎','🍌','🍇','🍊','🍓']},
    {name:'Meyveler',items:['🍎','🍌','🍇','🍊','🍓','🍑','🍒','🥝'],odd_from:'Hayvanlar',odds:['🐱','🐶','🐰','🐻']},
    {name:'Araçlar',items:['🚗','🚌','🚁','✈️','🚂','🚀','🚲','🛵'],odd_from:'Meyveler',odds:['🍎','🍌','🍇','🍊']},
    {name:'Giysiler',items:['👕','👗','🧥','👒','🧤','🧣','👟','👠'],odd_from:'Hayvanlar',odds:['🐱','🐶','🐰','🐸']},
    {name:'Yiyecekler',items:['🍕','🍔','🌮','🍩','🎂','🧁','🍪','🥐'],odd_from:'Araçlar',odds:['🚗','🚌','🚁','✈️']},
    {name:'Spor',items:['⚽','🏀','🎾','🏐','⚾','🏈','🎱','🏓'],odd_from:'Yiyecekler',odds:['🍕','🍔','🌮','🍩']},
    {name:'Müzik',items:['🎸','🎹','🎺','🥁','🎻','🪗','🎷','🪘'],odd_from:'Spor',odds:['⚽','🏀','🎾','🏐']},
    {name:'Doğa',items:['🌸','🌻','🌺','🌷','🌹','💐','🌼','🌿'],odd_from:'Araçlar',odds:['🚗','🚌','🚁','🚂']},
    {name:'Deniz',items:['🐟','🐠','🦈','🐙','🦑','🐳','🦀','🐚'],odd_from:'Giysiler',odds:['👕','👗','🧥','👒']},
    {name:'Ev Eşyaları',items:['🪑','🛋️','🛏️','📺','🪞','🕯️','⏰','📚'],odd_from:'Deniz',odds:['🐟','🐠','🦈','🐙']}
];
const CARD_COLORS=['#7c3aed','#2563eb','#059669','#d97706','#dc2626','#7c3aed','#2563eb','#059669','#d97706','#dc2626'];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}

function generateRound(){
    items=[];flyOutAnim=null;feedback='';groupLabel='';
    let cat=CATEGORIES[(round-1)%CATEGORIES.length];
    let pool=[...cat.items];
    let chosen=[];
    for(let i=0;i<3;i++){let ri=Math.floor(Math.random()*pool.length);chosen.push({emoji:pool[ri],isOdd:false});pool.splice(ri,1)}
    let oddPool=[...cat.odds];let oi=Math.floor(Math.random()*oddPool.length);
    chosen.push({emoji:oddPool[oi],isOdd:true});
    chosen.sort(()=>Math.random()-0.5);
    items=chosen;
    oddIdx=items.findIndex(it=>it.isOdd);
    groupLabel=cat.name;
}

generateRound();

function draw(){
    ctx.clearRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,W,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    particles.forEach((p)=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.r*=0.98;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}});
    particles=particles.filter(p=>p.life>0);

    if(state==='start'){
        ctx.fillStyle='#f0abfc';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('🔍 Hangisi Fazla?',W/2,180);
        ctx.fillStyle='#c4b5fd';ctx.font='22px Segoe UI';ctx.fillText('Gruba uymayan nesneyi bul!',W/2,230);
        ctx.fillStyle='#c084fc';ctx.font='18px Segoe UI';ctx.fillText('3 tanesi aynı gruptan, 1 tanesi farklı',W/2,265);
        roundRect(W/2-90,300,180,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);
    } else if(state==='play'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
        ctx.fillText('Tur '+round+'/'+maxRound+'  ⭐ '+score,W/2,40);
        ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';ctx.fillText('Farklı olanı bul ve tıkla!',W/2,70);

        let positions=[{x:170,y:180},{x:430,y:180},{x:170,y:390},{x:430,y:390}];
        for(let i=0;i<4;i++){
            if(flyOutAnim&&flyOutAnim.idx===i){
                let t=flyOutAnim.t;
                let fx=positions[i].x+(W+100-positions[i].x)*t;
                let fy=positions[i].y-t*200;
                ctx.globalAlpha=1-t;
                roundRect(fx-65,fy-65,130,130,20);ctx.fillStyle=CARD_COLORS[i];ctx.fill();
                ctx.font='60px Segoe UI';ctx.textAlign='center';ctx.fillText(items[i].emoji,fx,fy+20);
                ctx.globalAlpha=1;
                flyOutAnim.t+=0.03;
                if(flyOutAnim.t>=1){flyOutAnim=null;feedbackTimer=50}
                continue;
            }
            let shake=0;if(shakeIdx===i&&shakeTimer>0){shake=Math.sin(shakeTimer*0.5)*8;shakeTimer--;if(shakeTimer<=0)shakeIdx=-1}
            let px=positions[i].x+shake,py=positions[i].y;
            roundRect(px-65,py-65,130,130,20);ctx.fillStyle=CARD_COLORS[i];ctx.fill();
            ctx.strokeStyle='rgba(255,255,255,0.2)';ctx.lineWidth=2;ctx.stroke();
            ctx.font='60px Segoe UI';ctx.textAlign='center';ctx.fillText(items[i].emoji,px,py+20);
        }
        if(feedback){
            ctx.fillStyle=feedback.includes('Doğru')?'#4ade80':'#f87171';ctx.font='bold 26px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,570);
            if(feedback.includes('Doğru')&&groupLabel){ctx.fillStyle='#fbbf24';ctx.font='20px Segoe UI';ctx.fillText('Grup: '+groupLabel,W/2,600)}
        }
        if(feedbackTimer>0){feedbackTimer--;if(feedbackTimer<=0&&feedback.includes('Doğru')){round++;if(round>maxRound){state='win'}else{generateRound()}}}
    } else if(state==='win'){
        ctx.fillStyle='#fbbf24';ctx.font='bold 46px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler!',W/2,180);
        ctx.fillStyle='#e9d5ff';ctx.font='28px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxRound*10),W/2,240);
        ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';ctx.fillText('Hepsini doğru buldun!',W/2,280);
        roundRect(W/2-100,310,200,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);
        if(Math.random()<0.08)addP(Math.random()*W,Math.random()*H,CARD_COLORS[Math.floor(Math.random()*4)]);
    }
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',function(e){
    const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state==='start'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';generateRound()}}
    else if(state==='play'&&!flyOutAnim&&feedbackTimer<=0){
        let positions=[{x:170,y:180},{x:430,y:180},{x:170,y:390},{x:430,y:390}];
        for(let i=0;i<4;i++){
            if(mx>positions[i].x-65&&mx<positions[i].x+65&&my>positions[i].y-65&&my<positions[i].y+65){
                if(items[i].isOdd){
                    snd(true);score+=10;feedback='Doğru! ✨';
                    flyOutAnim={idx:i,t:0};
                    addP(positions[i].x,positions[i].y,'#4ade80');
                } else {
                    snd(false);feedback='Tekrar dene!';shakeIdx=i;shakeTimer=20;
                }
                break;
            }
        }
    }
    else if(state==='win'){if(mx>W/2-100&&mx<W/2+100&&my>310&&my<360){state='play';round=1;score=0;generateRound()}}
});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
draw();
</script></body></html>'''


def _build_prek_ab_buyuk_kucuk_html() -> str:
    """Büyüktür-Küçüktür — Size comparison game."""
    return '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Büyüktür-Küçüktür</title><style>body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}canvas{display:block;margin:20px auto;border-radius:18px;box-shadow:0 0 40px rgba(168,85,247,.4)}</style></head><body><canvas id="c"></canvas><script>
const W=700,H=650,canvas=document.getElementById('c');canvas.width=W;canvas.height=H;const ctx=canvas.getContext('2d');
let state='start',round=1,maxRound=10,score=0;
let particles=[];
let objs=[],question='',correctIdx=-1;
let feedback='',feedbackTimer=0;
let shakeIdx=-1,shakeTimer=0;
let bounceIdx=-1,bounceTimer=0;

const EMOJIS=['🍎','🌟','🏀','🐻','🎈','🚗','🌸','🎂','🐱','🐶','🍕','🌈','⚽','🎁','🦋','🐸'];
const QUESTIONS_BIG=['Büyük olanı seç!','En büyüğünü bul!','Hangisi daha büyük?'];
const QUESTIONS_SMALL=['Küçük olanı seç!','En küçüğünü bul!','Hangisi daha küçük?'];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}

function generateRound(){
    objs=[];feedback='';bounceIdx=-1;bounceTimer=0;
    let emoji=EMOJIS[Math.floor(Math.random()*EMOJIS.length)];
    let numObjs=round<=6?2:3;
    let askBig=round<=4?true:round<=7?false:Math.random()>0.5;
    let sizes=[];
    if(numObjs===2){
        let s1=40+Math.random()*20;
        let diff=round<=3?30:round<=6?20:15;
        let s2=s1+diff+Math.random()*10;
        sizes=[s1,s2];
        sizes.sort(()=>Math.random()-0.5);
    } else {
        let base=35+Math.random()*10;
        let diff=round<=8?20:12;
        sizes=[base,base+diff,base+diff*2];
        sizes.sort(()=>Math.random()-0.5);
    }
    let positions2=[{x:220,y:330},{x:480,y:330}];
    let positions3=[{x:150,y:330},{x:350,y:330},{x:550,y:330}];
    let positions=numObjs===2?positions2:positions3;
    for(let i=0;i<numObjs;i++){
        objs.push({emoji:emoji,size:sizes[i],x:positions[i].x,y:positions[i].y});
    }
    if(askBig){
        question=QUESTIONS_BIG[Math.floor(Math.random()*QUESTIONS_BIG.length)];
        let maxS=Math.max(...sizes);correctIdx=objs.findIndex(o=>o.size===maxS);
    } else {
        question=QUESTIONS_SMALL[Math.floor(Math.random()*QUESTIONS_SMALL.length)];
        let minS=Math.min(...sizes);correctIdx=objs.findIndex(o=>o.size===minS);
    }
    if(round===8||round===9){
        if(numObjs===3){
            question='Ortanca boyuttakini seç!';
            let sorted=[...sizes].sort((a,b)=>a-b);
            let medS=sorted[1];correctIdx=objs.findIndex(o=>o.size===medS);
        }
    }
}

generateRound();

function draw(){
    ctx.clearRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,W,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    particles.forEach((p)=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.r*=0.98;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}});
    particles=particles.filter(p=>p.life>0);

    if(state==='start'){
        ctx.fillStyle='#f0abfc';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('📏 Büyüktür-Küçüktür',W/2,180);
        ctx.fillStyle='#c4b5fd';ctx.font='22px Segoe UI';ctx.fillText('Boyut karşılaştırması yap!',W/2,230);
        ctx.fillStyle='#c084fc';ctx.font='18px Segoe UI';ctx.fillText('Büyük veya küçük olanı seç',W/2,265);
        roundRect(W/2-90,300,180,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);
    } else if(state==='play'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
        ctx.fillText('Tur '+round+'/'+maxRound+'  ⭐ '+score,W/2,40);
        ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';ctx.fillText(question,W/2,100);

        for(let i=0;i<objs.length;i++){
            let o=objs[i];
            let shake=0;if(shakeIdx===i&&shakeTimer>0){shake=Math.sin(shakeTimer*0.5)*8;shakeTimer--;if(shakeTimer<=0)shakeIdx=-1}
            let bounceY=0;if(bounceIdx===i&&bounceTimer>0){bounceY=Math.sin(bounceTimer*0.3)*15;bounceTimer--;if(bounceTimer<=0)bounceIdx=-1}
            let cx=o.x+shake,cy=o.y+bounceY;
            roundRect(cx-o.size-15,cy-o.size-15,o.size*2+30,o.size*2+30,18);
            ctx.fillStyle='rgba(139,92,246,0.2)';ctx.fill();
            ctx.strokeStyle='rgba(196,181,253,0.4)';ctx.lineWidth=2;ctx.stroke();
            ctx.font=Math.floor(o.size*1.3)+'px Segoe UI';ctx.textAlign='center';
            ctx.fillText(o.emoji,cx,cy+o.size*0.4);
        }
        if(feedback){ctx.fillStyle=feedback.includes('Doğru')?'#4ade80':'#f87171';ctx.font='bold 26px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,540)}
        if(feedbackTimer>0){feedbackTimer--;if(feedbackTimer<=0&&feedback.includes('Doğru')){round++;if(round>maxRound){state='win'}else{generateRound()}}}
    } else if(state==='win'){
        ctx.fillStyle='#fbbf24';ctx.font='bold 46px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler!',W/2,180);
        ctx.fillStyle='#e9d5ff';ctx.font='28px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxRound*10),W/2,240);
        ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';ctx.fillText('Boyut ustası oldun!',W/2,280);
        roundRect(W/2-100,310,200,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);
        if(Math.random()<0.08)addP(Math.random()*W,Math.random()*H,['#f0abfc','#c4b5fd','#fbbf24','#4ade80'][Math.floor(Math.random()*4)]);
    }
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',function(e){
    const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state==='start'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';generateRound()}}
    else if(state==='play'&&feedbackTimer<=0){
        for(let i=0;i<objs.length;i++){
            let o=objs[i];
            if(mx>o.x-o.size-15&&mx<o.x+o.size+15&&my>o.y-o.size-15&&my<o.y+o.size+15){
                if(i===correctIdx){
                    snd(true);score+=10;feedback='Doğru! ✨';bounceIdx=i;bounceTimer=30;feedbackTimer=50;
                    addP(o.x,o.y,'#4ade80');
                } else {
                    snd(false);feedback='Tekrar dene!';shakeIdx=i;shakeTimer=20;
                }
                break;
            }
        }
    }
    else if(state==='win'){if(mx>W/2-100&&mx<W/2+100&&my>310&&my<360){state='play';round=1;score=0;generateRound()}}
});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
draw();
</script></body></html>'''


def _build_prek_ab_ses_kaynagi_html() -> str:
    """Ses Kaynağını Bul — Match the sound to the animal."""
    return '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Ses Kaynağını Bul</title><style>body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}canvas{display:block;margin:20px auto;border-radius:18px;box-shadow:0 0 40px rgba(168,85,247,.4)}</style></head><body><canvas id="c"></canvas><script>
const W=700,H=650,canvas=document.getElementById('c');canvas.width=W;canvas.height=H;const ctx=canvas.getContext('2d');
let state='start',round=1,maxRound=10,score=0;
let particles=[];
let animals=[],currentAnimalIdx=-1,correctCardIdx=-1;
let feedback='',feedbackTimer=0;
let shakeIdx=-1,shakeTimer=0;
let bounceIdx=-1,bounceTimer=0;
let soundPlayed=false;

const ANIMAL_POOL=[
    {emoji:'🐱',name:'Kedi',freq:800,type:'sine',dur:0.3,wobble:true,wobbleRate:12,wobbleDepth:100},
    {emoji:'🐶',name:'Köpek',freq:300,type:'square',dur:0.15,burst:true,burstCount:3},
    {emoji:'🐦',name:'Kuş',freq:1200,type:'sine',dur:0.4,trill:true,trillRate:20,trillDepth:200},
    {emoji:'🐄',name:'İnek',freq:150,type:'sawtooth',dur:0.8,wobble:true,wobbleRate:3,wobbleDepth:30},
    {emoji:'🐸',name:'Kurbağa',freq:200,type:'square',dur:0.5,pulse:true,pulseRate:8},
    {emoji:'🦁',name:'Aslan',freq:100,type:'sawtooth',dur:0.7,wobble:true,wobbleRate:5,wobbleDepth:20},
    {emoji:'🐷',name:'Domuz',freq:400,type:'sawtooth',dur:0.4,wobble:true,wobbleRate:8,wobbleDepth:60},
    {emoji:'🦆',name:'Ördek',freq:500,type:'square',dur:0.2,burst:true,burstCount:2},
    {emoji:'🐴',name:'At',freq:250,type:'sawtooth',dur:0.5,wobble:true,wobbleRate:15,wobbleDepth:80},
    {emoji:'🦉',name:'Baykuş',freq:350,type:'sine',dur:0.6,wobble:true,wobbleRate:2,wobbleDepth:50}
];
const CARD_BG=['#7c3aed','#2563eb','#059669','#d97706'];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr,r:3+Math.random()*3})}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}

function playAnimalSound(animal){
    try{
        const a=new AudioContext();
        const o=a.createOscillator();
        const g=a.createGain();
        o.connect(g);g.connect(a.destination);
        o.frequency.value=animal.freq;
        o.type=animal.type||'sine';
        g.gain.value=0.3;
        o.start();
        let dur=animal.dur||0.4;
        if(animal.wobble){
            const lfo=a.createOscillator();const lfoG=a.createGain();
            lfo.frequency.value=animal.wobbleRate||10;lfoG.gain.value=animal.wobbleDepth||50;
            lfo.connect(lfoG);lfoG.connect(o.frequency);lfo.start();lfo.stop(a.currentTime+dur);
        }
        if(animal.trill){
            const lfo=a.createOscillator();const lfoG=a.createGain();
            lfo.frequency.value=animal.trillRate||20;lfoG.gain.value=animal.trillDepth||200;
            lfo.connect(lfoG);lfoG.connect(o.frequency);lfo.start();lfo.stop(a.currentTime+dur);
        }
        if(animal.pulse){
            const lfo=a.createOscillator();const lfoG=a.createGain();
            lfo.frequency.value=animal.pulseRate||8;lfoG.gain.value=0.3;
            lfo.connect(lfoG);lfoG.connect(g.gain);lfo.start();lfo.stop(a.currentTime+dur);
        }
        if(animal.burst){
            let cnt=animal.burstCount||2;
            for(let b=1;b<cnt;b++){
                setTimeout(()=>{
                    try{const o2=a.createOscillator();const g2=a.createGain();o2.connect(g2);g2.connect(a.destination);o2.frequency.value=animal.freq*(1+b*0.1);o2.type=animal.type;g2.gain.value=0.25;o2.start();g2.gain.exponentialRampToValueAtTime(0.001,a.currentTime+dur);o2.stop(a.currentTime+dur)}catch(e){}
                },b*150);
            }
        }
        g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+dur);
        o.stop(a.currentTime+dur);
    }catch(e){}
}

function generateRound(){
    animals=[];feedback='';bounceIdx=-1;bounceTimer=0;soundPlayed=false;
    let pool=[...ANIMAL_POOL];
    pool.sort(()=>Math.random()-0.5);
    let selected=pool.slice(0,4);
    currentAnimalIdx=Math.floor(Math.random()*4);
    animals=selected;
    correctCardIdx=currentAnimalIdx;
    setTimeout(()=>{playAnimalSound(animals[currentAnimalIdx]);soundPlayed=true},500);
}

generateRound();

function draw(){
    ctx.clearRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,W,H);grd.addColorStop(0,'#1a0533');grd.addColorStop(1,'#0d0221');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    particles.forEach((p)=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.r*=0.98;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}});
    particles=particles.filter(p=>p.life>0);

    if(state==='start'){
        ctx.fillStyle='#f0abfc';ctx.font='bold 42px Segoe UI';ctx.textAlign='center';ctx.fillText('🔊 Ses Kaynağını Bul',W/2,180);
        ctx.fillStyle='#c4b5fd';ctx.font='22px Segoe UI';ctx.fillText('Sesi dinle, hangi hayvana ait bul!',W/2,230);
        ctx.fillStyle='#c084fc';ctx.font='18px Segoe UI';ctx.fillText('Her hayvanın kendine özgü sesi var',W/2,265);
        roundRect(W/2-90,300,180,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);
    } else if(state==='play'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';
        ctx.fillText('Tur '+round+'/'+maxRound+'  ⭐ '+score,W/2,40);
        ctx.fillStyle='#fbbf24';ctx.font='bold 24px Segoe UI';ctx.fillText('Bu ses hangi hayvana ait?',W/2,85);

        // Replay button
        roundRect(W/2-80,105,160,40,20);ctx.fillStyle='rgba(124,58,237,0.6)';ctx.fill();
        ctx.strokeStyle='rgba(196,181,253,0.5)';ctx.lineWidth=1.5;ctx.stroke();
        ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.fillText('🔊 Tekrar Dinle',W/2,131);

        // Animal cards
        let cardW=130,cardH=160,gap=20;
        let totalW=4*cardW+3*gap;
        let startX=(W-totalW)/2;
        let cardY=200;

        for(let i=0;i<4;i++){
            if(i>=animals.length)continue;
            let cx=startX+i*(cardW+gap);
            let shake=0;if(shakeIdx===i&&shakeTimer>0){shake=Math.sin(shakeTimer*0.5)*8;shakeTimer--;if(shakeTimer<=0)shakeIdx=-1}
            let bounceY=0;if(bounceIdx===i&&bounceTimer>0){bounceY=Math.sin(bounceTimer*0.3)*12;bounceTimer--;if(bounceTimer<=0)bounceIdx=-1}

            roundRect(cx+shake,cardY+bounceY,cardW,cardH,18);ctx.fillStyle=CARD_BG[i];ctx.fill();
            ctx.strokeStyle='rgba(255,255,255,0.25)';ctx.lineWidth=2;ctx.stroke();

            // Glow for correct after feedback
            if(feedback.includes('Yanlış')&&i===correctCardIdx){
                ctx.shadowColor='#4ade80';ctx.shadowBlur=20;
                roundRect(cx,cardY,cardW,cardH,18);ctx.strokeStyle='#4ade80';ctx.lineWidth=3;ctx.stroke();
                ctx.shadowBlur=0;
            }

            ctx.font='60px Segoe UI';ctx.textAlign='center';ctx.fillText(animals[i].emoji,cx+cardW/2+shake,cardY+80+bounceY);
            ctx.fillStyle='#fff';ctx.font='bold 16px Segoe UI';ctx.fillText(animals[i].name,cx+cardW/2+shake,cardY+cardH-15+bounceY);
        }

        if(feedback){
            ctx.fillStyle=feedback.includes('Doğru')?'#4ade80':'#f87171';ctx.font='bold 28px Segoe UI';ctx.textAlign='center';
            ctx.fillText(feedback,W/2,440);
            if(feedback.includes('Doğru')){
                ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';
                ctx.fillText(animals[correctCardIdx].emoji+' '+animals[correctCardIdx].name+' sesi!',W/2,475);
            } else if(feedback.includes('Yanlış')){
                ctx.fillStyle='#fbbf24';ctx.font='18px Segoe UI';
                ctx.fillText('Doğru cevap: '+animals[correctCardIdx].emoji+' '+animals[correctCardIdx].name,W/2,475);
            }
        }
        if(feedbackTimer>0){feedbackTimer--;if(feedbackTimer<=0){round++;if(round>maxRound){state='win'}else{generateRound()}}}
    } else if(state==='win'){
        ctx.fillStyle='#fbbf24';ctx.font='bold 46px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler!',W/2,180);
        ctx.fillStyle='#e9d5ff';ctx.font='28px Segoe UI';ctx.fillText('Puan: '+score+' / '+(maxRound*10),W/2,240);
        ctx.fillStyle='#c4b5fd';ctx.font='20px Segoe UI';ctx.fillText('Tüm sesleri doğru buldun!',W/2,280);
        roundRect(W/2-100,310,200,50,25);ctx.fillStyle='#7c3aed';ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);
        if(Math.random()<0.08)addP(Math.random()*W,Math.random()*H,['#f0abfc','#fbbf24','#4ade80','#7c3aed'][Math.floor(Math.random()*4)]);
    }
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',function(e){
    const rect=canvas.getBoundingClientRect();const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state==='start'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';generateRound()}}
    else if(state==='play'){
        // Replay button
        if(mx>W/2-80&&mx<W/2+80&&my>105&&my<145&&animals.length>0){
            playAnimalSound(animals[currentAnimalIdx]);
            return;
        }
        if(feedbackTimer>0)return;
        let cardW=130,cardH=160,gap=20;
        let totalW=4*cardW+3*gap;
        let startX=(W-totalW)/2;
        let cardY=200;
        for(let i=0;i<4;i++){
            if(i>=animals.length)continue;
            let cx=startX+i*(cardW+gap);
            if(mx>cx&&mx<cx+cardW&&my>cardY&&my<cardY+cardH){
                if(i===correctCardIdx){
                    snd(true);score+=10;feedback='Doğru! ✨';bounceIdx=i;bounceTimer=30;feedbackTimer=60;
                    addP(cx+cardW/2,cardY+80,'#4ade80');
                } else {
                    snd(false);feedback='Yanlış!';shakeIdx=i;shakeTimer=20;feedbackTimer=60;
                }
                break;
            }
        }
    }
    else if(state==='win'){if(mx>W/2-100&&mx<W/2+100&&my>310&&my<360){state='play';round=1;score=0;generateRound()}}
});
canvas.addEventListener('touchstart',function(e){e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});
draw();
</script></body></html>'''
