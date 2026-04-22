# -*- coding: utf-8 -*-
"""Okul Öncesi Genel Yetenek Oyunları — 20 Premium HTML5 Oyun (Bölüm C: 11-15)."""


def _build_prek_ab_labirent_html():
    """Labirent Mini — Basit labirentte yolu bul, 10 tur, artan zorluk."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxRound=10,score=0,particles=[];
let maze=[],cols=5,rows=5,cellW=0,cellH=0,ox=0,oy=0;
let px=0,py=0,ex=0,ey=0,trail=[],animX=0,animY=0,animating=false;
const WALL_COLORS=['#a78bfa','#f472b6','#38bdf8','#fbbf24','#34d399'];
let wallColor='#a78bfa';
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function getMazeSize(){if(round<=3)return 5;if(round<=7)return 6;return 7}
function generateMaze(){const sz=getMazeSize();cols=sz;rows=sz;
maze=[];for(let r=0;r<rows;r++){maze[r]=[];for(let c=0;c<cols;c++){maze[r][c]={top:true,right:true,bottom:true,left:true,visited:false}}}
const stack=[];let cr=0,cc=0;maze[cr][cc].visited=true;stack.push([cr,cc]);
while(stack.length>0){const neighbors=[];const dr=[[-1,0],[1,0],[0,-1],[0,1]];
dr.forEach(([ddr,ddc])=>{const nr=cr+ddr,nc=cc+ddc;if(nr>=0&&nr<rows&&nc>=0&&nc<cols&&!maze[nr][nc].visited)neighbors.push([nr,nc,ddr,ddc])});
if(neighbors.length>0){const[nr,nc,ddr,ddc]=neighbors[Math.floor(Math.random()*neighbors.length)];
if(ddr===-1){maze[cr][cc].top=false;maze[nr][nc].bottom=false}
if(ddr===1){maze[cr][cc].bottom=false;maze[nr][nc].top=false}
if(ddc===-1){maze[cr][cc].left=false;maze[nr][nc].right=false}
if(ddc===1){maze[cr][cc].right=false;maze[nr][nc].left=false}
stack.push([cr,cc]);cr=nr;cc=nc;maze[cr][cc].visited=true}
else{const p=stack.pop();cr=p[0];cc=p[1]}}
const maxCell=Math.min(Math.floor(480/cols),Math.floor(420/rows));
cellW=maxCell;cellH=maxCell;
ox=Math.floor((W-cols*cellW)/2);oy=Math.floor((H-rows*cellH)/2)+20;
px=0;py=0;ex=cols-1;ey=rows-1;
animX=px;animY=py;trail=[[px,py]];
wallColor=WALL_COLORS[Math.floor(Math.random()*WALL_COLORS.length)]}
function canMove(r,c,dr,dc){if(r+dr<0||r+dr>=rows||c+dc<0||c+dc>=cols)return false;
if(dr===-1)return!maze[r][c].top;if(dr===1)return!maze[r][c].bottom;
if(dc===-1)return!maze[r][c].left;if(dc===1)return!maze[r][c].right;return false}
function movePlayer(dr,dc){if(animating||state!=='play')return;
if(!canMove(py,px,dr,dc))return;
animating=true;const tx=px+dc,ty=py+dr;
const startAX=animX,startAY=animY;const dur=120;const t0=performance.now();
function anim(now){const p=Math.min((now-t0)/dur,1);const ep=1-(1-p)*(1-p);
animX=startAX+(tx-startAX)*ep;animY=startAY+(ty-startAY)*ep;
if(p>=1){animX=tx;animY=ty;px=tx;py=ty;animating=false;
trail.push([px,py]);
if(px===ex&&py===ey){score+=10;snd(true);
addP(ox+ex*cellW+cellW/2,oy+ey*cellH+cellH/2);
round++;if(round>maxRound){state='win'}else{setTimeout(generateMaze,500)}}
return}requestAnimationFrame(anim)}requestAnimationFrame(anim)}
function drawMaze(){for(let r=0;r<rows;r++){for(let c=0;c<cols;c++){
const x=ox+c*cellW,y=oy+r*cellH;
ctx.fillStyle=(r+c)%2===0?'#1e1b4b':'#1a1740';ctx.fillRect(x,y,cellW,cellH);
ctx.strokeStyle=wallColor;ctx.lineWidth=3;
if(maze[r][c].top){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+cellW,y);ctx.stroke()}
if(maze[r][c].bottom){ctx.beginPath();ctx.moveTo(x,y+cellH);ctx.lineTo(x+cellW,y+cellH);ctx.stroke()}
if(maze[r][c].left){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y+cellH);ctx.stroke()}
if(maze[r][c].right){ctx.beginPath();ctx.moveTo(x+cellW,y);ctx.lineTo(x+cellW,y+cellH);ctx.stroke()}}}}
function drawTrail(){ctx.globalAlpha=0.25;trail.forEach(([tx,ty],i)=>{
ctx.fillStyle='#fbbf24';ctx.beginPath();
ctx.arc(ox+tx*cellW+cellW/2,oy+ty*cellH+cellH/2,cellW*0.15,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function drawBtns(){const bw=56,bh=46,gap=4,cx=W-100,cy=H-90;
const btns=[{l:'↑',dx:0,dy:-1,bx:cx,by:cy-bh-gap},{l:'↓',dx:0,dy:1,bx:cx,by:cy+bh+gap},
{l:'←',dx:-1,dy:0,bx:cx-bw-gap,by:cy},{l:'→',dx:1,dy:0,bx:cx+bw+gap,by:cy}];
btns.forEach(b=>{ctx.fillStyle='#7c3aed';ctx.beginPath();ctx.roundRect(b.bx-bw/2,b.by-bh/2,bw,bh,10);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(b.l,b.bx,b.by)});ctx.textBaseline='alphabetic';return btns}
let btnDefs=[];
function draw(){ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🐣 Labirent Mini',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Çıkışa ulaş! Ok butonlarını kullan.',W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,300,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Tebrikler! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'   Puan: '+score,W/2,25);
drawMaze();drawTrail();
const exx=ox+ex*cellW+cellW/2,exy=oy+ey*cellH+cellH/2;
ctx.font=Math.floor(cellW*0.6)+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText('⭐',exx,exy);
const pxx=ox+animX*cellW+cellW/2,pxy=oy+animY*cellH+cellH/2;
ctx.font=Math.floor(cellW*0.65)+'px Segoe UI';ctx.fillText('🐣',pxx,pxy);
ctx.textBaseline='alphabetic';
btnDefs=drawBtns();
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>300&&m.y<350){state='play';score=0;round=1;generateMaze()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;generateMaze()}return}
if(state==='play'){
const bw=56,bh=46,gap=4,cx=W-100,cy=H-90;
const btns=[{dx:0,dy:-1,bx:cx,by:cy-bh-gap},{dx:0,dy:1,bx:cx,by:cy+bh+gap},
{dx:-1,dy:0,bx:cx-bw-gap,by:cy},{dx:1,dy:0,bx:cx+bw+gap,by:cy}];
for(const b of btns){if(m.x>b.bx-bw/2&&m.x<b.bx+bw/2&&m.y>b.by-bh/2&&m.y<b.by+bh/2){movePlayer(b.dy,b.dx);return}}
const mc=Math.floor((m.x-ox)/cellW),mr=Math.floor((m.y-oy)/cellH);
if(mc>=0&&mc<cols&&mr>=0&&mr<rows){const ddx=mc-px,ddy=mr-py;
if(Math.abs(ddx)+Math.abs(ddy)===1)movePlayer(ddy,ddx)}}});
document.addEventListener('keydown',e=>{if(state!=='play')return;
if(e.key==='ArrowUp')movePlayer(-1,0);else if(e.key==='ArrowDown')movePlayer(1,0);
else if(e.key==='ArrowLeft')movePlayer(0,-1);else if(e.key==='ArrowRight')movePlayer(0,1)});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_ab_parca_butun_html():
    """Parça-Bütün (Puzzle 4-9 Parça) — Şekilleri sürükleyerek puzzle tamamla."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxRound=10,score=0,particles=[];
