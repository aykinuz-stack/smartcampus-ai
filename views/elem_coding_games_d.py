"""İlkokul Kodlama Oyunları 16-20."""


def _build_elem_code_muzik_kodla_html():
    """Müzik Kodla - Notaları sıralayarak melodi oluştur."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const NOTES=['Do','Re','Mi','Fa','Sol','La','Si'];
const FREQS=[262,294,330,349,392,440,494];
const NCOLS=['#e74c3c','#e67e22','#f1c40f','#2ecc71','#3498db','#9b59b6','#e84393'];
let targetSeq,userSeq,playing,feedback;

function genRound(){
    let len=3+Math.min(round,5);
    targetSeq=[];for(let i=0;i<len;i++)targetSeq.push(Math.floor(Math.random()*7));
    userSeq=[];playing=false;feedback='';
}
function playSeq(seq,cb){
    let i=0;playing=true;
    let iv=setInterval(()=>{
        if(i>=seq.length){clearInterval(iv);playing=false;if(cb)cb();return;}
        beep(FREQS[seq[i]],0.3);i++;
    },450);
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#e84393';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🎵 Muzik Kodla',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Hedef melodiyi notalari siralayarak olustur!',W/2,260);
        ctx.fillStyle='#e84393';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        // Target sequence
        ctx.fillStyle='#f39c12';ctx.font='bold 16px Arial';ctx.fillText('Hedef Melodi ('+targetSeq.length+' nota):',W/2,70);
        let tw=targetSeq.length*50;
        for(let i=0;i<targetSeq.length;i++){
            ctx.fillStyle=NCOLS[targetSeq[i]];ctx.beginPath();ctx.roundRect(W/2-tw/2+i*50,80,45,35,6);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 12px Arial';ctx.fillText(NOTES[targetSeq[i]],W/2-tw/2+i*50+22,102);
        }
        // Listen button
        ctx.fillStyle='#9b59b6';ctx.beginPath();ctx.roundRect(W/2-50,125,100,30,6);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 13px Arial';ctx.fillText('DINLE',W/2,143);
        // User sequence
        ctx.fillStyle='#3498db';ctx.font='bold 16px Arial';ctx.fillText('Senin Melodin:',W/2,185);
        for(let i=0;i<targetSeq.length;i++){
            if(i<userSeq.length){
                ctx.fillStyle=NCOLS[userSeq[i]];ctx.beginPath();ctx.roundRect(W/2-tw/2+i*50,195,45,35,6);ctx.fill();
                ctx.fillStyle='#fff';ctx.font='bold 12px Arial';ctx.fillText(NOTES[userSeq[i]],W/2-tw/2+i*50+22,217);
            }else{ctx.strokeStyle='#555';ctx.lineWidth=2;ctx.strokeRect(W/2-tw/2+i*50,195,45,35);}
        }
        // Note buttons
        for(let i=0;i<7;i++){
            ctx.fillStyle=NCOLS[i];ctx.beginPath();ctx.roundRect(65+i*85,260,75,55,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 18px Arial';ctx.fillText(NOTES[i],65+i*85+37,292);
        }
        // Controls
        ctx.fillStyle='#e74c3c';ctx.beginPath();ctx.roundRect(200,340,100,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 14px Arial';ctx.fillText('SIL',250,360);
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(400,340,100,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('KONTROL',450,360);
        if(feedback){ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 24px Arial';
            ctx.fillText(feedback=='ok'?'Dogru melodi!':'Yanlis, tekrar dene!',W/2,420);}
    }else if(state=='win'){
        ctx.fillStyle='#f1c40f';ctx.font='bold 42px Arial';ctx.textAlign='center';ctx.fillText('🏆 TEBRİKLER!',W/2,250);
        ctx.fillStyle='#ecf0f1';ctx.font='24px Arial';ctx.fillText('Toplam Puan: '+score,W/2,320);
    }
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}});
    particles=particles.filter(p=>p.life>0);
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',e=>{
    const rect=canvas.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';genRound();}return;}
    if(state!='play'||playing)return;
    if(feedback=='ok')return;if(feedback){feedback='';return;}
    if(mx>W/2-50&&mx<W/2+50&&my>125&&my<155){playSeq(targetSeq);return;}
    for(let i=0;i<7;i++){if(mx>65+i*85&&mx<65+i*85+75&&my>260&&my<315&&userSeq.length<targetSeq.length){userSeq.push(i);beep(FREQS[i],0.2);return;}}
    if(mx>200&&mx<300&&my>340&&my<375&&userSeq.length>0){userSeq.pop();return;}
    if(mx>400&&mx<500&&my>340&&my<375&&userSeq.length==targetSeq.length){
        let ok=true;for(let i=0;i<targetSeq.length;i++)if(userSeq[i]!==targetSeq[i])ok=false;
        if(ok){feedback='ok';score+=10;beep(523,0.15);addP(W/2,300,'#2ecc71');playSeq(userSeq,()=>{
            setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},500);});
        }else{feedback='no';beep(180,0.3);setTimeout(()=>{userSeq=[];feedback='';},1200);}
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_labirent_kodla_html():
    """Labirent Kodla - Program yazarak robotu yönlendir."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const GS=7,CS=52,OX=30,OY=40;
