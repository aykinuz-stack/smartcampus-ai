# -*- coding: utf-8 -*-
"""İlkokul Genel Yetenek Oyunları — Premium HTML5 Oyunlar (Bölüm D: 16-20)."""


def _build_elem_ab_yol_planlama_html():
    """Yol Planlama (Algoritma) — Grid üzerinde komutlarla hedefe ulaş."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
const GS=6,CS=60,OX=0,OY=0;
let grid=[],playerR=0,playerC=0,targetR=0,targetC=0,commands=[],maxCmd=8,executing=false,execIdx=0,execTimer=0;
let animPR=0,animPC=0,feedback='',feedbackTimer=0,showPath=false;
const DIRS=[{name:'↑',dr:-1,dc:0},{name:'↓',dr:1,dc:0},{name:'←',dr:0,dc:-1},{name:'→',dr:0,dc:1}];
function rnd(n){return Math.floor(Math.random()*n)}
function genLevel(){
grid=[];for(let r=0;r<GS;r++){grid[r]=[];for(let c=0;c<GS;c++)grid[r][c]=0}
playerR=rnd(3);playerC=rnd(3);
targetR=GS-1-rnd(2);targetC=GS-1-rnd(2);
if(targetR===playerR&&targetC===playerC)targetC=(targetC+1)%GS;
let obs=Math.min(round+2,10);
for(let i=0;i<obs;i++){let r=rnd(GS),c=rnd(GS),tries=0;
while(((r===playerR&&c===playerC)||(r===targetR&&c===targetC)||grid[r][c]===1)&&tries<50){r=rnd(GS);c=rnd(GS);tries++}
if(tries<50)grid[r][c]=1}
grid[playerR][playerC]=0;grid[targetR][targetC]=0;
commands=[];executing=false;execIdx=0;
animPR=playerR;animPC=playerC;feedback='';feedbackTimer=0;showPath=false;
maxCmd=Math.max(6,12-Math.floor(round/3))}
function getGX(){return(W-GS*CS)/2}
function getGY(){return 50}
function drawGrid(){
const gx=getGX(),gy=getGY();
for(let r=0;r<GS;r++)for(let c=0;c<GS;c++){
const x=gx+c*CS,y=gy+r*CS;
if(grid[r][c]===1){ctx.fillStyle='#4a2040';ctx.fillRect(x+1,y+1,CS-2,CS-2);
ctx.fillStyle='#e74c3c';ctx.font='24px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('🧱',x+CS/2,y+CS/2)}
else{ctx.fillStyle=(r+c)%2===0?'#1e3a5f':'#1a2f4a';ctx.fillRect(x+1,y+1,CS-2,CS-2)}}
const pr=executing?animPR:playerR,pc=executing?animPC:playerC;
ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('🤖',gx+pc*CS+CS/2,gy+pr*CS+CS/2);
ctx.fillText('🏁',gx+targetC*CS+CS/2,gy+targetR*CS+CS/2)}
function drawCmdBar(){
const bx=30,by=getGY()+GS*CS+15;
ctx.fillStyle='#e2e8f0';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
ctx.fillText('Komutlar ('+commands.length+'/'+maxCmd+'):',bx,by);
for(let i=0;i<commands.length;i++){
const cx=bx+i*42,cy=by+8;
ctx.fillStyle=executing&&i===execIdx?'#fbbf24':'#334155';
ctx.beginPath();ctx.roundRect(cx,cy,38,32,6);ctx.fill();
ctx.fillStyle=executing&&i===execIdx?'#000':'#e2e8f0';ctx.font='18px Segoe UI';ctx.textAlign='center';
ctx.fillText(DIRS[commands[i]].name,cx+19,cy+20)}}
function drawButtons(){
const by=getGY()+GS*CS+62;
const btnW=70,btnH=42,gap=10;
const labels=['↑ İleri','↓ Geri','← Sol','→ Sağ'];
const clrs=['#3b82f6','#8b5cf6','#ef4444','#10b981'];
for(let i=0;i<4;i++){
const bx=30+i*(btnW+gap),bcy=by;
ctx.fillStyle=clrs[i];ctx.beginPath();ctx.roundRect(bx,bcy,btnW,btnH,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
ctx.fillText(labels[i],bx+btnW/2,bcy+btnH/2+5)}
const rx=30+4*(btnW+gap)+10;
ctx.fillStyle='#f59e0b';ctx.beginPath();ctx.roundRect(rx,by,90,btnH,8);ctx.fill();
ctx.fillStyle='#000';ctx.font='bold 14px Segoe UI';ctx.fillText('ÇALIŞTIR',rx+45,by+btnH/2+5);
const sx=rx+100;
ctx.fillStyle='#64748b';ctx.beginPath();ctx.roundRect(sx,by,60,btnH,8);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 14px Segoe UI';ctx.fillText('SİL',sx+30,by+btnH/2+5)}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🤖 Yol Planlama',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Komutlarla robotu hedefe ulaştır!',W/2,230);
ctx.fillText('↑↓←→ butonlarıyla yol planla',W/2,260);
ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.roundRect(W/2-80,305,160,40,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,330);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 38px Segoe UI';ctx.textAlign='center';
ctx.fillText('TEBRİKLER!',W/2,200);ctx.font='26px Segoe UI';ctx.fillStyle='#e2e8f0';
ctx.fillText('Puan: '+score+'/100',W/2,260);ctx.font='20px Segoe UI';
ctx.fillText('Tüm yolları başarıyla planladın!',W/2,300);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,30);
drawGrid();drawCmdBar();
if(!executing)drawButtons();
if(feedbackTimer>0){ctx.fillStyle=feedback.includes('Doğru')?'#10b981':'#ef4444';
ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=Math.min(1,feedbackTimer);
ctx.fillText(feedback,W/2,H-15);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function executeStep(){
if(execIdx>=commands.length){
if(Math.round(animPR)===targetR&&Math.round(animPC)===targetC){
score+=10;beep(523,0.15);addP(getGX()+targetC*CS+CS/2,getGY()+targetR*CS+CS/2,'#10b981');
feedback='Doğru! Hedefe ulaştın! +10';feedbackTimer=2;
round++;if(round>maxR){setTimeout(()=>{state='win';for(let i=0;i<30;i++)addP(rnd(W),rnd(H),'#fbbf24')},800)}
else setTimeout(genLevel,1200)}
else{beep(180,0.3);feedback='Hedefe ulaşamadın! Tekrar dene.';feedbackTimer=2;
setTimeout(()=>{commands=[];executing=false;execIdx=0;animPR=playerR;animPC=playerC},1500)}
return}
const d=DIRS[commands[execIdx]];
const nr=Math.round(animPR)+d.dr,nc=Math.round(animPC)+d.dc;
if(nr<0||nr>=GS||nc<0||nc>=GS||grid[nr][nc]===1){
beep(180,0.3);feedback='Engel! Yol tıkandı.';feedbackTimer=2;
setTimeout(()=>{commands=[];executing=false;execIdx=0;animPR=playerR;animPC=playerC},1500);return}
animPR=nr;animPC=nc;execIdx++;
setTimeout(executeStep,400)}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(feedbackTimer>0)feedbackTimer-=dt;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function handleClick(mx,my){
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';score=0;round=1;genLevel()}return}
if(state==='win')return;
if(state!=='play'||executing)return;
const by=getGY()+GS*CS+62,btnW=70,btnH=42,gap=10;
for(let i=0;i<4;i++){const bx=30+i*(btnW+gap);
if(mx>=bx&&mx<=bx+btnW&&my>=by&&my<=by+btnH){if(commands.length<maxCmd){commands.push(i);beep(400+i*50,0.08)}return}}
const rx=30+4*(btnW+gap)+10;
if(mx>=rx&&mx<=rx+90&&my>=by&&my<=by+btnH){
if(commands.length>0){executing=true;execIdx=0;animPR=playerR;animPC=playerC;executeStep()}return}
const sx=rx+100;
if(mx>=sx&&mx<=sx+60&&my>=by&&my<=by+btnH){if(commands.length>0)commands.pop();return}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();handleClick((e.clientX-r.left)*(W/r.width),(e.clientY-r.top)*(H/r.height))});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0],r=cv.getBoundingClientRect();handleClick((t.clientX-r.left)*(W/r.width),(t.clientY-r.top)*(H/r.height))});
genLevel();requestAnimationFrame(upd);
</script></body></html>"""


