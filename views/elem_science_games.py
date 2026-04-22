# -*- coding: utf-8 -*-
"""İlkokul Eğlenceli Bilim Oyunları — 20 Premium HTML5 Oyun (Bölüm A: 1-5)."""


def _build_elem_sci_basit_devre_html():
    """Basit Devre Kur — Devre elemanlarını sürükle-bırak, ampulü yak."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[];
let nodes=[],wires=[],components=[],palette=[],dragComp=null,dragOx=0,dragOy=0;
let circuitComplete=false,bulbGlow=0,flowDots=[],hintArrow=null,animT=0;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

function buildLevel(){
    nodes=[];wires=[];components=[];palette=[];circuitComplete=false;bulbGlow=0;flowDots=[];hintArrow=null;
    if(round<=3){
        /* Simple series: battery-wire-bulb-wire back */
        nodes=[{x:200,y:250,id:'n0'},{x:500,y:250,id:'n1'},{x:500,y:450,id:'n2'},{x:200,y:450,id:'n3'}];
        wires=[{from:'n0',to:'n1',placed:true},{from:'n1',to:'n2',placed:true},{from:'n2',to:'n3',placed:true},{from:'n3',to:'n0',placed:true}];
        /* slots: battery at left, bulb at right */
        components=[
            {type:'battery',emoji:'🔋',label:'Pil',slot:{x:200,y:350},placed:false,x:0,y:0,w:70,h:40},
            {type:'bulb',emoji:'💡',label:'Ampul',slot:{x:500,y:350},placed:false,x:0,y:0,w:60,h:40}
        ];
        palette=[{type:'battery',emoji:'🔋',label:'Pil',px:120,py:80},{type:'bulb',emoji:'💡',label:'Ampul',px:280,py:80}];
    } else if(round<=7){
        /* Series with switch */
        nodes=[{x:150,y:230,id:'n0'},{x:350,y:230,id:'n1'},{x:550,y:230,id:'n2'},{x:550,y:450,id:'n3'},{x:350,y:450,id:'n4'},{x:150,y:450,id:'n5'}];
        wires=[{from:'n0',to:'n1',placed:true},{from:'n1',to:'n2',placed:true},{from:'n2',to:'n3',placed:true},{from:'n3',to:'n4',placed:true},{from:'n4',to:'n5',placed:true},{from:'n5',to:'n0',placed:true}];
        components=[
            {type:'battery',emoji:'🔋',label:'Pil',slot:{x:150,y:340},placed:false,x:0,y:0,w:70,h:40},
            {type:'switch',emoji:'🔌',label:'Anahtar',slot:{x:350,y:340},placed:false,x:0,y:0,w:70,h:40},
            {type:'bulb',emoji:'💡',label:'Ampul',slot:{x:550,y:340},placed:false,x:0,y:0,w:60,h:40}
        ];
        palette=[{type:'battery',emoji:'🔋',label:'Pil',px:100,py:80},{type:'switch',emoji:'🔌',label:'Anahtar',px:280,py:80},{type:'bulb',emoji:'💡',label:'Ampul',px:460,py:80}];
    } else {
        /* Parallel: battery + switch, two bulbs */
        nodes=[{x:130,y:220,id:'n0'},{x:350,y:220,id:'n1'},{x:570,y:220,id:'n2'},
               {x:570,y:340,id:'n3'},{x:570,y:460,id:'n4'},{x:350,y:460,id:'n5'},
               {x:130,y:460,id:'n6'},{x:130,y:340,id:'n7'},{x:350,y:340,id:'n8'}];
        wires=[{from:'n0',to:'n1',placed:true},{from:'n1',to:'n2',placed:true},{from:'n2',to:'n3',placed:true},
               {from:'n3',to:'n4',placed:true},{from:'n4',to:'n5',placed:true},{from:'n5',to:'n6',placed:true},
               {from:'n6',to:'n7',placed:true},{from:'n7',to:'n0',placed:true},{from:'n1',to:'n8',placed:true},{from:'n8',to:'n5',placed:true}];
        components=[
            {type:'battery',emoji:'🔋',label:'Pil',slot:{x:130,y:340},placed:false,x:0,y:0,w:70,h:40},
            {type:'switch',emoji:'🔌',label:'Anahtar',slot:{x:350,y:160},placed:false,x:0,y:0,w:70,h:40},
            {type:'bulb',emoji:'💡',label:'Ampul 1',slot:{x:570,y:340},placed:false,x:0,y:0,w:60,h:40},
            {type:'bulb2',emoji:'💡',label:'Ampul 2',slot:{x:350,y:340},placed:false,x:0,y:0,w:60,h:40}
        ];
        palette=[{type:'battery',emoji:'🔋',label:'Pil',px:70,py:80},{type:'switch',emoji:'🔌',label:'Anahtar',px:210,py:80},
                 {type:'bulb',emoji:'💡',label:'Ampul 1',px:380,py:80},{type:'bulb2',emoji:'💡',label:'Ampul 2',px:540,py:80}];
    }
    /* place palette items at their starting positions */
    components.forEach((c,i)=>{c.x=palette[i].px;c.y=palette[i].py});
}

function checkCircuit(){
    circuitComplete=components.every(c=>c.placed);
    if(circuitComplete){
        bulbGlow=1;
        /* create flow dots */
        flowDots=[];
        wires.forEach(w=>{
            const fn=nodes.find(n=>n.id===w.from),tn=nodes.find(n=>n.id===w.to);
            if(fn&&tn)flowDots.push({fx:fn.x,fy:fn.y,tx:tn.x,ty:tn.y,t:Math.random()});
        });
    }
}

function getNode(id){return nodes.find(n=>n.id===id)}

function drawWire(f,t,glow){
    ctx.strokeStyle=glow?'#fbbf24':'#60a5fa';ctx.lineWidth=glow?4:3;
    ctx.shadowColor=glow?'#fbbf24':'transparent';ctx.shadowBlur=glow?10:0;
    ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(t.x,t.y);ctx.stroke();
    ctx.shadowBlur=0;
}

function drawNode(n){
    ctx.beginPath();ctx.arc(n.x,n.y,8,0,Math.PI*2);
    ctx.fillStyle='#1e1b4b';ctx.fill();ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;ctx.stroke();
}

function drawComponent(c){
    const cx=c.placed?c.slot.x:c.x,cy=c.placed?c.slot.y:c.y;
    if(dragComp===c){return;} /* drawn separately while dragging */
    drawCompAt(c,cx,cy);
}

function drawCompAt(c,cx,cy){
    /* background box */
    const glow=circuitComplete&&(c.type==='bulb'||c.type==='bulb2');
    ctx.fillStyle=glow?'rgba(251,191,36,0.3)':'#1e1b4b';
    ctx.strokeStyle=c.placed?'#34d399':'#a78bfa';ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(cx-35,cy-22,70,44,10);ctx.fill();ctx.stroke();
    if(glow){ctx.shadowColor='#fbbf24';ctx.shadowBlur=20;ctx.beginPath();ctx.roundRect(cx-35,cy-22,70,44,10);ctx.fill();ctx.shadowBlur=0;}
    ctx.font='24px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#fff';ctx.fillText(c.emoji,cx,cy);
    ctx.font='11px Segoe UI';ctx.fillStyle='#e9d5ff';ctx.fillText(c.label,cx,cy+30);
    ctx.textBaseline='alphabetic';
}

function drawSlotHint(c){
    if(c.placed)return;
    ctx.setLineDash([5,5]);ctx.strokeStyle='#a78bfa60';ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(c.slot.x-35,c.slot.y-22,70,44,10);ctx.stroke();
    ctx.setLineDash([]);
    ctx.font='10px Segoe UI';ctx.textAlign='center';ctx.fillStyle='#a78bfa80';ctx.fillText(c.label+' buraya',c.slot.x,c.slot.y+38);
}

function draw(){
    ctx.clearRect(0,0,W,H);
    const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    animT+=0.02;

    if(state==='start'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
        ctx.fillText('⚡ Basit Devre Kur',W/2,160);
        ctx.font='20px Segoe UI';ctx.fillText('Devre elemanlarını doğru yere sürükle!',W/2,210);
        ctx.fillText('Ampulü yakarak devreyi tamamla.',W/2,240);
        ctx.font='60px Segoe UI';ctx.fillText('🔋💡🔌',W/2,340);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,400,160,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,432);
        return;
    }
    if(state==='win'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
        ctx.fillText('🏆 Tebrikler! Devre Ustası!',W/2,180);
        ctx.font='22px Segoe UI';ctx.fillText('Toplam Puan: '+score,W/2,230);
        ctx.fillText('10/10 devre tamamlandı!',W/2,270);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,320,180,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,352);
        particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
        return;
    }

    /* HUD */
    ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='left';ctx.fillText('⚡ Tur: '+round+'/'+maxR,15,25);
    ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,25);
    /* progress bar */
    ctx.fillStyle='#1e1b4b';ctx.fillRect(200,12,300,10);
    ctx.fillStyle='#34d399';ctx.fillRect(200,12,300*((round-1)/maxR),10);

    /* palette area */
    ctx.fillStyle='#0d022180';ctx.fillRect(30,55,640,60);
    ctx.strokeStyle='#a78bfa40';ctx.lineWidth=1;ctx.strokeRect(30,55,640,60);
    ctx.fillStyle='#a78bfa80';ctx.font='11px Segoe UI';ctx.textAlign='left';ctx.fillText('Elemanlar (sürükle)',40,70);

    /* draw board */
    ctx.strokeStyle='#1e1b4b';ctx.lineWidth=1;
    for(let x=50;x<W-50;x+=40){for(let y=130;y<H-30;y+=40){ctx.fillStyle='#0d022140';ctx.fillRect(x,y,1,1)}}

    /* wires */
    wires.forEach(w=>{
        const f=getNode(w.from),t=getNode(w.to);
        if(f&&t)drawWire(f,t,circuitComplete);
    });

    /* flow dots animation */
    if(circuitComplete){
        flowDots.forEach(d=>{
            d.t=(d.t+0.015)%1;
            const dx=d.fx+(d.tx-d.fx)*d.t,dy=d.fy+(d.ty-d.fy)*d.t;
            ctx.beginPath();ctx.arc(dx,dy,4,0,Math.PI*2);
            ctx.fillStyle='#fbbf24';ctx.shadowColor='#fbbf24';ctx.shadowBlur=8;ctx.fill();ctx.shadowBlur=0;
        });
    }

    /* nodes */
    nodes.forEach(n=>drawNode(n));

    /* slot hints */
    components.forEach(c=>drawSlotHint(c));

    /* components */
    components.forEach(c=>drawComponent(c));

    /* dragged component on top */
    if(dragComp){drawCompAt(dragComp,dragComp.x,dragComp.y);}

    /* hint arrow for next component to place */
    if(!circuitComplete){
        const next=components.find(c=>!c.placed);
        if(next&&!dragComp){
            const sx=next.placed?next.slot.x:next.x, sy=next.placed?next.slot.y:next.y;
            const tx=next.slot.x, ty=next.slot.y;
            const pulse=Math.sin(animT*3)*5;
            ctx.strokeStyle='#fbbf2480';ctx.lineWidth=2;ctx.setLineDash([6,4]);
            ctx.beginPath();ctx.moveTo(sx,sy+22);ctx.lineTo(tx,ty-30+pulse);ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle='#fbbf24';ctx.font='16px Segoe UI';ctx.textAlign='center';
            ctx.fillText('▼',tx,ty-28+pulse);
        }
    }

    /* success message */
    if(circuitComplete){
        ctx.fillStyle='#34d399';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
        ctx.fillText('✅ Devre tamamlandı! Ampul yanıyor!',W/2,H-50);
        const gp=Math.sin(animT*4)*0.3+0.7;
        ctx.globalAlpha=gp;ctx.font='50px Segoe UI';ctx.fillText('💡',W/2,H-90);ctx.globalAlpha=1;
    }

    /* particles */
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

let completedTimer=0;
function upd(){
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
    if(state==='play'&&circuitComplete){
        completedTimer++;
        if(completedTimer>90){
            completedTimer=0;
            score+=10;
            snd(true);addP(W/2,300,'#fbbf24');addP(W/2,300,'#34d399');
            round++;
            if(round>maxR){state='win';}else{buildLevel();}
        }
    }
    draw();requestAnimationFrame(upd);
}

function isInComp(mx,my,c){
    const cx=c.placed?c.slot.x:c.x, cy=c.placed?c.slot.y:c.y;
    return mx>cx-35&&mx<cx+35&&my>cy-22&&my<cy+22;
}

function isInSlot(mx,my,c){
    return Math.abs(mx-c.slot.x)<45&&Math.abs(my-c.slot.y)<30;
}

cv.addEventListener('mousedown',e=>{
    if(state!=='play'||circuitComplete)return;
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    for(let i=components.length-1;i>=0;i--){
        const c=components[i];
        if(!c.placed&&isInComp(mx,my,c)){
            dragComp=c;dragOx=mx-c.x;dragOy=my-c.y;break;
        }
    }
});
cv.addEventListener('mousemove',e=>{
    if(!dragComp)return;
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    dragComp.x=mx-dragOx;dragComp.y=my-dragOy;
});
cv.addEventListener('mouseup',e=>{
    if(!dragComp)return;
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(isInSlot(mx,my,dragComp)){
        dragComp.placed=true;
        snd(true);addP(dragComp.slot.x,dragComp.slot.y,'#34d399');
        checkCircuit();
    } else {
        /* snap back to palette */
        const pi=components.indexOf(dragComp);
        if(pi>=0&&pi<palette.length){dragComp.x=palette[pi].px;dragComp.y=palette[pi].py;}
    }
    dragComp=null;
});

cv.addEventListener('click',e=>{
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>400&&my<450){state='play';score=0;round=1;buildLevel();}return;}
    if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>320&&my<370){state='play';score=0;round=1;buildLevel();}return;}
});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
    const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);
    if(state!=='play'||circuitComplete){cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));return;}
    for(let i=components.length-1;i>=0;i--){
        const c=components[i];
        if(!c.placed&&isInComp(mx,my,c)){dragComp=c;dragOx=mx-c.x;dragOy=my-c.y;break;}
    }
},{passive:false});
cv.addEventListener('touchmove',e=>{e.preventDefault();if(!dragComp)return;const t=e.touches[0];
    const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);
    dragComp.x=mx-dragOx;dragComp.y=my-dragOy;
},{passive:false});
cv.addEventListener('touchend',e=>{e.preventDefault();if(!dragComp){return;}
    /* use last known position */
    if(isInSlot(dragComp.x,dragComp.y,dragComp)){
        dragComp.placed=true;snd(true);addP(dragComp.slot.x,dragComp.slot.y,'#34d399');checkCircuit();
    } else {
        const pi=components.indexOf(dragComp);
        if(pi>=0&&pi<palette.length){dragComp.x=palette[pi].px;dragComp.y=palette[pi].py;}
    }
    dragComp=null;
},{passive:false});

buildLevel();
upd();
</script></body></html>"""


