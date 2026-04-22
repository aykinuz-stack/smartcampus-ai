"""İlkokul Kodlama Oyunları 6-10."""


def _build_elem_code_pixel_boyama_html():
    """Piksel Sanatçısı - Hedef deseni piksel piksel boyayarak oluştur."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const COLORS=['#e74c3c','#3498db','#2ecc71','#f1c40f','#2c3e50','#ecf0f1'];
const CNAMES=['Kirmizi','Mavi','Yesil','Sari','Siyah','Beyaz'];
const PATTERNS=[
    [[0,0,0,0,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,0,0,0,0]],// cross
    [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]],// X
    [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],// O
    [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,0,0],[1,0,0,0,0],[1,1,1,1,1]],// E
    [[0,0,1,0,0],[0,1,0,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,0,1,0,0]],// diamond
    [[1,0,1,0,1],[0,1,0,1,0],[1,0,1,0,1],[0,1,0,1,0],[1,0,1,0,1]],// checkers
    [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],// T
    [[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]],// star
    [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1]],// M
    [[0,1,1,0,0],[0,1,0,1,0],[0,1,1,0,0],[0,1,0,1,0],[0,1,1,0,0]],// B
];
let target,player,selColor,patColor;
const GS=5,CS=50;

function genRound(){
    let pi=(round-1)%PATTERNS.length;
    target=PATTERNS[pi];
    patColor=Math.floor(Math.random()*4);
    player=[];for(let r=0;r<GS;r++){player[r]=[];for(let c=0;c<GS;c++)player[r][c]=-1;}
    selColor=patColor;
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#e84393';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('🎨 Piksel Sanatcisi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Hedef deseni piksel piksel boya!',W/2,260);
        ctx.fillStyle='#e84393';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        // Target
        ctx.fillStyle='#f39c12';ctx.font='bold 16px Arial';ctx.fillText('Hedef:',165,65);
        let tx=90,ty=80;
        for(let r=0;r<GS;r++)for(let c=0;c<GS;c++){
            ctx.fillStyle=target[r][c]==1?COLORS[patColor]:'#34495e';
            ctx.fillRect(tx+c*30,ty+r*30,28,28);
        }
        // Player grid
        ctx.fillStyle='#2ecc71';ctx.font='bold 16px Arial';ctx.fillText('Senin:',520,65);
        let px=395,py=80;
        for(let r=0;r<GS;r++)for(let c=0;c<GS;c++){
            ctx.fillStyle=player[r][c]>=0?COLORS[player[r][c]]:'#34495e';
            ctx.fillRect(px+c*CS,py+r*CS,CS-2,CS-2);
            ctx.strokeStyle='#4a6a8a';ctx.strokeRect(px+c*CS,py+r*CS,CS-2,CS-2);
        }
        // Color palette
        let cy=380;
        ctx.fillStyle='#ecf0f1';ctx.font='bold 16px Arial';ctx.fillText('Renk Sec:',W/2,cy-10);
        for(let i=0;i<COLORS.length;i++){
            ctx.fillStyle=COLORS[i];ctx.beginPath();ctx.roundRect(120+i*80,cy,65,40,8);ctx.fill();
            if(i==selColor){ctx.strokeStyle='#f1c40f';ctx.lineWidth=3;ctx.strokeRect(118+i*80,cy-2,69,44);ctx.lineWidth=1;}
            ctx.fillStyle='#fff';ctx.font='11px Arial';ctx.fillText(CNAMES[i],120+i*80+32,cy+55);
        }
        // Buttons
        ctx.fillStyle='#e74c3c';ctx.beginPath();ctx.roundRect(200,470,120,40,10);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 15px Arial';ctx.fillText('TEMİZLE',260,492);
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(380,470,120,40,10);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('KONTROL',440,492);
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
    let px=395,py=80;
    for(let r=0;r<GS;r++)for(let c=0;c<GS;c++){
        if(mx>px+c*CS&&mx<px+c*CS+CS-2&&my>py+r*CS&&my<py+r*CS+CS-2){
            player[r][c]=player[r][c]==selColor?-1:selColor;beep(400,0.05);return;
        }
    }
    for(let i=0;i<COLORS.length;i++){if(mx>120+i*80&&mx<120+i*80+65&&my>380&&my<420){selColor=i;return;}}
    if(mx>200&&mx<320&&my>470&&my<510){for(let r=0;r<GS;r++)for(let c=0;c<GS;c++)player[r][c]=-1;return;}
    if(mx>380&&mx<500&&my>470&&my<510){
        let ok=true;
        for(let r=0;r<GS;r++)for(let c=0;c<GS;c++){
            if(target[r][c]==1&&player[r][c]!=patColor)ok=false;
            if(target[r][c]==0&&player[r][c]>=0)ok=false;
        }
        if(ok){score+=10;beep(523,0.15);addP(W/2,400,'#2ecc71');round++;if(round>maxR)state='win';else genRound();}
        else beep(180,0.3);
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_degisken_kutusu_html():
    """Değişken Kutusu - Değişkenlerin değerlerini takip et."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const PROBS=[
    {steps:['x = 3','y = 5','sonuc = x + y'],q:'sonuc = ?',ans:8,opts:[6,7,8,15]},
    {steps:['a = 10','b = 4','c = a - b'],q:'c = ?',ans:6,opts:[6,14,40,4]},
    {steps:['n = 7','n = n + 3'],q:'n = ?',ans:10,opts:[7,3,10,21]},
    {steps:['x = 2','x = x * 4'],q:'x = ?',ans:8,opts:[6,8,2,4]},
    {steps:['a = 12','b = a / 3'],q:'b = ?',ans:4,opts:[3,4,9,36]},
    {steps:['x = 5','y = x','x = 10'],q:'y = ?',ans:5,opts:[5,10,15,0]},
    {steps:['a = 3','b = 4','c = a * b + 1'],q:'c = ?',ans:13,opts:[12,13,7,8]},
    {steps:['n = 20','n = n - 8','n = n / 2'],q:'n = ?',ans:6,opts:[4,6,8,12]},
    {steps:['x = 1','x = x + x','x = x + x'],q:'x = ?',ans:4,opts:[2,3,4,8]},
    {steps:['a = 9','b = 2','c = a % b'],q:'c = ? (kalan)',ans:1,opts:[0,1,4,2]},
];
let curProb,feedback,selOpt;