def _build_elem_ab_uc_tas_html():
    """Strateji Mini: 3 Taş — 3x3 tahtada stratejik taş oyunu."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
const BS=140,BX=0,BY=0;
let board=[0,0,0,0,0,0,0,0,0],phase='place',playerPieces=0,cpuPieces=0,turn='player';
let selectedCell=-1,feedback='',feedbackTimer=0,winLine=null,movePhasePlayer=false,moveFrom=-1;
let playerFirst=true,aiDelay=false;
const LINES=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
const ADJ=[[1,3,4],[0,2,3,4,5],[1,4,5],[0,1,4,6,7],[0,1,2,3,5,6,7,8],[1,2,4,7,8],[3,4,7],[3,4,5,6,8],[4,5,7]];
function getBX(){return(W-3*BS)/2}
function getBY(){return 120}
function resetBoard(){board=[0,0,0,0,0,0,0,0,0];phase='place';playerPieces=0;cpuPieces=0;
turn=playerFirst?'player':'cpu';selectedCell=-1;winLine=null;moveFrom=-1;
feedback='';feedbackTimer=0;aiDelay=false;
if(turn==='cpu')setTimeout(cpuMove,600)}
function checkWin(p){for(const l of LINES)if(board[l[0]]===p&&board[l[1]]===p&&board[l[2]]===p){winLine=l;return true}return false}
function cpuMove(){
if(state!=='play'||turn!=='player')return;
turn='cpu';aiDelay=true;
setTimeout(()=>{
aiDelay=false;
if(phase==='place'){
let mv=aiPlace();if(mv>=0){board[mv]=2;cpuPieces++;
if(cpuPieces>=3&&playerPieces>=3)phase='move';
if(checkWin(2)){endRound('cpu');return}
turn='player'}}
else{
let mv=aiMove();if(mv){board[mv.to]=2;board[mv.from]=0;
if(checkWin(2)){endRound('cpu');return}
turn='player'}}
},500)}
function aiPlace(){
for(const l of LINES){let c2=0,c0=0,empty=-1;
for(const i of l){if(board[i]===2)c2++;else if(board[i]===0){c0++;empty=i}}
if(c2===2&&c0===1)return empty}
for(const l of LINES){let c1=0,c0=0,empty=-1;
for(const i of l){if(board[i]===1)c1++;else if(board[i]===0){c0++;empty=i}}
if(c1===2&&c0===1)return empty}
if(board[4]===0)return 4;
const corners=[0,2,6,8];for(const c of corners)if(board[c]===0)return c;
for(let i=0;i<9;i++)if(board[i]===0)return i;return-1}
function aiMove(){
let cpuCells=[];for(let i=0;i<9;i++)if(board[i]===2)cpuCells.push(i);
for(const from of cpuCells)for(const to of ADJ[from])if(board[to]===0){
board[to]=2;board[from]=0;if(checkWin(2)){board[from]=2;board[to]=0;winLine=null;return{from,to}}
board[from]=2;board[to]=0;winLine=null}
let plCells=[];for(let i=0;i<9;i++)if(board[i]===1)plCells.push(i);
for(const from of plCells)for(const to of ADJ[from])if(board[to]===0){
board[to]=1;board[from]=0;if(checkWin(1)){board[from]=1;board[to]=0;winLine=null;
for(const cf of cpuCells)for(const ct of ADJ[cf])if(board[ct]===0){board[from]=1;board[to]=0;winLine=null;return{from:cf,to:ct}}
}board[from]=1;board[to]=0;winLine=null}
for(const from of cpuCells)for(const to of ADJ[from])if(board[to]===0)return{from,to};
return null}
function endRound(winner){
if(winner==='player'){score+=10;beep(523,0.15);feedback='Kazandın! +10';
addP(W/2,300,'#3b82f6')}
else if(winner==='cpu'){feedback='Bilgisayar kazandı!';beep(180,0.3)}
else{score+=5;beep(523,0.15);feedback='Berabere! +5'}
feedbackTimer=2;round++;playerFirst=!playerFirst;
if(round>maxR)setTimeout(()=>{state='win';for(let i=0;i<30;i++)addP(Math.random()*W,Math.random()*H,'#fbbf24')},1200);
else setTimeout(resetBoard,1500)}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('⭕✕ Strateji Mini: 3 Taş',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('3 taşını diz, sonra hareket ettir!',W/2,230);
ctx.fillText('Satır, sütun veya çaprazda 3 yap!',W/2,260);
ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.roundRect(W/2-80,305,160,40,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,330);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 38px Segoe UI';ctx.textAlign='center';
ctx.fillText('TEBRİKLER!',W/2,200);ctx.font='26px Segoe UI';ctx.fillStyle='#e2e8f0';
ctx.fillText('Puan: '+score+'/100',W/2,260);ctx.font='20px Segoe UI';
ctx.fillText('Strateji ustası oldun!',W/2,300);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,30);
ctx.fillStyle='#94a3b8';ctx.font='14px Segoe UI';
const phTxt=phase==='place'?'Taş Yerleştirme':'Taş Hareket Ettirme';
const turnTxt=turn==='player'?'Senin sıran':'Bilgisayar düşünüyor...';
ctx.fillText(phTxt+' — '+turnTxt,W/2,55);
const bx=getBX(),by=getBY();
ctx.fillStyle='#5c3d1e';ctx.beginPath();ctx.roundRect(bx-15,by-15,3*BS+30,3*BS+30,12);ctx.fill();
ctx.fillStyle='#8b6c42';ctx.beginPath();ctx.roundRect(bx-10,by-10,3*BS+20,3*BS+20,10);ctx.fill();
for(let r=0;r<3;r++)for(let c=0;c<3;c++){
const i=r*3+c,x=bx+c*BS,y=by+r*BS;
ctx.fillStyle=(r+c)%2===0?'#d4a76a':'#c49558';ctx.fillRect(x+2,y+2,BS-4,BS-4);
if(moveFrom===i){ctx.strokeStyle='#fbbf24';ctx.lineWidth=4;ctx.strokeRect(x+4,y+4,BS-8,BS-8)}
if(board[i]===1){ctx.fillStyle='#3b82f6';ctx.font='bold 60px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('✕',x+BS/2,y+BS/2)}
else if(board[i]===2){ctx.fillStyle='#ef4444';ctx.font='bold 60px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('⭕',x+BS/2,y+BS/2)}}
if(winLine){ctx.strokeStyle='#fbbf24';ctx.lineWidth=6;ctx.lineCap='round';
const x1=bx+winLine[0]%3*BS+BS/2,y1=by+Math.floor(winLine[0]/3)*BS+BS/2;
const x2=bx+winLine[2]%3*BS+BS/2,y2=by+Math.floor(winLine[2]/3)*BS+BS/2;
ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke()}
ctx.fillStyle='#3b82f6';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
ctx.fillText('Sen (✕): '+(3-playerPieces)+' taş kaldı',bx,by+3*BS+30);
ctx.fillStyle='#ef4444';ctx.textAlign='right';
ctx.fillText('Bilgisayar (⭕): '+(3-cpuPieces)+' taş kaldı',bx+3*BS,by+3*BS+30);
if(feedbackTimer>0){ctx.fillStyle=feedback.includes('Kazan')?'#10b981':feedback.includes('Bera')?'#f59e0b':'#ef4444';
ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=Math.min(1,feedbackTimer);
ctx.fillText(feedback,W/2,by+3*BS+65);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(feedbackTimer>0)feedbackTimer-=dt;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function handleClick(mx,my){
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';score=0;round=1;playerFirst=true;resetBoard()}return}
if(state==='win')return;
if(state!=='play'||turn!=='player'||aiDelay||winLine)return;
const bx=getBX(),by=getBY();
const c=Math.floor((mx-bx)/BS),r=Math.floor((my-by)/BS);
if(c<0||c>2||r<0||r>2)return;
const idx=r*3+c;
if(phase==='place'){
if(board[idx]!==0)return;
board[idx]=1;playerPieces++;beep(400,0.08);
if(checkWin(1)){endRound('player');return}
if(playerPieces>=3&&cpuPieces>=3)phase='move';
cpuMove()}
else{
if(moveFrom===-1){if(board[idx]===1){moveFrom=idx;beep(350,0.05)}}
else{if(idx===moveFrom){moveFrom=-1;return}
if(board[idx]!==0||!ADJ[moveFrom].includes(idx)){beep(180,0.1);moveFrom=-1;return}
board[idx]=1;board[moveFrom]=0;moveFrom=-1;beep(400,0.08);
if(checkWin(1)){endRound('player');return}
let allEmpty=true;for(let i=0;i<9;i++)if(board[i]===0){allEmpty=false;break}
cpuMove()}}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();handleClick((e.clientX-r.left)*(W/r.width),(e.clientY-r.top)*(H/r.height))});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0],r=cv.getBoundingClientRect();handleClick((t.clientX-r.left)*(W/r.width),(t.clientY-r.top)*(H/r.height))});
resetBoard();requestAnimationFrame(upd);
</script></body></html>"""


