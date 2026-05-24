/* ---------- Inline SVG icon system ---------- */
const ICONS = {
  grid:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
  upload:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
  chart:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/></svg>',
  spark:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l1.5 5.5L19 9l-5.5 1.5L12 16l-1.5-5.5L5 9l5.5-1.5z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/></svg>',
  shield:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z"/></svg>',
  cog:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.8l-.1-.1A2 2 0 1 1 7 4.6l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9c.3.6.9 1 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>',
  user:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  logout:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
  search:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="20" y1="20" x2="16.65" y2="16.65"/></svg>',
  lock:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
  bell:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 16H6l1.5-2V10a4.5 4.5 0 1 1 9 0v4z"/><path d="M10 20a2 2 0 0 0 4 0"/></svg>',
  file:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
  zap:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
  alert:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.86 1.82 18a2 2 0 0 0 1.7 3h16.94a2 2 0 0 0 1.7-3L13.7 3.86a2 2 0 0 0-3.4 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
  'upload-cloud':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.4 18.5A5 5 0 0 0 18 9h-1.3A8 8 0 1 0 3 16.3"/><polyline points="16 16 12 12 8 16"/></svg>',
  clock:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
  cloud:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19a4.5 4.5 0 1 0-1.3-8.8 7 7 0 1 0-13 3.3"/><path d="M3 19h14.5"/></svg>',
  'eye-off':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.9 17.9A10.7 10.7 0 0 1 12 20c-7 0-11-8-11-8a19.8 19.8 0 0 1 4.2-5.2"/><path d="M9.9 4.2A10.7 10.7 0 0 1 12 4c7 0 11 8 11 8a19.8 19.8 0 0 1-2.6 3.7"/><path d="M14.1 14.1a3 3 0 1 1-4.2-4.2"/><line x1="1" y1="1" x2="23" y2="23"/></svg>',
  key:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M10.8 12.2 21 2"/><path d="m18 5 3 3"/><path d="m15 8 3 3"/></svg>',
  trend:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
  entertain:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M9 10v4l4-2-4-2z" fill="currentColor"/></svg>',
  save:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M5 9h14"/><circle cx="12" cy="14" r="5"/></svg>',
};

document.querySelectorAll('[data-icon]').forEach(el=>{
  const key = el.getAttribute('data-icon');
  if(ICONS[key]) el.innerHTML = ICONS[key];
});

/* ---------- Sidebar toggle ---------- */
const sidebar = document.getElementById('sidebar');
document.getElementById('hamburger').addEventListener('click',()=> sidebar.classList.toggle('open'));
document.addEventListener('click',(e)=>{
  if(window.innerWidth<=900 && !sidebar.contains(e.target) && !e.target.closest('#hamburger')){
    sidebar.classList.remove('open');
  }
});
document.querySelectorAll('.nav-item').forEach(n=>{
  n.addEventListener('click',()=>{
    document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));
    n.classList.add('active');
  });
});

/* ---------- Animated count-ups ---------- */
function animateCount(el){
  const target = +el.dataset.count;
  const dur = 1400;
  const start = performance.now();
  function tick(t){
    const p = Math.min(1,(t-start)/dur);
    const eased = 1 - Math.pow(1-p,3);
    el.textContent = Math.floor(eased*target).toLocaleString('en-IN');
    if(p<1) requestAnimationFrame(tick);
    else el.textContent = target.toLocaleString('en-IN');
  }
  requestAnimationFrame(tick);
}
document.querySelectorAll('[data-count]').forEach(animateCount);

/* ---------- Gauge ---------- */
(function gauge(){
  const arc = document.getElementById('gaugeArc');
  const num = document.getElementById('scoreNum');
  const score = 78, total=100, max=414;
  const dur=1500, start=performance.now();
  function tick(t){
    const p = Math.min(1,(t-start)/dur);
    const eased = 1 - Math.pow(1-p,3);
    const val = score*eased;
    arc.style.strokeDashoffset = max - (max*(val/total));
    num.textContent = Math.floor(val);
    if(p<1) requestAnimationFrame(tick);
    else num.textContent = score;
  }
  requestAnimationFrame(tick);
})();