const DIRS=[[0,-1],[1,0],[0,1],[-1,0]];// up,right,down,left
let grid,rx,ry,dir,gx,gy,cmds,animating,animIdx,animRX,animRY,animDir;

function genMaze(){
    grid=[];for(let r=0;r<GS;r++){grid[r]=[];for(let c=0;c<GS;c++)grid[r][c]=0;}
    rx=0;ry=0;dir=1;gx=GS-1;gy=GS-1;
    let walls=3+Math.min(round,8);
    for(let w=0;w<walls;w++){let wx,wy;do{wx=Math.floor(Math.random()*GS);wy=Math.floor(Math.random()*GS);}while((wx==0&&wy==0)||(wx==gx&&wy==gy));grid[wy][wx]=1;}
    cmds=[];animating=false;
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}
const DARROWS=['↑','→','↓','←'];

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd2=ctx.createLinearGradient(0,0,0,H);grd2.addColorStop(0,'#1a1a2e');grd2.addColorStop(1,'#16213e');ctx.fillStyle=grd2;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#fdcb6e';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🧭 Labirent Kodla',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Komutlarla robotu hedefe ulastir!',W/2,260);
        ctx.fillStyle='#fdcb6e';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,25);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,25);ctx.textAlign='center';
        // Grid
        for(let r=0;r<GS;r++)for(let c=0;c<GS;c++){
            ctx.fillStyle=grid[r][c]==1?'#e74c3c':(r+c)%2==0?'#2c3e50':'#34495e';
            ctx.fillRect(OX+c*CS,OY+r*CS,CS,CS);ctx.strokeStyle='#4a6a8a';ctx.strokeRect(OX+c*CS,OY+r*CS,CS,CS);
        }
        let drx=animating?animRX:rx,dry=animating?animRY:ry,dd=animating?animDir:dir;
        ctx.font='28px Arial';ctx.textAlign='center';ctx.textBaseline='middle';
        ctx.fillText('🏁',OX+gx*CS+CS/2,OY+gy*CS+CS/2);
        ctx.fillStyle='#3498db';ctx.font='24px Arial';ctx.fillText(DARROWS[dd],OX+drx*CS+CS/2,OY+dry*CS+CS/2);
        // Command buttons (right side)
        let bx=420,by=50;
        ctx.fillStyle='#ecf0f1';ctx.font='bold 14px Arial';ctx.textBaseline='top';ctx.textAlign='center';ctx.fillText('Komutlar:',bx+100,by);
        let btns=[{t:'ILERI',c:'#2ecc71'},{t:'SAG DON',c:'#3498db'},{t:'SOL DON',c:'#e67e22'}];
        for(let i=0;i<3;i++){
            ctx.fillStyle=btns[i].c;ctx.beginPath();ctx.roundRect(bx+i*90,by+25,80,35,8);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 12px Arial';ctx.textBaseline='middle';ctx.fillText(btns[i].t,bx+i*90+40,by+43);
        }
        // Command queue
        ctx.fillStyle='#95a5a6';ctx.font='bold 12px Arial';ctx.textAlign='center';ctx.fillText('Program:',bx+100,by+80);
        for(let i=0;i<cmds.length&&i<12;i++){
            let ct=cmds[i]==0?'I':cmds[i]==1?'S':cmds[i]==2?'L':'?';
            ctx.fillStyle=cmds[i]==0?'#2ecc71':cmds[i]==1?'#3498db':'#e67e22';
            ctx.beginPath();ctx.roundRect(bx+(i%6)*42,by+95+Math.floor(i/6)*30,38,25,4);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 11px Arial';ctx.fillText(ct,bx+(i%6)*42+19,by+108+Math.floor(i/6)*30);
        }
        // Control buttons
        let cy=by+180;
        ctx.fillStyle='#e74c3c';ctx.beginPath();ctx.roundRect(bx,cy,80,30,6);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 12px Arial';ctx.fillText('SIFIRLA',bx+40,cy+16);
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(bx+100,cy,100,30,6);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('CALISTIR',bx+150,cy+16);
    }else if(state=='win'){
        ctx.textBaseline='middle';
        ctx.fillStyle='#f1c40f';ctx.font='bold 42px Arial';ctx.textAlign='center';ctx.fillText('🏆 TEBRİKLER!',W/2,250);
        ctx.fillStyle='#ecf0f1';ctx.font='24px Arial';ctx.fillText('Toplam Puan: '+score,W/2,320);
    }
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}});
    particles=particles.filter(p=>p.life>0);
    requestAnimationFrame(draw);
}

