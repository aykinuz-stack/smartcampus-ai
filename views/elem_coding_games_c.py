"""İlkokul Kodlama Oyunları 11-15."""


def _build_elem_code_fonksiyon_html():
    """Fonksiyon Fabrikası - Doğru fonksiyon çağrısını seç."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const QS=[
    {task:'3 kez yildiz ciz',ans:0,opts:['yildizCiz(3)','kareCiz(3)','yildizCiz(5)','cizgiCiz(3)']},
    {task:'5 kez kare ciz',ans:1,opts:['kareCiz(3)','kareCiz(5)','daireCiz(5)','kareCiz(1)']},
    {task:'2 kez daire ciz',ans:2,opts:['daireCiz(5)','kareCiz(2)','daireCiz(2)','yildizCiz(2)']},
    {task:'4 kez ucgen ciz',ans:0,opts:['ucgenCiz(4)','ucgenCiz(3)','kareCiz(4)','daireCiz(4)']},
    {task:'Sayiyi 2 ile carp',ans:1,opts:['topla(2)','carp(2)','bol(2)','cikar(2)']},
    {task:'Metni buyuk harfe cevir',ans:0,opts:['buyukHarf(metin)','kucukHarf(metin)','terstenYaz(metin)','sil(metin)']},
    {task:'Listeyi sirala',ans:2,opts:['listeBol()','listeEkle()','listeSirala()','listeSil()']},
    {task:'Ekrana mesaj yaz',ans:0,opts:['yazdir("Merhaba")','oku("Merhaba")','sil("Merhaba")','hesapla("Merhaba")']},
    {task:'7 kez tekrarla',ans:1,opts:['tekrarla(5)','tekrarla(7)','tekrarla(3)','tekrarla(10)']},
    {task:'Sayinin karesini hesapla',ans:0,opts:['kareAl(sayi)','kokAl(sayi)','topla(sayi)','carp(sayi)']},
];
let curQ,feedback,selOpt;

function genRound(){curQ=QS[(round-1)%QS.length];feedback='';selOpt=-1;}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#e67e22';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🏭 Fonksiyon Fabrikasi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Dogru fonksiyon cagrisini sec!',W/2,260);
        ctx.fillStyle='#e67e22';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        // Factory visual
        ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(100,80,500,100,12);ctx.fill();
        ctx.fillStyle='#f39c12';ctx.font='bold 22px Arial';ctx.fillText('Gorev: '+curQ.task,W/2,120);
        ctx.fillStyle='#95a5a6';ctx.font='14px Arial';ctx.fillText('Hangi fonksiyon bu gorevi yapar?',W/2,155);
        // Options
        for(let i=0;i<4;i++){
            let bx=100,by=220+i*70;
            ctx.fillStyle=selOpt==i?(feedback=='ok'?'#27ae60':'#e74c3c'):'#34495e';
            ctx.beginPath();ctx.roundRect(bx,by,500,55,10);ctx.fill();
            ctx.fillStyle='#2ecc71';ctx.font='bold 20px Courier New';ctx.fillText(curQ.opts[i],W/2,by+32);
        }
        if(feedback){
            ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 24px Arial';
            ctx.fillText(feedback=='ok'?'Dogru fonksiyon!':'Yanlis, tekrar dene!',W/2,550);
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
    for(let i=0;i<4;i++){
        if(mx>100&&mx<600&&my>220+i*70&&my<275+i*70){
            selOpt=i;
            if(i==curQ.ans){feedback='ok';score+=10;beep(523,0.15);addP(W/2,250+i*70,'#2ecc71');
                setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1000);
            }else{feedback='no';beep(180,0.3);setTimeout(()=>{feedback='';selOpt=-1;},1000);}
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_dizi_html():
    """Dizi Macerası - Dizi elemanları hakkında soruları cevapla."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

let arr,question,answer,opts,feedback,selOpt;