/* ---------- Pie Chart ---------- */
(function pie(){
  const data = [
    {name:'Food',         val:26, color:'#00d4ff'},
    {name:'Travel',       val:14, color:'#14f195'},
    {name:'Bills',        val:22, color:'#a78bfa'},
    {name:'Shopping',     val:18, color:'#ffb547'},
    {name:'Entertainment',val:10, color:'#ff5577'},
    {name:'Salary',       val:10, color:'#7aa6ff'},
  ];
  const totalSpend = 84210;
  const svg = document.getElementById('pie');
  const cx=100, cy=100, r=78, sw=22;
  let acc = 0;
  const total = data.reduce((s,d)=>s+d.val,0);
  const C = 2*Math.PI*r;
  // background ring
  svg.innerHTML = `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="${sw}"/>`;
  data.forEach((d,i)=>{
    const frac = d.val/total;
    const len = C*frac;
    const gap = C-len;
    const offset = -acc*C;
    const circle = document.createElementNS('http://www.w3.org/2000/svg','circle');
    circle.setAttribute('cx',cx); circle.setAttribute('cy',cy); circle.setAttribute('r',r);
    circle.setAttribute('fill','none');
    circle.setAttribute('stroke',d.color);
    circle.setAttribute('stroke-width',sw);
    circle.setAttribute('stroke-dasharray',`0 ${C}`);
    circle.setAttribute('stroke-linecap','butt');
    circle.setAttribute('transform',`rotate(-90 ${cx} ${cy})`);
    circle.style.transition = `stroke-dasharray 1.2s cubic-bezier(.2,.8,.2,1) ${i*0.08}s`;
    circle.style.filter = `drop-shadow(0 0 6px ${d.color})`;
    svg.appendChild(circle);
    requestAnimationFrame(()=>{
      circle.setAttribute('stroke-dasharray',`${len} ${gap}`);
      circle.setAttribute('stroke-dashoffset',offset);
    });
    acc += frac;
  });
  // legend list
  const ul = document.getElementById('catList');
  ul.innerHTML = data.map(d=>{
    const amt = Math.round(totalSpend*(d.val/total));
    return `<li>
      <span class="cat-left"><span class="cat-dot" style="background:${d.color};box-shadow:0 0 8px ${d.color}"></span>${d.name}</span>
      <span class="cat-right">${d.val}% · ₹${amt.toLocaleString('en-IN')}</span>
    </li>`;
  }).join('');
})();