def _build_elem_sci_iletken_yalitkan_html():
    """İletken–Yalıtkan Testi — Nesneyi devreye koy, ampulü yak."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=0,maxR=10,particles=[];
let objects=[
    {name:'Demir Anahtar',emoji:'🔑',conductor:true},
    {name:'Lastik',emoji:'🟤',conductor:false},
    {name:'Cam Bardak',emoji:'🥛',conductor:false},
    {name:'Bakır Tel',emoji:'🔌',conductor:true},
    {name:'Tahta Çubuk',emoji:'🪵',conductor:false},
    {name:'Alüminyum Folyo',emoji:'🪞',conductor:true},
    {name:'Plastik Kaşık',emoji:'🥄',conductor:false},
    {name:'Demir Çivi',emoji:'🪛',conductor:true},
    {name:'Kurşun Kalem Ucu',emoji:'✏️',conductor:true},
    {name:'Kağıt',emoji:'📄',conductor:false}
];
let shuffled=[...objects];
let currentObj=null,dragObj=null,dragX=0,dragY=0,objX=0,objY=0;
let placed=false,testResult=null,testTimer=0,bulbOn=false;
let classified={iletken:[],yalitkan:[]};
let animT=0,flowDots=[];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

function shuffle(arr){for(let i=arr.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}return arr}

function startRound(){
    if(round>=maxR){state='win';return;}
    currentObj=shuffled[round];
    objX=W/2;objY=160;
    placed=false;testResult=null;testTimer=0;bulbOn=false;
    flowDots=[];
}

/* Circuit positions */
const batX=100,batY=380,bulbX=600,bulbY=380;
const gapX=W/2,gapY=380;
const wireTop=320,wireBot=440;

function drawCircuit(){
    ctx.lineWidth=4;
    /* left wire: battery+ to gap left */
    ctx.strokeStyle=bulbOn?'#fbbf24':'#60a5fa';ctx.shadowColor=bulbOn?'#fbbf24':'transparent';ctx.shadowBlur=bulbOn?8:0;
    ctx.beginPath();ctx.moveTo(batX+40,batY);ctx.lineTo(gapX-50,gapY);ctx.stroke();
    /* right wire: gap right to bulb */
    ctx.beginPath();ctx.moveTo(gapX+50,gapY);ctx.lineTo(bulbX-40,bulbY);ctx.stroke();
    /* bottom wire: bulb back to battery */
    ctx.beginPath();ctx.moveTo(bulbX,bulbY+30);ctx.lineTo(bulbX,wireBot);ctx.lineTo(batX,wireBot);ctx.lineTo(batX,batY+30);ctx.stroke();
    ctx.shadowBlur=0;

    /* gap zone */
    ctx.setLineDash([6,4]);ctx.strokeStyle='#fbbf2480';ctx.lineWidth=2;
    ctx.strokeRect(gapX-50,gapY-30,100,60);ctx.setLineDash([]);
    if(!placed){ctx.fillStyle='#fbbf2440';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText('Buraya bırak',gapX,gapY+50);}

    /* battery */
    ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#ef4444';ctx.lineWidth=3;
    ctx.beginPath();ctx.roundRect(batX-30,batY-25,60,50,8);ctx.fill();ctx.stroke();
    ctx.fillStyle='#ef4444';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';ctx.fillText('+',batX+18,batY-12);
    ctx.fillStyle='#60a5fa';ctx.fillText('−',batX-18,batY-12);
    ctx.font='22px Segoe UI';ctx.fillText('🔋',batX,batY+8);

    /* bulb */
    if(bulbOn){
        ctx.shadowColor='#fbbf24';ctx.shadowBlur=30;
        ctx.beginPath();ctx.arc(bulbX,bulbY,28,0,Math.PI*2);ctx.fillStyle='#fbbf24';ctx.fill();
        ctx.shadowBlur=15;ctx.fill();ctx.shadowBlur=0;
        ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText('💡',bulbX,bulbY+10);
    } else {
        ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
        ctx.beginPath();ctx.arc(bulbX,bulbY,28,0,Math.PI*2);ctx.fill();ctx.stroke();
        ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText('💡',bulbX,bulbY+10);
    }

    /* flow dots if conducting */
    if(bulbOn){
        if(flowDots.length===0){
            for(let i=0;i<8;i++)flowDots.push({t:i/8});
        }
        flowDots.forEach(d=>{
            d.t=(d.t+0.01)%1;
            let fx,fy;
            /* trace path: bat -> gap -> bulb -> bottom -> bat */
            const seg=d.t*4;
            if(seg<1){const s=seg;fx=batX+40+(gapX-50-batX-40)*s;fy=batY;}
            else if(seg<2){const s=seg-1;fx=gapX+50+(bulbX-40-gapX-50)*s;fy=bulbY;}
            else if(seg<3){const s=seg-2;fx=bulbX+(batX-bulbX)*s;fy=wireBot;}
            else{const s=seg-3;fx=batX;fy=wireBot+(batY+30-wireBot)*s;}
            ctx.beginPath();ctx.arc(fx,fy,4,0,Math.PI*2);ctx.fillStyle='#fbbf24';ctx.shadowColor='#fbbf24';ctx.shadowBlur=6;ctx.fill();ctx.shadowBlur=0;
        });
    }
}

function drawClassTable(){
    const tableY=490,tableW=300,colW=150,rowH=22;
    /* table header */
    ctx.fillStyle='#1e1b4b';ctx.fillRect(W/2-tableW/2,tableY,tableW,30);
    ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;ctx.strokeRect(W/2-tableW/2,tableY,tableW,30);
    ctx.fillStyle='#34d399';ctx.font='bold 13px Segoe UI';ctx.textAlign='center';ctx.fillText('İletken ✓',W/2-colW/2,tableY+20);
    ctx.fillStyle='#ef4444';ctx.fillText('Yalıtkan ✗',W/2+colW/2,tableY+20);
    /* divider */
    ctx.beginPath();ctx.moveTo(W/2,tableY);ctx.lineTo(W/2,tableY+30+Math.max(classified.iletken.length,classified.yalitkan.length)*rowH);ctx.strokeStyle='#a78bfa40';ctx.stroke();
    /* items */
    const maxItems=Math.max(classified.iletken.length,classified.yalitkan.length);
    for(let i=0;i<maxItems;i++){
        const y=tableY+34+i*rowH;
        if(i<classified.iletken.length){ctx.fillStyle='#34d39980';ctx.font='12px Segoe UI';ctx.textAlign='center';ctx.fillText(classified.iletken[i],W/2-colW/2,y);}
        if(i<classified.yalitkan.length){ctx.fillStyle='#ef444480';ctx.fillText(classified.yalitkan[i],W/2+colW/2,y);}
    }
}

function draw(){
    ctx.clearRect(0,0,W,H);
    const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    animT+=0.02;

    if(state==='start'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
        ctx.fillText('🔬 İletken–Yalıtkan Testi',W/2,160);
        ctx.font='20px Segoe UI';ctx.fillText('Nesneyi devreye koy, ampul yanarsa iletken!',W/2,210);
        ctx.fillText('10 farklı nesneyi test et.',W/2,240);
        ctx.font='50px Segoe UI';ctx.fillText('🔋🔑💡',W/2,330);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,380,160,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,412);return;
    }
    if(state==='win'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
        ctx.fillText('🏆 Deney Tamamlandı!',W/2,100);
        ctx.font='22px Segoe UI';ctx.fillText('Puan: '+score+'/100',W/2,140);
        drawClassTable();
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,H-60,180,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,H-28);
        particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
        return;
    }

    /* HUD */
    ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='left';ctx.fillText('🔬 Tur: '+(round+1)+'/'+maxR,15,25);
    ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,25);
    ctx.fillStyle='#1e1b4b';ctx.fillRect(200,12,300,10);ctx.fillStyle='#34d399';ctx.fillRect(200,12,300*(round/maxR),10);

    /* circuit */
    drawCircuit();

    /* object to test (draggable or placed) */
    if(currentObj){
        const ox=placed?gapX:objX, oy=placed?gapY:objY;
        if(!dragObj||!placed){
            ctx.fillStyle='#1e1b4b';ctx.strokeStyle=COLORS[round%COLORS.length];ctx.lineWidth=3;
            ctx.beginPath();ctx.roundRect(ox-45,oy-30,90,60,12);ctx.fill();ctx.stroke();
            ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.fillText(currentObj.emoji,ox,oy+4);
            ctx.font='bold 12px Segoe UI';ctx.fillStyle='#e9d5ff';ctx.fillText(currentObj.name,ox,oy+40);
        }
        if(dragObj){
            ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#fbbf24';ctx.lineWidth=3;
            ctx.beginPath();ctx.roundRect(objX-45,objY-30,90,60,12);ctx.fill();ctx.stroke();
            ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.fillText(currentObj.emoji,objX,objY+4);
            ctx.font='bold 12px Segoe UI';ctx.fillStyle='#e9d5ff';ctx.fillText(currentObj.name,objX,objY+40);
        }
    }

    /* test result feedback */
    if(testResult!==null){
        ctx.font='bold 24px Segoe UI';ctx.textAlign='center';
        if(testResult){
            ctx.fillStyle='#34d399';ctx.fillText('İletken! ✓  Ampul yandı! +10',W/2,280);
        } else {
            ctx.fillStyle='#ef4444';ctx.fillText('Yalıtkan! ✗  Ampul yanmadı.',W/2,280);
        }
    }

    /* classification table */
    drawClassTable();

    /* particles */
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function upd(){
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
    if(state==='play'&&testResult!==null){
        testTimer++;
        if(testTimer>80){round++;startRound();}
    }
    draw();requestAnimationFrame(upd);
}

function placeObject(){
    placed=true;
    if(currentObj.conductor){
        bulbOn=true;testResult=true;score+=10;
        snd(true);addP(bulbX,bulbY,'#fbbf24');addP(gapX,gapY,'#34d399');
        classified.iletken.push(currentObj.emoji+' '+currentObj.name);
    } else {
        bulbOn=false;testResult=false;
        snd(false);addP(gapX,gapY,'#ef4444');
        classified.yalitkan.push(currentObj.emoji+' '+currentObj.name);
    }
}

cv.addEventListener('mousedown',e=>{
    if(state!=='play'||placed)return;
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(currentObj&&Math.abs(mx-objX)<45&&Math.abs(my-objY)<30){dragObj=true;dragX=mx-objX;dragY=my-objY;}
});
cv.addEventListener('mousemove',e=>{
    if(!dragObj)return;
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    objX=mx-dragX;objY=my-dragY;
});
cv.addEventListener('mouseup',e=>{
    if(!dragObj)return;dragObj=false;
    if(Math.abs(objX-gapX)<60&&Math.abs(objY-gapY)<40){placeObject();}
    else{objX=W/2;objY=160;}
});

cv.addEventListener('click',e=>{
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>380&&my<430){state='play';score=0;round=0;classified={iletken:[],yalitkan:[]};shuffled=shuffle([...objects]);startRound();}return;}
    if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>H-60&&my<H-10){state='play';score=0;round=0;classified={iletken:[],yalitkan:[]};shuffled=shuffle([...objects]);startRound();}return;}
});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
    const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);
    if(state!=='play'||placed){cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));return;}
    if(currentObj&&Math.abs(mx-objX)<45&&Math.abs(my-objY)<30){dragObj=true;dragX=mx-objX;dragY=my-objY;}
},{passive:false});
cv.addEventListener('touchmove',e=>{e.preventDefault();if(!dragObj)return;const t=e.touches[0];
    const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);
    objX=mx-dragX;objY=my-dragY;
},{passive:false});
cv.addEventListener('touchend',e=>{e.preventDefault();if(!dragObj)return;dragObj=false;
    if(Math.abs(objX-gapX)<60&&Math.abs(objY-gapY)<40){placeObject();}else{objX=W/2;objY=160;}
},{passive:false});

upd();
</script></body></html>"""