function runProg(){
    animating=true;animIdx=0;animRX=rx;animRY=ry;animDir=dir;
    let iv=setInterval(()=>{
        if(animIdx>=cmds.length){clearInterval(iv);animating=false;
            if(animRX==gx&&animRY==gy){score+=10;beep(523,0.15);addP(OX+gx*CS+CS/2,OY+gy*CS+CS/2,'#2ecc71');round++;if(round>maxR)state='win';else genMaze();}
            else{beep(180,0.3);cmds=[];}return;
        }
        let c=cmds[animIdx];
        if(c==0){let nx=animRX+DIRS[animDir][0],ny=animRY+DIRS[animDir][1];
            if(nx>=0&&nx<GS&&ny>=0&&ny<GS&&grid[ny][nx]!=1){animRX=nx;animRY=ny;}
            else{clearInterval(iv);animating=false;beep(180,0.3);cmds=[];return;}
        }else if(c==1){animDir=(animDir+1)%4;}
        else if(c==2){animDir=(animDir+3)%4;}
        animIdx++;
    },350);
}

canvas.addEventListener('click',e=>{
    const rect=canvas.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';genMaze();}return;}
    if(state!='play'||animating)return;
    let bx=420,by=50;
    for(let i=0;i<3;i++){if(mx>bx+i*90&&mx<bx+i*90+80&&my>by+25&&my<by+60&&cmds.length<12){cmds.push(i);beep(350+i*50,0.05);return;}}
    let cy=by+180;
    if(mx>bx&&mx<bx+80&&my>cy&&my<cy+30){cmds=[];return;}
    if(mx>bx+100&&mx<bx+200&&my>cy&&my<cy+30&&cmds.length>0){runProg();}
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_karsilastirma_html():
    """Karşılaştırma Operatörleri - Doğru operatörü seç."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const OPS=['>','<','==','!=','>=','<='];
let valA,valB,correctOp,feedback,selOp;

function genRound(){
    valA=Math.floor(Math.random()*20)-5;
    valB=Math.floor(Math.random()*20)-5;
    let valid=[];
    if(valA>valB)valid.push('>','!=','>=');
    if(valA<valB)valid.push('<','!=','<=');
    if(valA==valB)valid.push('==','>=','<=');
    if(valA!=valB)valid.push('!=');
    correctOp=valid[Math.floor(Math.random()*valid.length)];
    feedback='';selOp=-1;
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function checkOp(op){
    if(op=='>')return valA>valB;if(op=='<')return valA<valB;if(op=='==')return valA==valB;
    if(op=='!=')return valA!=valB;if(op=='>=')return valA>=valB;if(op=='<=')return valA<=valB;return false;
}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#00cec9';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('⚖️ Karsilastirma',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Dogru karsilastirma operatorunu sec!',W/2,260);
        ctx.fillStyle='#00cec9';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        // Expression
        ctx.fillStyle='#3498db';ctx.font='bold 64px Arial';ctx.fillText(valA,200,180);
        ctx.fillStyle='#f1c40f';ctx.font='bold 48px Arial';ctx.fillText('?',W/2,180);
        ctx.fillStyle='#e74c3c';ctx.font='bold 64px Arial';ctx.fillText(valB,500,180);
        ctx.fillStyle='#95a5a6';ctx.font='18px Arial';ctx.fillText('= true yapacak operatoru sec',W/2,230);
        // Operator buttons
        for(let i=0;i<6;i++){
            let col=selOp==i?(feedback=='ok'?'#27ae60':'#e74c3c'):'#34495e';
            ctx.fillStyle=col;ctx.beginPath();ctx.roundRect(80+i*95,280,85,55,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 24px Courier New';ctx.fillText(OPS[i],80+i*95+42,312);
        }
        if(feedback){ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 28px Arial';
            ctx.fillText(feedback=='ok'?valA+' '+OPS[selOp]+' '+valB+' = true ✓':'Yanlis operator!',W/2,400);}
    }else if(state=='win'){
        ctx.fillStyle='#f1c40f';ctx.font='bold 42px Arial';ctx.textAlign='center';ctx.fillText('🏆 TEBRİKLER!',W/2,250);
        ctx.fillStyle='#ecf0f1';ctx.font='24px Arial';ctx.fillText('Toplam Puan: '+score,W/2,320);
    }
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}});
    particles=particles.filter(p=>p.life>0);
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',e=>{
    const rect=canvas.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';genRound();}return;}
    if(state!='play'||feedback)return;
    for(let i=0;i<6;i++){
        if(mx>80+i*95&&mx<165+i*95&&my>280&&my<335){
            selOp=i;
            if(checkOp(OPS[i])){feedback='ok';score+=10;beep(523,0.15);addP(W/2,300,'#2ecc71');
                setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1200);
            }else{feedback='no';beep(180,0.3);setTimeout(()=>{feedback='';selOp=-1;},1000);}
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_olay_dinleyici_html():
    """Olay Dinleyici - Event-action eşleştirmesi yap."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const PAIRS=[
    [{e:'Butona tikla',a:'Kapi acilsin'},{e:'Fareyi kutuya gotir',a:'Kutu parlasn'},{e:'Tusabasn',a:'Karakter ziplas'}],
    [{e:'Zamanlayici bitsin',a:'Oyun dursun'},{e:'Canavar gelsin',a:'Alarm calsin'},{e:'Yildiz toplansin',a:'Puan artsin'}],
    [{e:'Fare saga gitsin',a:'Araba saga donsu'},{e:'Bosluk tusuna bas',a:'Ucak ateslesn'},{e:'Enter tusuna bas',a:'Mesaj gonderils'}],
    [{e:'Ekrana dokunulsn',a:'Top ziplasin'},{e:'Telefon sallansin',a:'Zar atilsin'},{e:'Ses duyulsun',a:'Isik yansn'}],
    [{e:'Sag ok tusuna bas',a:'Karakter yursn'},{e:'Yukari ok tusuna bas',a:'Karakter ziplasin'},{e:'P tusuna bas',a:'Oyun duraksas'}],
    [{e:'Mouse tiklansin',a:'Balon patlasn'},{e:'Skor 100 olsn',a:'Level atlansn'},{e:'Can 0 olsun',a:'Oyun bitsn'}],
    [{e:'Timer=0',a:'Bomba patlasn'},{e:'Coin toplansin',a:'Skor +10'},{e:'Boss yenilsin',a:'Zafer ekrani'}],
    [{e:'Gece olsun',a:'Isiklar yansn'},{e:'Yagmur baslasin',a:'Semsiye acilsn'},{e:'Ruzgar essin',a:'Yaprak ucssn'}],
    [{e:'Fare ikili tikla',a:'Dosya acilsin'},{e:'Surukle birak',a:'Dosya tasinsin'},{e:'Sag tikla',a:'Menu acilsin'}],
    [{e:'Sayfa yuklensin',a:'Animasyon basla'},{e:'Form gonderilsn',a:'Tesekkur mesaji'},{e:'Link tiklansin',a:'Sayfa degisn'}],
];
let curPairs,shuffledActions,connections,selEvent,feedback;

function genRound(){
    curPairs=PAIRS[(round-1)%PAIRS.length];
    shuffledActions=curPairs.map((_,i)=>i);
    for(let i=shuffledActions.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[shuffledActions[i],shuffledActions[j]]=[shuffledActions[j],shuffledActions[i]];}
    connections={};selEvent=-1;feedback='';
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#0984e3';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🔔 Olay Dinleyici',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Olaylari dogru aksiyonlarla eslestir!',W/2,260);
        ctx.fillStyle='#0984e3';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#f39c12';ctx.font='bold 18px Arial';ctx.fillText('Olayi sec, sonra aksiyonu sec',W/2,65);
        // Events (left)
        ctx.fillStyle='#95a5a6';ctx.font='bold 14px Arial';ctx.fillText('OLAYLAR',130,95);
        for(let i=0;i<curPairs.length;i++){
            let connected=connections[i]!==undefined;
            ctx.fillStyle=selEvent==i?'#f1c40f':connected?'#27ae60':'#2c3e50';
            ctx.beginPath();ctx.roundRect(30,110+i*80,240,60,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 14px Arial';ctx.fillText(curPairs[i].e,150,145+i*80);
        }
        // Actions (right)
        ctx.fillStyle='#95a5a6';ctx.font='bold 14px Arial';ctx.fillText('AKSIYONLAR',560,95);
        for(let i=0;i<shuffledActions.length;i++){
            let ai=shuffledActions[i];
            let used=Object.values(connections).includes(ai);
            ctx.fillStyle=used?'#27ae60':'#34495e';
            ctx.beginPath();ctx.roundRect(430,110+i*80,240,60,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 14px Arial';ctx.fillText(curPairs[ai].a,550,145+i*80);
        }
        // Connection lines
        for(let [ei,ai] of Object.entries(connections)){
            ctx.strokeStyle='#f1c40f';ctx.lineWidth=2;
            ctx.beginPath();ctx.moveTo(270,140+parseInt(ei)*80);
            let aIdx=shuffledActions.indexOf(parseInt(ai));
            ctx.lineTo(430,140+aIdx*80);ctx.stroke();ctx.lineWidth=1;
        }
        // Check button
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(W/2-60,500,120,40,10);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 16px Arial';ctx.fillText('KONTROL',W/2,522);
        if(feedback){ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 22px Arial';
            ctx.fillText(feedback=='ok'?'Tum eslesmelr dogru!':'Yanlis, tekrar dene!',W/2,580);}
    }else if(state=='win'){
        ctx.fillStyle='#f1c40f';ctx.font='bold 42px Arial';ctx.textAlign='center';ctx.fillText('🏆 TEBRİKLER!',W/2,250);
        ctx.fillStyle='#ecf0f1';ctx.font='24px Arial';ctx.fillText('Toplam Puan: '+score,W/2,320);
    }
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}});
    particles=particles.filter(p=>p.life>0);
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',e=>{
    const rect=canvas.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';genRound();}return;}
    if(state!='play')return;
    if(feedback=='ok')return;if(feedback){feedback='';connections={};selEvent=-1;return;}
    for(let i=0;i<curPairs.length;i++){if(mx>30&&mx<270&&my>110+i*80&&my<170+i*80){selEvent=i;beep(350,0.05);return;}}
    if(selEvent>=0){
        for(let i=0;i<shuffledActions.length;i++){
            if(mx>430&&mx<670&&my>110+i*80&&my<170+i*80){
                connections[selEvent]=shuffledActions[i];selEvent=-1;beep(450,0.08);return;
            }
        }
    }
    if(mx>W/2-60&&mx<W/2+60&&my>500&&my<540&&Object.keys(connections).length==curPairs.length){
        let ok=true;
        for(let i=0;i<curPairs.length;i++){if(connections[i]!==i)ok=false;}
        if(ok){feedback='ok';score+=10;beep(523,0.15);addP(W/2,500,'#2ecc71');
            setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1200);
        }else{feedback='no';beep(180,0.3);}
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_ai_ogret_html():
    """Yapay Zekayı Eğit - Örüntü tanıma ve sınıflandırma."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const SETS=[
    {cats:['Hayvan','Arac'],train:[['Kedi','Hayvan'],['Araba','Arac'],['Kopek','Hayvan'],['Ucak','Arac']],test:[['Kus','Hayvan'],['Gemi','Arac']]},
    {cats:['Meyve','Sebze'],train:[['Elma','Meyve'],['Havuc','Sebze'],['Muz','Meyve'],['Biber','Sebze']],test:[['Cilek','Meyve'],['Patates','Sebze']]},
    {cats:['Canli','Cansiz'],train:[['Agac','Canli'],['Tas','Cansiz'],['Cicek','Canli'],['Masa','Cansiz']],test:[['Balik','Canli'],['Kalem','Cansiz']]},
    {cats:['Sicak','Soguk'],train:[['Gunesl','Sicak'],['Buz','Soguk'],['Ates','Sicak'],['Kar','Soguk']],test:[['Cay','Sicak'],['Dondurm','Soguk']]},
    {cats:['Buyuk','Kucuk'],train:[['Fil','Buyuk'],['Karinca','Kucuk'],['Balina','Buyuk'],['Sinekk','Kucuk']],test:[['Zurafa','Buyuk'],['Fare','Kucuk']]},
    {cats:['Hizli','Yavas'],train:[['Citah','Hizli'],['Kaplum','Yavas'],['Roket','Hizli'],['Salyng','Yavas']],test:[['Ucak','Hizli'],['Aslan','Hizli']]},
    {cats:['Yuvarlk','Koseli'],train:[['Top','Yuvarlk'],['Kutu','Koseli'],['Tekerr','Yuvarlk'],['Kitap','Koseli']],test:[['Portakl','Yuvarlk'],['Dolap','Koseli']]},
    {cats:['Dogal','Yapay'],train:[['Deniz','Dogal'],['Bina','Yapay'],['Dag','Dogal'],['Yol','Yapay']],test:[['Orman','Dogal'],['Kopru','Yapay']]},
    {cats:['Sesli','Sessiz'],train:[['Davul','Sesli'],['Yastik','Sessiz'],['Ziil','Sesli'],['Kitap','Sessiz']],test:[['Gitar','Sesli'],['Kumas','Sessiz']]},
    {cats:['Su','Kara'],train:[['Balik','Su'],['Aslan','Kara'],['Yunus','Su'],['Tavsan','Kara']],test:[['Denizat','Su'],['Kedi','Kara']]},
];
let curSet,testIdx,correct,total,feedback;

function genRound(){
    curSet=SETS[(round-1)%SETS.length];testIdx=0;correct=0;total=0;feedback='';
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#a29bfe';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🤖 Yapay Zekayi Egit',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Orneklerden ogrenerek siniflandir!',W/2,260);
        ctx.fillStyle='#a29bfe';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        // Training zone
        ctx.fillStyle='rgba(46,204,113,0.15)';ctx.fillRect(30,60,310,200);
        ctx.fillStyle='#2ecc71';ctx.font='bold 16px Arial';ctx.fillText('EGITIM VERILERI',185,80);
        for(let i=0;i<curSet.train.length;i++){
            let r=Math.floor(i/2),c=i%2;
            ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(50+c*150,95+r*55,130,42,8);ctx.fill();
            ctx.fillStyle='#ecf0f1';ctx.font='bold 14px Arial';ctx.fillText(curSet.train[i][0]+' → '+curSet.train[i][1],115+c*150,120+r*55);
        }
        // Test zone
        if(testIdx<curSet.test.length){
            ctx.fillStyle='rgba(52,152,219,0.15)';ctx.fillRect(360,60,310,200);
            ctx.fillStyle='#3498db';ctx.font='bold 16px Arial';ctx.fillText('TEST',515,80);
            ctx.fillStyle='#f1c40f';ctx.font='bold 28px Arial';
            ctx.fillText(curSet.test[testIdx][0]+' = ?',515,150);
            // Category buttons
            for(let i=0;i<curSet.cats.length;i++){
                ctx.fillStyle=['#e74c3c','#3498db'][i];
                ctx.beginPath();ctx.roundRect(380+i*160,200,140,45,10);ctx.fill();
                ctx.fillStyle='#fff';ctx.font='bold 18px Arial';ctx.fillText(curSet.cats[i],380+i*160+70,226);
            }
        }
        // Accuracy
        ctx.fillStyle='#f39c12';ctx.font='bold 16px Arial';
        let acc=total>0?Math.round(correct/total*100):0;
        ctx.fillText('Dogruluk: '+acc+'% ('+correct+'/'+total+')',W/2,310);
        // Progress bar
        ctx.fillStyle='#34495e';ctx.fillRect(150,325,400,20);
        ctx.fillStyle='#2ecc71';ctx.fillRect(150,325,acc*4,20);
        if(feedback){ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 24px Arial';
            ctx.fillText(feedback=='ok'?'Dogru sinif!':'Yanlis sinif!',W/2,400);}
    }else if(state=='win'){
        ctx.fillStyle='#f1c40f';ctx.font='bold 42px Arial';ctx.textAlign='center';ctx.fillText('🏆 TEBRİKLER!',W/2,250);
        ctx.fillStyle='#ecf0f1';ctx.font='24px Arial';ctx.fillText('Toplam Puan: '+score,W/2,320);
    }
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}});
    particles=particles.filter(p=>p.life>0);
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',e=>{
    const rect=canvas.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';genRound();}return;}
    if(state!='play'||testIdx>=curSet.test.length)return;
    if(feedback){feedback='';return;}
    for(let i=0;i<curSet.cats.length;i++){
        if(mx>380+i*160&&mx<520+i*160&&my>200&&my<245){
            total++;
            let correctCat=curSet.test[testIdx][1];
            if(curSet.cats[i]==correctCat){correct++;feedback='ok';beep(523,0.15);addP(W/2,200,'#2ecc71');}
            else{feedback='no';beep(180,0.3);}
            testIdx++;
            if(testIdx>=curSet.test.length){
                setTimeout(()=>{score+=10;round++;if(round>maxR)state='win';else genRound();},1200);
            }
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""