/* ---------- Line Chart ---------- */
(function line(){
  const svg = document.getElementById('lineChart');
  const tooltip = document.getElementById('tooltip');
  const W=600,H=260,PAD={l:40,r:14,t:18,b:32};
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const income   = [62,68,71,75,78,82,80,85,88,92,95,98];
  const expenses = [40,46,52,48,55,60,58,64,62,70,68,72];
  const max = 110;
  const xs = (i)=> PAD.l + i*((W-PAD.l-PAD.r)/(months.length-1));
  const ys = (v)=> H-PAD.b - (v/max)*(H-PAD.t-PAD.b);

  // gradients + grid
  let html = `
  <defs>
    <linearGradient id="cyG" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#00d4ff" stop-opacity=".35"/>
      <stop offset="1" stop-color="#00d4ff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="grG" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#14f195" stop-opacity=".30"/>
      <stop offset="1" stop-color="#14f195" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="line1" x1="0" x2="1"><stop offset="0" stop-color="#00d4ff"/><stop offset="1" stop-color="#7aa6ff"/></linearGradient>
    <linearGradient id="line2" x1="0" x2="1"><stop offset="0" stop-color="#14f195"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
  </defs>`;
  // y grid
  for(let i=0;i<=4;i++){
    const y = PAD.t + i*((H-PAD.t-PAD.b)/4);
    const v = Math.round(max - (i*(max/4)));
    html += `<line x1="${PAD.l}" x2="${W-PAD.r}" y1="${y}" y2="${y}" stroke="rgba(255,255,255,.05)" stroke-dasharray="3 4"/>`;
    html += `<text x="${PAD.l-8}" y="${y+4}" fill="#6c7a91" font-size="10" text-anchor="end">${v}k</text>`;
  }
  // x labels
  months.forEach((m,i)=>{
    html += `<text x="${xs(i)}" y="${H-10}" fill="#6c7a91" font-size="10" text-anchor="middle">${m}</text>`;
  });

  const smooth = (pts)=>{
    let d=`M ${pts[0][0]} ${pts[0][1]}`;
    for(let i=1;i<pts.length;i++){
      const [x0,y0]=pts[i-1],[x1,y1]=pts[i];
      const cx=(x0+x1)/2;
      d+=` C ${cx} ${y0}, ${cx} ${y1}, ${x1} ${y1}`;
    }
    return d;
  };
  const ptsI = income.map((v,i)=>[xs(i),ys(v)]);
  const ptsE = expenses.map((v,i)=>[xs(i),ys(v)]);
  const pathI = smooth(ptsI);
  const pathE = smooth(ptsE);
  const areaI = pathI + ` L ${xs(months.length-1)} ${H-PAD.b} L ${PAD.l} ${H-PAD.b} Z`;
  const areaE = pathE + ` L ${xs(months.length-1)} ${H-PAD.b} L ${PAD.l} ${H-PAD.b} Z`;

  html += `<path d="${areaI}" fill="url(#cyG)"/>`;
  html += `<path d="${areaE}" fill="url(#grG)"/>`;
  html += `<path id="lI" d="${pathI}" fill="none" stroke="url(#line1)" stroke-width="2.4" stroke-linecap="round" style="filter:drop-shadow(0 0 6px rgba(0,212,255,.5))"/>`;
  html += `<path id="lE" d="${pathE}" fill="none" stroke="url(#line2)" stroke-width="2.4" stroke-linecap="round" style="filter:drop-shadow(0 0 6px rgba(20,241,149,.5))"/>`;

  // hover circles
  let circles='';
  ptsI.forEach((p,i)=>{ circles += `<circle data-m="${i}" data-t="Income" data-v="${income[i]}" cx="${p[0]}" cy="${p[1]}" r="4" fill="#00d4ff" stroke="#07111f" stroke-width="2" style="opacity:0;cursor:pointer;transition:opacity .2s"/>`;});
  ptsE.forEach((p,i)=>{ circles += `<circle data-m="${i}" data-t="Expenses" data-v="${expenses[i]}" cx="${p[0]}" cy="${p[1]}" r="4" fill="#14f195" stroke="#07111f" stroke-width="2" style="opacity:0;cursor:pointer;transition:opacity .2s"/>`;});
  html += circles;

  svg.innerHTML = html;

  // animate stroke draw
  ['lI','lE'].forEach(id=>{
    const p = document.getElementById(id);
    const L = p.getTotalLength();
    p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
    p.style.transition = 'stroke-dashoffset 1.6s ease-out';
    requestAnimationFrame(()=> p.style.strokeDashoffset = 0);
  });

  // hover tooltips
  svg.querySelectorAll('circle').forEach(c=>{
    c.addEventListener('mouseenter',(e)=>{
      c.style.opacity=1;
      const rect = svg.getBoundingClientRect();
      const wrap = svg.parentElement.getBoundingClientRect();
      const cx = +c.getAttribute('cx'), cy=+c.getAttribute('cy');
      const scaleX = rect.width / W;
      tooltip.innerHTML = `<b>${months[+c.dataset.m]}</b> · ${c.dataset.t}: ₹${c.dataset.v}k`;
      tooltip.style.left = (cx*scaleX + (rect.left-wrap.left) - 60)+'px';
      tooltip.style.top  = (cy*(rect.height/H) - 36)+'px';
      tooltip.style.opacity = 1;
    });
    c.addEventListener('mouseleave',()=>{ c.style.opacity=0; tooltip.style.opacity=0; });
  });
})();