def _build_elem_sci_kuvvet_yonu_html():
    """Kuvvet Yönü — Topa kuvvet uygula, hedefe ulaştır."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[],animT=0;

/* physics state */
let ballX=0,ballY=0,ballVX=0,ballVY=0,targetX=0,targetY=0;
let selectedDir=-1,selectedForce=1; /* 0=left,1=right,2=up,3=down; force 0=weak,1=med,2=strong */
let obstacles=[],trail=[],pushCount=0,maxPush=5,moving=false,won=false,wonTimer=0;
const friction=0.96,GRID=40,fieldL=50,fieldT=100,fieldW=600,fieldH=440;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

function buildLevel(){
    won=false;wonTimer=0;moving=false;pushCount=0;trail=[];selectedDir=-1;selectedForce=1;
    ballVX=0;ballVY=0;obstacles=[];
    if(round<=3){
        /* straight path */
        ballX=fieldL+60;ballY=fieldT+fieldH/2;
        targetX=fieldL+fieldW-80;targetY=fieldT+fieldH/2;
        maxPush=2;
    } else if(round<=7){
        /* need turns, obstacles */
        ballX=fieldL+60;ballY=fieldT+80;
        targetX=fieldL+fieldW-80;targetY=fieldT+fieldH-80;
        maxPush=round<=5?3:4;
        /* add walls */
        const wallCount=round-3;
        for(let i=0;i<wallCount;i++){
            obstacles.push({x:fieldL+150+i*120,y:fieldT+100+i*80,w:20,h:120+i*20});
        }
    } else {
        /* complex, moving target hint */
        ballX=fieldL+60;ballY=fieldT+fieldH/2;
        targetX=fieldL+fieldW-100;targetY=fieldT+60+(round-8)*100;
        maxPush=5;
        obstacles.push({x:fieldL+200,y:fieldT+80,w:20,h:200});
        obstacles.push({x:fieldL+380,y:fieldT+200,w:20,h:200});
        if(round>=10)obstacles.push({x:fieldL+280,y:fieldT+150,w:150,h:20});
    }
}

function applyForce(){
    if(moving||won||pushCount>=maxPush)return;
    if(selectedDir<0)return;
    const force=[4,8,14][selectedForce];
    const dx=[-1,1,0,0][selectedDir];
    const dy=[0,0,-1,1][selectedDir];
    ballVX+=dx*force;ballVY+=dy*force;
    pushCount++;moving=true;
    trail.push({x:ballX,y:ballY});
}

function checkCollision(){
    /* walls */
    if(ballX<fieldL+15){ballX=fieldL+15;ballVX=Math.abs(ballVX)*0.5;}
    if(ballX>fieldL+fieldW-15){ballX=fieldL+fieldW-15;ballVX=-Math.abs(ballVX)*0.5;}
    if(ballY<fieldT+15){ballY=fieldT+15;ballVY=Math.abs(ballVY)*0.5;}
    if(ballY>fieldT+fieldH-15){ballY=fieldT+fieldH-15;ballVY=-Math.abs(ballVY)*0.5;}
    /* obstacles */
    obstacles.forEach(o=>{
        if(ballX+12>o.x&&ballX-12<o.x+o.w&&ballY+12>o.y&&ballY-12<o.y+o.h){
            /* push out */
            const fromLeft=Math.abs(ballX-(o.x));
            const fromRight=Math.abs(ballX-(o.x+o.w));
            const fromTop=Math.abs(ballY-(o.y));
            const fromBot=Math.abs(ballY-(o.y+o.h));
            const minD=Math.min(fromLeft,fromRight,fromTop,fromBot);
            if(minD===fromLeft){ballX=o.x-13;ballVX=-Math.abs(ballVX)*0.4;}
            else if(minD===fromRight){ballX=o.x+o.w+13;ballVX=Math.abs(ballVX)*0.4;}
            else if(minD===fromTop){ballY=o.y-13;ballVY=-Math.abs(ballVY)*0.4;}
            else{ballY=o.y+o.h+13;ballVY=Math.abs(ballVY)*0.4;}
        }
    });
    /* target */
    if(Math.hypot(ballX-targetX,ballY-targetY)<30&&!won){
        won=true;score+=10;snd(true);addP(targetX,targetY,'#fbbf24');addP(targetX,targetY,'#34d399');
    }
}

function drawField(){
    /* grid */
    ctx.strokeStyle='#1e1b4b';ctx.lineWidth=1;
    for(let x=fieldL;x<=fieldL+fieldW;x+=GRID){ctx.beginPath();ctx.moveTo(x,fieldT);ctx.lineTo(x,fieldT+fieldH);ctx.stroke();}
    for(let y=fieldT;y<=fieldT+fieldH;y+=GRID){ctx.beginPath();ctx.moveTo(fieldL,y);ctx.lineTo(fieldL+fieldW,y);ctx.stroke();}
    /* border */
    ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;ctx.strokeRect(fieldL,fieldT,fieldW,fieldH);

    /* obstacles */
    obstacles.forEach(o=>{
        ctx.fillStyle='#7c3aed';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
        ctx.beginPath();ctx.roundRect(o.x,o.y,o.w,o.h,4);ctx.fill();ctx.stroke();
    });

    /* trail */
    for(let i=1;i<trail.length;i++){
        ctx.strokeStyle='#fbbf2440';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(trail[i-1].x,trail[i-1].y);ctx.lineTo(trail[i].x,trail[i].y);ctx.stroke();
    }
    if(trail.length>0){ctx.strokeStyle='#fbbf2440';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(trail[trail.length-1].x,trail[trail.length-1].y);ctx.lineTo(ballX,ballY);ctx.stroke();}

    /* target */
    const pulse=Math.sin(animT*3)*3;
    ctx.fillStyle='#34d39960';ctx.beginPath();ctx.arc(targetX,targetY,25+pulse,0,Math.PI*2);ctx.fill();
    ctx.font='28px Segoe UI';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🏁',targetX,targetY);

    /* ball */
    ctx.beginPath();ctx.arc(ballX,ballY,14,0,Math.PI*2);
    const bg=ctx.createRadialGradient(ballX-3,ballY-3,2,ballX,ballY,14);
    bg.addColorStop(0,'#ff6b9d');bg.addColorStop(1,'#c084fc');ctx.fillStyle=bg;ctx.fill();
    ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    ctx.textBaseline='alphabetic';
}

function drawControls(){
    const cx=W/2,cy=fieldT+fieldH+55;
    /* direction arrows */
    const dirs=[{label:'←',dx:-1,dy:0,bx:cx-90,by:cy},{label:'→',dx:1,dy:0,bx:cx-30,by:cy},{label:'↑',dx:0,dy:-1,bx:cx+30,by:cy},{label:'↓',dx:0,dy:1,bx:cx+90,by:cy}];
    dirs.forEach((d,i)=>{
        ctx.fillStyle=selectedDir===i?'#7c3aed':'#1e1b4b';ctx.strokeStyle=selectedDir===i?'#fbbf24':'#a78bfa';ctx.lineWidth=2;
        ctx.beginPath();ctx.roundRect(d.bx,d.by-18,50,36,8);ctx.fill();ctx.stroke();
        ctx.fillStyle=selectedDir===i?'#fbbf24':'#e9d5ff';ctx.font='bold 20px Segoe UI';ctx.textAlign='center';ctx.fillText(d.label,d.bx+25,d.by+7);
    });

    /* force selector */
    const forces=['Zayıf','Orta','Güçlü'];
    const fColors=['#60a5fa','#fbbf24','#ef4444'];
    forces.forEach((f,i)=>{
        const fx=cx+170+i*80,fy=cy;
        ctx.fillStyle=selectedForce===i?fColors[i]+'40':'#1e1b4b';ctx.strokeStyle=selectedForce===i?fColors[i]:'#a78bfa60';ctx.lineWidth=2;
        ctx.beginPath();ctx.roundRect(fx,fy-18,70,36,8);ctx.fill();ctx.stroke();
        ctx.fillStyle=selectedForce===i?fColors[i]:'#a78bfa';ctx.font='bold 12px Segoe UI';ctx.fillText(f,fx+35,fy+5);
    });

    /* apply button */
    const canApply=selectedDir>=0&&!moving&&!won&&pushCount<maxPush;
    ctx.fillStyle=canApply?'#34d399':'#1e1b4b60';ctx.beginPath();ctx.roundRect(cx-180,cy-18,80,36,8);ctx.fill();
    ctx.strokeStyle=canApply?'#34d399':'#a78bfa40';ctx.lineWidth=2;ctx.stroke();
    ctx.fillStyle=canApply?'#fff':'#a78bfa60';ctx.font='bold 14px Segoe UI';ctx.fillText('Uygula!',cx-140,cy+5);

    /* push counter */
    ctx.fillStyle='#e9d5ff80';ctx.font='12px Segoe UI';ctx.textAlign='left';ctx.fillText('Kalan itme: '+(maxPush-pushCount),15,cy+5);
}

function draw(){
    ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    animT+=0.03;

    if(state==='start'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
        ctx.fillText('💪 Kuvvet Yönü',W/2,160);
        ctx.font='20px Segoe UI';ctx.fillText('Topa kuvvet uygula, hedefe ulaştır!',W/2,210);
        ctx.fillText('Yön + güç seç, sonra "Uygula!" basla.',W/2,240);
        ctx.font='60px Segoe UI';ctx.fillText('⚽🏁',W/2,340);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,400,160,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,432);return;
    }
    if(state==='win'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
        ctx.fillText('🏆 Kuvvet Ustası!',W/2,180);
        ctx.font='22px Segoe UI';ctx.fillText('Toplam Puan: '+score,W/2,230);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,300,180,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,332);
        particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return;
    }

    /* HUD */
    ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='left';ctx.fillText('💪 Tur: '+round+'/'+maxR,15,25);
    ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,25);
    ctx.textAlign='center';ctx.fillStyle='#fbbf24';ctx.font='bold 14px Segoe UI';
    const diff=round<=3?'Kolay':round<=7?'Orta':'Zor';
    ctx.fillText(diff,W/2,25);
    ctx.fillStyle='#1e1b4b';ctx.fillRect(200,35,300,8);ctx.fillStyle='#34d399';ctx.fillRect(200,35,300*((round-1)/maxR),8);

    drawField();
    drawControls();

    /* win/fail messages */
    if(won){
        ctx.fillStyle='#34d399';ctx.font='bold 22px Segoe UI';ctx.textAlign='center';ctx.fillText('✅ Hedefe ulaştın! +10',W/2,fieldT-10);
    } else if(pushCount>=maxPush&&!moving){
        ctx.fillStyle='#ef4444';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('İtme hakkın bitti! Tekrar dene.',W/2,fieldT-10);
    }

    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function upd(){
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
    if(state==='play'){
        if(moving){
            ballX+=ballVX;ballY+=ballVY;
            ballVX*=friction;ballVY*=friction;
            checkCollision();
            if(Math.abs(ballVX)<0.2&&Math.abs(ballVY)<0.2){ballVX=0;ballVY=0;moving=false;}
        }
        if(won){
            wonTimer++;
            if(wonTimer>70){round++;if(round>maxR){state='win';}else{buildLevel();}}
        }
        /* auto-fail reset after no pushes left and stopped */
        if(pushCount>=maxPush&&!moving&&!won){
            wonTimer++;
            if(wonTimer>90){buildLevel();}
        }
    }
    draw();requestAnimationFrame(upd);
}

cv.addEventListener('click',e=>{
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>400&&my<450){state='play';score=0;round=1;buildLevel();}return;}
    if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>300&&my<350){state='play';score=0;round=1;buildLevel();}return;}

    const cx=W/2,cy=fieldT+fieldH+55;
    /* direction buttons */
    const dirBtns=[{bx:cx-90},{bx:cx-30},{bx:cx+30},{bx:cx+90}];
    dirBtns.forEach((d,i)=>{if(mx>d.bx&&mx<d.bx+50&&my>cy-18&&my<cy+18){selectedDir=i;}});
    /* force buttons */
    for(let i=0;i<3;i++){const fx=cx+170+i*80;if(mx>fx&&mx<fx+70&&my>cy-18&&my<cy+18){selectedForce=i;}}
    /* apply button */
    if(mx>cx-180&&mx<cx-100&&my>cy-18&&my<cy+18){applyForce();}
});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});

upd();
</script></body></html>"""