let pieces=[],gridCols=2,gridRows=2,cellW=0,cellH=0,gridOx=0,gridOy=0;
let dragging=null,dragOx=0,dragOy=0,placed=0;
let refShapeIdx=0;
const SHAPES=[
{name:'Ev',draw:function(cx,cy,sz,c){c.fillStyle='#ef4444';c.beginPath();c.moveTo(cx,cy-sz*0.45);c.lineTo(cx+sz*0.45,cy);c.lineTo(cx-sz*0.45,cy);c.closePath();c.fill();c.fillStyle='#fbbf24';c.fillRect(cx-sz*0.35,cy,sz*0.7,sz*0.45);c.fillStyle='#7c3aed';c.fillRect(cx-sz*0.1,cy+sz*0.15,sz*0.2,sz*0.3)}},
{name:'Ağaç',draw:function(cx,cy,sz,c){c.fillStyle='#854d0e';c.fillRect(cx-sz*0.08,cy+sz*0.1,sz*0.16,sz*0.35);c.fillStyle='#22c55e';c.beginPath();c.arc(cx,cy-sz*0.05,sz*0.32,0,Math.PI*2);c.fill();c.fillStyle='#16a34a';c.beginPath();c.arc(cx,cy+sz*0.05,sz*0.25,0,Math.PI*2);c.fill()}},
{name:'Araba',draw:function(cx,cy,sz,c){c.fillStyle='#3b82f6';c.beginPath();c.roundRect(cx-sz*0.4,cy-sz*0.1,sz*0.8,sz*0.3,6);c.fill();c.fillStyle='#60a5fa';c.beginPath();c.roundRect(cx-sz*0.25,cy-sz*0.3,sz*0.5,sz*0.22,5);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.arc(cx-sz*0.22,cy+sz*0.2,sz*0.1,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+sz*0.22,cy+sz*0.2,sz*0.1,0,Math.PI*2);c.fill()}},
{name:'Balık',draw:function(cx,cy,sz,c){c.fillStyle='#f97316';c.beginPath();c.ellipse(cx,cy,sz*0.38,sz*0.22,0,0,Math.PI*2);c.fill();c.fillStyle='#ea580c';c.beginPath();c.moveTo(cx+sz*0.35,cy);c.lineTo(cx+sz*0.5,cy-sz*0.2);c.lineTo(cx+sz*0.5,cy+sz*0.2);c.closePath();c.fill();c.fillStyle='#fff';c.beginPath();c.arc(cx-sz*0.18,cy-sz*0.04,sz*0.07,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.arc(cx-sz*0.17,cy-sz*0.04,sz*0.035,0,Math.PI*2);c.fill()}},
{name:'Çiçek',draw:function(cx,cy,sz,c){const cols=['#f472b6','#a78bfa','#fb923c','#38bdf8','#34d399'];for(let i=0;i<5;i++){const a=i*Math.PI*2/5-Math.PI/2;c.fillStyle=cols[i];c.beginPath();c.arc(cx+Math.cos(a)*sz*0.2,cy+Math.sin(a)*sz*0.2,sz*0.16,0,Math.PI*2);c.fill()}c.fillStyle='#fbbf24';c.beginPath();c.arc(cx,cy,sz*0.12,0,Math.PI*2);c.fill();c.fillStyle='#22c55e';c.fillRect(cx-sz*0.04,cy+sz*0.25,sz*0.08,sz*0.25)}},
{name:'Güneş',draw:function(cx,cy,sz,c){for(let i=0;i<8;i++){const a=i*Math.PI/4;c.strokeStyle='#fbbf24';c.lineWidth=3;c.beginPath();c.moveTo(cx+Math.cos(a)*sz*0.22,cy+Math.sin(a)*sz*0.22);c.lineTo(cx+Math.cos(a)*sz*0.4,cy+Math.sin(a)*sz*0.4);c.stroke()}c.fillStyle='#fbbf24';c.beginPath();c.arc(cx,cy,sz*0.2,0,Math.PI*2);c.fill();c.fillStyle='#f59e0b';c.beginPath();c.arc(cx-sz*0.05,cy-sz*0.03,sz*0.03,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+sz*0.07,cy-sz*0.03,sz*0.03,0,Math.PI*2);c.fill()}},
{name:'Yıldız',draw:function(cx,cy,sz,c){c.fillStyle='#fbbf24';c.beginPath();for(let i=0;i<5;i++){const ao=i*Math.PI*2/5-Math.PI/2;const ai=ao+Math.PI/5;c.lineTo(cx+Math.cos(ao)*sz*0.4,cy+Math.sin(ao)*sz*0.4);c.lineTo(cx+Math.cos(ai)*sz*0.18,cy+Math.sin(ai)*sz*0.18)}c.closePath();c.fill()}},
{name:'Kalp',draw:function(cx,cy,sz,c){c.fillStyle='#ef4444';c.beginPath();c.moveTo(cx,cy+sz*0.3);c.bezierCurveTo(cx-sz*0.5,cy-sz*0.1,cx-sz*0.5,cy-sz*0.45,cx,cy-sz*0.15);c.bezierCurveTo(cx+sz*0.5,cy-sz*0.45,cx+sz*0.5,cy-sz*0.1,cx,cy+sz*0.3);c.fill()}},
{name:'Kelebek',draw:function(cx,cy,sz,c){c.fillStyle='#a78bfa';c.beginPath();c.ellipse(cx-sz*0.22,cy-sz*0.12,sz*0.2,sz*0.15,-.3,0,Math.PI*2);c.fill();c.fillStyle='#f472b6';c.beginPath();c.ellipse(cx+sz*0.22,cy-sz*0.12,sz*0.2,sz*0.15,.3,0,Math.PI*2);c.fill();c.fillStyle='#c084fc';c.beginPath();c.ellipse(cx-sz*0.18,cy+sz*0.12,sz*0.16,sz*0.12,-.2,0,Math.PI*2);c.fill();c.fillStyle='#e879f9';c.beginPath();c.ellipse(cx+sz*0.18,cy+sz*0.12,sz*0.16,sz*0.12,.2,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.fillRect(cx-sz*0.025,cy-sz*0.25,sz*0.05,sz*0.5)}},
{name:'Bulut',draw:function(cx,cy,sz,c){c.fillStyle='#e0f2fe';c.beginPath();c.arc(cx-sz*0.15,cy,sz*0.18,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+sz*0.15,cy,sz*0.18,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx,cy-sz*0.1,sz*0.22,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx,cy+sz*0.05,sz*0.2,0,Math.PI*2);c.fill()}}
];
const PIECE_BG=['#7c3aed','#2563eb','#dc2626','#059669','#d97706','#be185d','#0891b2','#7c2d12','#4338ca'];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:1,clr:'#fbbf24',r:3+Math.random()*3})}
function getGrid(){if(round<=3)return{c:2,r:2};if(round<=7)return{c:3,r:2};return{c:3,r:3}}
function setup(){const g=getGrid();gridCols=g.c;gridRows=g.r;
const total=gridCols*gridRows;cellW=Math.floor(280/gridCols);cellH=Math.floor(280/gridRows);
gridOx=Math.floor((W-gridCols*cellW)/2);gridOy=160;
refShapeIdx=Math.floor(Math.random()*SHAPES.length);
placed=0;pieces=[];
for(let r=0;r<gridRows;r++){for(let c=0;c<gridCols;c++){
const idx=r*gridCols+c;
let sx,sy;
if(idx%2===0){sx=30+Math.random()*80;sy=140+Math.random()*350}
else{sx=W-180+Math.random()*80;sy=140+Math.random()*350}
pieces.push({idx,gr:r,gc:c,x:sx,y:sy,tx:gridOx+c*cellW,ty:gridOy+r*cellH,placed:false,bg:PIECE_BG[idx%PIECE_BG.length]})}}}
function drawRef(){const sz=70,cx=W/2,cy=82;
ctx.strokeStyle='#a78bfa60';ctx.lineWidth=1;ctx.setLineDash([4,4]);ctx.strokeRect(cx-sz/2-4,cy-sz/2-4,sz+8,sz+8);ctx.setLineDash([]);
SHAPES[refShapeIdx].draw(cx,cy,sz,ctx);
ctx.fillStyle='#e9d5ff';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText('Örnek: '+SHAPES[refShapeIdx].name,cx,cy+sz/2+16)}
function drawPieceContent(px,py,pw,ph,gc,gr){
const offCanvas=document.createElement('canvas');offCanvas.width=gridCols*cellW;offCanvas.height=gridRows*cellH;
const oc=offCanvas.getContext('2d');
SHAPES[refShapeIdx].draw(gridCols*cellW/2,gridRows*cellH/2,Math.min(gridCols*cellW,gridRows*cellH)*0.85,oc);
ctx.save();ctx.beginPath();ctx.rect(px,py,pw,ph);ctx.clip();
ctx.drawImage(offCanvas,gc*cellW,gr*cellH,cellW,cellH,px,py,pw,ph);ctx.restore()}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('🧩 Parça-Bütün Puzzle',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Parçaları sürükleyip yerine koy!',W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,300,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Harika! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'   Puan: '+score,W/2,25);
drawRef();
ctx.strokeStyle='#a78bfa40';ctx.lineWidth=1;ctx.setLineDash([6,4]);
for(let r=0;r<gridRows;r++){for(let c=0;c<gridCols;c++){ctx.strokeRect(gridOx+c*cellW,gridOy+r*cellH,cellW,cellH)}}
ctx.setLineDash([]);
pieces.filter(p=>p.placed).forEach(p=>{ctx.fillStyle=p.bg;ctx.fillRect(p.x,p.y,cellW,cellH);drawPieceContent(p.x,p.y,cellW,cellH,p.gc,p.gr);ctx.strokeStyle='#10b981';ctx.lineWidth=2;ctx.strokeRect(p.x,p.y,cellW,cellH)});
pieces.filter(p=>!p.placed).forEach(p=>{ctx.fillStyle=p.bg;ctx.beginPath();ctx.roundRect(p.x,p.y,cellW,cellH,8);ctx.fill();drawPieceContent(p.x,p.y,cellW,cellH,p.gc,p.gr);ctx.strokeStyle='#e9d5ff';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(p.x,p.y,cellW,cellH,8);ctx.stroke()});
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('mousedown',e=>{const m=gp(e);if(state!=='play')return;
for(let i=pieces.length-1;i>=0;i--){const p=pieces[i];if(!p.placed&&m.x>p.x&&m.x<p.x+cellW&&m.y>p.y&&m.y<p.y+cellH){dragging=p;dragOx=m.x-p.x;dragOy=m.y-p.y;break}}});
cv.addEventListener('mousemove',e=>{if(!dragging)return;const m=gp(e);dragging.x=m.x-dragOx;dragging.y=m.y-dragOy});
cv.addEventListener('mouseup',()=>{if(!dragging)return;
const p=dragging;dragging=null;
const dist=Math.hypot((p.x+cellW/2)-(p.tx+cellW/2),(p.y+cellH/2)-(p.ty+cellH/2));
if(dist<35){p.x=p.tx;p.y=p.ty;p.placed=true;placed++;snd(true);addP(p.tx+cellW/2,p.ty+cellH/2);
if(placed>=pieces.length){score+=10;round++;if(round>maxRound){state='win'}else{setTimeout(setup,600)}}}});
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>300&&m.y<350){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setup()}return}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}))});
cv.addEventListener('touchend',()=>cv.dispatchEvent(new MouseEvent('mouseup',{})));
upd();
</script></body></html>"""


def _build_prek_ab_duygu_yuzleri_html():
    """Duygu Yüzleri — Doğru duygu ifadesini bul, 10 tur."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxRound=10,score=0,particles=[];