def _build_elem_ab_puzzle_birlestir_html():
    """Parça Birleştir (Puzzle) — Karışık parçaları doğru sıraya diz."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
let gridN=3,pieces=[],selected=-1,moves=0,feedback='',feedbackTimer=0,solved=false;
const COLORS=['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#ec4899','#06b6d4','#f97316',
'#84cc16','#14b8a6','#e879f9','#fb923c','#38bdf8','#a3e635','#c084fc','#fb7185'];
const PATTERNS=['▲','★','●','◆','♦','♠','♣','♥','◉','✿','☀','⬟','⬡','✦','⊕','⊗'];
function getPieceSize(){return Math.floor(Math.min(360,W-100)/gridN)}
function getOX(){return(W-gridN*getPieceSize())/2}
function getOY(){return 100}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function genPuzzle(){
gridN=round<=4?3:(round<=7?3:4);
const total=gridN*gridN;
pieces=[];
let positions=[];for(let i=0;i<total;i++)positions.push(i);
let shuffled=positions.slice();
let tries=0;
do{shuffle(shuffled);tries++}while(shuffled.every((v,i)=>v===i)&&tries<100);
for(let i=0;i<total;i++){
pieces.push({id:i,pos:shuffled[i],clr:COLORS[i%COLORS.length],pat:PATTERNS[i%PATTERNS.length]})}
selected=-1;moves=0;solved=false;feedback='';feedbackTimer=0}
function checkSolved(){return pieces.every(p=>p.pos===p.id)}
function drawPiece(p,x,y,sz,mini){
const isCorrect=p.pos===p.id;
ctx.fillStyle=p.clr;
ctx.beginPath();ctx.roundRect(x+2,y+2,sz-4,sz-4,mini?4:8);ctx.fill();
if(isCorrect&&!mini){ctx.strokeStyle='#10b981';ctx.lineWidth=3;ctx.stroke()}
ctx.fillStyle='#fff';ctx.font=(mini?'bold 10px':'bold '+(sz>80?'28':'22')+'px')+' Segoe UI';
ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(p.pat,x+sz/2,y+sz/2-(mini?0:8));
ctx.font=(mini?'8px':'bold '+(sz>80?'18':'14')+'px')+' Segoe UI';
ctx.fillText(''+(p.id+1),x+sz/2,y+sz/2+(mini?8:18))}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🧩 Parça Birleştir',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('İki parçaya tıklayarak yerlerini değiştir!',W/2,230);
ctx.fillText('Tüm parçaları doğru sıraya diz!',W/2,260);
ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.roundRect(W/2-80,305,160,40,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,330);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 38px Segoe UI';ctx.textAlign='center';
ctx.fillText('TEBRİKLER!',W/2,200);ctx.font='26px Segoe UI';ctx.fillStyle='#e2e8f0';
ctx.fillText('Puan: '+score+'/100',W/2,260);ctx.font='20px Segoe UI';
ctx.fillText('Tüm yapbozları tamamladın!',W/2,300);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score+'   Hamle: '+moves,W/2,30);
ctx.fillStyle='#94a3b8';ctx.font='14px Segoe UI';
ctx.fillText(gridN+'x'+gridN+' Puzzle — Parçaları 1\\\'den '+(gridN*gridN)+'\\\'e sırala',W/2,55);
const sz=getPieceSize(),ox=getOX(),oy=getOY();
ctx.strokeStyle='#334155';ctx.lineWidth=2;
ctx.beginPath();ctx.roundRect(ox-5,oy-5,gridN*sz+10,gridN*sz+10,10);ctx.stroke();
for(const p of pieces){
const row=Math.floor(p.pos/gridN),col=p.pos%gridN;
const x=ox+col*sz,y=oy+row*sz;
if(selected===p.pos){ctx.save();ctx.shadowColor='#fbbf24';ctx.shadowBlur=15;
drawPiece(p,x,y,sz,false);ctx.restore()}
else drawPiece(p,x,y,sz,false)}
const refX=ox+gridN*sz+25,refY=oy;
ctx.fillStyle='#94a3b8';ctx.font='bold 12px Segoe UI';ctx.textAlign='left';
ctx.fillText('Hedef:',refX,refY-5);
const miniSz=Math.min(25,Math.floor(120/gridN));
for(let i=0;i<gridN*gridN;i++){
const r=Math.floor(i/gridN),c=i%gridN;
const mx=refX+c*miniSz,my=refY+r*miniSz;
ctx.fillStyle=COLORS[i%COLORS.length];ctx.beginPath();ctx.roundRect(mx+1,my+1,miniSz-2,miniSz-2,2);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 9px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(''+(i+1),mx+miniSz/2,my+miniSz/2)}
if(feedbackTimer>0){ctx.fillStyle=feedback.includes('Doğru')?'#10b981':'#e2e8f0';
ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=Math.min(1,feedbackTimer);
ctx.fillText(feedback,W/2,oy+gridN*sz+50);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(feedbackTimer>0)feedbackTimer-=dt;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function handleClick(mx,my){
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';score=0;round=1;genPuzzle()}return}
if(state==='win')return;
if(state!=='play'||solved)return;
const sz=getPieceSize(),ox=getOX(),oy=getOY();
const col=Math.floor((mx-ox)/sz),row=Math.floor((my-oy)/sz);
if(col<0||col>=gridN||row<0||row>=gridN)return;
const pos=row*gridN+col;
if(selected===-1){selected=pos;beep(350,0.05)}
else if(selected===pos){selected=-1}
else{
const p1=pieces.find(p=>p.pos===selected),p2=pieces.find(p=>p.pos===pos);
if(p1&&p2){const tmp=p1.pos;p1.pos=p2.pos;p2.pos=tmp;moves++;beep(400,0.08)}
selected=-1;
if(checkSolved()){solved=true;score+=10;beep(523,0.15);
const cx=ox+gridN*sz/2,cy=oy+gridN*sz/2;
addP(cx,cy,'#10b981');addP(cx-50,cy,'#3b82f6');addP(cx+50,cy,'#fbbf24');
feedback='Doğru! Tamamlandı! +10';feedbackTimer=2;
round++;if(round>maxR)setTimeout(()=>{state='win';for(let i=0;i<30;i++)addP(Math.random()*W,Math.random()*H,'#fbbf24')},1200);
else setTimeout(genPuzzle,1500)}}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();handleClick((e.clientX-r.left)*(W/r.width),(e.clientY-r.top)*(H/r.height))});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0],r=cv.getBoundingClientRect();handleClick((t.clientX-r.left)*(W/r.width),(t.clientY-r.top)*(H/r.height))});
genPuzzle();requestAnimationFrame(upd);
</script></body></html>"""