def _build_elem_sci_surtunme_yarisi_html():
    """Sürtünme Yarışı — 3 farklı zeminde araba yarışı, sürtünme öğren."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[],animT=0;

/* surfaces definition */
const allSurfaces=[
    {name:'Halı',emoji:'🟫',color:'#92400e',friction:0.92,label:'Yüksek Sürtünme'},
    {name:'Tahta',emoji:'🟨',color:'#ca8a04',friction:0.96,label:'Orta Sürtünme'},
    {name:'Buz',emoji:'🧊',color:'#38bdf8',friction:0.995,label:'Düşük Sürtünme'},
    {name:'Kum',emoji:'🏖️',color:'#d97706',friction:0.88,label:'Çok Yüksek Sürtünme'},
    {name:'Çimen',emoji:'🌿',color:'#16a34a',friction:0.93,label:'Yüksek Sürtünme'}
];

let surfaces=[allSurfaces[0],allSurfaces[1],allSurfaces[2]]; /* current 3 lanes */
let cars=[{x:80,v:0,dist:0},{x:80,v:0,dist:0},{x:80,v:0,dist:0}];
let racing=false,raceTimer=0,raceFinished=false;
let question='',qOpts=[],qAns=-1,answered=false,ansCorrect=false;
let dataTable=[]; /* filled with measurements */
let selectedLane=-1;

const laneY=[180,280,380],laneH=70,laneW=560,laneL=70;
const PUSH_FORCE=6;

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

function buildRound(){
    racing=false;raceTimer=0;raceFinished=false;answered=false;ansCorrect=false;selectedLane=-1;
    /* pick 3 surfaces */
    if(round<=4){surfaces=[allSurfaces[0],allSurfaces[1],allSurfaces[2]];}
    else if(round<=7){
        const picks=[allSurfaces[0],allSurfaces[1],allSurfaces[2],allSurfaces[3],allSurfaces[4]];
        const shuffled=[...picks].sort(()=>Math.random()-0.5);
        surfaces=[shuffled[0],shuffled[1],shuffled[2]];
    } else {
        const shuffled=[...allSurfaces].sort(()=>Math.random()-0.5);
        surfaces=[shuffled[0],shuffled[1],shuffled[2]];
    }
    cars=[{x:laneL+20,v:0,dist:0},{x:laneL+20,v:0,dist:0},{x:laneL+20,v:0,dist:0}];
    generateQuestion();
}

function generateQuestion(){
    /* sort surfaces by friction (lower friction = faster) */
    const sorted=[...surfaces].sort((a,b)=>b.friction-a.friction); /* highest friction first = slowest */
    const fastest=surfaces.reduce((a,b)=>a.friction>b.friction?a:b); /* highest friction value = lowest friction force = fastest */
    const slowest=surfaces.reduce((a,b)=>a.friction<b.friction?a:b);

    const questions=[
        {q:'Hangi zeminde araba en hızlı gider?',ans:fastest.name,opts:[surfaces[0].name,surfaces[1].name,surfaces[2].name]},
        {q:'Hangi zeminde sürtünme kuvveti en az?',ans:fastest.name,opts:[surfaces[0].name,surfaces[1].name,surfaces[2].name]},
        {q:'Hangi zeminde araba en yavaş durur?',ans:fastest.name,opts:[surfaces[0].name,surfaces[1].name,surfaces[2].name]},
        {q:'Hangi zeminde sürtünme kuvveti en çok?',ans:slowest.name,opts:[surfaces[0].name,surfaces[1].name,surfaces[2].name]},
        {q:'Hangi zeminde araba en kısa mesafe gider?',ans:slowest.name,opts:[surfaces[0].name,surfaces[1].name,surfaces[2].name]}
    ];
    const pick=questions[Math.floor(Math.random()*questions.length)];
    question=pick.q;
    qOpts=[...pick.opts].sort(()=>Math.random()-0.5);
    qAns=qOpts.indexOf(pick.ans);
}

function startRace(){
    if(racing||raceFinished)return;
    racing=true;
    cars.forEach(c=>{c.v=PUSH_FORCE;c.x=laneL+20;c.dist=0;});
}

function drawLane(idx){
    const y=laneY[idx],s=surfaces[idx],c=cars[idx];
    /* lane background */
    ctx.fillStyle=s.color+'40';ctx.fillRect(laneL,y,laneW,laneH);
    ctx.strokeStyle=s.color;ctx.lineWidth=2;ctx.strokeRect(laneL,y,laneW,laneH);
    /* texture dots for surface */
    ctx.fillStyle=s.color+'30';
    for(let tx=laneL;tx<laneL+laneW;tx+=15){for(let ty=y;ty<y+laneH;ty+=15){
        ctx.beginPath();ctx.arc(tx+Math.sin(tx*0.1+ty*0.2)*3,ty,1.5,0,Math.PI*2);ctx.fill();
    }}
    /* surface label */
    ctx.fillStyle=s.color;ctx.font='bold 14px Segoe UI';ctx.textAlign='left';
    ctx.fillText(s.emoji+' '+s.name,laneL+5,y-5);
    ctx.fillStyle='#a78bfa80';ctx.font='11px Segoe UI';ctx.fillText(s.label,laneL+laneW-130,y-5);
    /* car */
    ctx.font='30px Segoe UI';ctx.textAlign='center';ctx.fillText('🚗',c.x,y+laneH/2+10);
    /* speed lines if moving */
    if(c.v>0.5){
        ctx.strokeStyle='#fbbf2460';ctx.lineWidth=1;
        for(let i=0;i<3;i++){
            const lx=c.x-25-i*10-Math.random()*5,ly=y+laneH/2-8+i*8;
            ctx.beginPath();ctx.moveTo(lx,ly);ctx.lineTo(lx-10-c.v*2,ly);ctx.stroke();
        }
    }
    /* dust/particles for surface */
    if(c.v>1&&racing){
        if(Math.random()>0.7){
            const pc=s.name==='Buz'?'#38bdf8':s.name==='Kum'?'#d97706':s.color;
            particles.push({x:c.x-15,y:y+laneH/2+Math.random()*10,vx:-Math.random()*2,vy:(Math.random()-0.5)*2,life:0.6,clr:pc,r:2});
        }
    }
    /* distance marker */
    if(raceFinished){
        const distPx=Math.round(c.dist);
        ctx.fillStyle='#e9d5ff';ctx.font='bold 12px Segoe UI';ctx.textAlign='center';
        ctx.fillText(distPx+' cm',c.x,y+laneH+15);
    }
}

function drawSpeedometer(){
    const sx=W-80,sy=130;
    ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(sx-35,sy-30,70,80,8);ctx.fill();ctx.stroke();
    ctx.fillStyle='#e9d5ff';ctx.font='10px Segoe UI';ctx.textAlign='center';ctx.fillText('Hız',sx,sy-18);
    cars.forEach((c,i)=>{
        const barH=Math.min(c.v*8,50);
        ctx.fillStyle=surfaces[i].color;ctx.fillRect(sx-20+i*18,sy+40-barH,12,barH);
    });
}

function drawDataTable(){
    if(dataTable.length===0)return;
    const tx=15,ty=H-25-dataTable.length*16;
    ctx.fillStyle='#e9d5ff80';ctx.font='10px Segoe UI';ctx.textAlign='left';
    ctx.fillText('Ölçüm Tablosu:',tx,ty-5);
    dataTable.forEach((row,i)=>{
        ctx.fillStyle='#a78bfa80';ctx.font='10px Segoe UI';
        ctx.fillText('T'+(i+1)+': '+row,tx,ty+10+i*14);
    });
}

function draw(){
    ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    animT+=0.03;

    if(state==='start'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
        ctx.fillText('🏎️ Sürtünme Yarışı',W/2,150);
        ctx.font='20px Segoe UI';ctx.fillText('Aynı kuvvetle 3 farklı zeminde yarış!',W/2,200);
        ctx.fillText('Hangi zeminde en hızlı gider?',W/2,230);
        ctx.font='50px Segoe UI';ctx.fillText('🟫🟨🧊',W/2,330);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,390,160,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,422);return;
    }
    if(state==='win'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
        ctx.fillText('🏆 Sürtünme Uzmanı!',W/2,150);
        ctx.font='22px Segoe UI';ctx.fillText('Toplam Puan: '+score+'/100',W/2,200);
        drawDataTable();
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,250,180,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,282);
        particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return;
    }

    /* HUD */
    ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='left';ctx.fillText('🏎️ Tur: '+round+'/'+maxR,15,25);
    ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,25);
    ctx.fillStyle='#1e1b4b';ctx.fillRect(200,12,300,10);ctx.fillStyle='#34d399';ctx.fillRect(200,12,300*((round-1)/maxR),10);

    /* lanes */
    for(let i=0;i<3;i++)drawLane(i);
    drawSpeedometer();

    /* push button */
    if(!racing&&!raceFinished){
        ctx.fillStyle='#34d399';ctx.beginPath();ctx.roundRect(W/2-70,laneY[2]+laneH+20,140,40,10);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('İt! 💨',W/2,laneY[2]+laneH+46);
    }

    /* question area after race */
    if(raceFinished&&!answered){
        const qy=laneY[2]+laneH+25;
        ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
        ctx.beginPath();ctx.roundRect(50,qy,W-100,120,12);ctx.fill();ctx.stroke();
        ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';ctx.fillText(question,W/2,qy+25);
        qOpts.forEach((o,i)=>{
            const ox=120+i*200,oy=qy+45;
            ctx.fillStyle='#7c3aed';ctx.strokeStyle='#a78bfa';ctx.lineWidth=2;
            ctx.beginPath();ctx.roundRect(ox,oy,160,40,8);ctx.fill();ctx.stroke();
            ctx.fillStyle='#e9d5ff';ctx.font='bold 15px Segoe UI';ctx.fillText(o,ox+80,oy+26);
        });
    }
    if(answered){
        const qy=laneY[2]+laneH+30;
        ctx.font='bold 20px Segoe UI';ctx.textAlign='center';
        if(ansCorrect){ctx.fillStyle='#34d399';ctx.fillText('✅ Doğru! +10 puan',W/2,qy+20);}
        else{ctx.fillStyle='#ef4444';ctx.fillText('✗ Yanlış! Doğru cevap: '+qOpts[qAns],W/2,qy+20);}
    }

    drawDataTable();
    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

let ansTimer=0;
function upd(){
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.03;p.vy+=.05});particles=particles.filter(p=>p.life>0);
    if(state==='play'&&racing){
        let allStopped=true;
        cars.forEach((c,i)=>{
            c.v*=surfaces[i].friction;
            c.x+=c.v;c.dist+=c.v;
            if(c.x>laneL+laneW-30){c.x=laneL+laneW-30;c.v=0;}
            if(c.v>0.15)allStopped=false;
        });
        if(allStopped&&!raceFinished){
            raceFinished=true;racing=false;
            /* record data */
            const row=surfaces.map((s,i)=>s.emoji+Math.round(cars[i].dist)+'cm').join(' | ');
            dataTable.push(row);
        }
    }
    if(state==='play'&&answered){
        ansTimer++;
        if(ansTimer>80){ansTimer=0;round++;if(round>maxR){state='win';}else{buildRound();}}
    }
    draw();requestAnimationFrame(upd);
}

cv.addEventListener('click',e=>{
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>390&&my<440){state='play';score=0;round=1;dataTable=[];buildRound();}return;}
    if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>250&&my<300){state='play';score=0;round=1;dataTable=[];buildRound();}return;}

    /* push button */
    if(!racing&&!raceFinished&&mx>W/2-70&&mx<W/2+70&&my>laneY[2]+laneH+20&&my<laneY[2]+laneH+60){startRace();return;}

    /* answer buttons */
    if(raceFinished&&!answered){
        const qy=laneY[2]+laneH+25;
        qOpts.forEach((o,i)=>{
            const ox=120+i*200,oy=qy+45;
            if(mx>ox&&mx<ox+160&&my>oy&&my<oy+40){
                answered=true;ansTimer=0;
                if(i===qAns){ansCorrect=true;score+=10;snd(true);addP(W/2,qy,'#34d399');}
                else{ansCorrect=false;snd(false);addP(W/2,qy,'#ef4444');}
            }
        });
    }
});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}))},{passive:false});

upd();
</script></body></html>"""