/* ---------- Upload (drag & drop) ---------- */
(function upload(){
  const dz = document.getElementById('dropzone');
  const input = document.getElementById('fileInput');
  const progress = document.getElementById('progress');
  const bar = progress.querySelector('.bar');
  const body = document.getElementById('filesBody');

  function handle(files){
    if(!files || !files.length) return;
    progress.classList.add('show');
    bar.style.width = '0%';
    let p=0;
    const iv = setInterval(()=>{
      p += Math.random()*14 + 6;
      if(p>=100){
        p=100; clearInterval(iv);
        setTimeout(()=>{
          progress.classList.remove('show');
          bar.style.width='0%';
          [...files].forEach(f=>addRow(f));
        },280);
      }
      bar.style.width = p+'%';
    },140);
  }

  function addRow(f){
    const now = new Date();
    const fmt = (d)=> d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});
    const exp = new Date(now); exp.setDate(exp.getDate()+30);
    const tr = document.createElement('tr');
    tr.style.opacity=0; tr.style.transform='translateY(8px)';
    tr.innerHTML = `
      <td><i>${ICONS.file}</i> ${f.name}</td>
      <td>${fmt(now)}</td>
      <td><span class="status processing">Processing</span></td>
      <td>${fmt(exp)}</td>
      <td class="ta-right">
        <button class="btn ghost">View</button>
        <button class="btn primary">Analyze</button>
        <button class="btn danger">Delete</button>
      </td>`;
    body.prepend(tr);
    requestAnimationFrame(()=>{ tr.style.transition='all .4s ease'; tr.style.opacity=1; tr.style.transform='translateY(0)'; });
    setTimeout(()=>{ const s=tr.querySelector('.status'); s.className='status ready'; s.textContent='Ready'; },1600);
  }

  ['dragenter','dragover'].forEach(ev=> dz.addEventListener(ev,e=>{e.preventDefault();dz.classList.add('drag');}));
  ['dragleave','drop'].forEach(ev=> dz.addEventListener(ev,e=>{e.preventDefault();dz.classList.remove('drag');}));
  dz.addEventListener('drop', e=> handle(e.dataTransfer.files));
  input.addEventListener('change', e=> handle(e.target.files));

  // delegated delete
  body.addEventListener('click',(e)=>{
    if(e.target.classList.contains('danger')){
      const row = e.target.closest('tr');
      row.style.transition='all .3s ease';
      row.style.opacity=0; row.style.transform='translateX(-12px)';
      setTimeout(()=>row.remove(),300);
    }
  });
})();

/* ---------- Particle background ---------- */
(function particles(){
  const c = document.getElementById('particles');
  const ctx = c.getContext('2d');
  let w,h,parts=[];
  function resize(){ w=c.width=innerWidth; h=c.height=innerHeight;
    const n = Math.min(70, Math.floor(w*h/26000));
    parts = Array.from({length:n},()=>({
      x:Math.random()*w, y:Math.random()*h,
      vx:(Math.random()-.5)*.25, vy:(Math.random()-.5)*.25,
      r:Math.random()*1.6+.4,
      col: Math.random()>.5 ? '0,212,255' : '20,241,149'
    }));
  }
  function tick(){
    ctx.clearRect(0,0,w,h);
    for(let i=0;i<parts.length;i++){
      const p=parts[i];
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>w) p.vx*=-1;
      if(p.y<0||p.y>h) p.vy*=-1;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(${p.col},.55)`;
      ctx.shadowBlur=8; ctx.shadowColor=`rgba(${p.col},.7)`;
      ctx.fill();
      for(let j=i+1;j<parts.length;j++){
        const q=parts[j];
        const dx=p.x-q.x, dy=p.y-q.y, d=Math.sqrt(dx*dx+dy*dy);
        if(d<110){
          ctx.shadowBlur=0;
          ctx.strokeStyle=`rgba(${p.col},${(1-d/110)*.15})`;
          ctx.lineWidth=.6;
          ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y); ctx.stroke();
        }
      }
    }
    requestAnimationFrame(tick);
  }
  resize(); window.addEventListener('resize',resize); tick();
})();

const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

// Load saved theme
if (localStorage.getItem('theme') === 'light') {
  document.body.classList.add('light-mode');
  themeIcon.textContent = '🌙';
}

// Toggle theme
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');

    const isLight = document.body.classList.contains('light-mode');

    if (isLight) {
      localStorage.setItem('theme', 'light');
      themeIcon.textContent = '🌙';
    } else {
      localStorage.setItem('theme', 'dark');
      themeIcon.textContent = '☀️';
    }
  });
}