/* 幽靈塞車簡報的互動。所有模擬都用頁面裡的求解器（web/ovm.js，window.OVM）在讀者的瀏覽器即時算，
 * 不用事先算好的資料。這個檔案只負責畫面：不改DT、不改模型（web/PARITY.md的J12會掃這個檔案）。
 * 各頁的互動規格在pipeline/pages/pNN.md的「畫面和互動」「顯示設定」。 */
(() => {
  "use strict";
  const O = window.OVM, DATA = window.DECK_DATA;
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduceMQ = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  const reduce = () => reduceMQ.matches;
  const N = 22, L = 44, BETA = 0.25, TAU = 0.5, JAM = O.JAM_V, DT = O.DT;
  const RATE = 6;        // 第1、2頁：每秒6個模型時間（逐頁稿的顯示設定）
  const TS_RATE = 16;    // 第3頁：時空圖每秒畫16個模型時間
  const P4_RATE = 10;    // 第4頁：100模型時間大約10秒畫完
  const P8_RATE = 40;    // 第8頁的「播放」：300到1500大約30秒
  const CAR_LEN = 0.3;   // 車子畫的長度（模型長度）；只是畫法，車的位置照模型
  const C = { stop: "#d9412b", stopBg: "#b8321d", even: "#f2eee3", fast: "#2f7fd8", ink: "#1f2d27", soft: "#56645d", asphalt: "#47504c",
    act: "#ffc21a", actD: "#c9930a", infield: "#e2e9df", grid: "#e4ebe2", white: "#ffffff" };
  const HEAD = '"Chiron GoRound TC","Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif';
  const shared = { click: null };   // 第2頁讀者的點擊（第3頁用）；只放在記憶體，不存任何資料

  // ---------- 小工具 ----------
  function el(tag, props = {}, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(props)) {
      if (k === "class") e.className = v;
      else if (k === "html") e.innerHTML = v;
      else if (k === "text") e.textContent = v;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else if (v === true) e.setAttribute(k, "");
      else if (v !== false && v != null) e.setAttribute(k, v);
    }
    for (const c of kids) if (c != null) e.append(c);
    return e;
  }
  const btn = (label, cls, onclick) => el("button", { type: "button", class: "btn" + (cls ? " " + cls : ""), onclick }, label);
  const num = (x, d) => (x < 0 ? "−" : "") + Math.abs(x).toFixed(d);
  const trim = (x, d) => num(x, d).replace(/\.?0+$/, "");
  const liveEl = $("#live");
  const announce = t => { liveEl.textContent = ""; setTimeout(() => { liveEl.textContent = t; }, 40); };
  const tagHtml = k => ({ sim: '<span class="tag sim">【我們的模擬】</span>', exp: '<span class="tag exp">【實驗】</span>' })[k];
  const sleep0 = () => new Promise(r => setTimeout(r, 0));

  // ---------- 動畫：只有目前這一頁、而且畫面看得到的時候才跑 ----------
  const loop = {
    fns: new Set(), raf: 0, last: 0, lastPaint: 0, paint: true,   // paint：這一格要不要重畫（最多每秒30次；模型照實際經過的時間走，不受影響）
    add(f) { this.fns.add(f); if (!this.raf) { this.last = performance.now(); this.raf = requestAnimationFrame(t => this.tick(t)); } },
    del(f) { this.fns.delete(f); },
    tick(ts) {
      const dt = Math.min(0.1, Math.max(0, (ts - this.last) / 1000)); this.last = ts;
      this.paint = ts - this.lastPaint >= 1000 / 31; if (this.paint) this.lastPaint = ts;
      for (const f of [...this.fns]) { try { f(dt); } catch (err) { console.error(err); } }   // 一頁出錯不讓其他動畫停掉；錯誤照樣記在主控台
      this.raf = this.fns.size ? requestAnimationFrame(t => this.tick(t)) : 0;
    }
  };
  // 依播放速度換算要走幾步；每一步都是ovm.js的RK4，dt固定0.05
  function stepper(rate) {
    let acc = 0;
    return { reset() { acc = 0; }, take(dt) { acc += dt * rate / DT; const n = Math.floor(acc); acc -= n; return Math.min(n, 400); } };
  }

  // ---------- 畫布 ----------
  function fit(cv, hf) {   // 畫布還沒顯示（寬度太小）時回傳null，不畫
    const w = cv.clientWidth; if (w < 40) return null;
    const H = Math.round(hf(w));
    const dpr = Math.min(2, window.devicePixelRatio || 1), W = Math.round(w * dpr), HH = Math.round(H * dpr);
    if (cv.width !== W || cv.height !== HH) { cv.width = W; cv.height = HH; }
    if (cv.style.height !== H + "px") cv.style.height = H + "px";
    const ctx = cv.getContext("2d"); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx, w, h: H };
  }
  function rrect(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  /** 有底色的標籤；會把標籤留在畫布裡面，不會被切掉。 */
  function chip(ctx, txt, x, y, o) {
    const fs = o.fs || 15, font = `${o.weight || 800} ${fs}px ${HEAD}`;
    ctx.font = font; const tw = ctx.measureText(txt).width, pw = o.bg ? 8 : 0, hh = fs * 1.5;
    let x0 = o.align === "right" ? x - tw - pw * 2 : o.align === "left" ? x : x - tw / 2 - pw;
    if (o.bounds) x0 = Math.max(o.bounds[0], Math.min(o.bounds[1] - tw - pw * 2, x0));
    if (o.bg) { ctx.fillStyle = o.bg; rrect(ctx, x0, y - hh / 2, tw + pw * 2, hh, Math.min(8, hh / 2)); ctx.fill(); if (o.edge) { ctx.strokeStyle = o.edge; ctx.lineWidth = 1.5; ctx.stroke(); } }
    ctx.fillStyle = o.fill; ctx.textAlign = "left"; ctx.textBaseline = "middle"; ctx.fillText(txt, x0 + pw, y + 1);
    return [x0, y - hh / 2, tw + pw * 2, hh];
  }
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, f) => { const A = hex(a), B = hex(b); return `rgb(${A.map((x, i) => Math.round(x + (B[i] - x) * f)).join(",")})`; };
  const carColor = (v, vb) => v <= JAM ? C.stop : v <= vb ? mix(C.stop, C.even, Math.pow((v - JAM) / Math.max(1e-9, vb - JAM), 0.7)) : mix(C.even, C.fast, Math.min(1, (v - vb) / 0.8));

  // ---------- 環道 ----------
  const angOf = (x, Lr) => O.pmod(x, Lr) / Lr * 2 * Math.PI;   // 從正上方開始、順時針
  const at = (g, r, a) => [g.cx + r * Math.sin(a), g.cy - r * Math.cos(a)];
  function geom(w, Lr) {
    const cx = w / 2, cy = w / 2, R = w * 0.41, ppu = 2 * Math.PI * R / Lr;
    const cl = Math.max(6, CAR_LEN * ppu), cw = Math.max(6, Math.min(cl * 0.95, 13)), rw = Math.max(cw * 2, 15);
    return { w, cx, cy, R, ppu, cl, cw, rw, L: Lr };
  }
  function drawRoad(ctx, g) {
    ctx.strokeStyle = C.asphalt; ctx.lineWidth = g.rw; ctx.beginPath(); ctx.arc(g.cx, g.cy, g.R, 0, 2 * Math.PI); ctx.stroke();
    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = Math.max(1, g.w / 420);
    for (const r of [g.R - g.rw / 2 + 2, g.R + g.rw / 2 - 2]) { ctx.beginPath(); ctx.arc(g.cx, g.cy, r, 0, 2 * Math.PI); ctx.stroke(); }
    ctx.fillStyle = "rgba(255,255,255,.4)";
    for (let k = 0; k < 8; k++) {
      const a = (k + 0.5) / 8 * 2 * Math.PI, [x, y] = at(g, g.R, a), s = g.cw * 0.5;
      ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.beginPath(); ctx.moveTo(s * 1.2, 0); ctx.lineTo(-s * 0.6, -s * 0.7); ctx.lineTo(-s * 0.2, 0); ctx.lineTo(-s * 0.6, s * 0.7); ctx.fill(); ctx.restore();
    }
  }
  function drawCars(ctx, g, s) {
    const vb = O.V(s.L / s.N), flashOn = s.flash != null && (reduce() || Math.floor(performance.now() / 160) % 2 === 0);   // 減少動態時不閃，改成持續亮1秒
    for (let n = 0; n < s.N; n++) {
      const a = angOf(s.x[n], s.L), [x, y] = at(g, g.R, a);
      ctx.save(); ctx.translate(x, y); ctx.rotate(a);
      ctx.fillStyle = n === s.flash && flashOn ? C.act : carColor(s.v[n], vb); ctx.strokeStyle = C.ink; ctx.lineWidth = 0.8;
      rrect(ctx, -g.cl / 2, -g.cw / 2, g.cl, g.cw, g.cw * 0.32); ctx.fill(); ctx.stroke();
      ctx.fillStyle = "rgba(31,45,39,.55)"; ctx.fillRect(g.cl * 0.08, -g.cw * 0.3, g.cl * 0.2, g.cw * 0.6);
      ctx.restore();
    }
  }
  /** 最大的一團幾乎停住的車（車速低於0.1、編號相鄰）；回傳它在環上的起點和終點（模型位置）。 */
  function jamSpan(s) {
    const gs = O.clusters(s.v); if (!gs.length) return null;
    let gp = gs[0]; for (const q of gs) if (q.length > gp.length) gp = q;
    const x0 = s.x[gp[0]]; let span = 0;
    for (let i = 1; i < gp.length; i++) span += O.pmod(s.x[gp[i]] - s.x[gp[i - 1]], s.L);
    return { from: x0, to: x0 + span, mid: x0 + span / 2, cars: gp };
  }
  const ZOOM = 3;
  /** 畫環道。s：{x, v, N, L, sel, selLabel, focus, flash, lens, small}。局部放大只是把同一個畫面放大3倍，車的位置不變。 */
  function drawRing(cv, s) {
    const f = fit(cv, w => w); if (!f) return null;
    const { ctx, w } = f, g = geom(w, s.L);
    ctx.clearRect(0, 0, w, w);
    ctx.fillStyle = C.infield; ctx.beginPath(); ctx.arc(g.cx, g.cy, g.R + g.rw, 0, 2 * Math.PI); ctx.fill();
    drawRoad(ctx, g); drawCars(ctx, g, s);
    const fs = Math.max(14, Math.min(17, w / 30)), jam = jamSpan(s), outer = g.R + g.rw / 2 + 5;
    if (jam) {   // 塞車團：環外側的紅色帶子
      const a0 = angOf(jam.from, s.L) - g.cl / g.ppu / s.L * 2 * Math.PI * 0.8, a1 = a0 + (jam.to - jam.from + g.cl / g.ppu * 1.6) / s.L * 2 * Math.PI;
      ctx.strokeStyle = C.stop; ctx.lineWidth = Math.max(7, w / 60); ctx.lineCap = "round";
      ctx.beginPath(); ctx.arc(g.cx, g.cy, outer + ctx.lineWidth / 2, a0 - Math.PI / 2, a1 - Math.PI / 2); ctx.stroke(); ctx.lineCap = "butt";
    }
    const halo = n => { const [x, y] = at(g, g.R, angOf(s.x[n], s.L)), r = g.cl * 0.75 + 7;
      ctx.lineWidth = 5; ctx.strokeStyle = C.ink; ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI); ctx.stroke();
      ctx.lineWidth = 3; ctx.strokeStyle = C.act; ctx.stroke(); };
    if (s.sel != null) halo(s.sel);
    if (s.focus != null && s.focus !== s.sel) { const [x, y] = at(g, g.R, angOf(s.x[s.focus], s.L)); ctx.setLineDash([4, 3]); ctx.lineWidth = 3; ctx.strokeStyle = C.ink; ctx.beginPath(); ctx.arc(x, y, g.cl * 0.75 + 9, 0, 2 * Math.PI); ctx.stroke(); ctx.setLineDash([]); }
    if (s.small) return g;
    chip(ctx, "車子順時針前進", g.cx, g.cy - g.R * 0.7, { fs, fill: C.soft, weight: 700 });
    if (s.hint && !jam && s.sel == null) {   // 還沒點車：直接在環道中間說要做什麼
      chip(ctx, s.hint[0], g.cx, g.cy - fs * 0.9, { fs: fs + 3, fill: C.ink, bg: C.act });
      if (s.hint[1]) chip(ctx, s.hint[1], g.cx, g.cy + fs * 1.3, { fs, fill: C.ink, bg: "rgba(255,255,255,.9)", weight: 700 });
    }
    const target = jam ? { pos: jam.mid, kind: "jam", text: "這裡幾乎停住了" } : s.sel != null && s.lens ? { pos: s.x[s.sel], kind: "sel", text: s.selLabel || "你點的車" } : null;
    if (s.lens && target) {
      const Rl = g.R * 0.56, lx = g.cx, ly = g.cy + g.R * 0.1, a = angOf(target.pos, s.L), [px, py] = at(g, g.R, a);
      ctx.save(); ctx.beginPath(); ctx.arc(lx, ly, Rl, 0, 2 * Math.PI); ctx.clip();
      ctx.fillStyle = C.infield; ctx.fillRect(lx - Rl, ly - Rl, Rl * 2, Rl * 2);
      ctx.translate(lx, ly); ctx.rotate(-a); ctx.scale(ZOOM, ZOOM); ctx.translate(-px, -py);
      drawRoad(ctx, g); drawCars(ctx, g, s);
      ctx.restore();
      const col = target.kind === "jam" ? C.stop : C.ink;
      ctx.lineWidth = 4; ctx.strokeStyle = col; ctx.beginPath(); ctx.arc(lx, ly, Rl, 0, 2 * Math.PI); ctx.stroke();
      // 放大範圍標在環上，讓讀者對得起來
      const half = Rl / (ZOOM * g.ppu) / s.L * 2 * Math.PI;
      if (target.kind === "sel") { ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(g.cx, g.cy, g.R - g.rw / 2 - 5, a - half - Math.PI / 2, a + half - Math.PI / 2); ctx.stroke(); }
      chip(ctx, target.text, lx, ly - Rl + fs * 0.9 + 4, { fs, fill: target.kind === "jam" ? "#ffffff" : C.ink, bg: target.kind === "jam" ? C.stopBg : C.act });
      chip(ctx, `放大${ZOOM}倍，車往右開`, lx, ly + Rl - fs * 0.9 - 4, { fs: fs - 1, fill: C.ink, bg: "rgba(255,255,255,.92)", weight: 700 });
    }
    return g;
  }
  /** 點環道：找最靠近的車。點在路旁邊一點點也算，手機上比較好點。 */
  function pickCar(cv, ev, s) {
    const r = cv.getBoundingClientRect(), w = r.width, g = geom(w, s.L);
    const dx = ev.clientX - r.left - g.cx, dy = ev.clientY - r.top - g.cy, d = Math.hypot(dx, dy);
    if (Math.abs(d - g.R) > Math.max(g.rw * 1.6, 28)) return null;
    const pos = O.pmod(Math.atan2(dx, -dy), 2 * Math.PI) / (2 * Math.PI) * s.L;
    let best = null, bd = Infinity;
    for (let n = 0; n < s.N; n++) { const q = Math.abs(O.pmod(s.x[n] - pos + s.L / 2, s.L) - s.L / 2); if (q < bd) { bd = q; best = n; } }
    return best;
  }
  function ringKey(extra) {
    return el("div", { class: "key" },
      el("span", {}, el("i", { style: `background:${C.stop}` }), "幾乎停住（車速低於0.1）"),
      el("span", {}, el("i", { style: `background:${C.even};box-shadow:inset 0 0 0 1px ${C.asphalt}` }), "均勻車流的速度"),
      el("span", {}, el("i", { style: `background:${C.fast}` }), "比均勻車流快"),
      extra ? el("span", {}, el("i", { class: "ring-sel" }), extra) : null);
  }
  /** 可以點的環道（滑鼠、手指、鍵盤）。 */
  function clickableRing(cv, getState, onPick, label, onMove) {
    cv.classList.add("pick"); cv.tabIndex = 0; cv.setAttribute("role", "button");
    let focus = 0, focused = false;
    const setLabel = () => cv.setAttribute("aria-label", `${label}用左右方向鍵選車，按Enter讓選中的車輕踩一下煞車。現在選的是第${focus}台車。`);
    setLabel();
    cv.addEventListener("click", ev => { const s = getState(); const n = pickCar(cv, ev, s); if (n != null) onPick(n); });
    cv.addEventListener("keydown", ev => {
      const s = getState();
      if (["ArrowRight", "ArrowDown"].includes(ev.key)) focus = (focus + 1) % s.N;
      else if (["ArrowLeft", "ArrowUp"].includes(ev.key)) focus = (focus - 1 + s.N) % s.N;
      else if (ev.key === "Enter" || ev.key === " ") { onPick(focus); }
      else return;
      ev.preventDefault(); setLabel(); if (onMove) onMove();
    });
    cv.addEventListener("focus", () => { focused = true; if (onMove) onMove(); }); cv.addEventListener("blur", () => { focused = false; if (onMove) onMove(); });
    return { focus: () => focused ? focus : null };
  }

  // ---------- 折線圖（第4、5、6頁） ----------
  const LOGTICK = [1, 0.1, 0.01, 0.001, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11];
  const SUP = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
  const logLabel = v => v >= 1e-4 ? String(v) : "10" + String(Math.round(Math.log10(v))).split("").map(c => SUP[c]).join("");
  function lineChart(cv, o) {
    const f = fit(cv, o.height || (w => Math.round(Math.min(360, Math.max(220, w * 0.62))))); if (!f) return null;
    const { ctx, w, h } = f;
    const fs = w < 420 ? 14 : 15, pad = { l: o.log ? 60 : 48, r: 14, t: 14, b: 42 };
    const W = w - pad.l - pad.r, H = h - pad.t - pad.b;
    const ly = v => o.log ? Math.log10(Math.max(v, o.y0 / 10)) : v, Y0 = ly(o.y0), Y1 = ly(o.y1);
    const X = x => pad.l + (x - o.x0) / (o.x1 - o.x0) * W, Y = v => pad.t + (1 - (Math.min(Math.max(ly(v), Y0), Y1) - Y0) / (Y1 - Y0)) * H;
    ctx.clearRect(0, 0, w, h); ctx.fillStyle = "#ffffff"; ctx.fillRect(0, 0, w, h);
    ctx.font = `600 ${fs}px ${HEAD}`; ctx.textBaseline = "middle";
    const yt = o.log ? LOGTICK.filter(v => v <= o.y1 * 1.0001 && v >= o.y0 * 0.9999) : o.yticks;
    const every = o.log && H / Math.max(1, yt.length - 1) < 26 ? 2 : 1;   // 刻度太擠時隔一個標一次數字
    yt.forEach((v, i) => { const y = Y(v); ctx.strokeStyle = C.grid; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(pad.l + W, y); ctx.stroke();
      if (i % every === 0) { ctx.fillStyle = C.soft; ctx.textAlign = "right"; ctx.fillText(o.log ? logLabel(v) : String(v), pad.l - 6, y); } });
    for (const x of o.xticks) { const px = X(x); ctx.fillStyle = C.soft; ctx.textAlign = "center"; ctx.fillText(String(x), px, pad.t + H + 12); }
    ctx.fillStyle = C.soft; ctx.textAlign = "center"; ctx.fillText(o.xlabel, pad.l + W / 2, h - 10);
    ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, pad.t + H); ctx.lineTo(pad.l + W, pad.t + H); ctx.stroke();
    for (const ref of o.refs || []) { const y = Y(ref.v); ctx.setLineDash([6, 5]); ctx.strokeStyle = ref.color || C.soft; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(pad.l + W, y); ctx.stroke(); ctx.setLineDash([]);
      chip(ctx, ref.text, pad.l + W - 2, y - fs * 0.9, { fs: fs - 1, fill: ref.color || C.soft, bg: "rgba(255,255,255,.9)", align: "right", weight: 700 }); }
    for (const sr of o.series) {
      const pts = sr.pts; if (pts.length < 2) continue;
      ctx.strokeStyle = sr.color; ctx.lineWidth = sr.width || 2.5; ctx.setLineDash(sr.dash || []); ctx.lineJoin = "round";
      ctx.beginPath(); ctx.moveTo(X(pts[0][0]), Y(pts[0][1])); for (let i = 1; i < pts.length; i++) ctx.lineTo(X(pts[i][0]), Y(pts[i][1])); ctx.stroke(); ctx.setLineDash([]);
    }
    if (o.empty) { const lh = (fs + 1) * 1.6;   // 還沒有資料：在圖中間分行寫要做什麼
      o.empty.forEach((t, i) => chip(ctx, t, pad.l + W / 2, pad.t + H / 2 + (i - (o.empty.length - 1) / 2) * lh, { fs: fs + 1, fill: C.ink, bg: "rgba(255,244,207,.95)", bounds: [pad.l + 2, pad.l + W - 2] })); }
    for (const n of o.notes || []) chip(ctx, n.text, X(n.x), Y(n.y), { fs, fill: n.fill || C.ink, bg: n.bg || C.act, align: n.align || "right", bounds: [pad.l + 2, pad.l + W - 2] });
    return { X, Y, pad, W, H };
  }
  const legend = items => el("ul", { class: "legend" }, ...items.map(it => el("li", { html: `<svg viewBox="0 0 30 10" aria-hidden="true"><line x1="1" y1="5" x2="29" y2="5" stroke="${it.color}" stroke-width="3" ${it.dash ? `stroke-dasharray="${it.dash.join(" ")}"` : ""}/></svg>${it.label}` })));

  // ---------- 文字的出現時機 ----------
  function gate(sec, from, layers, msg) {
    const blocks = $$(".main > [data-i]", sec).filter(e => +e.dataset.i >= from);
    const extra = layers ? $$('[data-layer="know"], [data-layer="adv"]', sec) : [];
    const wait = el("p", { class: "wait" }, msg);
    blocks.forEach(e => { e.hidden = true; }); extra.forEach(e => { e.hidden = true; });
    if (blocks.length) blocks[0].before(wait); else $(".main", sec).append(wait);
    let open = false;
    return { open(note) { if (open) return; open = true; blocks.forEach(e => { e.hidden = false; }); extra.forEach(e => { e.hidden = false; }); wait.remove(); if (note !== false) announce("下面出現了新的說明。"); }, get isOpen() { return open; } };
  }
  /** 先猜再看：沒選之前，下面的模擬鎖著。 */
  function predict(container, question, options, onChoose) {
    const box = el("div", { class: "ask" }, el("p", {}, question));
    const bs = options.map(t => { const b = el("button", { type: "button", class: "opt", "aria-pressed": "false" }, t);
      b.addEventListener("click", () => { bs.forEach(x => x.setAttribute("aria-pressed", String(x === b))); onChoose(t, b); }); return b; });
    bs.forEach(b => box.append(b)); container.append(box); return box;
  }
  function lockable(node, note) {
    const wrap = el("div", { class: "locked" }), msg = el("p", { class: "lock-note" }, note);
    node.hidden = true; wrap.append(msg, node);
    return { wrap, unlock() { msg.remove(); node.hidden = false; } };
  }
  function exhibit(stage, opts = {}) {
    const cv = el("canvas", { class: "ring", role: "img", "aria-label": opts.ringLabel || "環狀道路的動畫" });
    const model = el("div", { class: "model" }, cv);
    const left = el("div", {}, model, opts.key || null);
    const placard = el("div", { class: "placard" });
    stage.append(el("div", { class: "exhibit" }, left, placard));
    return { cv, placard, left };
  }
  function clockEl() {
    const b = el("b", {}, "0.0");
    const box = el("div", {}, el("div", { class: "clock" }, b, el("span", {}, "模型時間 t")), el("p", { class: "fine" }, "動畫已加速，模型時間沒有單位，不是秒。"));
    return { box, set(t) { const s = t.toFixed(1); if (b.textContent !== s) b.textContent = s; } };
  }
  function steps(labels) {
    const ol = el("ol", { class: "steps" }, ...labels.map(t => el("li", {}, t)));
    return { ol, set(k) { [...ol.children].forEach((li, i) => { li.className = i < k ? "done" : i === k ? "now" : ""; if (i === k) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current"); }); } };
  }
  const say = (cls) => el("p", { class: "say" + (cls ? " " + cls : ""), "aria-live": "polite" });

  // ---------- 背景計算（Web Worker；用同一份ovm.js） ----------
  function workerMain(O, m, post) {
    try {
      if (m.cmd === "measure") {
        const pts = []; const r = O.measureV2(m.N, 44.0, 1.0, 1e-6, (t, a1) => { pts.push([t, a1]); });
        post({ id: m.id, pts, r });
      } else if (m.cmd === "verdict") {
        post({ id: m.id, r: O.verdictN(m.N, 44.0, 1.0) });
      } else if (m.cmd === "smooth") {
        const rule = m.kind === "R0" ? null : m.kind === "R1" ? new O.AvgRule() : new O.TargetRule(O.V(2.0) * m.mult);
        const frames = [];
        const res = O.smoothingRun(rule, 0.1, { onStep: m.frames ? r => { if (r._steps % 10 === 0 && r.t >= 300 - 1e-9) frames.push([r.t, Array.from(r.x), Array.from(r.v)]); } : null });
        post({ id: m.id, std: res.std, vmin: res.vmin, jamFrac: res.jamFrac, mean: res.mean, sane: res.sane, minH: res.minH, x: Array.from(res.ring.x), v: Array.from(res.ring.v), frames });
      } else post({ id: m.id, error: "不認得的計算：" + m.cmd });
    } catch (err) { post({ id: m.id, error: String((err && err.message) || err) }); }
  }
  /** 計算引擎。run(訊息, 群組)回傳Promise，結果是{...}、{cancelled: true}或{error}。
   *  cancel(群組)：還沒開始的不算了；Worker正在算的，把Worker關掉重開（其他群組的工作重新送）。
   *  Worker不能用時改在主執行緒算，會先通知onFallback的人（第6頁要先問讀者）。 */
  const engine = (() => {
    let w = null, id = 0; const cbs = new Map(), sent = new Map(), timers = new Map(), fallbacks = [];
    const finish = d => { const f = cbs.get(d.id); cbs.delete(d.id); sent.delete(d.id); timers.delete(d.id); if (f) f(d); };
    const local = m => { timers.set(m.id, setTimeout(() => { timers.delete(m.id); if (cbs.has(m.id)) workerMain(O, m, finish); }, 0)); };
    const SRC = () => $("#ovm-src").textContent + "\n;(function(){var workerMain=" + workerMain.toString() + ";self.onmessage=function(e){workerMain(self.OVM,e.data,function(d){self.postMessage(d);});};})();";
    function fallback() {
      if (w) { try { w.terminate(); } catch (e) { /* 已經壞了 */ } w = null; }
      fallbacks.forEach(f => f());
      for (const m of sent.values()) if (!timers.has(m.id)) local(m);
    }
    function spawn() {
      try {
        w = new Worker(URL.createObjectURL(new Blob([SRC()], { type: "text/javascript" })));
        w.onmessage = e => finish(e.data);
        w.onerror = ev => { if (ev && ev.preventDefault) ev.preventDefault(); fallback(); };   // 載入失敗（例如被沙盒擋掉）
      } catch (err) { w = null; }
    }
    spawn();
    return {
      get mode() { return w ? "worker" : "main"; },
      onFallback(f) { fallbacks.push(f); },
      run(msg, group) { return new Promise(res => { const m = Object.assign({ id: ++id, group: group || "" }, msg); cbs.set(m.id, res); sent.set(m.id, m);
        if (w) w.postMessage(m); else local(m); }); },
      cancel(group) {
        const mine = [...sent.values()].filter(m => m.group === group); if (!mine.length) return;
        for (const m of mine) { const t = timers.get(m.id); if (t != null) clearTimeout(t); finish({ id: m.id, cancelled: true }); }
        if (w) { w.terminate(); spawn(); for (const m of sent.values()) { if (w) w.postMessage(m); else local(m); } }
      }
    };
  })();
  /** 兩個互斥的選項（例如「快轉｜播放動畫」）。 */
  function segmented(label, options, onChange) {
    let cur = 0;
    const bs = options.map((t, i) => el("button", { type: "button", "aria-pressed": String(i === 0), onclick: () => { cur = i; bs.forEach((b, j) => b.setAttribute("aria-pressed", String(j === i))); onChange(i); } }, t));
    const box = el("div", { class: "seg-wrap" }, el("span", { class: "seg-label" }, label), el("div", { class: "seg", role: "group", "aria-label": label }, ...bs));
    return { el: box, get value() { return cur; } };
  }

  // =====================================================================
  const PAGES = {};

  // ---------- 第1頁：一台車往前偏一點點 ----------
  PAGES[1] = sec => {
    const g = gate(sec, 2, false, "等到有車幾乎停住，這裡會出現接下來的說明。");
    const ex = exhibit($(".stage", sec), { key: ringKey("一開始往前偏了一點點的車"), ringLabel: "22台車的環狀道路動畫。黃色圈起來的車一開始往前偏了一點點。" });
    const clock = clockEl(), msg = say(), bPlay = btn("暫停", ""), bReplay = btn("重播", "plain"), bFF = btn("快轉到有車幾乎停住", "plain");
    ex.placard.append(el("p", { class: "say" }, "黃色圈起來的這台車，一開始往前偏了一點點（我們故意放的）。"), clock.box, el("div", { class: "btns" }, bPlay, bReplay, bFF), msg);
    let ring, jam, playing; const st = stepper(RATE);
    const reset = () => { const x = Array.from({ length: N }, (_, n) => n * 2.0); x[0] += 0.1; ring = new O.Ring(N, L, 1.0, x); jam = false; playing = !reduce(); st.reset(); msg.textContent = ""; msg.className = "say"; sync(); draw(); };
    // 照ours-model-offset-jam的量法：每0.5模型時間看一次有沒有車速低於0.1
    const stepOne = () => { ring.step(); if (ring._steps % 10 === 0 && ring.minSpeed() < JAM) { jam = true; playing = false; msg.textContent = "這裡幾乎停住了。"; msg.className = "say jam"; g.open(); return false; } return true; };
    const sync = () => { bPlay.textContent = playing ? "暫停" : jam ? "繼續播放" : "播放"; bFF.disabled = jam; };
    const draw = () => { drawRing(ex.cv, { x: ring.x, v: ring.v, N, L, sel: 0, selLabel: "往前偏了一點的車", lens: true }); clock.set(ring.t); };
    bPlay.onclick = () => { playing = !playing; sync(); };
    bReplay.onclick = () => { reset(); playing = true; sync(); };
    bFF.onclick = () => { for (let i = 0; i < 40000 && !jam; i++) stepOne(); sync(); draw(); };
    const tick = dt => { if (!vis.on || !playing) return; const n = st.take(dt); for (let i = 0; i < n; i++) if (!stepOne()) break; sync(); if (loop.paint || !playing) draw(); };
    const vis = watch(ex.cv);
    reset();
    return { enter() { loop.add(tick); }, leave() { loop.del(tick); }, draw };
  };

  // ---------- 第2頁：點一台車煞一下 ----------
  PAGES[2] = sec => {
    const g = gate(sec, 2, false, "點一台車、等到有車幾乎停住，這裡會出現接下來的說明。");
    const ex = exhibit($(".stage", sec), { key: ringKey("你點的車") });
    const sp = steps(["點任何一台車，讓它輕輕踩一下煞車", "看後面的車", "找出幾乎停住的地方"]);
    const clock = clockEl(), msg = say(), bPlay = btn("暫停", ""), bReset = btn("重來", "plain"), bFF = btn("快轉到有車幾乎停住", "plain");
    ex.placard.append(sp.ol, msg, clock.box, el("div", { class: "btns" }, bPlay, bReset, bFF), el("p", { class: "fine" }, "手機上直接點車；用鍵盤的話，先按Tab選到環道，再用方向鍵選車、按Enter。"));
    let demo, t, jam, playing, flashUntil = 0; const st = stepper(RATE);
    const state = () => { const [x, v] = demo.state(t); return { x, v, N, L }; };
    const now = () => demo.ring ? demo.time() : t;
    const reset = () => { demo = new O.ClickDemo(N, L, 1.0); t = 0; jam = false; playing = !reduce(); st.reset(); sp.set(0); msg.textContent = "點任何一台車，讓它輕輕踩一下煞車。"; msg.className = "say"; sync(); draw(); };
    const sync = () => { bPlay.textContent = playing ? "暫停" : "播放"; bFF.disabled = !demo.ring || jam; };
    const stepOne = () => { demo.ring.step(); if (demo.ring.minSpeed() < JAM) { jam = true; playing = false; sp.set(3); msg.textContent = "這裡幾乎停住了。"; msg.className = "say jam"; g.open(); return false; } return true; };
    const click = n => {
      if (demo.ring) { msg.textContent = "已經點過一台了。按「重來」可以點別台再試一次。"; return; }
      demo.click(t, n, TAU, BETA); shared.click = { car: n, tc: t }; flashUntil = performance.now() + 1000;
      playing = true; sp.set(1); msg.textContent = "你剛剛讓這台車慢了一下。"; msg.className = "say"; sync(); announce(`你讓第${n}台車輕踩了一下煞車。`);
    };
    const cr = clickableRing(ex.cv, state, click, "22台車的環狀道路，點一台車讓它輕踩一下煞車。", () => draw());
    const draw = () => { const s = state(); drawRing(ex.cv, Object.assign(s, { hint: ["點環道上任一台車", "它會輕輕踩一下煞車"], sel: demo.ring ? demo.ring.brake[0] : null, focus: cr.focus(), flash: demo.ring && performance.now() < flashUntil ? demo.ring.brake[0] : null, lens: true, selLabel: "你點的車" })); clock.set(now()); };
    bPlay.onclick = () => { playing = !playing; sync(); };
    bReset.onclick = () => { reset(); };
    bFF.onclick = () => { for (let i = 0; i < 40000 && !jam; i++) stepOne(); sync(); draw(); };
    const tick = dt => { if (!vis.on) return; const was = playing;
      if (playing) { const n = st.take(dt); if (!demo.ring) t += n * DT; else for (let i = 0; i < n; i++) if (!stepOne()) break; sync(); }
      if ((was || performance.now() < flashUntil + 100) && (loop.paint || !playing)) draw(); };
    const vis = watch(ex.cv);
    reset();
    return { enter() { loop.add(tick); }, leave() { loop.del(tick); }, draw };
  };

  // ---------- 第3頁：時空圖 ----------
  PAGES[3] = sec => {
    const g = gate(sec, 3, true, "選了答案之後，這裡會出現接下來的說明。");
    const stage = $(".stage", sec);
    const tile = (svg, a, b) => el("figure", {}, el("div", { html: svg }), el("figcaption", {}, a, el("span", {}, b)));
    const SV = (inner) => `<svg viewBox="0 0 80 64" aria-hidden="true">${inner}</svg>`;
    const t3 = tile(SV(`<text x="40" y="42" text-anchor="middle" font-size="30" font-weight="800" fill="${C.soft}">?</text>`), "帶子往哪邊斜？", "選了答案才揭曉");
    t3.classList.add("q");
    const guide = el("div", { class: "guide", role: "group", "aria-label": "時空圖的讀法" },
      tile(SV(`<line x1="12" y1="10" x2="66" y2="54" stroke="${C.ink}" stroke-width="7" stroke-linecap="round"/><line x1="12" y1="10" x2="66" y2="54" stroke="${C.act}" stroke-width="4" stroke-linecap="round"/>`), "往右下斜", "在往前開"),
      tile(SV(`<line x1="40" y1="8" x2="42" y2="56" stroke="${C.stop}" stroke-width="5" stroke-linecap="round"/>`), "幾乎直直往下", "幾乎停住"), t3);
    const cv = el("canvas", { class: "chart", role: "img", "aria-label": "時空圖：橫軸是環道上的位置，縱軸是模型時間，時間往下增加。" });
    const mini = el("canvas", { class: "ring", role: "img", "aria-label": "跟時空圖同步的小環道" });
    const sp = steps(["看一台車的軌跡", "疊上其他車", "猜帶子往哪邊移"]);
    const msg = say(), note = el("p", { class: "fine" }), bAll = btn("疊上其他車", ""), bRe = btn("重畫這台車", "plain");
    const askBox = el("div", {});
    msg.classList.add("p3-act"); askBox.classList.add("p3-act");
    const placard = el("div", { class: "placard" }, el("div", { class: "mini" }, mini), sp.ol, msg, note, el("div", { class: "btns p3-act" }, bAll, bRe), askBox);
    const span = el("p", { class: "ts-range" }), legendLine = el("p", { class: "fine", style: "margin:8px 4px 0" }, "灰線是其他車，紅色是車速低於0.1的地方，黃線是我們挑出來跟著看的那台車。");
    stage.append(guide, el("div", { class: "ts-grid" }, el("div", { class: "model flat" }, span, cv, legendLine), placard));
    let D = null, mode = "one", prog = 0, cursor = 0, chosen = null; bAll.disabled = true;
    const ask = predict(askBox, "塞住的地方連成一條帶子。這條帶子往哪邊移？", ["往右，跟車子同方向", "往左，跟車子反方向", "不動"], t => { chosen = t; reveal(); });
    ask.hidden = true;
    function compute() {
      const auto = !shared.click, ck = shared.click || { car: 0, tc: 0 };
      const d = new O.ClickDemo(N, L, 1.0); d.click(ck.tc, ck.car, TAU, BETA);
      const S_END = 400, frames = [[0, Float64Array.from(d.ring.x), Float64Array.from(d.ring.v)]];
      while (d.ring.t < S_END - 1e-9) { d.ring.step(); if (d.ring._steps % 10 === 0) frames.push([d.ring.t, Float64Array.from(d.ring.x), Float64Array.from(d.ring.v)]); }
      const track = O.trackWave(frames, N, L), c = track.length >= 2 ? O.fitSlope(track) : NaN;
      let hl = ck.car, enter = 0, exit = 0;
      if (track.length) {   // 挑一台會穿過「被追蹤的那團」的車：追蹤開始60模型時間後（塞車團已經長好），在那一團裡最慢的那台
        const tp = track.find(p => p[0] >= track[0][0] + 60 - 1e-9) || track[0], k0 = Math.round(tp[0] / 0.5), pos = O.pmod(tp[1], L);
        const near = n => Math.abs(O.pmod(frames[k0][1][n] - pos + L / 2, L) - L / 2) <= 3;
        hl = -1; for (let n = 0; n < N; n++) if (frames[k0][2][n] < JAM && near(n) && (hl < 0 || frames[k0][2][n] < frames[k0][2][hl])) hl = n;
        if (hl < 0) { hl = 0; for (let n = 1; n < N; n++) if (frames[k0][2][n] < frames[k0][2][hl]) hl = n; }
        let k = k0; while (k > 0 && frames[k - 1][2][hl] < JAM) k--; enter = k; while (k < frames.length - 1 && frames[k][2][hl] < JAM) k++; exit = k;
      }
      D = { ck, auto, frames, track, c, hl, enter, exit, key: `${ck.car}@${ck.tc}` };
      note.textContent = auto ? "你在第2頁沒有點車，這次由我們替你點了第0台車。" : `用的是你在第2頁點的那一次（第${ck.car}台車，模型時間${ck.tc.toFixed(1)}）。`;
      restart();
    }
    function windowOf(w) {   // 手機上畫80模型時間、桌機110，以這台車穿過塞車的那段為中心
      const W = w < 560 ? 80 : 110, mid = D.track.length ? (D.enter + D.exit) / 2 * 0.5 : 60;
      const s0 = Math.max(0, Math.min(400 - W, Math.round((mid - W / 2) / 0.5) * 0.5));
      return [Math.round(s0 / 0.5), Math.round((s0 + W) / 0.5)];
    }
    function restart() { mode = "one"; prog = null; chosen = null; bAll.disabled = true; ask.hidden = true; sp.set(0); msg.textContent = "這是一台車的軌跡。"; t3.classList.add("q"); }
    function reveal() {
      mode = "reveal"; sp.set(3);
      if (!D.track.length) { msg.textContent = "這次沒有追到塞車團，回第2頁按「重來」再點一次。"; return; }
      const back = D.c < 0;
      t3.classList.remove("q");
      t3.querySelector("div").innerHTML = SV(`<line x1="${back ? 64 : 16}" y1="10" x2="${back ? 22 : 58}" y2="50" stroke="#fff" stroke-width="12" stroke-linecap="round"/><line x1="${back ? 64 : 16}" y1="10" x2="${back ? 22 : 58}" y2="50" stroke="${C.ink}" stroke-width="6" stroke-linecap="round"/><path d="${back ? "M14 58 L20 40 L32 52 Z" : "M66 58 L60 40 L48 52 Z"}" fill="${C.ink}"/>`);
      t3.querySelector("figcaption").firstChild.textContent = back ? "帶子往左下斜" : "帶子往右下斜";
      t3.querySelector("figcaption span").textContent = back ? "塞住的位置往後退" : "塞住的位置往前移";
      msg.textContent = `你選了「${chosen}」。圖上的黑色箭頭，是程式從軌跡量出來的塞車團移動方向。`;
      g.open();
      // 手機上圖和答案是上下排的：揭曉時把圖捲回畫面裡，讓箭頭和說明在一起
      if (window.innerWidth < 860) cv.scrollIntoView({ block: "start", behavior: reduce() ? "auto" : "smooth" });
    }
    bAll.onclick = () => { mode = "all"; sp.set(2); ask.hidden = false; msg.textContent = "22台車的軌跡都畫上去了。"; bAll.disabled = true; };
    bRe.onclick = () => restart();
    // 疊上全部的車之後，圖本身不再變，只有時間游標在動：把圖畫一次存起來，之後每一格只貼上去再畫游標，減輕手機的負擔
    let cache = null, cacheKey = "";
    function draw() {
      if (!D) return;
      const f = fit(cv, w => w < 560 ? w * 1.3 : Math.min(w * 0.8, 680)); if (!f) return;
      const { ctx, w, h } = f;
      const [K0, K1] = windowOf(w), F = D.frames;
      if (prog == null) prog = K0;
      const pad = { l: w < 560 ? 48 : 60, r: 12, t: 72, b: 14 }, W = w - pad.l - pad.r, H = h - pad.t - pad.b, Y = k => pad.t + (k - K0) / (K1 - K0) * H;
      const key = mode === "one" ? "" : [mode, cv.width, cv.height, K0, K1, D.key].join();
      if (key && key === cacheKey) ctx.drawImage(cache, 0, 0, w, h);
      else { paint(ctx, w, h, K0, K1, pad, W, H);
        if (key) { cache = cache || document.createElement("canvas"); cache.width = cv.width; cache.height = cv.height; const cc = cache.getContext("2d"); cc.clearRect(0, 0, cache.width, cache.height); cc.drawImage(cv, 0, 0); cacheKey = key; } }
      if (mode !== "one") { ctx.setLineDash([5, 5]); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5; const cy2 = Y(cursor); ctx.beginPath(); ctx.moveTo(pad.l, cy2); ctx.lineTo(pad.l + W, cy2); ctx.stroke(); ctx.setLineDash([]); }
      const fk = mode === "one" ? Math.max(K0, Math.min(K1, Math.floor(prog))) : Math.round(cursor);
      drawRing(mini, { x: F[fk][1], v: F[fk][2], N, L, sel: D.hl, small: true });
    }
    function paint(ctx, w, h, K0, K1, pad, W, H) {
      const F = D.frames, tc = D.ck.tc;
      const X = x => pad.l + O.pmod(x, L) / L * W, Y = k => pad.t + (k - K0) / (K1 - K0) * H, fs = w < 560 ? 13 : 15;
      ctx.fillStyle = "#ffffff"; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = C.grid; ctx.lineWidth = 1; ctx.font = `600 ${fs}px ${HEAD}`; ctx.textBaseline = "middle";
      for (let x = 0; x <= 44; x += 11) { const px = pad.l + x / L * W; ctx.beginPath(); ctx.moveTo(px, pad.t); ctx.lineTo(px, pad.t + H); ctx.stroke(); ctx.fillStyle = C.soft; ctx.textAlign = "center"; ctx.fillText(String(x), px, pad.t - 12); }
      const tA = tc + K0 * 0.5, tB = tc + K1 * 0.5;
      span.textContent = `這張圖只畫點擊之後的一段：模型時間${tA.toFixed(1)}到${tB.toFixed(1)}（點擊在${tc.toFixed(1)}）。`;
      for (let t = Math.ceil(tA / 20) * 20; t <= tB; t += 20) { const py = Y((t - tc) / 0.5); ctx.strokeStyle = C.grid; ctx.beginPath(); ctx.moveTo(pad.l, py); ctx.lineTo(pad.l + W, py); ctx.stroke(); ctx.fillStyle = C.soft; ctx.textAlign = "right"; ctx.fillText(String(t), pad.l - 6, py); }
      chip(ctx, "位置（0和44是同一點）", pad.l, 14, { fs, fill: C.soft, align: "left", weight: 700 });
      const ay = 42, x1 = pad.l + W - 2, x0 = x1 - Math.min(90, W * 0.22);
      ctx.strokeStyle = C.ink; ctx.fillStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x0, ay); ctx.lineTo(x1 - 8, ay); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x1, ay); ctx.lineTo(x1 - 12, ay - 7); ctx.lineTo(x1 - 12, ay + 7); ctx.fill();
      chip(ctx, "車子前進的方向", x0 - 8, ay, { fs, fill: C.ink, align: "right" });
      ctx.save(); ctx.translate(14, pad.t + H / 2); ctx.rotate(-Math.PI / 2); chip(ctx, "模型時間（往下增加）", 0, 0, { fs, fill: C.soft, weight: 700 }); ctx.restore();
      ctx.save(); ctx.beginPath(); ctx.rect(pad.l, pad.t, W, H); ctx.clip();
      const seg = (n, kA, kB, style) => { for (let k = Math.max(K0 + 1, kA); k <= kB; k++) { const p = F[k - 1][1][n], q = F[k][1][n]; if (Math.abs(O.pmod(q, L) - O.pmod(p, L)) < L / 2) { style(F[k][2][n]); ctx.beginPath(); ctx.moveTo(X(p), Y(k - 1)); ctx.lineTo(X(q), Y(k)); ctx.stroke(); } } };
      ctx.lineCap = "round";
      if (mode !== "one") for (let n = 0; n < N; n++) if (n !== D.hl) seg(n, K0 + 1, K1, v => { if (v < JAM) { ctx.strokeStyle = C.stop; ctx.lineWidth = 2.6; } else { ctx.strokeStyle = "rgba(71,80,76,.34)"; ctx.lineWidth = 1.3; } });
      const kEnd = mode === "one" ? Math.min(K1, Math.floor(prog)) : K1;
      seg(D.hl, K0 + 1, kEnd, () => { ctx.strokeStyle = C.ink; ctx.lineWidth = 8; });
      seg(D.hl, K0 + 1, kEnd, v => { ctx.strokeStyle = v < JAM ? C.stop : C.act; ctx.lineWidth = 4.5; });
      if (mode === "reveal" && D.track.length) {
        const pts = D.track.filter(([s]) => s >= K0 * 0.5 - 1e-9 && s <= K1 * 0.5 + 1e-9).map(([s, p]) => [X(p) + (w < 560 ? 13 : 18), Y(s / 0.5), O.pmod(p, L)]);   // 箭頭畫在塞車團旁邊，不蓋住紅色的帶子
        const stroke = (wd, cl) => { ctx.strokeStyle = cl; ctx.lineWidth = wd; for (let i = 1; i < pts.length; i++) if (Math.abs(pts[i][2] - pts[i - 1][2]) < L / 2) { ctx.beginPath(); ctx.moveTo(pts[i - 1][0], pts[i - 1][1]); ctx.lineTo(pts[i][0], pts[i][1]); ctx.stroke(); } };
        if (pts.length > 4) {
          stroke(13, "rgba(255,255,255,.95)"); stroke(6, C.ink);
          const e = pts[pts.length - 1], p2 = pts[pts.length - 5], an = Math.atan2(e[1] - p2[1], e[0] - p2[0]);
          ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(e[0] + 22 * Math.cos(an), e[1] + 22 * Math.sin(an)); ctx.lineTo(e[0] + 18 * Math.cos(an + 2.5), e[1] + 18 * Math.sin(an + 2.5)); ctx.lineTo(e[0] + 18 * Math.cos(an - 2.5), e[1] + 18 * Math.sin(an - 2.5)); ctx.fill();
        }
      }
      ctx.restore();
      const B = [pad.l + 2, pad.l + W - 2];
      const hk = Math.max(K0, Math.min(kEnd, mode === "one" ? kEnd : K0 + 6)), hx = X(F[hk][1][D.hl]), hy = Y(hk);
      ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(hx, hy, 7, 0, 2 * Math.PI); ctx.fill(); ctx.fillStyle = C.act; ctx.beginPath(); ctx.arc(hx, hy, 4.5, 0, 2 * Math.PI); ctx.fill();
      chip(ctx, "這台車", hx + (hx > pad.l + W * 0.6 ? -14 : 14), hy, { fs: fs + 1, fill: C.ink, bg: C.act, align: hx > pad.l + W * 0.6 ? "right" : "left", bounds: B });
      if (D.track.length && kEnd >= D.enter + 2 && D.enter >= K0) { const sx = X(F[D.enter][1][D.hl]), sy = Y(D.enter) + 6, right = sx > pad.l + W * 0.3;   // 放在塞車帶子的左邊，右邊留給箭頭
        chip(ctx, "幾乎停住：線直直往下", sx + (right ? -16 : 16), sy, { fs, fill: "#ffffff", bg: C.stopBg, align: right ? "right" : "left", bounds: B }); }
      if (mode === "reveal" && D.track.length) {
        const inW = D.track.filter(([s]) => s >= K0 * 0.5 && s <= K1 * 0.5); const m = inW[Math.floor(inW.length * 0.6)] || D.track[0];
        const mx = X(m[1]), my = Y(m[0] / 0.5), right = mx > pad.l + W / 2;
        chip(ctx, D.c < 0 ? "塞車團往後移" : "塞車團往前移", mx + (right ? -22 : 22), my, { fs: fs + 3, fill: "#ffffff", bg: C.ink, align: right ? "right" : "left", bounds: B });
      }
    }
    let st = 0;
    const tick = dt => {
      if (!vis.on || !D) return;
      const [K0, K1] = windowOf(cv.clientWidth);
      if (prog == null) prog = K0;
      if (mode === "one") { prog = reduce() ? K1 : Math.min(K1, prog + dt * TS_RATE / 0.5);
        if (bAll.disabled && (prog >= D.exit + 4 || prog >= K1 || !D.track.length) && prog > K0) { bAll.disabled = false; if (!D.track.length || prog >= D.exit) msg.textContent = "這台車穿過塞住的地方了。按「疊上其他車」。"; sp.set(1); } }
      else { cursor = reduce() ? K0 + (K1 - K0) * 0.5 : (cursor < K0 || cursor >= K1 ? K0 : cursor + dt * TS_RATE / 0.5); }
      st += dt; if (loop.paint) draw();
    };
    const vis = watch(cv);
    return { enter() { if (!D || D.key !== `${(shared.click || { car: 0 }).car}@${(shared.click || { tc: 0 }).tc}` || (D.auto && shared.click)) compute(); loop.add(tick); }, leave() { loop.del(tick); }, draw };
  };

  // ---------- 第4頁：四條線 ----------
  PAGES[4] = sec => {
    const g = gate(sec, 2, false, "按「開始」、兩張圖畫完之後，這裡會出現接下來的說明。");
    const stage = $(".stage", sec), FOL = [1, 5, 10, 15];
    const STY = [{ color: C.ink, dash: null }, { color: C.fast, dash: [9, 4] }, { color: "#b4550f", dash: [3, 4] }, { color: "#6447b8", dash: [12, 4, 3, 4] }];
    const run = a => { const d = new O.ClickDemo(N, L, a); d.click(20.0, 0, TAU, BETA); const fol = FOL.map(j => O.pmod(0 - j, N));
      const out = fol.map(n => [[0, d.ring.v[n]]]); while (d.ring.t < 100 - 1e-9) { d.ring.step(); if (d.ring._steps % 10 === 0) fol.forEach((n, i) => out[i].push([d.ring.t, d.ring.v[n]])); } return out; };
    let R = null, prog = 0, playing = false;
    const boxes = [1.0, 2.5].map(a => { const cv = el("canvas", { class: "chart", role: "img", "aria-label": `車速對時間的圖，a=${a}，被點那台車後面第1、5、10、15台車` });
      return { a, cv, box: el("div", { class: "chart-box" }, el("h3", {}, a === 1 ? "第2頁的條件（a=1）" : "每台車調整得更快（a=2.5）"), cv) }; });
    const msg = say(), bGo = btn("開始", "");
    stage.append(el("p", { class: "exp-caption" }, "22台車、平均車距2、同樣的煞車"), el("div", { class: "btns", style: "margin:0 0 14px;align-items:center" }, bGo, msg),
      el("div", { class: "charts2" }, ...boxes.map(b => b.box)),
      legend(FOL.map((j, i) => ({ color: STY[i].color, dash: STY[i].dash, label: `後面第${j}台` }))),
      el("p", { class: "fine" }, "這四台是事先決定的，不是挑出來好看的。橫軸是點擊之後的模型時間，兩張圖的縱軸範圍相同。"));
    let ymin = 0, ymax = 2.0;
    function draw() {
      boxes.forEach((b, bi) => lineChart(b.cv, { x0: 0, x1: 100, y0: ymin, y1: ymax, xticks: [0, 20, 40, 60, 80, 100], yticks: [0, 0.4, 0.8, 1.2, 1.6, 2.0].filter(v => v <= ymax + 1e-9 && v >= ymin - 1e-9), xlabel: "點擊之後的模型時間",
        empty: R ? null : ["按上面的「開始」", "比較同一個煞車", "在兩種條件下怎麼傳下去"],
        series: R ? R[bi].map((pts, i) => ({ pts: pts.filter(p => p[0] <= prog + 1e-9), color: STY[i].color, dash: STY[i].dash, width: 2.5 })) : [] }));
    }
    bGo.onclick = () => { if (!R) { R = [run(1.0), run(2.5)]; const all = R.flat(2).map(pt => pt[1]); /* 兩張圖、四條線的所有車速 */ ymin = Math.min(0, Math.floor(Math.min(...all) * 5) / 5); ymax = Math.ceil(Math.max(...all) * 5) / 5; }
      prog = reduce() ? 100 : 0; playing = true; bGo.textContent = "重播"; msg.textContent = "邊算邊畫中……"; draw(); };
    const tick = dt => { if (!vis.on || !playing) return; prog = Math.min(100, prog + dt * P4_RATE); if (prog >= 100) { playing = false; msg.textContent = "畫完了。"; g.open(); } if (loop.paint || !playing) draw(); };
    const vis = watch(stage);
    return { enter() { loop.add(tick); draw(); }, leave() { loop.del(tick); }, draw };
  };

  // ---------- 第5頁：調得多快 ----------
  PAGES[5] = sec => {
    const g = gate(sec, 2, true, "跑過至少兩個不同的a，再按「揭曉」，這裡會出現接下來的說明。");
    const stage = $(".stage", sec), AS = [1.0, 1.90, 1.98, 2.2, 2.5, 3.0], fa = a => a.toFixed(a === 1 || a === 3 || a === 2.2 || a === 2.5 ? 1 : 2);
    const askBox = el("div", {}); stage.append(askBox);
    const body = el("div", {}), lk = lockable(body, "先選一個答案，下面的模擬才會打開。");
    stage.append(lk.wrap);
    predict(askBox, "如果每台車都更快把車速調到想開的速度，剛剛那團塞車還會出現嗎？", ["會", "不會", "看調多快"], () => lk.unlock());
    const ex = exhibit(body, { key: ringKey("你點的車") });
    const range = el("input", { type: "range", min: "0", max: "5", step: "1", value: "0", id: "p5a", "aria-valuetext": "a = 1.0" });
    const out = el("output", { for: "p5a" }, "a = 1.0");
    const slider = el("div", { class: "slider" }, el("label", { for: "p5a" }, "a：把車速調過去有多快"), el("span", { class: "fine" }, "a越大，車速調得越快。"), out, range, el("div", { class: "ticks", "aria-hidden": "true" }, ...AS.map(a => el("span", {}, fa(a)))));
    const clock = clockEl(), msg = say(), bFF = btn("快轉", ""), bPlay = btn("暫停", "plain"), bReset = btn("重來", "plain");
    let animPref = false;
    const seg5 = segmented("a=1.90、1.98點了之後：", ["直接快轉", "播放動畫"], i => { animPref = i === 1; }), bAnim = seg5.el;
    const hist = el("ul", { class: "fine", style: "margin:0;padding-left:1.2em" }), bReveal = btn("揭曉", ""); bReveal.hidden = true;
    // 沿用逐頁稿第5頁：「越靠近分界，變化越慢……靠近分界時，光看車子很難分出來」；揭曉前不提「分界」
    const nearNote = el("p", { class: "near-note" }, "這個a值，擾動的變化很慢，光看車子很難分出來，要看下面那張小圖。"); nearNote.hidden = true;
    ex.placard.append(slider, nearNote, msg, clock.box, el("div", { class: "btns" }, bFF, bPlay, bReset), bAnim, hist, bReveal);
    const cv = el("canvas", { class: "chart", role: "img", "aria-label": "擾動大小對時間的圖，縱軸是對數刻度" }), chartNote = el("p", { class: "fine" });
    body.append(el("div", { class: "chart-box", style: "margin-top:18px" }, el("h3", {}, "擾動大小（所有車裡，車速跟均勻車流差最多的值）"), cv, chartNote));
    let a = 1.0, demo, t, pts, done, playing, run = 0; const ran = new Set(), st = stepper(RATE);
    const END = a => a === 1.0 ? 1500 : a < 2 ? 1500 : 300, XMAX = a => a === 1.0 ? 100 : a < 2 ? 1500 : 300;
    const reset = () => { run++; demo = new O.ClickDemo(N, L, a); t = 0; pts = []; done = null; playing = !reduce(); st.reset(); msg.textContent = "點一台車，讓它輕踩一下煞車。"; msg.className = "say"; chartNote.textContent = ""; sync(); draw(); };
    const sync = () => { bFF.disabled = !demo.ring || !!done; bPlay.disabled = !!done; bPlay.textContent = playing ? "暫停" : "播放"; bAnim.hidden = !(a > 1.5 && a < 2); nearNote.hidden = !(a > 1.5 && a < 2); };
    const finish = text => { done = text; playing = false; ran.add(a); msg.textContent = `a = ${fa(a)}：${text}`; msg.className = "say" + (text === "塞住了" ? " jam" : "");
      hist.append(el("li", {}, `a = ${fa(a)}：${text}`)); if (ran.size >= 2 && !g.isOpen) bReveal.hidden = false; sync(); draw(); };
    const judge = () => {
      const r = demo.ring;
      if (r.minV < JAM) return "塞住了";
      if (a === 1.0) return "點完1500模型時間都沒有出現幾乎停住的車";
      if (a < 2) { const last = pts.filter(p => p[0] >= END(a) - 300 - 1e-9).map(p => [p[0], Math.log(p[1])]); return O.fitSlope(last) > 0 ? "還沒塞住，擾動在慢慢變大" : "擾動在慢慢變小"; }
      const A = r.maxDev(); return A < 0.01 ? "擾動縮到0.01以下了" : `擾動還有${A.toFixed(3)}，沒有縮到0.01以下`;
    };
    const stepOne = () => { const r = demo.ring; r.step(); if (r._steps % 10 === 0) pts.push([r.t, r.maxDev()]);
      if (a === 1.0 && r.minSpeed() < JAM) { finish("塞住了"); return false; }
      if (r.t >= END(a) - 1e-9) { finish(judge()); return false; } return true; };
    let ffRun = -1;
    async function fastForward() { if (ffRun === run) return; const my = ffRun = run; playing = false; sync(); msg.textContent = "快轉中……";
      while (!done && my === run) { for (let i = 0; i < 1500 && !done; i++) stepOne(); draw(); await sleep0(); } }
    const click = n => { if (!lk || body.hidden) return; if (demo.ring) { msg.textContent = "已經點過了。按「重來」或換一個a再試。"; return; }
      demo.click(t, n, TAU, BETA); msg.textContent = "跑跑看……"; if (a > 1.5 && a < 2 && !animPref) fastForward(); else { playing = true; sync(); } };
    const cr = clickableRing(ex.cv, () => { const [x, v] = demo.state(t); return { x, v, N, L }; }, click, "22台車的環狀道路，點一台車讓它輕踩一下煞車。", () => draw());
    // 擾動圖只在內容變了才重畫：新增資料點、完成、重設、換a、點車、寬度改變（第3輪之後的限定效能修補）。
    // 環道照原本每一格畫；force＝true時（例如視窗大小改變）一定重畫。
    let chartKey = "";
    function draw(force) {
      const [x, v] = demo.state(t);
      drawRing(ex.cv, { x, v, N, L, hint: ["點環道上任一台車", "它會輕輕踩一下煞車"], sel: demo.ring ? demo.ring.brake[0] : null, focus: cr.focus(), lens: true });
      clock.set(demo.ring ? demo.time() : t);
      const key = [pts.length, done || "", a, !!demo.ring, cv.clientWidth].join("|");
      if (!force && key === chartKey) return;
      const xm = XMAX(a), last = pts[pts.length - 1];
      chartKey = lineChart(cv, { x0: 0, x1: xm, y0: 1e-5, y1: 1, log: true, xticks: xm === 100 ? [0, 25, 50, 75, 100] : xm === 300 ? [0, 100, 200, 300] : [0, 500, 1000, 1500], xlabel: "點擊之後的模型時間",
        refs: a > 2 ? [{ v: 0.01, text: "0.01" }] : [], series: [{ pts, color: C.ink, width: 2.5 }], notes: done && last ? [{ x: last[0], y: last[1], text: done, bg: done === "塞住了" ? C.stopBg : C.act, fill: done === "塞住了" ? "#fff" : C.ink }] : [] }) ? key : "";
      chartNote.textContent = demo.ring ? `a = ${fa(a)}，每0.5模型時間記一次。` : "";
    }
    range.addEventListener("input", () => { a = AS[+range.value]; out.textContent = `a = ${fa(a)}`; range.setAttribute("aria-valuetext", out.textContent); reset(); });
    bFF.onclick = () => fastForward();
    bPlay.onclick = () => { playing = !playing; sync(); };
    bReset.onclick = () => reset();
    bReveal.onclick = () => { g.open(); bReveal.hidden = true; };
    const tick = dt => { if (!vis.on || body.hidden || !playing || done) return; const n = st.take(dt); if (!demo.ring) t += n * DT; else for (let i = 0; i < n; i++) if (!stepOne()) break; if (loop.paint || done) draw(); };
    const vis = watch(stage);
    reset();
    return { enter() { loop.add(tick); }, leave() { loop.del(tick); run++; if (demo.ring && !done) playing = false; }, draw: () => draw(true) };   // 外面（視窗大小改變）呼叫時一定重畫
  };

  // ---------- 第6頁：車數 ----------
  PAGES[6] = sec => {
    const g = gate(sec, 2, true, "按「把3到60台全部跑一次」、算完之後，這裡會出現接下來的說明。");
    const stage = $(".stage", sec), askBox = el("div", {}); stage.append(askBox);
    const body = el("div", {}), lk = lockable(body, "先選一個答案，下面的模擬才會打開。"); stage.append(lk.wrap);
    predict(askBox, "環長和調整快慢都不變，車數多少時，繞一圈剛好一個起伏的小擾動會越變越大？", ["越多", "越少", "中間那段"], () => { lk.unlock(); draw(); renderStrip(); });
    const ex = exhibit(body, { ringLabel: "環道上的車，加了很小的擾動，眼睛看不出來" });
    const range = el("input", { type: "range", min: "3", max: "60", step: "1", value: "22", id: "p6n" }), out = el("output", { for: "p6n" }, "22台");
    const info = el("p", { class: "fine", style: "font-size:17px;color:var(--ink)" });
    const msg = say(), verdictBox = el("p", { class: "verdict-line", "aria-live": "polite" }), bOne = btn("跑這個車數", "");
    ex.placard.append(el("div", { class: "slider" }, el("label", { for: "p6n" }, "車數N（環長44、a=1）"), out, range, el("div", { class: "ticks", "aria-hidden": "true" }, el("span", {}, "3"), el("span", {}, "60"))), info, el("div", { class: "btns" }, bOne), msg, verdictBox);
    const cv = el("canvas", { class: "chart", role: "img", "aria-label": "這個車數的擾動大小對時間的圖，縱軸是對數刻度" }), cvNote = el("p", { class: "fine" });
    body.append(el("div", { class: "chart-box", style: "margin-top:18px" }, el("h3", {}, "擾動大小（繞一圈一個起伏的那種波）"), cv, cvNote));
    // 全部跑一次：按鈕、停止、Worker不能用時的確認
    const strip = el("div", { class: "strip", style: "margin-top:12px" }), prog = el("p", { class: "progress", "aria-live": "polite" });
    const bAll = btn("把3到60台全部跑一次", ""), bStop = btn("停止", "plain"); bStop.hidden = true;
    const bYes = btn("照樣全部跑", ""), bNo = btn("先不要", "plain");
    const confirmBox = el("div", { class: "confirm", role: "group", "aria-label": "要不要在畫面這邊計算" },
      el("p", {}, "這個瀏覽器不能在背景計算，只能在畫面這邊算。全部跑一次的時候，畫面可能會卡頓，按鈕和捲動可能反應變慢，要等多久要看你的裝置。要跑嗎？"),
      el("div", { class: "btns" }, bYes, bNo)); confirmBox.hidden = true;
    const KEY = { up: ["+", "放大"], down: ["−", "不放大"], na: ["?", "無法判定"], gap: ["≈", "公式算出的變化接近0，只比差距"], bad: ["!", "跟公式不符"], wait: ["…", "還沒算"] };
    const keyList = el("ul", { class: "strip-key" }, ...["up", "down", "na", "gap", "wait"].map(k => el("li", {}, el("b", { class: "c-" + k, "aria-hidden": "true" }, KEY[k][0]), KEY[k][1])));
    body.append(el("div", { class: "chart-box", style: "margin-top:18px" }, el("h3", {}, "3到60台的結果條"),
      el("p", { class: "fine" }, "每一格是一個車數，框起來的是你在上面選的車數。「公式預測」照有限車數的公式；「我們的模擬」照model/CRITERIA.md第2、3版事先定好的量法，在你的瀏覽器裡算。"),
      keyList, el("div", { class: "btns", style: "margin-top:12px" }, bAll, bStop), confirmBox, prog, strip));
    let n = 22, ring, single = null, oneRun = 0, consent = false, running = false, sweepRun = 0, spent = 0; const sweep = {}, st = stepper(RATE);
    const theory = {}; for (let k = 3; k <= 60; k++) theory[k] = O.theorySigma(1.0, 44 / k, k);
    const doneCount = () => Object.keys(sweep).length;
    const REASON = r => r.reason.startsWith("k=1 > ") ? "擾動長到0.001以上，停止" : r.reason.startsWith("k=1 < ") ? "擾動縮到0.0000000001以下，停止" : r.reason === "t = 2100" ? "跑到上限2100，停止" : "別的波變得太大，停止";
    function cellOf(k, verdict) { const s = theory[k];
      if (!verdict) return "wait"; if (verdict === "相符") return s > 0 ? "up" : "down"; if (verdict === "相符（只比差距）") return "gap"; if (verdict === "數值無法判定") return "na"; return "bad"; }
    // 選到的車數，用人話說結論。說法沿用逐頁稿第6頁審過的句子；數字是這次模擬實際量到的
    function sayVerdict(k, res) {
      const c = cellOf(k, res.verdict), f = theory[k] > 0 ? "放大" : "不放大";
      const used = res.runs[0].length;   // 主要那次（ε=1e−6）的有效長度，跟證據卡ours-model-n-sweep的「190左右」同一個量
      const tail = c === "na" ? `能用來量的時間只有約${used}，少於我們事先定的200。照規則標成「無法判定」，不能說已經驗證過。`
        : c === "gap" ? "公式算出的變化幾乎是0，照事先的規則只比數值的差距、不比變大還是變小。"
        : c === "bad" ? "跟公式不符。" : `跟公式一樣，小擾動會${c === "up" ? "放大" : "變小"}。`;
      verdictBox.innerHTML = ""; verdictBox.append(el("b", {}, `${k}台：`), `公式預測${f}；我們的模擬：${KEY[c][1]}。${tail}`);
    }
    const setN = k => { n = k; oneRun++; out.textContent = `${k}台`; range.setAttribute("aria-valuetext", `${k}台`); ring = O.modeRing(k, L, 1.0, 1e-6); st.reset(); single = null;
      info.textContent = `平均車距 44÷${k} = ${trim(44 / k, 3)}，均勻車流的速度 ${O.V(44 / k).toFixed(4)}`; cvNote.textContent = ""; msg.textContent = ""; verdictBox.textContent = ""; bOne.disabled = false; mark(); draw(); };
    bOne.onclick = async () => {
      const k = n, my = ++oneRun; bOne.disabled = true; engine.cancel("p6one");
      msg.textContent = `正在算${k}台……${engine.mode === "main" ? "（這個瀏覽器只能在畫面這邊算，可能會卡頓一下）" : ""}`;
      const [res, ver] = await Promise.all([engine.run({ cmd: "measure", N: k }, "p6one"), sweep[k] ? Promise.resolve({ r: { verdict: sweep[k].verdict, runs: sweep[k].runs } }) : engine.run({ cmd: "verdict", N: k }, "p6one")]);
      if (my !== oneRun) return;
      bOne.disabled = false;
      if (res.cancelled || ver.cancelled) { msg.textContent = ""; return; }
      if (res.error || ver.error) { msg.textContent = `${k}台算到一半出錯了：${res.error || ver.error}。可以再按一次「跑這個車數」。`; return; }
      single = res; msg.textContent = `${k}台：${REASON(res.r)}（模型時間${res.r.stop.toFixed(0)}）。`;
      if (!sweep[k]) { sweep[k] = { verdict: ver.r.verdict, runs: ver.r.runs }; updateCell(k); }
      sayVerdict(k, ver.r); draw();
    };
    function simCell(k, td) { const c = cellOf(k, sweep[k] && sweep[k].verdict); td.className = "c-" + c + (k === n ? " sel" : ""); td.textContent = "";
      td.append(el("span", { "aria-hidden": "true" }, KEY[c][0]), el("span", { class: "sr" }, KEY[c][1] + (k === n ? "（你選的車數）" : ""))); return td; }
    const updateCell = k => { const td = strip.querySelector(`td[data-n="${k}"]`); if (td) simCell(k, td); };
    function mark() { $$("[data-col]", strip).forEach(e => e.classList.toggle("sel", +e.dataset.col === n)); $$("td[data-n]", strip).forEach(td => simCell(+td.dataset.n, td)); }
    // 一列放幾個車數：每格至少約19px寬，兩位數的車數才不會擠在一起（列標題約佔90px）
    const perRow = () => Math.max(6, Math.min(29, Math.floor(((strip.clientWidth || 300) - 90) / 19)));
    function renderStrip() {
      strip.textContent = ""; const per = perRow();
      for (let a0 = 3; a0 <= 60; a0 += per) {
        const ks = []; for (let k = a0; k < a0 + per && k <= 60; k++) ks.push(k);
        const tb = el("table", {}, el("caption", { class: "sr" }, `車數${ks[0]}到${ks[ks.length - 1]}台`),
          el("thead", {}, el("tr", {}, el("th", { scope: "col" }, "車數"), ...ks.map(k => el("th", { scope: "col", "data-col": k, class: k === n ? "sel" : "" }, String(k))))),
          el("tbody", {}, el("tr", {}, el("th", { scope: "row" }, "公式預測"), ...ks.map(k => { const c = theory[k] > 0 ? "up" : "down"; return el("td", { class: "c-" + c + (k === n ? " sel" : ""), "data-col": k }, el("span", { "aria-hidden": "true" }, KEY[c][0]), el("span", { class: "sr" }, KEY[c][1])); })),
            el("tr", {}, el("th", { scope: "row" }, "我們的模擬"), ...ks.map(k => simCell(k, el("td", { "data-n": k }))))));
        strip.append(tb);
      }
    }
    function syncSweep() {
      const left = 58 - doneCount();
      bStop.hidden = !running; bAll.hidden = left === 0; bAll.disabled = running;
      bAll.textContent = left === 58 ? "把3到60台全部跑一次" : `繼續跑剩下的（還有${left}個）`;
    }
    function stopSweep(why) {
      if (!running) return; running = false; sweepRun++; engine.cancel("p6all");
      prog.textContent = `${why}目前算完${doneCount()}／58個車數，已經算完的會保留。`; syncSweep();
    }
    async function runSweep() {
      confirmBox.hidden = true; running = true; const my = ++sweepRun, t0 = performance.now(); syncSweep();
      prog.textContent = `模擬已算完 ${doneCount()}／58 個車數`;
      for (let q = 3; q <= 60; q++) {
        if (sweep[q]) continue;
        const res = await engine.run({ cmd: "verdict", N: q }, "p6all");
        if (my !== sweepRun || res.cancelled) return;
        if (res.error) { running = false; prog.textContent = `算${q}台的時候出錯了：${res.error}。已經算完的會保留，可以按「繼續跑剩下的」再試一次。`; syncSweep(); return; }
        sweep[q] = { verdict: res.r.verdict, runs: res.r.runs }; updateCell(q);
        prog.textContent = `模擬已算完 ${doneCount()}／58 個車數`;
      }
      spent += (performance.now() - t0) / 1000; running = false; syncSweep();
      prog.textContent = `模擬算完了（58個車數，在你的瀏覽器裡一共花了約${spent.toFixed(0)}秒）。`; g.open();
    }
    bAll.onclick = () => {
      if (running) return;
      if (engine.mode === "main" && !consent) { confirmBox.hidden = false; bYes.focus(); return; }
      runSweep().catch(err => { running = false; prog.textContent = `計算出錯了：${err}`; syncSweep(); });
    };
    bYes.onclick = () => { consent = true; confirmBox.hidden = true; bAll.onclick(); };
    bNo.onclick = () => { confirmBox.hidden = true; prog.textContent = "沒有跑。想跑的時候再按一次。"; bAll.focus(); };
    bStop.onclick = () => { stopSweep("已停止。"); bAll.focus(); };
    // 跑到一半Worker壞掉：先停下來問，不直接改在畫面這邊算
    engine.onFallback(() => { if (running && !consent) { stopSweep("背景計算停止運作了。"); confirmBox.hidden = false; } });
    function draw() {
      if (body.hidden) return;
      drawRing(ex.cv, { x: ring.x, v: ring.v, N: n, L, small: false });
      lineChart(cv, { x0: 0, x1: 2100, y0: 1e-11, y1: 0.01, log: true, xticks: [0, 700, 1400, 2100], xlabel: "模型時間", refs: [{ v: 1e-3, text: "0.001：長太大就停" }, { v: 1e-10, text: "縮太小就停" }],
        series: single ? [{ pts: single.pts, color: C.ink, width: 2.5 }] : [] });
    }
    range.addEventListener("input", () => setN(+range.value));
    const tick = dt => { if (!vis.on || body.hidden) return; if (!reduce()) { const k = st.take(dt); for (let i = 0; i < k; i++) ring.step(); if (loop.paint) drawRing(ex.cv, { x: ring.x, v: ring.v, N: n, L }); } };
    const vis = watch(stage);
    setN(22); renderStrip(); syncSweep();
    let rs = 0; new ResizeObserver(() => { const w = perRow(); if (w !== rs) { rs = w; renderStrip(); } }).observe(strip);
    return { enter() { loop.add(tick); }, leave() { loop.del(tick); stopSweep("離開這一頁時停止了。"); engine.cancel("p6one"); oneRun++; bOne.disabled = false; if (msg.textContent.startsWith("正在算")) msg.textContent = ""; }, draw };
  };

  // ---------- 第7頁：三個實驗 ----------
  PAGES[7] = sec => {
    sec.classList.add("p7");
    const ul = $(".main ul", sec); if (!ul) return {};
    ul.classList.add("exp-grid");
    ul.before(el("p", { class: "exp-caption" }, "三個都是封閉的環道。"));
    const MAP = { "2008": "sugiyama2008", "2013": "tadaki2013", "2018": "stern2018" };
    $$("li", ul).forEach(li => { const y = (li.textContent.match(/(2008|2013|2018)年/) || [])[1], s = DATA.sources.find(q => q.id === MAP[y]);
      if (s) li.append(el("a", { class: "paper", href: s.url, target: "_blank", rel: "noopener", "aria-label": `論文連結（${y}年的實驗）` }, "論文連結")); });
    return {};
  };

  // ---------- 第8頁：一台車讓車流變好 ----------
  PAGES[8] = sec => {
    const g = gate(sec, 9, false, "做完第三題、按「揭曉」之後，這裡會出現第三題的答案。");
    const after = i => $(`.main > [data-i="${i}"]`, sec);
    // 一、長條圖（數字從逐頁稿讀，見build_site.py的bars()）
    const NAMES = { std: "車速起伏的變化", fuel: "油耗的變化", flow: "通過量的變化" }, MAX = 90;
    const bars = el("div", { class: "bars", role: "group", "aria-label": "2018年實驗的結果長條圖" },
      el("p", { style: "margin:0", html: `${tagHtml("exp")}我們依論文的數字自己畫的長條圖（不是論文的圖）` }),
      el("div", { class: "bar-axis", "aria-hidden": "true" }, el("span", {}), el("span", {}, "← 減少"), el("span", {}, "增加 →")));
    for (const k of ["std", "fuel", "flow"]) {
      bars.append(el("h3", {}, NAMES[k]));
      DATA.bars[k].forEach((v, i) => {
        const pct = Math.abs(v) / MAX * 100, label = `${v < 0 ? "少了" : "多了"}${Math.abs(v)}%`, inside = pct > 55;
        const bar = el("i", { style: `width:${pct}%` }), span = el("span", { style: inside ? (v < 0 ? `left:${100 - pct}%;padding-left:8px;color:#fff` : `right:${100 - pct}%;padding-right:8px;color:#fff`) : (v < 0 ? `right:calc(${pct}% + 6px)` : `left:calc(${pct}% + 6px)`) }, label);
        bars.append(el("div", { class: "bar-row", role: "img", "aria-label": `${NAMES[k]}，實驗${"ABC"[i]}：${label}` },
          el("b", { "aria-hidden": "true" }, "ABC"[i]),
          // 窄螢幕（≤560px）改用這一行文字，長條另起一行；寬螢幕不顯示（見deck.css的.bar-t）
          el("div", { class: "bar-t" }, el("b", {}, `實驗${"ABC"[i]}`), el("span", { "aria-hidden": "true" }, "｜"), el("span", {}, label)),
          v < 0 ? el("div", { class: "bar-l" }, bar, span) : el("div", { class: "bar-l" }), v < 0 ? el("div", { class: "bar-r" }) : el("div", { class: "bar-r" }, bar, span)));
      });
    }
    bars.append(el("p", { class: "fine", style: "margin:0" }, "比的是：剛出現波、還沒控制的時段，跟控制開啟中表現最好的時段。每種控制方式只做了一場。"));
    after(3).after(bars);

    // 二、我們的模擬：平滑車
    const cv = el("canvas", { class: "ring", role: "img", "aria-label": "模型時間300時的環道，已經形成塞車，標出來的是要換成平滑車的那台" });
    const clock = clockEl(), msg = say(), res1 = el("dl", { class: "results" });
    const bR3 = btn("固定目標速度", ""), bR1 = btn("照自己過去的平均速度", "plain");
    let playAnim = false;
    const seg = segmented("跑的時候：", ["快轉", "播放動畫"], i => { playAnim = i === 1; });
    const box2 = el("div", { class: "sim-box", id: "p8-sim" }, el("p", { style: "margin:0", html: `${tagHtml("sim")}環道上已經形成塞車。選一種規則，把標出來的這台車換成平滑車。` }),
      el("p", { class: "fine", style: "margin:0" }, "平滑車的規則是我們自己設計的，不是實驗用的控制方式。"),
      el("div", { class: "split" }, el("div", { class: "model" }, cv), el("div", { style: "display:grid;gap:12px" }, el("div", { class: "btns" }, bR3, bR1), seg.el, clock.box, msg, res1)),
      el("p", { class: "fine", style: "margin:0" }, "從模型時間300換成平滑車，跑到1500；在1000到1500這一段算下面三件事，分三列，不合成一個分數。同時在背景跑一個「不換」的對照。"),
      el("p", { style: "margin:0;font-size:17px" }, "失敗的例子：只限制加速度、沒有安全機制的平滑車會撞車。"));
    after(6).after(box2);

    // 三、第三題
    const MULT = [0.9, 1.0, 1.05, 1.1, 1.2], fm = m => (Math.round(m * 100) % 10 ? m.toFixed(2) : m.toFixed(1));
    const q3 = el("div", { class: "sim-box", id: "p8-q3" }), q3body = el("div", { style: "display:grid;gap:12px" }), lk = lockable(q3body, "先選一個答案，滑桿才會打開。");
    const range = el("input", { type: "range", min: "0", max: "4", step: "1", value: "1", id: "p8u" }), out = el("output", { for: "p8u" });
    const res3 = el("dl", { class: "results" }), msg3 = say(), hist = el("ul", { class: "fine", style: "margin:0;padding-left:1.2em" }), bRev = btn("揭曉", ""); bRev.hidden = true;
    // 揭曉要做的兩件事，一開始就列出來（條件跟原本一樣：1.0倍和任一個大於1.0倍都跑過）
    const todo1 = el("li", {}, "先跑1.0倍（原本均勻車流的速度）"), todo2 = el("li", {}, "再跑任一個大於1.0倍");
    const todo = el("div", { class: "todo-box" }, el("p", { style: "margin:0;font-weight:700" }, "要看第三題的答案，先做這兩件事："), el("ol", { class: "todo" }, todo1, todo2));
    const bRun = btn("跑這個值", "");
    q3body.append(todo, el("div", { class: "slider" }, el("label", { for: "p8u" }, "平滑車的目標速度（固定目標速度的規則）"), out, range, el("div", { class: "ticks", "aria-hidden": "true" }, ...MULT.map(m => el("span", {}, `${fm(m)}倍`)))), el("div", { class: "btns" }, bRun), msg3, res3, hist, bRev);
    predict(q3, "把目標速度設得比原本均勻車流的速度快，車速起伏一定會更小嗎？", ["一定會更小", "不一定，可能更大", "沒有差別"], () => lk.unlock());
    q3.append(lk.wrap); after(8).after(q3);
    // 頁首的跳轉：這頁很長，先讓讀者知道有哪幾段可以操作（內容一個字都不刪）
    const jumpTo = (node, focusSel) => () => { node.scrollIntoView({ block: "start", behavior: reduce() ? "auto" : "smooth" }); const f = $(focusSel, node); if (f) f.focus({ preventScroll: true }); };
    bars.tabIndex = -1;
    $(".main", sec).prepend(el("nav", { class: "jump", "aria-label": "這一頁的三段" }, el("p", {}, "這一頁有一份實驗結果，和兩個可以自己操作的地方："),
      el("button", { type: "button", onclick: jumpTo(bars, "h3") }, "看實驗結果"),
      el("button", { type: "button", onclick: jumpTo(box2, "button") }, "換一台平滑車"),
      el("button", { type: "button", onclick: jumpTo(q3, "button") }, "第三題")));

    // 同一個計算只送一次：算過的存起來，正在算的共用同一個Promise
    const cache = {}, pend = {};
    const compute = (key, msgObj) => {
      if (cache[key]) return Promise.resolve(cache[key]);
      if (!pend[key]) pend[key] = engine.run(msgObj, "p8").then(r => { delete pend[key]; if (!r.error && !r.cancelled) cache[key] = r; return r; });
      return pend[key];
    };
    const getBase = () => compute("R0", { cmd: "smooth", kind: "R0" });
    let x300 = null, ring = null, frames = null, fi = 0, playing = false, busy = false, q3Seq = 0; const tried = new Set();
    const showU = () => { const m = MULT[+range.value]; out.textContent = `均勻車流速度的${fm(m)}倍（${(O.V(2) * m).toFixed(3)}）`; range.setAttribute("aria-valuetext", out.textContent); };
    showU();
    const rows = (dl, r, base) => { dl.textContent = "";
      const row = (k, v, cls) => dl.append(el("div", {}, el("dt", {}, k), el("dd", { class: cls || "" }, v)));
      row("車速起伏", `是不換的時候的${Math.round(r.std / base.std * 100)}%`);
      row("平均車速", `不換的時候是${base.mean.toFixed(3)}，換了之後是${r.mean.toFixed(3)}`);
      row("安全", `最小車距${r.minH.toFixed(3)}，${r.minH > 0 ? "沒有撞車" : "撞車了（車距變成負的）"}`, r.minH > 0 ? "" : "bad-text"); };
    const failed = r => r.error || r.cancelled;
    function initRing() { if (x300) return; const x = Array.from({ length: N }, (_, n) => n * 2.0); x[0] += 0.1; const r = new O.Ring(N, L, 1.0, x); while (r.t < 300 - 1e-9) r.step(); x300 = { x: r.x, v: r.v, t: r.t }; ring = x300; }
    async function go(kind, label) {
      if (busy) return; busy = true; [bR3, bR1].forEach(b => { b.disabled = true; }); const anim = playAnim;
      msg.textContent = `「${label}」計算中……`; res1.textContent = "";
      const key = kind === "R3" ? "R3:1" : kind, [b0, r] = await Promise.all([getBase(), compute(key + (anim ? ":frames" : ""), { cmd: "smooth", kind, mult: 1.0, frames: anim })]);
      busy = false; [bR3, bR1].forEach(b => { b.disabled = false; });
      if (failed(b0) || failed(r)) { msg.textContent = `「${label}」算到一半出錯了：${b0.error || r.error || "被中斷"}。可以再按一次。`; return; }
      if (anim && r.frames.length) { frames = r.frames; fi = 0; playing = true; msg.textContent = `「${label}」播放中……`; frames.done = () => { msg.textContent = `「${label}」跑完了。`; rows(res1, r, b0); }; }
      else { ring = { x: r.x, v: r.v, t: 1500 }; msg.textContent = `「${label}」跑完了（快轉）。`; rows(res1, r, b0); draw(); }
    }
    bR3.onclick = () => go("R3", "固定目標速度");
    bR1.onclick = () => go("R1", "照自己過去的平均速度");
    function syncTodo() {
      todo1.classList.toggle("done", tried.has(1.0)); todo2.classList.toggle("done", [...tried].some(q => q > 1.0));
      if (tried.has(1.0) && [...tried].some(q => q > 1.0) && !g.isOpen) bRev.hidden = false;
    }
    // 只顯示「現在選的那個值」的結果：比較舊的請求回來時，如果讀者已經換了值，就不寫到畫面上
    async function runQ3() {
      const m = MULT[+range.value], my = ++q3Seq;
      msg3.textContent = `${fm(m)}倍：計算中……`; res3.textContent = "";
      const [b0, r] = await Promise.all([getBase(), compute("R3:" + m, { cmd: "smooth", kind: "R3", mult: m })]);
      if (!failed(b0) && !failed(r) && !tried.has(m)) { tried.add(m); hist.append(el("li", {}, `${fm(m)}倍：車速起伏是不換的時候的${Math.round(r.std / b0.std * 100)}%`)); syncTodo(); }
      if (my !== q3Seq || MULT[+range.value] !== m) return;
      if (failed(b0) || failed(r)) { msg3.textContent = `${fm(m)}倍算到一半出錯了：${b0.error || r.error || "被中斷"}。可以再按「跑這個值」。`; return; }
      msg3.textContent = `${fm(m)}倍：跑完了。`; rows(res3, r, b0);
    }
    range.addEventListener("input", () => { showU(); q3Seq++; msg3.textContent = ""; res3.textContent = ""; });
    range.addEventListener("change", runQ3);
    bRun.onclick = runQ3;
    bRev.onclick = () => { g.open(); bRev.hidden = true; };
    function draw() { if (!ring) return; drawRing(cv, { x: ring.x, v: ring.v, N, L, sel: 0, selLabel: "換成平滑車的車", lens: true }); clock.set(ring.t); }
    const tick = dt => { if (!vis.on) return;
      if (playing && frames) { fi = Math.min(frames.length - 1, fi + dt * P8_RATE / 0.5); const f = frames[Math.floor(fi)]; ring = { x: f[1], v: f[2], t: f[0] }; if (fi >= frames.length - 1) { playing = false; frames.done(); } }
      if (playing || frames) { if (loop.paint || !playing) draw(); if (!playing) frames = null; } };
    const vis = watch(box2);
    return { enter() { initRing(); draw(); loop.add(tick); }, leave() { loop.del(tick); }, draw };
  };

  // ---------- 第10頁：三個問題 ----------
  PAGES[10] = sec => {
    const qs = $$(".quiz", sec); qs.forEach((q, i) => { q.hidden = i > 0; });
    // 三題做完之後的思考題：不計分、不收集答案（文字是使用者核准的，見runs/2026-11-13-n7-build-r3.md）
    const think = el("div", { class: "think" }, el("h3", {}, "想一想（不計分）"),
      el("p", {}, "不看前面，你能用一句話說明，為什麼沒有車禍或障礙物，也可能出現塞車嗎？"),
      el("p", { class: "fine" }, "不用寫下來，這裡也不會記錄你的答案。想不出來的話，可以回去看："),
      el("p", { class: "back-links" }, ...[1, 2, 3, 4].map(k => el("a", { href: `#p${k}` }, `第${k}頁：${DATA.titles[k - 1]}`))));
    const further = el("div", { class: "further", hidden: true }, think, el("h3", {}, "延伸閱讀"),
      el("ul", {}, el("li", {}, el("a", { href: `${DATA.repo}/blob/main/wiki/index.md`, target: "_blank", rel: "noopener" }, "這份簡報的知識庫（LLM Wiki）入口")),
        ...DATA.sources.map(s => el("li", {}, el("a", { href: s.url, target: "_blank", rel: "noopener" }, `${s.title}（${s.year}）`)))),
      el("h3", {}, "這份簡報怎麼做出來的"),
      el("ul", {}, el("li", {}, el("a", { href: DATA.repo, target: "_blank", rel: "noopener" }, "專案的原始碼和Wiki（GitHub）")),
        el("li", {}, el("a", { href: `${DATA.repo}/tree/main/runs`, target: "_blank", rel: "noopener" }, "每一關的檢查和審查紀錄（runs/）"))));
    $(".main", sec).append(further);
    qs.forEach((q, i) => {
      const opts = $$(".opt", q), verdict = $(".verdict", q), why = $(".why", q);
      opts.forEach(b => b.setAttribute("aria-pressed", "false"));
      const pages = [...new Set([...why.textContent.matchAll(/第(\d+(?:、\d+)*)頁/g)].flatMap(m => m[1].split("、")))].sort((x, y) => x - y);
      if (pages.length) why.append(el("p", { class: "back-links" }, "答案在：", ...pages.map(p => el("a", { href: `#p${p}` }, `第${p}頁`))));
      const next = btn(i < qs.length - 1 ? "下一題" : "看延伸閱讀", ""); next.hidden = true; q.append(next);
      next.onclick = () => { if (i < qs.length - 1) { qs[i + 1].hidden = false; $("h3", qs[i + 1]).setAttribute("tabindex", "-1"); $("h3", qs[i + 1]).focus(); } else { further.hidden = false; $("h3", further).setAttribute("tabindex", "-1"); $("h3", further).focus(); } next.hidden = true; };
      opts.forEach(b => b.addEventListener("click", () => {
        opts.forEach(x => x.setAttribute("aria-pressed", String(x === b)));
        const ok = b.dataset.right === "1";
        verdict.hidden = false; verdict.className = "verdict " + (ok ? "ok" : "no"); verdict.textContent = ok ? "對" : "再想想";
        opts.forEach(x => { if (x.dataset.right === "1" && !x.querySelector(".badge")) { x.classList.add("right"); x.append(el("span", { class: "badge" }, "正確答案")); } });
        why.hidden = false; if (next.hidden && (i < qs.length - 1 ? qs[i + 1].hidden : further.hidden)) next.hidden = false;
      }));
    });
    return {};
  };

  // ---------- 畫面看不到時不算、不畫 ----------
  function watch(node) {
    const v = { on: true };
    if ("IntersectionObserver" in window) new IntersectionObserver(es => { for (const e of es) v.on = e.isIntersecting; }).observe(node);
    return v;
  }

  // ---------- 換頁 ----------
  const secs = $$("section.page"), total = secs.length, ctrls = {};
  const dots = $("#dots"), where = $("#where"), toc = $("#toc");
  secs.forEach((s, i) => {
    const t = DATA.titles[i];
    dots.append(el("button", { type: "button", class: "dot", "aria-label": `第${i + 1}頁：${t}`, onclick: () => go(i + 1, true) }));
    toc.append(el("li", {}, el("a", { href: `#p${i + 1}` }, t)));
  });
  toc.addEventListener("click", () => { $(".toc").open = false; });
  let cur = 0;
  function show(pg, focus) {
    if (pg === cur) return;
    if (cur && ctrls[cur] && ctrls[cur].leave) ctrls[cur].leave();
    cur = pg;
    secs.forEach((s, i) => { s.hidden = i + 1 !== pg; });
    const sec = secs[pg - 1];
    if (!ctrls[pg]) ctrls[pg] = (PAGES[pg] || (() => ({})))(sec) || {};
    if (ctrls[pg].enter) ctrls[pg].enter();
    $$(".dot", dots).forEach((d, i) => { if (i + 1 === pg) d.setAttribute("aria-current", "page"); else d.removeAttribute("aria-current"); });
    $$("a", toc).forEach((a, i) => { if (i + 1 === pg) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
    where.textContent = `第${pg}頁／共${total}頁`;
    $('[data-go="prev"]').disabled = pg === 1; $('[data-go="next"]').disabled = pg === total;
    document.title = `${DATA.titles[pg - 1]}｜幽靈塞車`;
    window.scrollTo(0, 0);
    if (focus) $("h2", sec).focus({ preventScroll: true });
  }
  // 網址加#pN，讓返回鍵和分享連結能用。在沙盒裡（例如被嵌在別的網頁的iframe、about:srcdoc）不能改網址，就只換頁
  function go(pg, focus) { pg = Math.max(1, Math.min(total, pg)); try { if (location.hash !== `#p${pg}`) history.pushState(null, "", `#p${pg}`); } catch (err) { /* 不能改網址 */ } show(pg, focus); }
  // 頁內連結（目錄、第10頁「答案在」）自己換頁，不交給瀏覽器：在about:srcdoc裡#p1會被解讀成外層網頁的網址
  document.addEventListener("click", e => { const a = e.target.closest('a[href^="#p"]'); if (!a || e.ctrlKey || e.metaKey || e.shiftKey) return;
    const m = /^#p(\d+)$/.exec(a.getAttribute("href")); if (!m) return; e.preventDefault(); $(".toc").open = false; go(+m[1], true); });
  const fromHash = () => { const m = /^#p(\d+)$/.exec(location.hash); return m ? Math.max(1, Math.min(total, +m[1])) : 1; };
  window.addEventListener("popstate", () => show(fromHash(), true));
  window.addEventListener("hashchange", () => show(fromHash(), true));
  $('[data-go="prev"]').onclick = () => go(cur - 1, true);
  $('[data-go="next"]').onclick = () => go(cur + 1, true);
  document.addEventListener("keydown", e => {
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
    const t = e.target; if (t.closest("input, select, textarea, canvas.pick, [contenteditable]")) return;
    if (e.key === "ArrowRight" || e.key === "PageDown") { if (cur < total) { e.preventDefault(); go(cur + 1, true); } }
    else if (e.key === "ArrowLeft" || e.key === "PageUp") { if (cur > 1) { e.preventDefault(); go(cur - 1, true); } }
  });
  let rz = 0; window.addEventListener("resize", () => { cancelAnimationFrame(rz); rz = requestAnimationFrame(() => { const c = ctrls[cur]; if (c && c.draw) c.draw(); }); });
  show(fromHash(), false);
  window.addEventListener("load", () => window.scrollTo(0, 0), { once: true });   // 網址有#p3時，瀏覽器會自己捲到那一節；改回從頁首開始，目錄按鈕才看得到
  window.__deck = { engine, go, shared, get page() { return cur; } };   // 給自動測試讀狀態用，不影響畫面
})();