def _build_elem_sci_kaldirac_ustasi_html():
    """Kaldıraç Ustası — Dayanağı ayarla, ağır cismi kaldır."""
    return """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:linear-gradient(135deg,#1a0533,#0d0221);overflow:hidden;font-family:'Segoe UI',sans-serif}
canvas{display:block;margin:0 auto}</style></head><body>
<canvas id="c"></canvas>
<script>
const W=700,H=650,cv=document.getElementById('c');cv.width=W;cv.height=H;const ctx=cv.getContext('2d');
const COLORS=['#ff6b9d','#c084fc','#fbbf24','#34d399','#60a5fa','#f472b6','#a78bfa','#fb923c','#4ade80','#38bdf8'];
let state='start',score=0,round=1,maxR=10,particles=[],animT=0;

/* lever physics */
const beamLen=500,beamY=380,beamCX=W/2;
let fulcrumX=W/2; /* draggable */
let objectWeight=20,objectEmoji='🪨',objectLabel='Taş';
let playerStrength=15; /* max force player can apply */
let beamAngle=0,targetAngle=0,lifting=false,liftSuccess=false,liftTimer=0;
let draggingFulcrum=false,showHint='',effortNeeded=0,effortAvailable=0;

/* objects per round */
const levelObjects=[
    {w:15,emoji:'🪨',label:'Küçük Taş',str:20},
    {w:20,emoji:'🪨',label:'Taş',str:18},
    {w:25,emoji:'📦',label:'Kutu',str:18},
    {w:30,emoji:'🧱',label:'Tuğla',str:16},
    {w:35,emoji:'🪨',label:'Büyük Taş',str:16},
    {w:40,emoji:'📦',label:'Ağır Kutu',str:15},
    {w:50,emoji:'🏗️',label:'Beton Blok',str:15},
    {w:60,emoji:'🪨',label:'Kaya',str:14},
    {w:75,emoji:'🚗',label:'Araba',str:14},
    {w:100,emoji:'🏠',label:'Küçük Ev',str:13}
];

function snd(ok){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=ok?523:180;o.type=ok?'sine':'sawtooth';g.gain.value=.3;o.start();if(ok)setTimeout(()=>o.frequency.value=659,100);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.4);o.stop(a.currentTime+.4)}catch(e){}}
function addP(x,y,c){for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,life:1,clr:c||'#fbbf24',r:2+Math.random()*4})}

function buildLevel(){
    lifting=false;liftSuccess=false;liftTimer=0;beamAngle=0;targetAngle=0;showHint='';draggingFulcrum=false;
    const obj=levelObjects[Math.min(round-1,levelObjects.length-1)];
    objectWeight=obj.w;objectEmoji=obj.emoji;objectLabel=obj.label;playerStrength=obj.str;
    fulcrumX=W/2; /* reset to center */
    calcEffort();
}

function calcEffort(){
    /* moment: weight * distWeight = effort * distPlayer */
    const leftEnd=beamCX-beamLen/2, rightEnd=beamCX+beamLen/2;
    const distWeight=Math.abs(fulcrumX-leftEnd); /* object on left end */
    const distPlayer=Math.abs(rightEnd-fulcrumX); /* player on right end */
    if(distPlayer<10){effortNeeded=9999;} else {effortNeeded=objectWeight*distWeight/distPlayer;}
    effortAvailable=playerStrength;
}

function tryLift(){
    if(lifting||liftSuccess)return;
    calcEffort();
    lifting=true;
    if(effortNeeded<=effortAvailable){
        targetAngle=-0.25; /* tilt: left side goes up */
        liftSuccess=true;
        score+=10;snd(true);
        addP(beamCX-beamLen/2,beamY-40,'#fbbf24');addP(beamCX+beamLen/2,beamY,'#34d399');
        showHint='✅ Kaldırdın! Kuvvet yeterli!';
    } else {
        targetAngle=0.05; /* slight fail tilt */
        liftSuccess=false;
        snd(false);
        const ratio=effortNeeded/effortAvailable;
        if(ratio>2)showHint='❌ Çok ağır! Dayanağı nesneye yaklaştır!';
        else if(ratio>1.3)showHint='❌ Biraz daha yaklaştır!';
        else showHint='❌ Az kaldı! Dayanağı biraz daha sola kaydır.';
    }
}

function drawFulcrum(fx,fy){
    /* triangle */
    ctx.fillStyle='#f59e0b';ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(fx,fy);ctx.lineTo(fx-20,fy+35);ctx.lineTo(fx+20,fy+35);ctx.closePath();ctx.fill();ctx.stroke();
    /* drag hint */
    if(!lifting){
        ctx.fillStyle='#fbbf2480';ctx.font='10px Segoe UI';ctx.textAlign='center';ctx.fillText('◄ sürükle ►',fx,fy+50);
    }
}

function drawBeam(){
    ctx.save();
    ctx.translate(fulcrumX,beamY);
    ctx.rotate(beamAngle);

    const halfLen=beamLen/2;
    const leftX=-halfLen+(fulcrumX-beamCX+beamLen/2)-beamLen/2+halfLen; /* simplify: just use -halfLen and +halfLen relative */

    /* beam bar */
    ctx.fillStyle='#7c3aed';ctx.strokeStyle='#a78bfa';ctx.lineWidth=3;
    ctx.beginPath();ctx.roundRect(-(fulcrumX-(beamCX-beamLen/2)),-8,(beamLen),16,4);ctx.fill();ctx.stroke();

    /* left end = object */
    const objRelX=-(fulcrumX-(beamCX-beamLen/2));
    ctx.font='36px Segoe UI';ctx.textAlign='center';ctx.fillText(objectEmoji,objRelX+10,-25);
    ctx.fillStyle='#e9d5ff';ctx.font='bold 12px Segoe UI';ctx.fillText(objectLabel,objRelX+10,-55);
    ctx.fillStyle='#ef4444';ctx.font='11px Segoe UI';ctx.fillText(objectWeight+' kg',objRelX+10,30);

    /* right end = player */
    const playerRelX=beamLen-(fulcrumX-(beamCX-beamLen/2));
    ctx.font='32px Segoe UI';ctx.fillText('🧒',playerRelX-10,-20);
    ctx.fillStyle='#34d399';ctx.font='11px Segoe UI';ctx.textAlign='center';ctx.fillText('Güç: '+playerStrength,playerRelX-10,30);

    ctx.restore();
}

function drawForceBar(){
    const barX=50,barY=500,barW=300,barH=25;
    /* background */
    ctx.fillStyle='#1e1b4b';ctx.strokeStyle='#a78bfa';ctx.lineWidth=1;
    ctx.beginPath();ctx.roundRect(barX,barY,barW,barH,6);ctx.fill();ctx.stroke();
    /* effort needed bar */
    const maxForce=Math.max(effortNeeded,effortAvailable,1);
    const neededW=Math.min(effortNeeded/maxForce,1)*barW;
    ctx.fillStyle='#ef444480';ctx.fillRect(barX,barY,neededW,barH);
    /* player strength bar */
    const availW=Math.min(effortAvailable/maxForce,1)*barW;
    ctx.fillStyle='#34d39980';ctx.fillRect(barX,barY+barH+5,availW,barH);
    ctx.strokeStyle='#a78bfa';ctx.strokeRect(barX,barY+barH+5,barW,barH);

    ctx.fillStyle='#ef4444';ctx.font='bold 12px Segoe UI';ctx.textAlign='left';
    ctx.fillText('Gereken kuvvet: '+effortNeeded.toFixed(1),barX+barW+10,barY+17);
    ctx.fillStyle='#34d399';ctx.fillText('Senin gücün: '+effortAvailable,barX+barW+10,barY+barH+22);

    /* ratio indicator */
    if(effortNeeded>0){
        const ratio=effortAvailable/effortNeeded;
        ctx.fillStyle=ratio>=1?'#34d399':'#ef4444';ctx.font='bold 14px Segoe UI';ctx.textAlign='center';
        ctx.fillText(ratio>=1?'Yeterli! ✓':'Yetersiz ✗',barX+barW/2,barY-10);
    }
}

function drawDistanceMarkers(){
    const y=beamY+50;
    ctx.fillStyle='#a78bfa40';ctx.font='10px Segoe UI';ctx.textAlign='center';
    /* fulcrum position relative markers */
    const leftDist=Math.round(fulcrumX-(beamCX-beamLen/2));
    const rightDist=Math.round((beamCX+beamLen/2)-fulcrumX);
    ctx.fillStyle='#ef4444';ctx.fillText('←'+leftDist+'px→',beamCX-beamLen/2+(fulcrumX-(beamCX-beamLen/2))/2,y);
    ctx.fillStyle='#34d399';ctx.fillText('←'+rightDist+'px→',fulcrumX+(beamCX+beamLen/2-fulcrumX)/2,y);
}

function draw(){
    ctx.clearRect(0,0,W,H);const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1a0533');g.addColorStop(1,'#0d0221');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    animT+=0.03;

    if(state==='start'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 34px Segoe UI';ctx.textAlign='center';
        ctx.fillText('⚖️ Kaldıraç Ustası',W/2,150);
        ctx.font='20px Segoe UI';ctx.fillText('Dayanağı doğru yere koy, ağırlığı kaldır!',W/2,200);
        ctx.fillText('Dayanak nesneye yakınsa daha kolay!',W/2,230);
        ctx.font='60px Segoe UI';ctx.fillText('🪨⚖️🧒',W/2,340);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-80,400,160,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Başla!',W/2,432);return;
    }
    if(state==='win'){
        ctx.fillStyle='#e9d5ff';ctx.font='bold 36px Segoe UI';ctx.textAlign='center';
        ctx.fillText('🏆 Kaldıraç Ustası!',W/2,180);
        ctx.font='22px Segoe UI';ctx.fillText('Toplam Puan: '+score+'/100',W/2,230);
        ctx.fillText('Tüm ağırlıkları kaldırdın!',W/2,270);
        ctx.fillStyle='#a78bfa';ctx.beginPath();ctx.roundRect(W/2-90,320,180,50,12);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 22px Segoe UI';ctx.fillText('Tekrar Oyna',W/2,352);
        particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;return;
    }

    /* HUD */
    ctx.fillStyle='#e9d5ff';ctx.font='bold 16px Segoe UI';ctx.textAlign='left';ctx.fillText('⚖️ Tur: '+round+'/'+maxR,15,25);
    ctx.textAlign='right';ctx.fillText('Puan: '+score,W-15,25);
    ctx.fillStyle='#1e1b4b';ctx.fillRect(200,12,300,10);ctx.fillStyle='#34d399';ctx.fillRect(200,12,300*((round-1)/maxR),10);

    /* title for this round */
    ctx.fillStyle='#fbbf24';ctx.font='bold 16px Segoe UI';ctx.textAlign='center';
    ctx.fillText('Kaldırılacak: '+objectEmoji+' '+objectLabel+' ('+objectWeight+' kg)',W/2,60);

    /* ground */
    ctx.fillStyle='#166534';ctx.fillRect(0,beamY+35,W,H-beamY-35);
    ctx.fillStyle='#15803d';ctx.fillRect(0,beamY+35,W,3);

    /* fulcrum */
    drawFulcrum(fulcrumX,beamY);

    /* beam with components */
    drawBeam();

    /* distance markers */
    drawDistanceMarkers();

    /* force bar */
    drawForceBar();

    /* lift button */
    if(!lifting){
        ctx.fillStyle='#34d399';ctx.beginPath();ctx.roundRect(W/2+180,beamY+70,120,40,10);ctx.fill();
        ctx.fillStyle='#fff';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';ctx.fillText('Kaldır! 💪',W/2+240,beamY+96);
    }

    /* hint/result */
    if(showHint){
        ctx.fillStyle=liftSuccess?'#34d399':'#ef4444';ctx.font='bold 18px Segoe UI';ctx.textAlign='center';
        ctx.fillText(showHint,W/2,100);
    }

    /* lever principle explanation */
    ctx.fillStyle='#a78bfa60';ctx.font='11px Segoe UI';ctx.textAlign='center';
    ctx.fillText('Kaldıraç prensibi: Ağırlık x Mesafe = Kuvvet x Mesafe',W/2,H-15);

    particles.forEach(p=>{ctx.globalAlpha=p.life;ctx.fillStyle=p.clr;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
}

function upd(){
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.life-=.025;p.vy+=.08});particles=particles.filter(p=>p.life>0);
    if(state==='play'){
        /* animate beam angle */
        if(lifting){
            beamAngle+=(targetAngle-beamAngle)*0.08;
            liftTimer++;
            if(liftTimer>100){
                if(liftSuccess){round++;if(round>maxR){state='win';}else{buildLevel();}}
                else{lifting=false;liftTimer=0;beamAngle=0;targetAngle=0;showHint='';}
            }
        }
        if(!lifting)calcEffort();
    }
    draw();requestAnimationFrame(upd);
}

cv.addEventListener('mousedown',e=>{
    if(state!=='play'||lifting)return;
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(Math.abs(mx-fulcrumX)<25&&Math.abs(my-beamY)<40){draggingFulcrum=true;}
});
cv.addEventListener('mousemove',e=>{
    if(!draggingFulcrum)return;
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width);
    const minX=beamCX-beamLen/2+30,maxX=beamCX+beamLen/2-30;
    fulcrumX=Math.max(minX,Math.min(maxX,mx));
});
cv.addEventListener('mouseup',()=>{draggingFulcrum=false;});

cv.addEventListener('click',e=>{
    const r=cv.getBoundingClientRect();const mx=(e.clientX-r.left)*(W/r.width),my=(e.clientY-r.top)*(H/r.height);
    if(state==='start'){if(mx>W/2-80&&mx<W/2+80&&my>400&&my<450){state='play';score=0;round=1;buildLevel();}return;}
    if(state==='win'){if(mx>W/2-90&&mx<W/2+90&&my>320&&my<370){state='play';score=0;round=1;buildLevel();}return;}
    /* lift button */
    if(!lifting&&mx>W/2+180&&mx<W/2+300&&my>beamY+70&&my<beamY+110){tryLift();}
});

cv.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];
    const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width),my=(t.clientY-r.top)*(H/r.height);
    if(state!=='play'||lifting){cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));return;}
    if(Math.abs(mx-fulcrumX)<25&&Math.abs(my-beamY)<40){draggingFulcrum=true;}
    else{cv.dispatchEvent(new MouseEvent('click',{clientX:t.clientX,clientY:t.clientY}));}
},{passive:false});
cv.addEventListener('touchmove',e=>{e.preventDefault();if(!draggingFulcrum)return;const t=e.touches[0];
    const r=cv.getBoundingClientRect();const mx=(t.clientX-r.left)*(W/r.width);
    const minX=beamCX-beamLen/2+30,maxX=beamCX+beamLen/2-30;
    fulcrumX=Math.max(minX,Math.min(maxX,mx));
},{passive:false});
cv.addEventListener('touchend',e=>{e.preventDefault();draggingFulcrum=false;},{passive:false});

upd();
</script></body></html>"""
