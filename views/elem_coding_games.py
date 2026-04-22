"""İlkokul Kodlama Oyunları 1-5."""


def _build_elem_code_komut_sirala_html():
    """Komut Sırala - Komutları doğru sıraya koy, robotu hedefe ulaştır."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const CMDS=['↑ Yukarı','↓ Aşağı','← Sol','→ Sağ'];
const DIR={0:{dx:0,dy:-1},1:{dx:0,dy:1},2:{dx:-1,dy:0},3:{dx:1,dy:0}};
let grid,robotX,robotY,goalX,goalY,cmdSlots,availCmds,correctSeq,animating,animStep,animTimer;
let cmdColors=['#e74c3c','#3498db','#2ecc71','#f39c12','#9b59b6','#1abc9c','#e67e22','#e84393'];

function genRound(){
    grid=[];for(let i=0;i<6;i++){grid[i]=[];for(let j=0;j<6;j++)grid[i][j]=0;}
    robotX=0;robotY=Math.floor(Math.random()*3)+1;
    goalX=5;goalY=Math.floor(Math.random()*3)+1;
    correctSeq=[];
    let cx=robotX,cy=robotY;
    let steps=3+Math.min(round,5);
    for(let s=0;s<steps;s++){
        let possible=[];
        if(cx<5)possible.push(3);
        if(cx>0)possible.push(2);
        if(cy<5)possible.push(1);
        if(cy>0)possible.push(0);
        let d=possible[Math.floor(Math.random()*possible.length)];
        if(cx<goalX&&Math.random()<0.6)d=3;
        correctSeq.push(d);
        cx+=DIR[d].dx;cy+=DIR[d].dy;
    }
    goalX=cx;goalY=cy;
    availCmds=correctSeq.map(c=>({cmd:c,used:false}));
    for(let i=availCmds.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[availCmds[i],availCmds[j]]=[availCmds[j],availCmds[i]];}
    cmdSlots=[];animating=false;animStep=-1;
}

function addParticles(x,y,col){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,col});}

function drawGrid(){
    const gs=55,ox=220,oy=60;
    for(let r=0;r<6;r++)for(let c=0;c<6;c++){
        ctx.fillStyle=(r+c)%2==0?'#2c3e50':'#34495e';
        ctx.fillRect(ox+c*gs,oy+r*gs,gs,gs);
        ctx.strokeStyle='#4a6a8a';ctx.strokeRect(ox+c*gs,oy+r*gs,gs,gs);
    }
    let rx=robotX,ry=robotY;
    if(animating&&animStep>=0){
        for(let i=0;i<=Math.min(animStep,cmdSlots.length-1);i++){
            rx+=DIR[cmdSlots[i]].dx;ry+=DIR[cmdSlots[i]].dy;
        }
    }
    ctx.font='30px Arial';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText('🏁',ox+goalX*gs+gs/2,oy+goalY*gs+gs/2);
    ctx.fillText('🤖',ox+rx*gs+gs/2,oy+ry*gs+gs/2);
}

function drawCmds(){
    ctx.font='bold 14px Arial';ctx.textAlign='center';ctx.textBaseline='middle';
    let ox=50,oy=420;
    ctx.fillStyle='#ecf0f1';ctx.font='bold 16px Arial';
    ctx.fillText('Komutlar:',80,oy-20);
    for(let i=0;i<availCmds.length;i++){
        let ac=availCmds[i];
        ctx.fillStyle=ac.used?'#555':cmdColors[i%cmdColors.length];
        ctx.beginPath();ctx.roundRect(ox+i*95,oy,85,35,8);ctx.fill();
        ctx.fillStyle=ac.used?'#888':'#fff';ctx.font='bold 13px Arial';
        ctx.fillText(CMDS[ac.cmd],ox+i*95+42,oy+18);
    }
    ctx.fillStyle='#ecf0f1';ctx.font='bold 16px Arial';
    ctx.fillText('Sıralama:',80,oy+60);
    for(let i=0;i<correctSeq.length;i++){
        ctx.strokeStyle='#7f8c8d';ctx.lineWidth=2;
        ctx.strokeRect(ox+i*95,oy+75,85,35);
        if(i<cmdSlots.length){
            ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(ox+i*95,oy+75,85,35,8);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 13px Arial';
            ctx.fillText(CMDS[cmdSlots[i]],ox+i*95+42,oy+93);
        }else{
            ctx.fillStyle='#95a5a6';ctx.font='12px Arial';
            ctx.fillText((i+1)+'.',ox+i*95+42,oy+93);
        }
    }
    let btnX=250,btnY=570;
    ctx.fillStyle='#e74c3c';ctx.beginPath();ctx.roundRect(btnX,btnY,90,35,8);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 14px Arial';ctx.fillText('TEMİZLE',btnX+45,btnY+18);
    ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(btnX+110,btnY,90,35,8);ctx.fill();
    ctx.fillStyle='#fff';ctx.fillText('ÇALIŞTIR',btnX+155,btnY+18);
}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#e74c3c';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('📋 Komut Sırala',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Komutları doğru sıraya koyarak robotu hedefe ulaştır!',W/2,260);
        ctx.fillStyle='#e74c3c';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';
        ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
        ctx.textAlign='center';
        drawGrid();drawCmds();
    }else if(state=='win'){
        ctx.fillStyle='#f1c40f';ctx.font='bold 42px Arial';ctx.textAlign='center';
        ctx.fillText('🏆 TEBRİKLER!',W/2,250);
        ctx.fillStyle='#ecf0f1';ctx.font='24px Arial';
        ctx.fillText('Toplam Puan: '+score,W/2,320);
    }
    particles.forEach((p,i)=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;
        if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,3,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}
    });
    particles=particles.filter(p=>p.life>0);
    requestAnimationFrame(draw);
}

canvas.addEventListener('click',e=>{
    const rect=canvas.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';genRound();}return;}
    if(state!='play'||animating)return;
    let ox=50,oy=420;
    for(let i=0;i<availCmds.length;i++){
        if(!availCmds[i].used&&mx>ox+i*95&&mx<ox+i*95+85&&my>oy&&my<oy+35){
            cmdSlots.push(availCmds[i].cmd);availCmds[i].used=true;beep(400+i*50,0.1);return;
        }
    }
    let btnX=250,btnY=570;
    if(mx>btnX&&mx<btnX+90&&my>btnY&&my<btnY+35){
        cmdSlots=[];availCmds.forEach(a=>a.used=false);return;
    }
    if(mx>btnX+110&&mx<btnX+200&&my>btnY&&my<btnY+35&&cmdSlots.length==correctSeq.length){
        animating=true;animStep=-1;
        let ok=true;for(let i=0;i<correctSeq.length;i++)if(cmdSlots[i]!==correctSeq[i])ok=false;
        let rx=robotX,ry=robotY,valid=true;
        for(let i=0;i<cmdSlots.length;i++){
            rx+=DIR[cmdSlots[i]].dx;ry+=DIR[cmdSlots[i]].dy;
            if(rx<0||rx>5||ry<0||ry>5){valid=false;break;}
        }
        let step=0;
        let iv=setInterval(()=>{animStep=step;step++;
            if(step>cmdSlots.length){
                clearInterval(iv);animating=false;
                if(valid&&rx==goalX&&ry==goalY){
                    score+=10;beep(523,0.15);addParticles(W/2,300,'#2ecc71');
                    round++;if(round>maxR)state='win';else genRound();
                }else{beep(180,0.3);cmdSlots=[];availCmds.forEach(a=>a.used=false);}
            }
        },400);
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_dongu_ustasi_html():
    """Döngü Ustası - Döngü kullanarak deseni oluştur."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const SHAPES=['⭐','🔵','🟢','❤️','🔶','🟣','🔺','🟤'];