function genRound(){
    let n=4+Math.min(round,3);
    arr=[];for(let i=0;i<n;i++)arr.push(Math.floor(Math.random()*20)+1);
    let qtype=Math.floor(Math.random()*5);
    if(qtype==0){let idx=Math.floor(Math.random()*n)+1;question=idx+'. eleman nedir?';answer=arr[idx-1];}
    else if(qtype==1){question='En buyuk eleman?';answer=Math.max(...arr);}
    else if(qtype==2){question='En kucuk eleman?';answer=Math.min(...arr);}
    else if(qtype==3){question='Elemanlarin toplami?';answer=arr.reduce((a,b)=>a+b,0);}
    else{question='Kac eleman var?';answer=arr.length;}
    opts=[answer];
    while(opts.length<4){let o=answer+Math.floor(Math.random()*10)-5;if(o!=answer&&o>0&&!opts.includes(o))opts.push(o);}
    for(let i=opts.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[opts[i],opts[j]]=[opts[j],opts[i]];}
    feedback='';selOpt=-1;
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#00cec9';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('📋 Dizi Macerasi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Dizi elemanlari hakkinda sorulari cevapla!',W/2,260);
        ctx.fillStyle='#00cec9';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        // Array visual
        let bw=Math.min(70,550/arr.length),ox=(W-bw*arr.length)/2;
        let COLS=['#e74c3c','#3498db','#2ecc71','#f1c40f','#9b59b6','#e67e22','#1abc9c','#e84393'];
        for(let i=0;i<arr.length;i++){
            ctx.fillStyle=COLS[i%COLS.length];ctx.beginPath();ctx.roundRect(ox+i*bw+3,100,bw-6,60,8);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 22px Arial';ctx.fillText(arr[i],ox+i*bw+bw/2,135);
            ctx.fillStyle='#95a5a6';ctx.font='12px Arial';ctx.fillText('['+(i+1)+']',ox+i*bw+bw/2,180);
        }
        ctx.fillStyle='#f1c40f';ctx.font='bold 22px Arial';ctx.fillText(question,W/2,240);
        for(let i=0;i<4;i++){
            ctx.fillStyle=selOpt==i?(feedback=='ok'?'#27ae60':'#e74c3c'):'#34495e';
            ctx.beginPath();ctx.roundRect(120+i*130,280,110,50,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 22px Arial';ctx.fillText(opts[i],120+i*130+55,310);
        }
        if(feedback){
            ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 24px Arial';
            ctx.fillText(feedback=='ok'?'Dogru!':'Yanlis!',W/2,400);
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
    for(let i=0;i<4;i++){
        if(mx>120+i*130&&mx<230+i*130&&my>280&&my<330){
            selOpt=i;
            if(opts[i]==answer){feedback='ok';score+=10;beep(523,0.15);addP(W/2,310,'#2ecc71');
                setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1000);
            }else{feedback='no';beep(180,0.3);setTimeout(()=>{feedback='';selOpt=-1;},1000);}
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_animasyon_html():
    """Animasyon Kodla - Parametreleri seçerek hedef animasyonu oluştur."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const OBJS=['Top','Yildiz','Kare'];
const MOVES=['Ziplama','Kayma','Dolanma'];
const SPEEDS=['Yavas','Normal','Hizli'];
const COLS=['#e74c3c','#3498db','#2ecc71','#f1c40f'];
let targetObj,targetMove,targetSpeed,targetCol;
let selObj,selMove,selSpeed,selCol,feedback,animT;

function genRound(){
    targetObj=Math.floor(Math.random()*3);targetMove=Math.floor(Math.random()*3);
    targetSpeed=Math.floor(Math.random()*3);targetCol=Math.floor(Math.random()*4);
    selObj=-1;selMove=-1;selSpeed=-1;selCol=-1;feedback='';animT=0;
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function drawObj(x,y,obj,col,t,move,spd){
    let sp=[1,2,3.5][spd];
    let px=x,py=y;
    if(move==0)py=y-Math.abs(Math.sin(t*sp*0.05))*30;
    else if(move==1)px=x+Math.sin(t*sp*0.03)*40;
    else{px=x+Math.cos(t*sp*0.04)*25;py=y+Math.sin(t*sp*0.04)*25;}
    ctx.fillStyle=COLS[col];
    if(obj==0){ctx.beginPath();ctx.arc(px,py,15,0,Math.PI*2);ctx.fill();}
    else if(obj==1){ctx.font='28px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('⭐',px,py);}
    else{ctx.fillRect(px-12,py-12,24,24);}
}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    animT++;
    if(state=='start'){
        ctx.fillStyle='#fd79a8';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🎬 Animasyon Kodla',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Parametreleri secerek hedef animasyonu olustur!',W/2,260);
        ctx.fillStyle='#fd79a8';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.textBaseline='middle';
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,25);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,25);ctx.textAlign='center';
        // Target animation
        ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(50,50,280,120,10);ctx.fill();
        ctx.fillStyle='#f39c12';ctx.font='bold 14px Arial';ctx.fillText('Hedef:',190,65);
        drawObj(190,120,targetObj,targetCol,animT,targetMove,targetSpeed);
        // Player animation
        ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(370,50,280,120,10);ctx.fill();
        ctx.fillStyle='#3498db';ctx.font='bold 14px Arial';ctx.fillText('Senin:',510,65);
        if(selObj>=0&&selMove>=0&&selSpeed>=0&&selCol>=0)drawObj(510,120,selObj,selCol,animT,selMove,selSpeed);
        // Controls
        let cy=200;
        ctx.fillStyle='#ecf0f1';ctx.font='bold 15px Arial';
        ctx.fillText('Nesne:',100,cy);
        for(let i=0;i<3;i++){ctx.fillStyle=selObj==i?'#e74c3c':'#34495e';ctx.beginPath();ctx.roundRect(160+i*100,cy-15,90,30,6);ctx.fill();ctx.fillStyle='#fff';ctx.font='13px Arial';ctx.fillText(OBJS[i],205+i*100,cy);}
        cy+=50;ctx.fillStyle='#ecf0f1';ctx.font='bold 15px Arial';ctx.fillText('Hareket:',100,cy);
        for(let i=0;i<3;i++){ctx.fillStyle=selMove==i?'#e74c3c':'#34495e';ctx.beginPath();ctx.roundRect(160+i*100,cy-15,90,30,6);ctx.fill();ctx.fillStyle='#fff';ctx.font='13px Arial';ctx.fillText(MOVES[i],205+i*100,cy);}
        cy+=50;ctx.fillStyle='#ecf0f1';ctx.font='bold 15px Arial';ctx.fillText('Hiz:',100,cy);
        for(let i=0;i<3;i++){ctx.fillStyle=selSpeed==i?'#e74c3c':'#34495e';ctx.beginPath();ctx.roundRect(160+i*100,cy-15,90,30,6);ctx.fill();ctx.fillStyle='#fff';ctx.font='13px Arial';ctx.fillText(SPEEDS[i],205+i*100,cy);}
        cy+=50;ctx.fillStyle='#ecf0f1';ctx.font='bold 15px Arial';ctx.fillText('Renk:',100,cy);
        for(let i=0;i<4;i++){ctx.fillStyle=COLS[i];ctx.beginPath();ctx.arc(180+i*80,cy,15,0,Math.PI*2);ctx.fill();if(selCol==i){ctx.strokeStyle='#fff';ctx.lineWidth=3;ctx.stroke();ctx.lineWidth=1;}}
        // Check button
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(W/2-60,cy+40,120,40,10);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 16px Arial';ctx.fillText('KONTROL',W/2,cy+62);
        if(feedback){ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 22px Arial';ctx.fillText(feedback=='ok'?'Eslesme!':'Uyusmuyor!',W/2,cy+110);}
    }else if(state=='win'){
        ctx.textBaseline='middle';
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
    if(feedback){feedback='';return;}
    let cy=200;
    for(let i=0;i<3;i++)if(mx>160+i*100&&mx<250+i*100&&my>cy-15&&my<cy+15){selObj=i;beep(400,0.05);return;}
    cy+=50;for(let i=0;i<3;i++)if(mx>160+i*100&&mx<250+i*100&&my>cy-15&&my<cy+15){selMove=i;beep(400,0.05);return;}
    cy+=50;for(let i=0;i<3;i++)if(mx>160+i*100&&mx<250+i*100&&my>cy-15&&my<cy+15){selSpeed=i;beep(400,0.05);return;}
    cy+=50;for(let i=0;i<4;i++){let dx=mx-(180+i*80),dy=my-cy;if(dx*dx+dy*dy<225){selCol=i;beep(400,0.05);return;}}
    if(mx>W/2-60&&mx<W/2+60&&my>cy+40&&my<cy+80){
        if(selObj==targetObj&&selMove==targetMove&&selSpeed==targetSpeed&&selCol==targetCol){
            feedback='ok';score+=10;beep(523,0.15);addP(W/2,cy+60,'#2ecc71');
            setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1000);
        }else{feedback='no';beep(180,0.3);}
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_sifreleme_html():
    """Şifreleme Ustası - Caesar cipher ile şifre çöz."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const ALPHA='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const WORDS=['KALEM','OKUL','KITAP','SINIF','MASA','DEFTER','SILGI','TAHTA','ODEV','BILGI','OYUN','RENK','GUNES','YILDIZ','DENIZ'];
let word,key,encrypted,userInput,feedback;

function encrypt(w,k){let r='';for(let c of w){let i=ALPHA.indexOf(c);r+=i>=0?ALPHA[(i+k)%26]:c;}return r;}
function genRound(){
    word=WORDS[Math.floor(Math.random()*WORDS.length)];
    key=1+Math.floor(Math.random()*5);
    encrypted=encrypt(word,key);
    userInput='';feedback='';
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#6c5ce7';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🔐 Sifreleme Ustasi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Caesar sifresiyle gizli kelimeyi coz!',W/2,260);
        ctx.fillStyle='#6c5ce7';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#f39c12';ctx.font='bold 18px Arial';
        ctx.fillText('Anahtar: -'+key+' (her harfi '+key+' geri kaydir)',W/2,70);
        ctx.fillStyle='#e74c3c';ctx.font='bold 32px Courier New';ctx.fillText('Sifre: '+encrypted,W/2,120);
        // Alphabet reference
        ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(30,145,640,35,6);ctx.fill();
        ctx.font='bold 13px Courier New';ctx.fillStyle='#95a5a6';
        for(let i=0;i<26;i++)ctx.fillText(ALPHA[i],50+i*24,167);
        // User input display
        ctx.fillStyle='#2ecc71';ctx.font='bold 32px Courier New';
        ctx.fillText('Cozum: '+(userInput||'_'.repeat(word.length)),W/2,220);
        // Letter buttons (2 rows)
        for(let i=0;i<26;i++){
            let row=i<13?0:1;let col=i<13?i:i-13;
            let bx=75+col*45,by=260+row*50;
            ctx.fillStyle='#34495e';ctx.beginPath();ctx.roundRect(bx,by,40,40,6);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 16px Arial';ctx.fillText(ALPHA[i],bx+20,by+22);
        }
        // Controls
        ctx.fillStyle='#e74c3c';ctx.beginPath();ctx.roundRect(200,380,100,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 14px Arial';ctx.fillText('SIL',250,400);
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(400,380,100,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('KONTROL',450,400);
        if(feedback){ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 24px Arial';
            ctx.fillText(feedback=='ok'?'Cozuldu!':'Yanlis!',W/2,460);}
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
    if(state!='play'||feedback=='ok')return;
    if(feedback){feedback='';return;}
    for(let i=0;i<26;i++){
        let row=i<13?0:1;let col=i<13?i:i-13;
        let bx=75+col*45,by=260+row*50;
        if(mx>bx&&mx<bx+40&&my>by&&my<by+40&&userInput.length<word.length){
            userInput+=ALPHA[i];beep(350+i*10,0.05);return;
        }
    }
    if(mx>200&&mx<300&&my>380&&my<415&&userInput.length>0){userInput=userInput.slice(0,-1);return;}
    if(mx>400&&mx<500&&my>380&&my<415&&userInput.length==word.length){
        if(userInput==word){feedback='ok';score+=10;beep(523,0.15);addP(W/2,220,'#2ecc71');
            setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1000);
        }else{feedback='no';beep(180,0.3);setTimeout(()=>{userInput='';feedback='';},1200);}
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_oyun_tasarla_html():
    """Mini Oyun Tasarlacısı - Kuralları seçerek oyun tasarla."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const QS=[
    {q:'Karakter zipliyorsa ve engel duvarse, ne olur?',ans:0,opts:['Duvardan atlar','Duvari kirar','Durur','Ucar']},
    {q:'Hiz=Hizli, Engel=Yavas hareket ediyor. Zor mu?',ans:1,opts:['Cok zor','Kolay','Imkansiz','Normal']},
    {q:'Kazanma kosulu "5 yildiz topla". 3 yildiz varsa?',ans:2,opts:['Kazanir','Kaybeder','Devam eder','Biter']},
    {q:'Karakter ucabiliyor, engel yerde. Zorluk?',ans:0,opts:['Cok kolay','Cok zor','Normal','Imkansiz']},
    {q:'2 oyuncu + isbirligi gerekiyor. Tek oynarsan?',ans:1,opts:['Kazanirsin','Kazanamazsin','Hizli biter','Fark etmez']},
    {q:'Zamanlayici 5sn, 10 gorev var. Yetisir mi?',ans:1,opts:['Rahat yetisir','Yetismez','Belki','Kesinlikle']},
    {q:'Can=3, her engel 1 can alir. 4 engelle ne olur?',ans:0,opts:['Kaybedersin','Kazanirsin','3 can kalir','5 can olur']},
    {q:'Level 1 yavas, Level 2 hizli. Ne degisti?',ans:2,opts:['Engeller','Karakter','Hiz','Puan']},
    {q:'Puan sistemi: Yildiz=10, Elmas=50. 3 elmas kac puan?',ans:0,opts:['150','30','50','100']},
    {q:'Random engel + sabit harita. Her oyun ayni mi?',ans:1,opts:['Evet ayni','Hayir farkli','Belki','Belli olmaz']},
];
let curQ,feedback,selOpt;

function genRound(){curQ=QS[(round-1)%QS.length];feedback='';selOpt=-1;}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#00b894';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🎮 Oyun Tasarlacisi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Oyun tasarim kurallarini degerlendir!',W/2,260);
        ctx.fillStyle='#00b894';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#2c3e50';ctx.beginPath();ctx.roundRect(50,70,600,80,12);ctx.fill();
        ctx.fillStyle='#f1c40f';ctx.font='bold 18px Arial';ctx.fillText(curQ.q,W/2,115);
        for(let i=0;i<4;i++){
            ctx.fillStyle=selOpt==i?(feedback=='ok'?'#27ae60':'#e74c3c'):'#34495e';
            ctx.beginPath();ctx.roundRect(100,190+i*70,500,55,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 18px Arial';ctx.fillText(curQ.opts[i],W/2,222+i*70);
        }
        if(feedback){ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 24px Arial';
            ctx.fillText(feedback=='ok'?'Dogru dusundun!':'Tekrar dusun!',W/2,510);}
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
    for(let i=0;i<4;i++){
        if(mx>100&&mx<600&&my>190+i*70&&my<245+i*70){
            selOpt=i;
            if(i==curQ.ans){feedback='ok';score+=10;beep(523,0.15);addP(W/2,220+i*70,'#2ecc71');
                setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1000);
            }else{feedback='no';beep(180,0.3);setTimeout(()=>{feedback='';selOpt=-1;},1000);}
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""
