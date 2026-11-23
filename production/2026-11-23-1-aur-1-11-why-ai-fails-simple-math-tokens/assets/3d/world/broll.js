/* Motion-text B-roll (2D) for the 2026-11-22 Shorts. Original layouts; icons are Lucide (ISC) inlined by build.py as window.ICONS.
   One variant per scene via window.WORLD.broll. Everything is a pure function of the timeline time st.t (deterministic). */
(function () {
  var CFG = window.WORLD, D = CFG.dur, W = 1080;
  window.__timelines = window.__timelines || {};
  var root = document.getElementById("b-stage");
  var COL = { cyan: "#4CC9F0", amber: "#FFB703", mint: "#3DDC97", coral: "#FF5D73", violet: "#9B7BFF", ink: "#FFFFFF", muted: "#AAB4CF", blue: "#8FB4FF" };
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
  function sm(x) { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); }
  function seg(p, a, b) { return sm((p - a) / (b - a)); }
  function back(x) { x = clamp(x, 0, 1); var c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }
  function el(tag, cls, parent, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; (parent || root).appendChild(e); return e; }
  function icon(name, color, size) {
    var svg = (window.ICONS[name] || "").replace("<svg", '<svg style="width:' + size + "px;height:" + size + "px;stroke:" + color + '"');
    return svg;
  }
  // ---------- building blocks ----------
  function node(x, y, name, label, color, size) {
    size = size || 190;
    var n = el("div", "b-node");
    n.style.left = (x - size / 2) + "px"; n.style.top = (y - size / 2) + "px"; n.style.width = size + "px"; n.style.height = size + "px";
    n.style.borderColor = color; n.style.setProperty("--c", color);
    n.innerHTML = icon(name, color, Math.round(size * 0.52));
    var l = el("div", "b-label", root, label); l.style.color = color;
    l.style.left = (x - 200) + "px"; l.style.top = (y + size / 2 + 12) + "px";
    return { e: n, l: l, x: x, y: y, c: color, size: size };
  }
  function show(nd, k, lit) {
    var s = k <= 0 ? 0 : 0.6 + 0.4 * back(k);
    nd.e.style.transform = "scale(" + s + ")"; nd.e.style.opacity = clamp(k * 1.5, 0, 1);
    nd.l.style.opacity = clamp(k * 1.5, 0, 1);
    nd.e.style.boxShadow = "0 0 " + (20 + 60 * (lit || 0)) + "px " + (lit ? nd.c : "rgba(0,0,0,0.4)");
    nd.e.style.background = lit ? "rgba(30,44,90,0.98)" : "rgba(16,24,52,0.92)";
  }
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "1080"); svg.setAttribute("height", "1920"); svg.style.position = "absolute"; svg.style.left = "0"; svg.style.top = "0";
  root.appendChild(svg);
  function path(d, color, width, dash) {
    var p = document.createElementNS("http://www.w3.org/2000/svg", "path");
    p.setAttribute("d", d); p.setAttribute("fill", "none"); p.setAttribute("stroke", color); p.setAttribute("stroke-width", width || 8);
    p.setAttribute("stroke-linecap", "round"); if (dash) p.setAttribute("stroke-dasharray", dash);
    svg.appendChild(p); var L = p.getTotalLength(); return { p: p, L: L };
  }
  function draw(pp, k) { if (!pp.p.getAttribute("stroke-dasharray") || pp.solid) { pp.solid = true; pp.p.setAttribute("stroke-dasharray", pp.L + " " + pp.L); } pp.p.setAttribute("stroke-dashoffset", pp.L * (1 - clamp(k, 0, 1))); }
  function dotAt(dot, pp, k) { var pt = pp.p.getPointAtLength(pp.L * clamp(k, 0, 1)); dot.style.transform = "translate(" + (pt.x - 22) + "px," + (pt.y - 22) + "px)"; }
  function newDot(color) { var d = el("div", "b-dot"); d.style.background = color; d.style.boxShadow = "0 0 30px 12px " + color; return d; }
  function line(a, b) { return "M " + a.x + " " + (a.y + a.size / 2 + 62) + " L " + b.x + " " + (b.y - b.size / 2 - 10); }
  function hline(a, b) { return "M " + (a.x + a.size / 2 + 10) + " " + a.y + " L " + (b.x - b.size / 2 - 10) + " " + b.y; }
  function console_(x, y, w, h, title) {
    var c = el("div", "b-console"); c.style.left = x + "px"; c.style.top = y + "px"; c.style.width = w + "px"; c.style.height = h + "px";
    el("div", "b-con-title", c, '<span style="color:#FF5D73">●</span> <span style="color:#FFB703">●</span> <span style="color:#3DDC97">●</span>&nbsp;&nbsp;' + title);
    var body = el("div", "b-con-body", c);
    return { c: c, body: body };
  }
  function typed(text, k) { var n = Math.round(text.length * clamp(k, 0, 1)); return text.slice(0, n); }
  function rowHTML(tag, color, text, k, caret) {
    if (k <= 0) return "";
    return '<div class="b-row"><span class="b-tag" style="color:' + color + ';border-color:' + color + '">' + tag + '</span> ' + typed(text, k) +
      (caret && k < 1 ? '<span class="b-caret">▍</span>' : "") + "</div>";
  }
  var big = el("div", "b-big"); var sub = el("div", "b-sub");
  function bigText(html, k, y, color) {
    big.innerHTML = html; big.style.top = y + "px"; big.style.color = color || COL.ink;
    big.style.opacity = clamp(k * 1.4, 0, 1); big.style.transform = "translateX(-50%) scale(" + (0.85 + 0.15 * back(k)) + ")";
  }
  function subText(html, k, y, color) {
    sub.innerHTML = html; sub.style.top = y + "px"; sub.style.color = color || COL.muted;
    sub.style.opacity = clamp(k * 1.4, 0, 1); sub.style.transform = "translateX(-50%) translateY(" + (20 * (1 - sm(k))) + "px)";
  }

  // ---------- variants ----------
  var V = {};
  V.formula = function () {
    var llm = node(300, 560, "brain", "LLM", COL.violet, 210), tools = node(780, 560, "wrench", "Tools", COL.amber, 210),
        loop = node(300, 960, "repeat", "Loop", COL.mint, 210), agent = node(780, 960, "bot", "AI Agent", COL.cyan, 230);
    var plus1 = el("div", "b-op", root, "+"), plus2 = el("div", "b-op", root, "+"), eq = el("div", "b-op", root, "=");
    plus1.style.left = "500px"; plus1.style.top = "500px"; plus2.style.left = "250px"; plus2.style.top = "735px"; eq.style.left = "500px"; eq.style.top = "900px";
    return function (t, p) {
      bigText("AI AGENT = ?", 1 - seg(p, 0.38, 0.46), 640, COL.ink);
      show(llm, seg(p, 0.46, 0.54), p > 0.46 && p < 0.62 ? 1 : 0.2);
      plus1.style.opacity = seg(p, 0.6, 0.66);
      show(tools, seg(p, 0.62, 0.7), p > 0.62 && p < 0.78 ? 1 : 0.2);
      plus2.style.opacity = seg(p, 0.76, 0.82);
      show(loop, seg(p, 0.78, 0.86), p > 0.78 && p < 0.92 ? 1 : 0.2);
      eq.style.opacity = seg(p, 0.88, 0.92);
      show(agent, seg(p, 0.9, 0.98), p > 0.9 ? 0.6 + 0.4 * Math.sin(t * 8) : 0);
      subText("Anthropic: agents = LLMs using tools in a loop", seg(p, 0.05, 0.2) * (1 - seg(p, 0.38, 0.46)), 820);
    };
  };
  function traceScene(mode) {
    var con = console_(70, 300, 940, mode === 1 ? 300 : 470, "agent.run()  ·  example");
    var y = mode === 1 ? 830 : 1010, s = 150;
    var user = node(150, y, "user", "User", COL.blue, s), llm = node(410, y, "brain", "LLM", COL.violet, s),
        tool = node(670, y, "search", "Tool", COL.amber, s), db = node(930, y, "database", "Data", COL.mint, s);
    var l1 = path(hline(user, llm), COL.blue, 7), l2 = path(hline(llm, tool), COL.violet, 7), l3 = path(hline(tool, db), COL.amber, 7);
    var dot = newDot(COL.ink);
    var goal = "GOAL  Goa ki sabse sasti travel";
    return function (t, p) {
      if (mode === 1) {
        draw(l1, seg(p, 0.12, 0.25)); draw(l2, seg(p, 0.2, 0.33)); draw(l3, seg(p, 0.28, 0.41));
        [user, llm, tool, db].forEach(function (n, i) { show(n, seg(p, 0.02 + i * 0.08, 0.12 + i * 0.08), 0.2); });
        con.body.innerHTML = rowHTML("GOAL", COL.cyan, "Goa ki sabse sasti travel", seg(p, 0.42, 0.85), true);
        var k = seg(p, 0.45, 0.95); dotAt(dot, l1, k); dot.style.opacity = k > 0 && k < 1 ? 1 : 0;
        show(llm, 1, k >= 1 ? 1 : 0.2);
        subText("ReAct loop: Think → Act → Observe", seg(p, 0.15, 0.3), 1180, COL.muted);
      } else {
        draw(l1, 1); draw(l2, 1); draw(l3, 1);
        var think = seg(p, 0.02, 0.3), act = seg(p, 0.36, 0.55), obs = seg(p, 0.62, 0.92);
        con.body.innerHTML = rowHTML("GOAL", COL.cyan, "Goa ki sabse sasti travel", 1) +
          rowHTML("THINK", COL.violet, "pehle flights check karo", think, true) +
          rowHTML("ACT", COL.amber, "search_flights(\"Goa\")", act, true) +
          rowHTML("OBSERVE", COL.coral, "₹₹₹₹  bahut mehenga  ✗", obs, true);
        show(user, 1, 0.1); show(llm, 1, think > 0 && think < 1 ? 1 : 0.2); show(tool, 1, act > 0 && obs < 0.5 ? 1 : 0.2); show(db, 1, obs > 0 && obs < 1 ? 1 : 0.2);
        // dot: LLM -> tool during ACT, tool -> db -> back during OBSERVE
        if (act > 0 && act < 1) { dotAt(dot, l2, act); dot.style.opacity = 1; }
        else if (obs > 0 && obs < 1) { dotAt(dot, l3, obs < 0.5 ? obs * 2 : 2 - obs * 2); dot.style.opacity = 1; dot.style.background = obs < 0.5 ? COL.ink : COL.coral; }
        else dot.style.opacity = 0;
        subText("har step ka result → next decision", seg(p, 0.85, 0.95), 1180, COL.muted);
      }
    };
  }
  V.trace1 = function () { return traceScene(1); };
  V.trace2 = function () { return traceScene(2); };
  V.loop = function () {
    var cx = 540, cy = 790, R = 300;
    var ring = path("M " + cx + " " + (cy - R) + " A " + R + " " + R + " 0 1 1 " + (cx - 0.1) + " " + (cy - R), "rgba(76,201,240,0.55)", 10);
    var think = node(cx, cy - R, "brain", "Think", COL.violet, 170), act = node(cx + R * 0.87, cy + R * 0.5, "wrench", "Act", COL.amber, 170),
        obs = node(cx - R * 0.87, cy + R * 0.5, "eye", "Observe", COL.mint, 170), core = node(cx, cy, "bot", "Agent", COL.cyan, 200);
    var dot = newDot(COL.ink);
    return function (t, p) {
      draw(ring, seg(p, 0.0, 0.25));
      show(core, seg(p, 0.0, 0.1), 0.5 + 0.5 * Math.sin(t * 6));
      var k = seg(p, 0.2, 1.0) * 2 % 1, ang = -Math.PI / 2 + k * Math.PI * 2;
      var dx = cx + R * Math.cos(ang), dy = cy + R * Math.sin(ang);
      dot.style.transform = "translate(" + (dx - 22) + "px," + (dy - 22) + "px)"; dot.style.opacity = p > 0.2 ? 1 : 0;
      function near(a) { var d = Math.abs(Math.atan2(Math.sin(ang - a), Math.cos(ang - a))); return p > 0.2 ? clamp(1 - d / 0.7, 0, 1) : 0; }
      show(think, seg(p, 0.05, 0.15), near(-Math.PI / 2)); show(act, seg(p, 0.1, 0.2), near(Math.PI / 6)); show(obs, seg(p, 0.15, 0.25), near(5 * Math.PI / 6));
      subText("har result ke baad → <b style='color:#FFB703'>next move</b>", seg(p, 0.45, 0.6), 1200, COL.ink);
    };
  };
  V.request = function () {
    var win = el("div", "b-chat"); win.style.left = "90px"; win.style.top = "330px";
    el("div", "b-chat-title", win, icon("message-square", COL.blue, 44) + "&nbsp; Teams chat · example");
    var body = el("div", "b-chat-body", win);
    var agent = node(540, 1060, "bot", "Agent Service", COL.cyan, 200);
    var pkt = el("div", "b-pkt", root, icon("mail", COL.ink, 60));
    var lane = path("M 540 760 L 540 930", "rgba(143,180,255,0.6)", 8, "4 22");
    var q = "mera leave balance kitna hai?";
    return function (t, p) {
      var k = seg(p, 0.35, 0.85);
      body.innerHTML = '<div class="b-msg">' + icon("user", COL.blue, 52) + '<div class="b-bubble">' + typed(q, k) + (k < 1 && p > 0.35 ? '<span class="b-caret">▍</span>' : "") + "</div></div>";
      win.style.opacity = seg(p, 0.0, 0.12); win.style.transform = "translateY(" + (40 * (1 - seg(p, 0, 0.15))) + "px)";
      show(agent, seg(p, 0.05, 0.2), p > 0.95 ? 1 : 0.25);
      var f = seg(p, 0.86, 0.98);
      pkt.style.opacity = f > 0 && f < 1 ? 1 : 0; pkt.style.transform = "translate(500px," + (720 + 220 * f) + "px) scale(" + (1 - 0.3 * f) + ")";
      lane.p.setAttribute("stroke-dashoffset", -t * 60);
    };
  };
  V.security = function () {
    var x = 540, ys = [340, 610, 880, 1150];
    var user = node(x, ys[0], "user", "User input", COL.blue, 140), gIn = node(x, ys[1], "shield-check", "Input check", COL.mint, 150),
        agent = node(x, ys[2], "bot", "Agent", COL.cyan, 160), gOut = node(x, ys[3], "shield-check", "Output check", COL.mint, 150);
    var badge = el("div", "b-badge", root, icon("key-round", "#8FB4FF", 52) + "&nbsp;Entra identity");
    var p1 = path("M 540 492 L 540 528", COL.blue, 8), p2 = path("M 540 762 L 540 795", COL.mint, 8), p3 = path("M 540 1032 L 540 1068", COL.cyan, 8);
    var prev = el("div", "b-chip", root, "agent guardrails: preview"); prev.style.left = "650px"; prev.style.top = "585px";
    var dGood = newDot(COL.mint), dBad = newDot(COL.coral), x_ = el("div", "b-x", root, "✗");
    x_.style.left = "330px"; x_.style.top = "540px";
    return function (t, p) {
      [p1, p2, p3].forEach(function (pp, i) { draw(pp, seg(p, 0.03 + i * 0.05, 0.15 + i * 0.05)); });
      show(user, seg(p, 0.0, 0.1), 0.2); show(gIn, seg(p, 0.05, 0.15), 0.2); show(agent, seg(p, 0.1, 0.2), 0.2); show(gOut, seg(p, 0.15, 0.25), 0.2);
      prev.style.opacity = seg(p, 0.2, 0.3);
      var g = seg(p, 0.2, 0.5);
      if (g > 0 && g < 1) { var q = g * 3; dotAt(dGood, q < 1 ? p1 : q < 2 ? p2 : p3, q % 1); dGood.style.opacity = 1; } else dGood.style.opacity = 0;
      show(gIn, 1, (g > 0.25 && g < 0.45) ? 1 : 0.2); show(gOut, 1, (g > 0.85 && g < 1) ? 1 : 0.2);
      var b = seg(p, 0.28, 0.42); dotAt(dBad, p1, Math.min(b, 0.98)); dBad.style.opacity = b > 0 && p < 0.5 ? 1 : 0;
      x_.style.opacity = p > 0.42 && p < 0.56 ? 1 : 0;
      show(gIn, 1, p > 0.42 && p < 0.56 ? 1 : (g > 0.25 && g < 0.45 ? 1 : 0.2));
      var k = seg(p, 0.6, 0.78);
      badge.style.opacity = k; badge.style.transform = "translate(" + (760 - 120 * k) + "px," + (840) + "px)";
      show(agent, 1, k >= 1 ? 0.8 : 0.2);
    };
  };
  V.flow = function () {
    var teams = node(540, 340, "message-square", "Teams", COL.blue, 130), svc = node(540, 600, "bot", "Agent Service", COL.cyan, 150),
        model = node(220, 900, "brain", "Model", COL.violet, 130), iq = node(540, 900, "database", "Foundry IQ", COL.mint, 130),
        tools = node(860, 900, "wrench", "Tools", COL.amber, 130), guard = node(540, 1170, "shield-check", "Guardrails", COL.mint, 130);
    var e = [path("M 540 480 L 540 520", COL.blue, 8), path("M 470 750 L 260 830", COL.violet, 8), path("M 540 750 L 540 830", COL.mint, 8),
             path("M 610 750 L 820 830", COL.amber, 8), path("M 540 1040 L 540 1100", COL.mint, 8)];
    var dot = newDot(COL.ink);
    var nodes = [teams, svc, model, iq, tools, guard];
    return function (t, p) {
      nodes.forEach(function (n, i) { show(n, seg(p, i * 0.05, 0.08 + i * 0.05), 0.2); });
      e.forEach(function (pp, i) { draw(pp, seg(p, 0.1 + i * 0.04, 0.2 + i * 0.04)); });
      var k = seg(p, 0.3, 0.95), legs = [[e[0], teams, svc], [e[1], svc, model], [e[2], svc, iq], [e[3], svc, tools], [e[4], iq, guard]];
      var li = Math.min(4, Math.floor(k * 5)), lk = k * 5 - li;
      if (k > 0 && k < 1) { dotAt(dot, legs[li][0], lk); dot.style.opacity = 1; show(legs[li][2], 1, lk > 0.6 ? 1 : 0.2); } else dot.style.opacity = 0;
      if (k >= 1) nodes.forEach(function (n) { show(n, 1, 0.5 + 0.3 * Math.sin(t * 6)); });
    };
  };
  // ---------- 2026-11-23 variants (tokens Short) ----------
  function chips(labels, x0, y, color, gap) {
    return labels.map(function (s, i) {
      var c = el("div", "b-chip", root, s); c.style.fontSize = "64px"; c.style.fontWeight = "900"; c.style.color = color; c.style.borderColor = color;
      c.style.borderRadius = "18px"; c.style.padding = "8px 26px"; c.style.background = "rgba(16,24,52,0.95)";
      c.style.left = (x0 + i * gap) + "px"; c.style.top = y + "px"; return c;
    });
  }
  V.tokens = function () {
    var txt = node(540, 450, "type", "Text", COL.ink, 180), cut = node(540, 800, "scissors", "Tokens", COL.amber, 180), cpu = node(540, 1150, "cpu", "Model", COL.violet, 180);
    var l1 = path("M 540 602 L 540 698", COL.ink, 8), l2 = path("M 540 952 L 540 1048", COL.amber, 8);
    var raw = el("div", "b-chip", root, "8302447"); raw.style.fontSize = "60px"; raw.style.fontWeight = "900"; raw.style.color = COL.ink; raw.style.left = "690px"; raw.style.top = "410px";
    var ch = chips(["830", "244", "7"], 640, 765, COL.amber, 150);
    var dot = newDot(COL.ink);
    return function (t, p) {
      show(txt, seg(p, 0.0, 0.12), p < 0.3 ? 1 : 0.25);
      raw.style.opacity = seg(p, 0.08, 0.18) * (1 - seg(p, 0.45, 0.55));
      draw(l1, seg(p, 0.15, 0.3));
      show(cut, seg(p, 0.25, 0.38), p > 0.3 && p < 0.7 ? 1 : 0.25);
      ch.forEach(function (c, i) { var k = seg(p, 0.42 + i * 0.06, 0.52 + i * 0.06); c.style.opacity = k; c.style.transform = "translateY(" + (-40 * (1 - k)) + "px)"; });
      draw(l2, seg(p, 0.55, 0.7));
      show(cpu, seg(p, 0.62, 0.75), p > 0.72 ? 0.6 + 0.4 * Math.sin(t * 7) : 0.25);
      var k = seg(p, 0.15, 0.85);
      if (k > 0 && k < 1) { dotAt(dot, k < 0.5 ? l1 : l2, k < 0.5 ? k * 2 : (k - 0.5) * 2); dot.style.opacity = 1; } else dot.style.opacity = 0;
      subText("the model sees chunks, not digits", seg(p, 0.8, 0.92), 1330, COL.ink);
    };
  };
  V.letters = function () {
    var word = el("div", "b-big", root, "strawberry"); word.style.fontSize = "120px";
    var ch = chips(["str", "aw", "berry"], 200, 760, COL.amber, 230);
    var hide = node(540, 1080, "eye-off", "", COL.coral, 170);
    var q = el("div", "b-sub", root, "how many r's?");
    var ctr = el("div", "b-big", root, ""); ctr.style.fontSize = "110px";
    return function (t, p) {
      word.style.top = "470px"; word.style.opacity = seg(p, 0.0, 0.12) * (1 - seg(p, 0.3, 0.4));
      ch.forEach(function (c, i) { var k = seg(p, 0.3 + i * 0.06, 0.42 + i * 0.06); c.style.opacity = k; c.style.transform = "scale(" + (0.7 + 0.3 * k) + ")"; });
      show(hide, seg(p, 0.5, 0.62), 0.6 + 0.4 * Math.sin(t * 6));
      q.style.top = "620px"; q.style.opacity = seg(p, 0.1, 0.2); q.style.transform = "translateX(-50%)"; q.style.color = COL.ink;
      var guess = p < 0.7 ? "" : (Math.floor(t * 3) % 2 ? "2?" : "3?");
      ctr.textContent = guess; ctr.style.top = "1260px"; ctr.style.color = COL.coral; ctr.style.opacity = p > 0.7 ? 1 : 0;
    };
  };
  var draw_ = V[CFG.broll]();
  document.getElementById("w-pill").textContent = CFG.pill;
  var pill = document.getElementById("w-pill");
  if (CFG.pill.length > 34) pill.style.fontSize = "44px"; else if (CFG.pill.length > 27) pill.style.fontSize = "50px";
  if (CFG.src) document.getElementById("w-src").textContent = CFG.src; else document.getElementById("w-src").style.display = "none";
  var st = { t: 0 };
  var tl = gsap.timeline({ paused: true });
  tl.to(st, { t: D, duration: D, ease: "none" }, 0);
  window.__timelines["main"] = tl;
  var ph = CFG.phase || [0, 1];
  function render() {
    var p = ph[0] + clamp(st.t / D, 0, 1) * (ph[1] - ph[0]);
    pill.style.opacity = seg(st.t, 0.05, 0.3);
    document.getElementById("b-grid").style.backgroundPosition = "0px " + (st.t * 30) + "px";
    draw_(st.t, p);
  }
  tl.eventCallback("onUpdate", render);
  render();
})();