def _build_elem_ab_sesli_sira_html():
    """Hafıza: Sesli Sıra — Simon-says tarzı sayı ve ses hafıza oyunu."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
const FREQS=[0,330,370,415,440,494,523,587,659,698];
const BTN_CLRS=['','#ef4444','#f97316','#f59e0b','#10b981','#06b6d4','#3b82f6','#8b5cf6','#ec4899','#f43f5e'];
const BTN_GLOW=['','#fca5a5','#fdba74','#fde047','#6ee7b7','#67e8f9','#93c5fd','#c4b5fd','#f9a8d4','#fda4af'];
let sequence=[],playerIdx=0,showingSeq=false,showIdx=0,showTimer=0;
let activeBtn=-1,activeTimer=0,seqLen=3,retries=0,maxRetries=2;
let feedback='',feedbackTimer=0,inputLocked=false,phase='watch';
function rnd(n){return Math.floor(Math.random()*n)}
function playNote(n){
if(n<1||n>9)return;
const o=actx.createOscillator(),g=actx.createGain();
o.type='triangle';o.connect(g);g.connect(actx.destination);
o.frequency.value=FREQS[n];g.gain.value=0.3;o.start();
g.gain.exponentialRampToValueAtTime(0.001,actx.currentTime+0.35);o.stop(actx.currentTime+0.35)}
function genSequence(){
seqLen=Math.min(2+round,12);
sequence=[];for(let i=0;i<seqLen;i++)sequence.push(1+rnd(9));
playerIdx=0;retries=0;phase='watch';inputLocked=true;
feedback='';feedbackTimer=0;
setTimeout(playSequence,600)}
function playSequence(){
showingSeq=true;showIdx=0;showTimer=0;
function step(){
if(showIdx>=sequence.length){showingSeq=false;activeBtn=-1;phase='input';inputLocked=false;
feedback='Sıra sende! Tekrarla!';feedbackTimer=2;return}
activeBtn=sequence[showIdx];playNote(activeBtn);activeTimer=0.4;
showIdx++;setTimeout(step,600)}
step()}
function getBtnRect(n){
const cols=3,bsz=100,gap=15;
const r=Math.floor((n-1)/cols),c=(n-1)%cols;
const totalW=cols*bsz+(cols-1)*gap,totalH=3*bsz+2*gap;
const ox=(W-totalW)/2,oy=220;
return{x:ox+c*(bsz+gap),y:oy+r*(bsz+gap),w:bsz,h:bsz}}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🎵 Sesli Sıra Hafızası',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Sayı sırasını dinle ve tekrarla!',W/2,230);
ctx.fillText('Her turda sıra uzar!',W/2,260);
ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.roundRect(W/2-80,305,160,40,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,330);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 38px Segoe UI';ctx.textAlign='center';
ctx.fillText('TEBRİKLER!',W/2,200);ctx.font='26px Segoe UI';ctx.fillStyle='#e2e8f0';
ctx.fillText('Puan: '+score+'/100',W/2,260);ctx.font='20px Segoe UI';
ctx.fillText('Hafızan süper!',W/2,300);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,30);
ctx.fillStyle='#94a3b8';ctx.font='14px Segoe UI';
const infoTxt=phase==='watch'?'İzle ve dinle...':'Sıra sende! ('+playerIdx+'/'+seqLen+')';
ctx.fillText('Sıra uzunluğu: '+seqLen+'   '+infoTxt,W/2,55);
for(let n=1;n<=9;n++){
const b=getBtnRect(n);
const isActive=activeBtn===n&&activeTimer>0;
if(isActive){ctx.save();ctx.shadowColor=BTN_GLOW[n];ctx.shadowBlur=25;
ctx.fillStyle=BTN_GLOW[n];ctx.beginPath();ctx.roundRect(b.x,b.y,b.w,b.h,14);ctx.fill();ctx.restore()}
else{ctx.fillStyle=BTN_CLRS[n];ctx.beginPath();ctx.roundRect(b.x,b.y,b.w,b.h,14);ctx.fill()}
ctx.fillStyle=isActive?'#000':'#fff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(''+n,b.x+b.w/2,b.y+b.h/2)}
const seqY=180;
ctx.fillStyle='#64748b';ctx.font='14px Segoe UI';ctx.textAlign='center';
ctx.fillText('Sıra:',W/2,seqY-5);
for(let i=0;i<seqLen;i++){
const sx=W/2-(seqLen*28)/2+i*28+14;
if(phase==='watch'&&showingSeq&&i<showIdx){ctx.fillStyle='#fbbf24';ctx.font='bold 18px Segoe UI';ctx.fillText(''+sequence[i],sx,seqY+15)}
else if(phase==='input'&&i<playerIdx){ctx.fillStyle='#10b981';ctx.font='bold 18px Segoe UI';ctx.fillText('✓',sx,seqY+15)}
else{ctx.fillStyle='#334155';ctx.font='18px Segoe UI';ctx.fillText('•',sx,seqY+15)}}
if(feedbackTimer>0){ctx.fillStyle=feedback.includes('Doğru')||feedback.includes('sende')?'#10b981':'#ef4444';
ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=Math.min(1,feedbackTimer);
ctx.fillText(feedback,W/2,590);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(feedbackTimer>0)feedbackTimer-=dt;
if(activeTimer>0)activeTimer-=dt;
if(activeTimer<=0)activeBtn=-1;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function handleClick(mx,my){
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';score=0;round=1;genSequence()}return}
if(state==='win')return;
if(state!=='play'||inputLocked||phase!=='input')return;
for(let n=1;n<=9;n++){const b=getBtnRect(n);
if(mx>=b.x&&mx<=b.x+b.w&&my>=b.y&&my<=b.y+b.h){
activeBtn=n;activeTimer=0.25;playNote(n);
if(n===sequence[playerIdx]){
playerIdx++;
if(playerIdx>=seqLen){
score+=10;beep(523,0.15);addP(W/2,400,'#10b981');
feedback='Doğru! +10';feedbackTimer=2;inputLocked=true;
round++;if(round>maxR)setTimeout(()=>{state='win';for(let i=0;i<30;i++)addP(Math.random()*W,Math.random()*H,'#fbbf24')},1200);
else setTimeout(genSequence,1500)}}
else{
beep(180,0.3);retries++;
if(retries>=maxRetries){feedback='Yanlış! Sonraki tura geçiliyor.';feedbackTimer=2;inputLocked=true;
round++;if(round>maxR)setTimeout(()=>{state='win';for(let i=0;i<30;i++)addP(Math.random()*W,Math.random()*H,'#fbbf24')},1200);
else setTimeout(genSequence,1500)}
else{feedback='Yanlış! Tekrar dinle. (Deneme '+(retries+1)+'/'+maxRetries+')';feedbackTimer=2;
inputLocked=true;playerIdx=0;setTimeout(()=>{phase='watch';playSequence()},1500)}}
return}}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();handleClick((e.clientX-r.left)*(W/r.width),(e.clientY-r.top)*(H/r.height))});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0],r=cv.getBoundingClientRect();handleClick((t.clientX-r.left)*(W/r.width),(t.clientY-r.top)*(H/r.height))});
requestAnimationFrame(upd);
</script></body></html>"""