let targetCount,targetShape,selectedCount,selectedShape,resultShown,resultOk;

function genRound(){
    targetCount=2+Math.floor(Math.random()*6);
    targetShape=SHAPES[Math.floor(Math.random()*SHAPES.length)];
    selectedCount=0;selectedShape='';resultShown=false;resultOk=false;
}

function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#2ecc71';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🔄 Döngü Ustası',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Doğru döngüyü seçerek deseni oluştur!',W/2,260);
        ctx.fillStyle='#2ecc71';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';
        ctx.fillText('Seviye: '+round+'/'+maxR,20,30);ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);
        ctx.textAlign='center';
        ctx.fillStyle='#f39c12';ctx.font='bold 20px Arial';ctx.fillText('Hedef Desen:',W/2,75);
        let tw=targetCount*40;
        ctx.font='28px Arial';
        for(let i=0;i<targetCount;i++) ctx.fillText(targetShape,W/2-tw/2+i*40+20,115);
        ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(50,150,600,80,12);ctx.fill();
        ctx.fillStyle='#ecf0f1';ctx.font='16px Arial';
        ctx.fillText('Tek tek yazmak yerine DÖNGÜ kullan!',W/2,175);
        ctx.fillStyle='#7f8c8d';ctx.font='14px Arial';
        ctx.fillText(targetCount+' kez '+targetShape+' yazmak = '+targetCount+' satır kod... Döngüyle sadece 1 satır!',W/2,205);
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.fillText('Kaç kez tekrarla?',200,270);
        for(let i=0;i<7;i++){
            let n=i+2;
            ctx.fillStyle=selectedCount==n?'#e74c3c':'#3498db';
            ctx.beginPath();ctx.roundRect(80+i*80,285,65,40,8);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 18px Arial';ctx.fillText(n+'',80+i*80+32,307);
        }
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.fillText('Hangi şekli?',200,355);
        for(let i=0;i<SHAPES.length;i++){
            ctx.fillStyle=selectedShape==SHAPES[i]?'#e74c3c':'#34495e';
            ctx.beginPath();ctx.roundRect(60+i*78,370,65,45,8);ctx.fill();
            ctx.font='26px Arial';ctx.fillText(SHAPES[i],60+i*78+32,400);
        }
        if(selectedCount>0&&selectedShape){
            ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(100,440,500,60,12);ctx.fill();
            ctx.fillStyle='#2ecc71';ctx.font='bold 16px Arial';
            ctx.fillText(selectedCount+' kez tekrarla: [ '+selectedShape+' çiz ]',W/2,475);
        }
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(W/2-60,520,120,40,10);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 16px Arial';ctx.fillText('ÇALIŞTIR',W/2,542);
        if(resultShown){
            ctx.fillStyle=resultOk?'rgba(46,204,113,0.3)':'rgba(231,76,60,0.3)';
            ctx.fillRect(0,0,W,H);
            ctx.fillStyle=resultOk?'#2ecc71':'#e74c3c';ctx.font='bold 28px Arial';
            ctx.fillText(resultOk?'✓ Doğru!':'✗ Yanlış, tekrar dene!',W/2,600);
        }
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
    if(resultShown){resultShown=false;return;}
    for(let i=0;i<7;i++){let n=i+2;if(mx>80+i*80&&mx<80+i*80+65&&my>285&&my<325){selectedCount=n;beep(300+i*40,0.1);return;}}
    for(let i=0;i<SHAPES.length;i++){if(mx>60+i*78&&mx<60+i*78+65&&my>370&&my<415){selectedShape=SHAPES[i];beep(400+i*30,0.1);return;}}
    if(mx>W/2-60&&mx<W/2+60&&my>520&&my<560&&selectedCount>0&&selectedShape){
        resultOk=(selectedCount==targetCount&&selectedShape==targetShape);
        resultShown=true;
        if(resultOk){score+=10;beep(523,0.15);addP(W/2,475,'#2ecc71');
            setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},800);
        }else{beep(180,0.3);}
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_kosul_yolu_html():
    """Koşul Kapısı - If/Else koşullarını değerlendir."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const RULES=[
    {text:'Eğer sayı ÇİFT ise → Sol, DEĞİLSE → Sağ',check:v=>v%2==0},
    {text:'Eğer sayı TEK ise → Sol, DEĞİLSE → Sağ',check:v=>v%2!=0},
    {text:'Eğer sayı > 5 ise → Sol, DEĞİLSE → Sağ',check:v=>v>5},
    {text:'Eğer sayı < 10 ise → Sol, DEĞİLSE → Sağ',check:v=>v<10},
    {text:'Eğer sayı 3 ile bölünür ise → Sol, DEĞİLSE → Sağ',check:v=>v%3==0},
    {text:'Eğer sayı >= 7 ise → Sol, DEĞİLSE → Sağ',check:v=>v>=7},
    {text:'Eğer sayı ASAL ise → Sol, DEĞİLSE → Sağ',check:v=>{if(v<2)return false;for(let i=2;i<=Math.sqrt(v);i++)if(v%i==0)return false;return true;}},
    {text:'Eğer sayı 5 ile bölünür ise → Sol, DEĞİLSE → Sağ',check:v=>v%5==0},
    {text:'Eğer sayı <= 4 ise → Sol, DEĞİLSE → Sağ',check:v=>v<=4},
    {text:'Eğer sayı 2 ile bölünür VE > 6 → Sol, DEĞİLSE → Sağ',check:v=>v%2==0&&v>6},
];
let curRule,curValue,correctSide,feedback,feedbackTimer;

function genRound(){
    curRule=RULES[(round-1)%RULES.length];
    curValue=Math.floor(Math.random()*15)+1;
    correctSide=curRule.check(curValue)?'sol':'sag';
    feedback='';feedbackTimer=0;
}
function addP(x,y,c){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#9b59b6';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🚦 Koşul Kapısı',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('If/Else koşullarını değerlendirerek doğru yolu seç!',W/2,260);
        ctx.fillStyle='#9b59b6';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(50,60,600,50,10);ctx.fill();
        ctx.fillStyle='#f39c12';ctx.font='bold 15px Arial';ctx.fillText(curRule.text,W/2,90);
        ctx.fillStyle='#e74c3c';ctx.font='bold 64px Arial';ctx.fillText(curValue,W/2,200);
        ctx.fillStyle='#7f8c8d';ctx.font='16px Arial';ctx.fillText('Bu sayı koşulu sağlıyor mu?',W/2,250);
        // Fork road
        ctx.strokeStyle='#f39c12';ctx.lineWidth=4;
        ctx.beginPath();ctx.moveTo(W/2,280);ctx.lineTo(W/2,320);ctx.stroke();
        ctx.beginPath();ctx.moveTo(W/2,320);ctx.lineTo(200,400);ctx.stroke();
        ctx.beginPath();ctx.moveTo(W/2,320);ctx.lineTo(500,400);ctx.stroke();
        ctx.fillStyle='#2ecc71';ctx.beginPath();ctx.roundRect(130,400,140,60,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Arial';ctx.fillText('← SOL',200,435);
        ctx.fillStyle='#3498db';ctx.beginPath();ctx.roundRect(430,400,140,60,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('SAĞ →',500,435);
        ctx.fillStyle='#95a5a6';ctx.font='14px Arial';
        ctx.fillText('(Koşul DOĞRU)',200,475);ctx.fillText('(Koşul YANLIŞ)',500,475);
        if(feedback){
            ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 28px Arial';
            ctx.fillText(feedback=='ok'?'✓ Doğru!':'✗ Yanlış!',W/2,550);
        }
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
    if(mx>130&&mx<270&&my>400&&my<460){
        let ok=correctSide=='sol';feedback=ok?'ok':'no';
        if(ok){score+=10;beep(523,0.15);addP(200,430,'#2ecc71');}else beep(180,0.3);
        setTimeout(()=>{feedback='';if(correctSide=='sol'&&ok||correctSide!='sol'&&!ok){round++;if(round>maxR)state='win';else genRound();}else genRound();},1000);
    }
    if(mx>430&&mx<570&&my>400&&my<460){
        let ok=correctSide=='sag';feedback=ok?'ok':'no';
        if(ok){score+=10;beep(523,0.15);addP(500,430,'#2ecc71');}else beep(180,0.3);
        setTimeout(()=>{feedback='';round++;if(round>maxR)state='win';else genRound();},1000);
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_hata_bul_html():
    """Bug Avcısı - Koddaki hatayı bul."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const PUZZLES=[
    {lines:['x = 5','y = 3','toplam = x - y','yazdir(toplam)'],bug:2,fix:'toplam = x + y',expect:'Beklenen: 8'},
    {lines:['sayi = 10','sayi = sayi + 5','yazdir(sayi)','# Sonuc: 20'],bug:3,fix:'# Sonuc: 15',expect:'10+5=15, 20 degil'},
    {lines:['a = 4','b = a * 2','c = b + a','yazdir(c)  # 10'],bug:2,fix:'c = b + a  # 12',expect:'8+4=12'},
    {lines:['i = 1','toplam = 0','toplam = toplam + i','i = i + 2'],bug:3,fix:'i = i + 1',expect:'+2 degil +1 artmali'},
    {lines:['fiyat = 100','indirim = 20','son = fiyat + indirim','yazdir(son)'],bug:2,fix:'son = fiyat - indirim',expect:'Indirim cikarilmali'},
    {lines:['liste = [3, 1, 4]','en_buyuk = liste[0]','# en_buyuk: 3','liste.sirala()  # [1,3,4]'],bug:2,fix:'# en_buyuk: 4',expect:'En buyuk 4'},
    {lines:['x = 7','y = x','x = 3','yazdir(y)  # 3'],bug:3,fix:'yazdir(y)  # 7',expect:'y=7 atanmisti'},
    {lines:['n = 6','kare = n * n','yazdir(kare) # 12'],bug:2,fix:'yazdir(kare) # 36',expect:'6*6=36'},
    {lines:['a = "Merhaba"','b = "Dunya"','c = a + b','# c = MerhabaDunya'],bug:2,fix:'c = a + " " + b',expect:'Bosluk lazim'},
    {lines:['x = 15','y = x / 3','yazdir(y) # 3'],bug:2,fix:'yazdir(y) # 5',expect:'15/3=5'},
];
let curPuzzle,foundBug,feedback;