const EMOTIONS_BASE=[
{name:'Mutlu',q:'Mutlu yüzü bul!',draw:function(cx,cy,r,c){c.fillStyle='#fbbf24';c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.arc(cx-r*0.3,cy-r*0.15,r*0.08,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+r*0.3,cy-r*0.15,r*0.08,0,Math.PI*2);c.fill();c.strokeStyle='#1e1b4b';c.lineWidth=3;c.beginPath();c.arc(cx,cy+r*0.05,r*0.35,0.1*Math.PI,0.9*Math.PI);c.stroke()}},
{name:'Üzgün',q:'Üzgün yüzü bul!',draw:function(cx,cy,r,c){c.fillStyle='#60a5fa';c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.arc(cx-r*0.3,cy-r*0.15,r*0.08,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+r*0.3,cy-r*0.15,r*0.08,0,Math.PI*2);c.fill();c.strokeStyle='#1e1b4b';c.lineWidth=3;c.beginPath();c.arc(cx,cy+r*0.35,r*0.3,1.1*Math.PI,1.9*Math.PI);c.stroke();c.fillStyle='#38bdf8';c.beginPath();c.ellipse(cx+r*0.35,cy+r*0.05,r*0.06,r*0.1,0,0,Math.PI*2);c.fill()}},
{name:'Kızgın',q:'Kızgın yüzü bul!',draw:function(cx,cy,r,c){c.fillStyle='#ef4444';c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.arc(cx-r*0.3,cy-r*0.05,r*0.08,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+r*0.3,cy-r*0.05,r*0.08,0,Math.PI*2);c.fill();c.strokeStyle='#1e1b4b';c.lineWidth=3;c.beginPath();c.moveTo(cx-r*0.45,cy-r*0.3);c.lineTo(cx-r*0.15,cy-r*0.15);c.stroke();c.beginPath();c.moveTo(cx+r*0.45,cy-r*0.3);c.lineTo(cx+r*0.15,cy-r*0.15);c.stroke();c.beginPath();c.moveTo(cx-r*0.3,cy+r*0.3);c.lineTo(cx+r*0.3,cy+r*0.3);c.stroke()}},
{name:'Şaşkın',q:'Şaşkın yüzü bul!',draw:function(cx,cy,r,c){c.fillStyle='#a78bfa';c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.arc(cx-r*0.3,cy-r*0.15,r*0.1,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+r*0.3,cy-r*0.15,r*0.1,0,Math.PI*2);c.fill();c.strokeStyle='#1e1b4b';c.lineWidth=2;c.beginPath();c.arc(cx-r*0.3,cy-r*0.3,r*0.2,0,Math.PI*2);c.stroke();c.beginPath();c.arc(cx+r*0.3,cy-r*0.3,r*0.2,0,Math.PI*2);c.stroke();c.fillStyle='#1e1b4b';c.beginPath();c.ellipse(cx,cy+r*0.3,r*0.15,r*0.2,0,0,Math.PI*2);c.fill()}}
];
const EMOTIONS_EXTRA=[
{name:'Uykulu',q:'Uykulu yüzü bul!',draw:function(cx,cy,r,c){c.fillStyle='#c4b5fd';c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.fill();c.strokeStyle='#1e1b4b';c.lineWidth=3;c.beginPath();c.arc(cx-r*0.3,cy-r*0.1,r*0.12,0,Math.PI);c.stroke();c.beginPath();c.arc(cx+r*0.3,cy-r*0.1,r*0.12,0,Math.PI);c.stroke();c.fillStyle='#1e1b4b';c.beginPath();c.ellipse(cx,cy+r*0.3,r*0.2,r*0.08,0,0,Math.PI*2);c.fill();c.fillStyle='#e9d5ff';c.font=(r*0.35)+'px Segoe UI';c.textAlign='center';c.fillText('z',cx+r*0.5,cy-r*0.4);c.font=(r*0.25)+'px Segoe UI';c.fillText('z',cx+r*0.65,cy-r*0.6)}},
{name:'Korkmuş',q:'Korkmuş yüzü bul!',draw:function(cx,cy,r,c){c.fillStyle='#86efac';c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(cx-r*0.28,cy-r*0.12,r*0.14,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+r*0.28,cy-r*0.12,r*0.14,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.arc(cx-r*0.28,cy-r*0.12,r*0.06,0,Math.PI*2);c.fill();c.beginPath();c.arc(cx+r*0.28,cy-r*0.12,r*0.06,0,Math.PI*2);c.fill();c.fillStyle='#1e1b4b';c.beginPath();c.ellipse(cx,cy+r*0.3,r*0.12,r*0.18,0,0,Math.PI*2);c.fill();c.strokeStyle='#1e1b4b';c.lineWidth=2;c.beginPath();c.moveTo(cx-r*0.42,cy-r*0.35);c.lineTo(cx-r*0.15,cy-r*0.28);c.stroke();c.beginPath();c.moveTo(cx+r*0.42,cy-r*0.35);c.lineTo(cx+r*0.15,cy-r*0.28);c.stroke()}}
];
let EMOTIONS=[...EMOTIONS_BASE];
let cards=[],target=0,answered=false,feedback='',feedbackTimer=0,correctIdx=-1,wrongIdx=-1,bounceT=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#fbbf24',r:3+Math.random()*4})}
function setup(){if(round>5)EMOTIONS=[...EMOTIONS_BASE,...EMOTIONS_EXTRA];else EMOTIONS=[...EMOTIONS_BASE];
const pool=[...EMOTIONS].sort(()=>Math.random()-.5);
cards=pool.slice(0,4);
target=Math.floor(Math.random()*4);
answered=false;feedback='';feedbackTimer=0;correctIdx=-1;wrongIdx=-1;bounceT=0}
function cardRect(i){const cw=130,ch=150,gap=20,totalW=4*cw+3*gap,sx=(W-totalW)/2;
return{x:sx+i*(cw+gap),y:280,w:cw,h:ch}}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('😊 Duygu Yüzleri',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Doğru duygu ifadesini bul!',W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,300,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Süper! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'   Puan: '+score,W/2,30);
ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';
if(cards.length>0&&cards[target])ctx.fillText(cards[target].q,W/2,80);
for(let i=0;i<4;i++){if(i>=cards.length)continue;
const cr=cardRect(i);let offY=0;
if(i===correctIdx&&bounceT>0){offY=-Math.abs(Math.sin(bounceT*0.15))*15}
if(i===wrongIdx&&feedbackTimer>0){offY=Math.sin(feedbackTimer*0.8)*5}
ctx.fillStyle=(i===correctIdx&&answered)?'#10b98140':'#1e1b4b';
ctx.strokeStyle=(i===correctIdx&&answered)?'#10b981':'#a78bfa';ctx.lineWidth=3;
ctx.beginPath();ctx.roundRect(cr.x,cr.y+offY,cr.w,cr.h,14);ctx.fill();ctx.stroke();
cards[i].draw(cr.x+cr.w/2,cr.y+offY+cr.h/2-15,Math.min(cr.w,cr.h)*0.3,ctx);
ctx.fillStyle='#e9d5ff';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
if(answered)ctx.fillText(cards[i].name,cr.x+cr.w/2,cr.y+offY+cr.h-10)}
if(feedback){ctx.fillStyle=feedback==='Doğru!'?'#10b981':'#ef4444';ctx.font='bold 32px Segoe UI';ctx.textAlign='center';ctx.fillText(feedback,W/2,240)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
if(bounceT>0)bounceT--;if(feedbackTimer>0)feedbackTimer--;draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>300&&m.y<350){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setup()}return}
if(state!=='play'||answered)return;
for(let i=0;i<4;i++){const cr=cardRect(i);
if(m.x>cr.x&&m.x<cr.x+cr.w&&m.y>cr.y&&m.y<cr.y+cr.h){
answered=true;
if(i===target){score+=10;snd(true);feedback='Doğru!';correctIdx=i;bounceT=40;
addP(cr.x+cr.w/2,cr.y+cr.h/2)}
else{snd(false);feedback='Yanlış!';wrongIdx=i;correctIdx=target;feedbackTimer=30}
setTimeout(()=>{round++;if(round>maxRound){state='win'}else{setup()}},1500);
break}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_ab_sayma_dokunusu_html():
    """1-10 Sayma Dokunuşu — Hedef sayıda nesneye dokun, 10 tur."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxRound=10,score=0,particles=[];
const ITEM_SETS=[
{emoji:'🍎',name:'Elma'},{emoji:'⭐',name:'Yıldız'},{emoji:'❤️',name:'Kalp'},
{emoji:'🌸',name:'Çiçek'},{emoji:'🎈',name:'Balon'},{emoji:'🐟',name:'Balık'},
{emoji:'🍊',name:'Portakal'},{emoji:'🦋',name:'Kelebek'},{emoji:'🔵',name:'Top'},
{emoji:'🍓',name:'Çilek'}
];
let items=[],targetCount=0,selectedCount=0,currentSet=null,showResult=false,resultOk=false,resultTimer=0;
let btnPulse=0;
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:'#fbbf24',r:3+Math.random()*4})}
function setup(){targetCount=round<=10?round:Math.floor(Math.random()*10)+1;
currentSet=ITEM_SETS[(round-1)%ITEM_SETS.length];
const totalItems=targetCount+2+Math.floor(Math.random()*3);
items=[];selectedCount=0;showResult=false;resultTimer=0;
const cols=Math.ceil(Math.sqrt(totalItems*1.3));
const rowH=Math.ceil(totalItems/cols);
const cw=Math.min(90,Math.floor((W-100)/cols));
const ch=Math.min(90,Math.floor(340/rowH));
const startX=(W-cols*cw)/2;const startY=180;
for(let i=0;i<totalItems;i++){
const col=i%cols,row=Math.floor(i/cols);
const bx=startX+col*cw+cw/2+Math.random()*20-10;
const by=startY+row*ch+ch/2+Math.random()*20-10;
items.push({x:bx,y:by,selected:false,scale:1})}}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('👆 Sayma Dokunuşu',W/2,200);ctx.font='20px Segoe UI';ctx.fillText('Doğru sayıda nesneye dokun!',W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,300,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Muhteşem! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'   Puan: '+score,W/2,25);
if(currentSet){ctx.fillStyle='#fbbf24';ctx.font='bold 28px Segoe UI';
ctx.fillText(targetCount+' '+currentSet.name+'ya Dokun! '+currentSet.emoji,W/2,75)}
ctx.fillStyle='#a78bfa';ctx.font='bold 20px Segoe UI';
ctx.fillText('Seçilen: '+selectedCount+' / '+targetCount,W/2,115);
items.forEach((it,i)=>{const sz=it.selected?48:40;
ctx.font=sz+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
if(currentSet)ctx.fillText(currentSet.emoji,it.x,it.y);
if(it.selected){ctx.strokeStyle='#10b981';ctx.lineWidth=3;ctx.beginPath();ctx.arc(it.x,it.y,28,0,Math.PI*2);ctx.stroke();
ctx.fillStyle='#10b981';ctx.font='bold 18px Segoe UI';ctx.fillText('✓',it.x+22,it.y-18)}});
ctx.textBaseline='alphabetic';
btnPulse+=0.05;const ps=1+Math.sin(btnPulse)*0.05;
const btnW=140*ps,btnH=44*ps,btnX=W/2-btnW/2,btnY=H-80;
ctx.fillStyle=showResult?'#4b5563':'#10b981';ctx.beginPath();ctx.roundRect(btnX,btnY,btnW,btnH,12);ctx.fill();
ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tamam!',W/2,btnY+btnH/2+7);
if(showResult){ctx.fillStyle=resultOk?'#10b981':'#ef4444';ctx.font='bold 30px Segoe UI';
ctx.fillText(resultOk?'Doğru! +10':'Yanlış! Doğru: '+targetCount,W/2,H-120)}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
function upd(){particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
function checkSubmit(){if(showResult)return;
showResult=true;resultOk=selectedCount===targetCount;
if(resultOk){score+=10;snd(true);addP(W/2,H/2)}else{snd(false)}
resultTimer=setTimeout(()=>{round++;if(round>maxRound){state='win'}else{setup()}},1800)}
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>300&&m.y<350){state='play';score=0;round=1;setup()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setup()}return}
if(state!=='play')return;
if(showResult)return;
const btnW=140,btnH=44,btnX=W/2-btnW/2,btnY=H-80;
if(m.x>btnX&&m.x<btnX+btnW&&m.y>btnY&&m.y<btnY+btnH){checkSubmit();return}
for(let i=items.length-1;i>=0;i--){const it=items[i];
if(Math.hypot(m.x-it.x,m.y-it.y)<32){
it.selected=!it.selected;selectedCount=items.filter(t=>t.selected).length;
snd(it.selected);break}}});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
upd();
</script></body></html>"""


def _build_prek_ab_hizli_dokun_html():
    """Hızlı Dokun (Dikkat / Go-NoGo) — Hedef nesneye hızlıca dokun, 10 tur."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
let state='start',round=1,maxRound=10,score=0,particles=[];
const TARGET_SETS=[
{target:'⭐',distractors:['🔶','🔷','🔵','🟡']},
{target:'❤️',distractors:['🧡','💛','💜','🖤']},
{target:'🐱',distractors:['🐶','🐰','🐻','🐼']},
{target:'🍎',distractors:['🍊','🍋','🍇','🍓']},
{target:'🌸',distractors:['🌻','🌺','🌷','🌼']},
{target:'🚗',distractors:['🚕','🚙','🏍️','🚲']},
{target:'⚽',distractors:['🏀','🏈','🎾','⚾']},
{target:'🎵',distractors:['🎶','🎸','🥁','🎺']},
{target:'🦋',distractors:['🐞','🐝','🐛','🦗']},
{target:'🌙',distractors:['☀️','💫','✨','🔥']}
];
let currentSetIdx=0,subRound=0,maxSub=4,currentObj='',isTarget=false;
let tapped=false,showTime=1500,showTimer=0,feedbackText='',feedbackColor='',feedbackTimer=0;
let flashColor='',flashTimer=0,objScale=1,objPulse=0;
let roundScore=0,roundItems=[];
function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=0.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.4);o.stop(a.currentTime+0.4)}catch(e){}}
function addP(x,y,clr){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,life:1,clr:clr||'#fbbf24',r:3+Math.random()*4})}
function getShowTime(){if(round<=3)return 1500;if(round<=7)return 1100;return 800}
function setupRound(){currentSetIdx=(round-1)%TARGET_SETS.length;
const set=TARGET_SETS[currentSetIdx];
maxSub=3+Math.floor(Math.random()*3);
roundItems=[];
const targetCount=1+Math.floor(Math.random()*2);
for(let i=0;i<targetCount;i++)roundItems.push({obj:set.target,isTarget:true});
for(let i=0;i<maxSub-targetCount;i++){roundItems.push({obj:set.distractors[Math.floor(Math.random()*set.distractors.length)],isTarget:false})}
roundItems.sort(()=>Math.random()-.5);
subRound=0;roundScore=0;showTime=getShowTime();nextSub()}
function nextSub(){if(subRound>=roundItems.length){score+=roundScore;round++;
if(round>maxRound){state='win';return}
setTimeout(setupRound,800);return}
const item=roundItems[subRound];currentObj=item.obj;isTarget=item.isTarget;
tapped=false;showTimer=showTime;feedbackText='';feedbackTimer=0;flashTimer=0;objScale=0.3;objPulse=0}
function handleTap(){if(state!=='play'||tapped||showTimer<=0)return;
tapped=true;
if(isTarget){roundScore+=10;feedbackText='+10';feedbackColor='#10b981';flashColor='#10b98130';flashTimer=20;
snd(true);addP(W/2,H/2+30,'#10b981')}
else{roundScore=Math.max(0,roundScore-5);feedbackText='-5 Hayır!';feedbackColor='#ef4444';flashColor='#ef444430';flashTimer=20;
snd(false)}
feedbackTimer=40;showTimer=Math.min(showTimer,400)}
function draw(){ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#1a0533');bg.addColorStop(1,'#0d0221');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
if(flashTimer>0){ctx.fillStyle=flashColor;ctx.fillRect(0,0,W,H)}
if(state==='start'){ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';ctx.fillText('⚡ Hızlı Dokun',W/2,180);ctx.font='20px Segoe UI';ctx.fillText('Yalnızca hedef nesne gelince dokun!',W/2,230);ctx.fillText('Başka nesneye dokunma!',W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,300,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,332);return}
if(state==='win'){ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';ctx.fillText('🎉 Bravo! 🎉',W/2,200);ctx.font='24px Segoe UI';ctx.fillText('Puan: '+score,W/2,260);ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,310,160,50,14);ctx.fill();ctx.fillStyle='#fff';ctx.font='bold 20px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,342);particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return}
ctx.fillStyle='#e9d5ff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
ctx.fillText('Tur: '+round+'/'+maxRound+'   Puan: '+score,W/2,30);
const set=TARGET_SETS[currentSetIdx];
ctx.fillStyle='#fbbf24';ctx.font='bold 22px Segoe UI';
ctx.fillText('Yalnızca '+set.target+' gelince dokun!',W/2,75);
ctx.fillStyle='#a78bfa60';ctx.font='14px Segoe UI';
const subText=(subRound+1)+'/'+roundItems.length;
ctx.fillText('Gösterim: '+subText,W/2,100);
const barW=200,barH=8,barX=(W-barW)/2,barY=110;
ctx.fillStyle='#1e1b4b';ctx.fillRect(barX,barY,barW,barH);
ctx.fillStyle='#a78bfa';ctx.fillRect(barX,barY,barW*(showTimer/showTime),barH);
if(showTimer>0){
objPulse+=0.08;const sc=Math.min(objScale+(1-objScale)*0.15,1);objScale=sc;
const baseSize=100*objScale;
ctx.font=baseSize+'px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';
ctx.fillText(currentObj,W/2,H/2+20);
ctx.textBaseline='alphabetic';
if(isTarget){ctx.fillStyle='#10b98180';ctx.font='16px Segoe UI';ctx.fillText('DOKUN!',W/2,H/2+100)}
}
if(feedbackTimer>0){ctx.fillStyle=feedbackColor;ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
ctx.globalAlpha=feedbackTimer/40;ctx.fillText(feedbackText,W/2,H/2-80);ctx.globalAlpha=1}
particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1}
let lastT=0;
function upd(t){const dt=t-lastT;lastT=t;
if(state==='play'&&showTimer>0){showTimer-=dt;
if(showTimer<=0){showTimer=0;
if(!tapped){if(isTarget){feedbackText='Kaçırdın!';feedbackColor='#f59e0b';feedbackTimer=35}
else{roundScore+=5;feedbackText='✓ Doğru!';feedbackColor='#10b981';feedbackTimer=35}}
setTimeout(()=>{subRound++;nextSub()},600)}}
if(flashTimer>0)flashTimer--;if(feedbackTimer>0)feedbackTimer--;
particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=0.025;p.vy+=0.1});particles=particles.filter(p=>p.life>0);
draw();requestAnimationFrame(upd)}
function gp(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)}}
cv.addEventListener('click',e=>{const m=gp(e);
if(state==='start'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>300&&m.y<350){state='play';score=0;round=1;setupRound()}return}
if(state==='win'){if(m.x>W/2-80&&m.x<W/2+80&&m.y>310&&m.y<360){state='play';score=0;round=1;setupRound()}return}
handleTap()});
cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))});
requestAnimationFrame(upd);
</script></body></html>"""