def _build_elem_ab_problem_cozme_html():
    """Problem Çözme Kartları — Sözel matematik ve mantık problemleri."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a1a2e,#16213e);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxR=10,score=0,particles=[];
const actx=new(window.AudioContext||window.webkitAudioContext)();
function beep(f,d){const o=actx.createOscillator(),g=actx.createGain();o.connect(g);g.connect(actx.destination);o.frequency.value=f;o.start();g.gain.exponentialRampToValueAtTime(.001,actx.currentTime+d);o.stop(actx.currentTime+d)}
function addP(x,y,clr){for(let i=0;i<15;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
let curProblem=null,answered=false,feedback='',feedbackTimer=0,explanation='',showExpl=false;
const PROBLEMS=[
{cat:'İşlem',q:"Ali'nin 15 elması var. 7 tanesini Ayşe'ye verdi. Sonra annesi 4 elma daha getirdi. Ali'de kaç elma kaldı?",a:12,opts:[10,12,14,8],exp:'15 - 7 = 8, sonra 8 + 4 = 12'},
{cat:'İşlem',q:"Bir bahçede 24 ağaç var. 8 tanesi elma, 6 tanesi armut, geri kalanı kiraz ağacı. Kaç kiraz ağacı var?",a:10,opts:[10,12,8,14],exp:'24 - 8 - 6 = 10 kiraz ağacı'},
{cat:'Mantık',q:"Bir sırada 5 çocuk oturuyor. Elif soldan 2. sırada. Elif sağdan kaçıncı sırada?",a:4,opts:[3,4,5,2],exp:'5 - 2 + 1 = 4. sırada'},
{cat:'İşlem',q:"Markette bir defter 8 TL, bir kalem 3 TL. Emre 2 defter ve 3 kalem aldı. Toplam kaç TL ödedi?",a:25,opts:[22,25,27,19],exp:'2×8 = 16 TL + 3×3 = 9 TL = 25 TL'},
{cat:'Sıralama',q:"Hangi sayı sırayı tamamlar? 2, 5, 8, 11, ?",a:14,opts:[12,13,14,15],exp:'Her sayı 3 artıyor: 11 + 3 = 14'},
{cat:'Mantık',q:"Bir kutuda 4 kırmızı ve 6 mavi top var. Gözleri kapalı 1 top çekersen, hangi renk gelme olasılığı daha yüksek?",a:0,opts:['Mavi','Kırmızı','Eşit','Bilinemez'],exp:'6 mavi > 4 kırmızı, mavi daha olası'},
{cat:'İşlem',q:"Zeynep 50 TL ile alışverişe gitti. 18 TL ekmek ve 12 TL süt aldı. Kaç TL para üstü alır?",a:20,opts:[20,22,18,24],exp:'50 - 18 - 12 = 20 TL'},
{cat:'Sıralama',q:"Hangi sayı sırayı tamamlar? 1, 4, 9, 16, ?",a:25,opts:[20,24,25,30],exp:'Kareler: 1², 2², 3², 4², 5²=25'},
{cat:'Mantık',q:"Ahmet, Mehmet'ten uzun. Mehmet, Can'dan uzun. En kısa kim?",a:0,opts:['Can','Mehmet','Ahmet','Bilinemez'],exp:'Ahmet > Mehmet > Can, en kısa Can'},
{cat:'İşlem',q:"Bir sınıfta 32 öğrenci var. 15'i kız ise kaç erkek öğrenci var?",a:17,opts:[15,17,18,16],exp:'32 - 15 = 17 erkek'},
{cat:'Sıralama',q:"Hangi sayı sırayı tamamlar? 3, 6, 12, 24, ?",a:48,opts:[36,42,48,30],exp:'Her sayı 2 ile çarpılır: 24 × 2 = 48'},
{cat:'İşlem',q:"Bir çiftlikte 12 tavuk ve 8 inek var. Toplam kaç ayak var?",a:56,opts:[40,56,48,60],exp:'12×2=24 tavuk ayağı + 8×4=32 inek ayağı = 56'},
{cat:'Mantık',q:"Bugün Salı ise 3 gün sonra hangi gün olur?",a:0,opts:['Cuma','Perşembe','Cumartesi','Çarşamba'],exp:'Salı→Çarşamba→Perşembe→Cuma'},
{cat:'İşlem',q:"Ece 3 kutuya eşit sayıda kalem koydu. Toplamda 27 kalem var. Her kutuda kaç kalem var?",a:9,opts:[7,8,9,10],exp:'27 ÷ 3 = 9 kalem'},
{cat:'Mantık',q:"Bir sayı 4'e bölündüğünde 3 kalıyor. 3'e bölündüğünde 2 kalıyor. Bu sayı hangisi?",a:11,opts:[7,9,11,13],exp:'11÷4=2 kalan 3 ✓, 11÷3=3 kalan 2 ✓'},
{cat:'İşlem',q:"Bir otobüste 45 yolcu var. İlk durakta 12 kişi indi, 8 kişi bindi. Otobüste kaç yolcu var?",a:41,opts:[41,39,43,37],exp:'45 - 12 + 8 = 41 yolcu'},
{cat:'Sıralama',q:"Hangi sayı sırayı tamamlar? 100, 90, 81, 73, ?",a:66,opts:[64,65,66,68],exp:'Farklar: 10, 9, 8, 7 → 73 - 7 = 66'},
{cat:'İşlem',q:"Bir pastanın yarısının yarısı kaçta kaçtır?",a:0,opts:['1/4','1/2','1/3','1/8'],exp:'1/2 × 1/2 = 1/4'},
{cat:'Mantık',q:"5 arkadaş birbirleriyle birer kez tokalaştı. Toplam kaç tokalaşma oldu?",a:10,opts:[8,10,12,15],exp:'5×4/2 = 10 tokalaşma'},
{cat:'İşlem',q:"Mert'in doğum günü 15 gün sonra. Bugün ayın 18'i ise doğum günü ayın kaçı?",a:0,opts:['3','33','2','1'],exp:'18 + 15 = 33 → sonraki ayın 3\\'ü (30 gün varsayımı)'}
];
let usedProblems=[];
function genProblem(){
if(usedProblems.length>=PROBLEMS.length)usedProblems=[];
let idx;
do{idx=Math.floor(Math.random()*PROBLEMS.length)}while(usedProblems.includes(idx));
usedProblems.push(idx);
const p=PROBLEMS[idx];
let opts=p.opts.slice();
let correctVal=p.a;
if(typeof opts[0]==='string'){correctVal=opts[p.a]}
shuffle(opts);
let correctIdx=0;
if(typeof p.opts[0]==='string'){correctIdx=opts.indexOf(p.opts[p.a])}
else{correctIdx=opts.indexOf(p.a)}
curProblem={cat:p.cat,q:p.q,opts:opts,correctIdx:correctIdx,exp:p.exp};
answered=false;feedback='';feedbackTimer=0;showExpl=false;explanation=''}
function wrapText(text,x,y,maxW,lineH){
const words=text.split(' ');let line='';let ly=y;
for(const w of words){const test=line+w+' ';
if(ctx.measureText(test).width>maxW&&line!==''){ctx.fillText(line.trim(),x,ly);ly+=lineH;line=w+' '}
else line=test}
ctx.fillText(line.trim(),x,ly);return ly+lineH}
function draw(){ctx.clearRect(0,0,W,H);
const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e2e8f0';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
ctx.fillText('🧠 Problem Çözme Kartları',W/2,180);ctx.font='20px Segoe UI';
ctx.fillText('Sözel problemleri oku ve çöz!',W/2,230);
ctx.fillText('Mantık, işlem ve sıralama soruları!',W/2,260);
ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.roundRect(W/2-80,305,160,40,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('▶ BAŞLA',W/2,330);return}
if(state==='win'){ctx.fillStyle='#fbbf24';ctx.font='bold 38px Segoe UI';ctx.textAlign='center';
ctx.fillText('TEBRİKLER!',W/2,200);ctx.font='26px Segoe UI';ctx.fillStyle='#e2e8f0';
ctx.fillText('Puan: '+score+'/100',W/2,260);ctx.font='20px Segoe UI';
ctx.fillText('Problem çözme ustası oldun!',W/2,300);
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
if(!curProblem)return;
ctx.fillStyle='#e2e8f0';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxR+'   Puan: '+score,W/2,30);
const catClr=curProblem.cat==='İşlem'?'#3b82f6':curProblem.cat==='Mantık'?'#8b5cf6':'#10b981';
ctx.fillStyle=catClr+'30';ctx.beginPath();ctx.roundRect(W/2-50,42,100,26,8);ctx.fill();
ctx.fillStyle=catClr;ctx.font='bold 13px Segoe UI';ctx.fillText(curProblem.cat,W/2,59);
const cardX=60,cardY=80,cardW=W-120,cardH=200;
ctx.fillStyle='#94A3B8';ctx.beginPath();ctx.roundRect(cardX,cardY,cardW,cardH,16);ctx.fill();
ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.stroke();
ctx.fillStyle='#f59e0b';ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
ctx.fillText('Soru '+round,cardX+20,cardY+28);
ctx.fillStyle='#e2e8f0';ctx.font='18px Segoe UI';ctx.textAlign='center';
wrapText(curProblem.q,W/2,cardY+65,cardW-40,26);
const optY=310,optH=55,optGap=12;
for(let i=0;i<curProblem.opts.length;i++){
const oy=optY+i*(optH+optGap);
let bgClr='#94A3B8',borderClr='#475569';
if(answered){
if(i===curProblem.correctIdx){bgClr='#064e3b';borderClr='#10b981'}
else{bgClr='#94A3B8';borderClr='#334155'}}
ctx.fillStyle=bgClr;ctx.beginPath();ctx.roundRect(100,oy,W-200,optH,12);ctx.fill();
ctx.strokeStyle=borderClr;ctx.lineWidth=2;ctx.stroke();
const labels=['A','B','C','D'];
ctx.fillStyle='#94a3b8';ctx.font='bold 16px Segoe UI';ctx.textAlign='left';
ctx.fillText(labels[i]+')',115,oy+optH/2+6);
ctx.fillStyle='#e2e8f0';ctx.font='18px Segoe UI';ctx.textAlign='left';
ctx.fillText(''+curProblem.opts[i],150,oy+optH/2+6)}
if(showExpl&&explanation){
const ey=optY+4*(optH+optGap)+5;
ctx.fillStyle='#1e3a5f';ctx.beginPath();ctx.roundRect(80,ey,W-160,50,10);ctx.fill();
ctx.fillStyle='#93c5fd';ctx.font='15px Segoe UI';ctx.textAlign='center';
ctx.fillText('💡 '+explanation,W/2,ey+30)}
if(feedbackTimer>0){
ctx.fillStyle=feedback.includes('Doğru')?'#10b981':'#ef4444';
ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.globalAlpha=Math.min(1,feedbackTimer);
ctx.fillText(feedback,W/2,H-20);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=lastT?Math.min((t-lastT)/1000,0.1):0.016;lastT=t;
if(feedbackTimer>0)feedbackTimer-=dt;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.02;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function handleClick(mx,my){
if(state==='start'){if(my>300&&my<350&&mx>W/2-80&&mx<W/2+80){state='play';score=0;round=1;usedProblems=[];genProblem()}return}
if(state==='win')return;
if(state!=='play'||!curProblem)return;
if(answered){return}
const optY=310,optH=55,optGap=12;
for(let i=0;i<curProblem.opts.length;i++){
const oy=optY+i*(optH+optGap);
if(mx>=100&&mx<=W-100&&my>=oy&&my<=oy+optH){
answered=true;
if(i===curProblem.correctIdx){score+=10;beep(523,0.15);addP(W/2,oy+optH/2,'#10b981');
feedback='Doğru! +10';feedbackTimer=2}
else{beep(180,0.3);feedback='Yanlış! Doğru cevap: '+curProblem.opts[curProblem.correctIdx];feedbackTimer=2.5}
explanation=curProblem.exp;showExpl=true;
round++;
if(round>maxR)setTimeout(()=>{state='win';for(let i=0;i<30;i++)addP(Math.random()*W,Math.random()*H,'#fbbf24')},2000);
else setTimeout(()=>{genProblem()},2200);
return}}}
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();handleClick((e.clientX-r.left)*(W/r.width),(e.clientY-r.top)*(H/r.height))});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0],r=cv.getBoundingClientRect();handleClick((t.clientX-r.left)*(W/r.width),(t.clientY-r.top)*(H/r.height))});
requestAnimationFrame(upd);
</script></body></html>"""