function genRound(){curPuzzle=PUZZLES[(round-1)%PUZZLES.length];foundBug=false;feedback='';}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#e67e22';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🐛 Bug Avcisi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Koddaki hatayi bul ve tikla!',W/2,260);
        ctx.fillStyle='#e67e22';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#f39c12';ctx.font='bold 20px Arial';ctx.fillText('Hatali satiri bul ve tikla!',W/2,75);
        ctx.fillStyle='#95a5a6';ctx.font='14px Arial';ctx.fillText(curPuzzle.expect,W/2,100);
        // Code editor
        let codeX=100,codeY=130,lineH=55;
        ctx.fillStyle='#1e272e';ctx.beginPath();ctx.roundRect(codeX-20,codeY-10,540,curPuzzle.lines.length*lineH+20,12);ctx.fill();
        ctx.font='bold 18px Courier New';
        for(let i=0;i<curPuzzle.lines.length;i++){
            let ly=codeY+i*lineH;
            if(foundBug&&i==curPuzzle.bug){
                ctx.fillStyle='rgba(46,204,113,0.3)';ctx.fillRect(codeX-10,ly-5,520,lineH-5);
                ctx.fillStyle='#2ecc71';
            }else{
                ctx.fillStyle='rgba(44,62,80,0.5)';ctx.fillRect(codeX-10,ly-5,520,lineH-5);
                ctx.fillStyle='#ecf0f1';
            }
            ctx.textAlign='left';
            ctx.fillStyle='#7f8c8d';ctx.fillText((i+1)+'.',codeX,ly+18);
            ctx.fillStyle=foundBug&&i==curPuzzle.bug?'#2ecc71':'#ecf0f1';
            ctx.fillText(curPuzzle.lines[i],codeX+40,ly+18);
            if(foundBug&&i==curPuzzle.bug){
                ctx.fillStyle='#27ae60';ctx.font='bold 14px Arial';
                ctx.fillText('Dogru: '+curPuzzle.fix,codeX+40,ly+40);
                ctx.font='bold 18px Courier New';
            }
        }
        if(feedback){
            ctx.textAlign='center';ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 24px Arial';
            ctx.fillText(feedback=='ok'?'Hatayi buldun!':'Yanlis satir, tekrar dene!',W/2,codeY+curPuzzle.lines.length*lineH+50);
        }
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
    if(state!='play'||foundBug)return;
    let codeX=100,codeY=130,lineH=55;
    for(let i=0;i<curPuzzle.lines.length;i++){
        let ly=codeY+i*lineH;
        if(mx>codeX-10&&mx<codeX+510&&my>ly-5&&my<ly+lineH-5){
            if(i==curPuzzle.bug){
                foundBug=true;feedback='ok';score+=10;beep(523,0.15);addP(W/2,ly+20,'#2ecc71');
                setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1500);
            }else{feedback='no';beep(180,0.3);setTimeout(()=>{feedback='';},1000);}
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_robot_yonlendir_html():
    """Robot Yönlendir - Komut dizisiyle robotu hedefe götür."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const GS=6,CS=65;
let grid,robotX,robotY,goalX,goalY,cmds,animating,animIdx,animRX,animRY;
const DX=[0,0,-1,1],DY=[-1,1,0,0],ARROWS=['↑','↓','←','→'];

function genMaze(){
    grid=[];for(let r=0;r<GS;r++){grid[r]=[];for(let c=0;c<GS;c++)grid[r][c]=0;}
    robotX=0;robotY=0;
    goalX=GS-1;goalY=GS-1;
    let walls=2+Math.min(round,6);
    for(let w=0;w<walls;w++){
        let wx,wy;
        do{wx=Math.floor(Math.random()*GS);wy=Math.floor(Math.random()*GS);}
        while((wx==0&&wy==0)||(wx==goalX&&wy==goalY));
        grid[wy][wx]=1;
    }
    cmds=[];animating=false;animIdx=-1;
}

function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}
const OX=175,OY=50;

function drawGrid(){
    for(let r=0;r<GS;r++)for(let c=0;c<GS;c++){
        ctx.fillStyle=grid[r][c]==1?'#e74c3c':(r+c)%2==0?'#2c3e50':'#34495e';
        ctx.fillRect(OX+c*CS,OY+r*CS,CS,CS);
        ctx.strokeStyle='#4a6a8a';ctx.strokeRect(OX+c*CS,OY+r*CS,CS,CS);
    }
    let rx=animating?animRX:robotX,ry=animating?animRY:robotY;
    ctx.font='35px Arial';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText('🏁',OX+goalX*CS+CS/2,OY+goalY*CS+CS/2);
    ctx.fillText('🤖',OX+rx*CS+CS/2,OY+ry*CS+CS/2);
}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#1abc9c';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🤖 Robot Yönlendir',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Komutlarla robotu hedefe ulaştır!',W/2,260);
        ctx.fillStyle='#1abc9c';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.textBaseline='middle';
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,25);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,25);ctx.textAlign='center';
        drawGrid();
        // Command queue
        let qy=OY+GS*CS+15;
        ctx.fillStyle='#ecf0f1';ctx.font='bold 14px Arial';ctx.fillText('Komut Dizisi (maks 10):',W/2,qy);
        for(let i=0;i<10;i++){
            ctx.strokeStyle=i<cmds.length?'#2ecc71':'#555';ctx.lineWidth=2;
            ctx.strokeRect(120+i*48,qy+10,42,30);
            if(i<cmds.length){ctx.fillStyle='#2ecc71';ctx.font='20px Arial';ctx.fillText(ARROWS[cmds[i]],120+i*48+21,qy+27);}
        }
        // Arrow buttons
        let by=qy+55;
        let arrowCols=['#3498db','#e74c3c','#f39c12','#2ecc71'];
        for(let i=0;i<4;i++){
            ctx.fillStyle=arrowCols[i];ctx.beginPath();ctx.roundRect(180+i*90,by,75,45,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 24px Arial';ctx.fillText(ARROWS[i],180+i*90+37,by+24);
        }
        // Control buttons
        let cy=by+60;
        ctx.fillStyle='#e74c3c';ctx.beginPath();ctx.roundRect(150,cy,80,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 14px Arial';ctx.fillText('SİL',190,cy+18);
        ctx.fillStyle='#e67e22';ctx.beginPath();ctx.roundRect(250,cy,100,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('TEMİZLE',300,cy+18);
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(370,cy,110,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('ÇALIŞTIR',425,cy+18);
    }else if(state=='win'){
        ctx.textBaseline='middle';
        ctx.fillStyle='#f1c40f';ctx.font='bold 42px Arial';ctx.textAlign='center';ctx.fillText('🏆 TEBRİKLER!',W/2,250);
        ctx.fillStyle='#ecf0f1';ctx.font='24px Arial';ctx.fillText('Toplam Puan: '+score,W/2,320);
    }
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;if(p.life>0){ctx.globalAlpha=p.life;ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}});
    particles=particles.filter(p=>p.life>0);
    requestAnimationFrame(draw);
}

function runCmds(){
    animating=true;animIdx=0;animRX=robotX;animRY=robotY;
    let iv=setInterval(()=>{
        if(animIdx>=cmds.length){clearInterval(iv);animating=false;
            if(animRX==goalX&&animRY==goalY){score+=10;beep(523,0.15);addP(OX+goalX*CS+CS/2,OY+goalY*CS+CS/2,'#2ecc71');round++;if(round>maxR)state='win';else genMaze();}
            else{beep(180,0.3);cmds=[];}
            return;
        }
        let nx=animRX+DX[cmds[animIdx]],ny=animRY+DY[cmds[animIdx]];
        if(nx<0||nx>=GS||ny<0||ny>=GS||grid[ny][nx]==1){clearInterval(iv);animating=false;beep(180,0.3);cmds=[];return;}
        animRX=nx;animRY=ny;animIdx++;
    },350);
}

canvas.addEventListener('click',e=>{
    const rect=canvas.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(W/rect.width),my=(e.clientY-rect.top)*(H/rect.height);
    if(state=='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';genMaze();}return;}
    if(state!='play'||animating)return;
    let qy=OY+GS*CS+15,by=qy+55,cy=by+60;
    for(let i=0;i<4;i++){if(mx>180+i*90&&mx<180+i*90+75&&my>by&&my<by+45&&cmds.length<10){cmds.push(i);beep(350+i*50,0.1);return;}}
    if(mx>150&&mx<230&&my>cy&&my<cy+35&&cmds.length>0){cmds.pop();return;}
    if(mx>250&&mx<350&&my>cy&&my<cy+35){cmds=[];return;}
    if(mx>370&&mx<480&&my>cy&&my<cy+35&&cmds.length>0){runCmds();}
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""