function genRound(){curProb=PROBS[(round-1)%PROBS.length];feedback='';selOpt=-1;}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#3498db';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('📦 Degisken Kutusu',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Degiskenlerin degerlerini takip et!',W/2,260);
        ctx.fillStyle='#3498db';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#1e272e';ctx.beginPath();ctx.roundRect(100,70,500,curProb.steps.length*50+20,12);ctx.fill();
        ctx.font='bold 20px Courier New';ctx.textAlign='left';
        for(let i=0;i<curProb.steps.length;i++){
            ctx.fillStyle='#7f8c8d';ctx.fillText((i+1)+'.',120,105+i*50);
            ctx.fillStyle='#2ecc71';ctx.fillText(curProb.steps[i],160,105+i*50);
        }
        let qy=100+curProb.steps.length*50+40;
        ctx.textAlign='center';ctx.fillStyle='#f1c40f';ctx.font='bold 24px Arial';
        ctx.fillText(curProb.q,W/2,qy);
        for(let i=0;i<4;i++){
            ctx.fillStyle=selOpt==i?(feedback=='ok'?'#27ae60':'#e74c3c'):'#34495e';
            ctx.beginPath();ctx.roundRect(100+i*140,qy+30,120,50,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 22px Arial';ctx.fillText(curProb.opts[i],100+i*140+60,qy+58);
        }
        if(feedback){
            ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 22px Arial';
            ctx.fillText(feedback=='ok'?'Dogru!':'Yanlis!',W/2,qy+120);
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
    let qy=100+curProb.steps.length*50+40;
    for(let i=0;i<4;i++){
        if(mx>100+i*140&&mx<100+i*140+120&&my>qy+30&&my<qy+80){
            selOpt=i;
            if(curProb.opts[i]==curProb.ans){feedback='ok';score+=10;beep(523,0.15);addP(W/2,qy+60,'#2ecc71');
                setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1000);
            }else{feedback='no';beep(180,0.3);setTimeout(()=>{feedback='';selOpt=-1;},1000);}
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_siralama_algo_html():
    """Sıralama Algoritması - Swap yaparak sayıları sırala."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

let bars,selected,swaps,sorted;
const COLS=['#e74c3c','#3498db','#2ecc71','#f1c40f','#9b59b6','#e67e22','#1abc9c','#e84393'];

function genRound(){
    let n=5+Math.min(round,3);
    bars=[];for(let i=1;i<=n;i++)bars.push(i);
    for(let i=bars.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[bars[i],bars[j]]=[bars[j],bars[i]];}
    selected=-1;swaps=0;sorted=false;
}
function isSorted(){for(let i=1;i<bars.length;i++)if(bars[i]<bars[i-1])return false;return true;}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#e67e22';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('📊 Siralama Algoritmasi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Barlari swap yaparak kucukten buyuge sirala!',W/2,260);
        ctx.fillStyle='#e67e22';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#f39c12';ctx.font='bold 16px Arial';ctx.fillText('Swap: '+swaps,W/2,55);
        let bw=Math.min(80,600/bars.length),maxH=350,ox=(W-bw*bars.length)/2;
        for(let i=0;i<bars.length;i++){
            let h=bars[i]/bars.length*maxH;
            ctx.fillStyle=i==selected?'#f1c40f':COLS[i%COLS.length];
            ctx.beginPath();ctx.roundRect(ox+i*bw+5,400-h,bw-10,h,6);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 18px Arial';ctx.fillText(bars[i],ox+i*bw+bw/2,420);
        }
        if(sorted){
            ctx.fillStyle='#2ecc71';ctx.font='bold 28px Arial';ctx.fillText('Siralandi! '+swaps+' swap',W/2,500);
        }
        ctx.fillStyle='#95a5a6';ctx.font='14px Arial';ctx.fillText('Iki bara tiklayarak swap yap',W/2,560);
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
    if(state!='play'||sorted)return;
    let bw=Math.min(80,600/bars.length),ox=(W-bw*bars.length)/2;
    for(let i=0;i<bars.length;i++){
        if(mx>ox+i*bw&&mx<ox+(i+1)*bw&&my>80&&my<440){
            if(selected==-1){selected=i;beep(350,0.05);}
            else if(selected==i){selected=-1;}
            else{
                [bars[selected],bars[i]]=[bars[i],bars[selected]];
                swaps++;selected=-1;beep(450,0.08);
                if(isSorted()){sorted=true;score+=10;beep(523,0.15);addP(W/2,400,'#2ecc71');
                    setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1200);
                }
            }
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_binary_sayilar_html():
    """Binary Macerası - İkili sayı sistemini öğren."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

let target,bits,feedback;
const VALS=[128,64,32,16,8,4,2,1];

function genRound(){
    let maxVal=round<=3?15:round<=6?63:255;
    target=Math.floor(Math.random()*maxVal)+1;
    bits=[0,0,0,0,0,0,0,0];feedback='';
}
function getTotal(){let s=0;for(let i=0;i<8;i++)s+=bits[i]*VALS[i];return s;}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#00b894';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('💻 Binary Macerasi',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Ikili sayi sistemini ogren!',W/2,260);
        ctx.fillStyle='#00b894';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#f1c40f';ctx.font='bold 32px Arial';ctx.fillText('Hedef: '+target,W/2,90);
        let total=getTotal();
        ctx.fillStyle=total==target?'#2ecc71':'#ecf0f1';ctx.font='bold 24px Arial';
        ctx.fillText('Toplam: '+total,W/2,130);
        // Bit switches
        let ox=60,sw=72;
        ctx.fillStyle='#95a5a6';ctx.font='bold 14px Arial';
        for(let i=0;i<8;i++){
            ctx.fillStyle='#7f8c8d';ctx.font='bold 14px Arial';
            ctx.fillText(VALS[i],ox+i*sw+sw/2,180);
            ctx.fillStyle=bits[i]?'#2ecc71':'#34495e';
            ctx.beginPath();ctx.roundRect(ox+i*sw+8,200,sw-16,80,12);ctx.fill();
            ctx.strokeStyle=bits[i]?'#27ae60':'#555';ctx.lineWidth=2;
            ctx.strokeRect(ox+i*sw+8,200,sw-16,80);
            ctx.fillStyle='#fff';ctx.font='bold 28px Arial';
            ctx.fillText(bits[i]?'1':'0',ox+i*sw+sw/2,245);
            ctx.fillStyle='#95a5a6';ctx.font='12px Arial';
            ctx.fillText(bits[i]?'ON':'OFF',ox+i*sw+sw/2,275);
        }
        // Binary string
        ctx.fillStyle='#3498db';ctx.font='bold 20px Courier New';
        let bs=bits.join('');
        ctx.fillText('Binary: '+bs,W/2,330);
        // Check button
        if(total==target&&!feedback){
            ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(W/2-60,370,120,40,10);ctx.fill();
            ctx.fillStyle='#fff';ctx.font='bold 16px Arial';ctx.fillText('KONTROL',W/2,392);
        }
        if(feedback){
            ctx.fillStyle='#2ecc71';ctx.font='bold 28px Arial';
            ctx.fillText('Dogru! '+target+' = '+bits.join(''),W/2,430);
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
    let ox=60,sw=72;
    for(let i=0;i<8;i++){
        if(mx>ox+i*sw+8&&mx<ox+i*sw+sw-8&&my>200&&my<280){
            bits[i]=1-bits[i];beep(300+i*50,0.08);
            if(getTotal()==target){
                feedback='ok';score+=10;beep(523,0.15);addP(W/2,300,'#2ecc71');
                setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1200);
            }
            return;
        }
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""


def _build_elem_code_akis_diyagrami_html():
    """Akış Diyagramı - Algoritmayi flowchart olarak sırala."""
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(0,0,0,.5);}
</style></head><body><canvas id="c" width="700" height="650"></canvas><script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d'),W=700,H=650;
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}

const FLOWS=[
    {title:'Sayi cift mi?',steps:['Basla','Sayi gir','Sayi%2==0?','Cift yaz','Tek yaz','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Iki sayidan buyugu bul',steps:['Basla','a ve b gir','a>b mi?','a buyuk yaz','b buyuk yaz','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Notu hesapla',steps:['Basla','Notu gir','Not>=50?','Gecti yaz','Kaldi yaz','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Toplama yap',steps:['Basla','a gir','b gir','toplam=a+b','toplam yaz','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Sicaklik kontrolu',steps:['Basla','Derece gir','Derece>30?','Sicak yaz','Serin yaz','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Yas kontrolu',steps:['Basla','Yas gir','Yas>=18?','Yetiskin','Cocuk','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Kare hesapla',steps:['Basla','Sayi gir','kare=sayi*sayi','kare yaz','Bitis',''],correct:[0,1,2,3,4]},
    {title:'Carpma yap',steps:['Basla','a gir','b gir','sonuc=a*b','sonuc yaz','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Ucgen alan',steps:['Basla','Taban gir','Yukseklik gir','alan=t*y/2','alan yaz','Bitis'],correct:[0,1,2,3,4,5]},
    {title:'Pozitif mi?',steps:['Basla','Sayi gir','Sayi>0?','Pozitif','Negatif','Bitis'],correct:[0,1,2,3,4,5]},
];
let curFlow,shuffled,placed,selIdx,feedback;
const SHAPES=['oval','para','para','diamond','rect','rect','oval'];
const SHCOLS=['#2ecc71','#3498db','#3498db','#f39c12','#9b59b6','#9b59b6','#e74c3c'];

function genRound(){
    curFlow=FLOWS[(round-1)%FLOWS.length];
    let n=curFlow.steps.filter(s=>s).length;
    shuffled=[];for(let i=0;i<n;i++)shuffled.push(i);
    for(let i=shuffled.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]];}
    placed=[];selIdx=-1;feedback='';
}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,col:c});}

function draw(){
    ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
    let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,'#1a1a2e');grd.addColorStop(1,'#16213e');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
    if(state=='start'){
        ctx.fillStyle='#9b59b6';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText('📐 Akis Diyagrami',W/2,200);
        ctx.fillStyle='#bdc3c7';ctx.font='18px Arial';ctx.fillText('Adimlari dogru siraya koyarak akis olustur!',W/2,260);
        ctx.fillStyle='#9b59b6';ctx.fillRect(W/2-80,305,160,40);
        ctx.fillStyle='#fff';ctx.font='bold 20px Arial';ctx.fillText('▶ BAŞLA',W/2,327);
    }else if(state=='play'){
        ctx.fillStyle='#ecf0f1';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('Seviye: '+round+'/'+maxR,20,30);
        ctx.textAlign='right';ctx.fillText('Puan: '+score,W-20,30);ctx.textAlign='center';
        ctx.fillStyle='#f1c40f';ctx.font='bold 18px Arial';ctx.fillText('Algoritma: '+curFlow.title,W/2,65);
        // Shuffled items on left
        let n=curFlow.steps.filter(s=>s).length;
        ctx.fillStyle='#95a5a6';ctx.font='bold 14px Arial';ctx.fillText('Adimlar:',100,90);
        for(let i=0;i<shuffled.length;i++){
            let si=shuffled[i];
            let used=placed.includes(si);
            ctx.fillStyle=used?'#555':SHCOLS[si%SHCOLS.length];
            ctx.beginPath();ctx.roundRect(30,105+i*50,180,40,8);ctx.fill();
            ctx.fillStyle=used?'#777':'#fff';ctx.font='bold 13px Arial';
            ctx.fillText(curFlow.steps[si],120,128+i*50);
            if(selIdx==i&&!used){ctx.strokeStyle='#f1c40f';ctx.lineWidth=3;ctx.strokeRect(28,103+i*50,184,44);ctx.lineWidth=1;}
        }
        // Placed slots on right
        ctx.fillStyle='#95a5a6';ctx.font='bold 14px Arial';ctx.fillText('Sira:',520,90);
        for(let i=0;i<n;i++){
            ctx.strokeStyle='#7f8c8d';ctx.lineWidth=2;
            ctx.strokeRect(420,105+i*50,200,40);
            if(i<placed.length){
                ctx.fillStyle=SHCOLS[placed[i]%SHCOLS.length];ctx.beginPath();ctx.roundRect(420,105+i*50,200,40,8);ctx.fill();
                ctx.fillStyle='#fff';ctx.font='bold 13px Arial';ctx.fillText(curFlow.steps[placed[i]],520,128+i*50);
            }else{
                ctx.fillStyle='#555';ctx.font='12px Arial';ctx.fillText((i+1)+'. adim',520,128+i*50);
            }
            if(i<n-1){ctx.strokeStyle='#7f8c8d';ctx.beginPath();ctx.moveTo(520,145+i*50);ctx.lineTo(520,155+i*50);ctx.stroke();
                ctx.fillStyle='#7f8c8d';ctx.fillText('↓',520,157+i*50);}
        }
        // Buttons
        ctx.fillStyle='#e74c3c';ctx.beginPath();ctx.roundRect(230,540,100,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 14px Arial';ctx.fillText('GERİ AL',280,560);
        ctx.fillStyle='#27ae60';ctx.beginPath();ctx.roundRect(370,540,100,35,8);ctx.fill();
        ctx.fillStyle='#fff';ctx.fillText('KONTROL',420,560);
        if(feedback){
            ctx.fillStyle=feedback=='ok'?'#2ecc71':'#e74c3c';ctx.font='bold 22px Arial';
            ctx.fillText(feedback=='ok'?'Dogru sira!':'Yanlis, tekrar dene!',W/2,610);
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
    if(feedback=='ok')return;
    if(feedback=='no'){feedback='';return;}
    // Click shuffled item
    for(let i=0;i<shuffled.length;i++){
        if(mx>30&&mx<210&&my>105+i*50&&my<145+i*50&&!placed.includes(shuffled[i])){
            placed.push(shuffled[i]);beep(400+i*30,0.08);return;
        }
    }
    // Geri al
    if(mx>230&&mx<330&&my>540&&my<575&&placed.length>0){placed.pop();return;}
    // Kontrol
    let n=curFlow.steps.filter(s=>s).length;
    if(mx>370&&mx<470&&my>540&&my<575&&placed.length==n){
        let ok=true;
        for(let i=0;i<n;i++)if(placed[i]!=curFlow.correct[i])ok=false;
        if(ok){feedback='ok';score+=10;beep(523,0.15);addP(W/2,500,'#2ecc71');
            setTimeout(()=>{round++;if(round>maxR)state='win';else genRound();},1200);
        }else{feedback='no';beep(180,0.3);setTimeout(()=>{placed=[];feedback='';},1500);}
    }
});
canvas.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
draw();
</script></body></html>"""
