/* "Hundreds of AI agents built a browser" world (2026-11-23, original, procedural).
   A dusk construction site: a giant browser window on scaffolding (x 0, z -8), a site booth with a door marked LOCK
   (x 0, z 2), a crew of 20 small hard-hat robots, a planner robot at a task board (x -7) and a judge robot with a stamp (x 7).
   Everything is a pure function of st.t via KIT.frame (deterministic). */
(function () {
  var K = KIT, THREE = K.THREE, V = K.V, seg = K.seg, sm = K.sm, lerp = K.lerp, lerpV = K.lerpV, clamp = K.clamp;
  var C = K.C, CSS = K.CSS, SHOT = K.SHOT, scene = K.scene;
  K.lights(0x1b1633, 30, 110);
  (function () { var c = document.getElementById("w-counter"); c.style.background = "rgba(11,16,32,0.9)"; c.style.padding = "6px 26px"; c.style.borderRadius = "22px"; c.style.fontSize = "72px"; c.style.right = "50px"; })();

  // ---------- ground + sky ----------
  K.box(120, 0.1, 120, K.std(0x3a3346), 0, -0.05, 0);
  var sky = K.textCanvas(1024, 512, function (g, w, h) {
    var gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#1d2350"); gr.addColorStop(0.6, "#6a3d6e"); gr.addColorStop(1, "#e08a5a");
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (var i = 0; i < 18; i++) { var bw = 40 + K.rng() * 70, bh = 60 + K.rng() * 170, bx = K.rng() * w; g.fillStyle = "#2a2140"; g.fillRect(bx, h - bh, bw, bh); }
    for (var c = 0; c < 2; c++) { g.strokeStyle = "#2a2140"; g.lineWidth = 6; var cx = 160 + c * 620; g.beginPath(); g.moveTo(cx, h); g.lineTo(cx, 120); g.lineTo(cx + 220, 120); g.stroke(); g.beginPath(); g.moveTo(cx + 200, 120); g.lineTo(cx + 200, 200); g.stroke(); }
  });
  K.plane(90, 40, new THREE.MeshBasicMaterial({ map: sky.tex }), 0, 18, -40, 0);
  // stripes on the ground (site markings)
  for (var s = -3; s <= 3; s++) K.box(0.25, 0.02, 9, K.std(C.amber, { e: C.amber, ei: 0.15 }), s * 2.2, 0.01, 7);

  // ---------- giant browser window on scaffolding ----------
  var WZ = -8, WY = 6.2, WW = 13, WH = 9;
  var pole = K.std(0x8a8fa0, { m: 0.4, r: 0.4 });
  [-7.2, -2.4, 2.4, 7.2].forEach(function (x) { K.box(0.18, 11.5, 0.18, pole, x, 5.75, WZ + 1.0); K.box(0.18, 11.5, 0.18, pole, x, 5.75, WZ - 0.6); });
  [2.2, 5.6, 9.0].forEach(function (y) { K.box(14.6, 0.14, 0.14, pole, 0, y, WZ + 1.0); K.box(14.6, 0.5, 1.8, K.std(0x5b4636), 0, y - 0.2, WZ + 0.3); });
  var frameMat = K.std(0x1d2540, { r: 0.4 });
  K.box(WW + 0.4, WH + 0.4, 0.3, frameMat, 0, WY, WZ - 0.2);
  var bar = K.textCanvas(1024, 96, function (g, w, h) {
    g.fillStyle = "#2b3560"; g.fillRect(0, 0, w, h);
    [CSS.coral, CSS.amber, CSS.mint].forEach(function (c, i) { g.fillStyle = c; g.beginPath(); g.arc(40 + i * 40, 48, 13, 0, 7); g.fill(); });
    g.fillStyle = "#0e1430"; K.roundRect(g, 180, 22, 640, 52, 26); g.fill();
    g.fillStyle = "#AAB4CF"; g.font = "700 32px " + K.FONT; g.textBaseline = "middle"; g.fillText("new-browser://from-scratch", 210, 49);
  });
  K.plane(WW, 1.0, new THREE.MeshBasicMaterial({ map: bar.tex }), 0, WY + WH / 2 - 0.5, WZ - 0.02, 0);
  // content panels: 4 x 3 grid that fills in
  var panels = [];
  var pcol = [CSS.cyan, CSS.violet, CSS.mint, CSS.amber];
  for (var r = 0; r < 3; r++) for (var c = 0; c < 4; c++) {
    var tex = K.textCanvas(256, 200, (function (col, r, c) { return function (g, w, h) {
      g.fillStyle = "#16204a"; g.fillRect(0, 0, w, h);
      g.fillStyle = col; g.fillRect(16, 18, w * (0.4 + 0.15 * ((r + c) % 3)), 22);
      g.fillStyle = "#3a4a86"; for (var k = 0; k < 4; k++) g.fillRect(16, 60 + k * 30, w - 32 - (k * 23 % 60), 14);
    }; })(pcol[(r + c) % 4], r, c));
    var m = K.plane(WW / 4 - 0.3, (WH - 1.2) / 3 - 0.3, new THREE.MeshBasicMaterial({ map: tex.tex, transparent: true }),
      -WW / 2 + (c + 0.5) * WW / 4, WY + WH / 2 - 1.0 - (r + 0.5) * (WH - 1.2) / 3, WZ, 0);
    m.userData = { home: m.position.clone(), i: r * 4 + c };
    panels.push(m);
  }
  var winLight = new THREE.PointLight(0x8fb4ff, 0, 30); winLight.position.set(0, WY, WZ + 5); scene.add(winLight);
  // hanging sign (shot 8)
  var expSign = K.plane(6.4, 1.3, K.sign("EXPERIMENT", CSS.amber, 900, 180, 110), 0, 13, WZ + 1.4, 0);

  // ---------- site booth with the LOCK door ----------
  var boothMat = K.std(0xd9a441, { r: 0.6 });
  var booth = new THREE.Group(); scene.add(booth);
  K.box(4.2, 3.2, 0.25, boothMat, 0, 1.6, 1.2, booth);           // back
  K.box(0.25, 3.2, 2.4, boothMat, -2.0, 1.6, 2.3, booth);
  K.box(0.25, 3.2, 2.4, boothMat, 2.0, 1.6, 2.3, booth);
  K.box(4.4, 0.25, 2.8, K.std(0x6b4a34), 0, 3.3, 2.3, booth);
  K.box(1.2, 2.4, 0.12, K.std(0x2b3560), 0, 1.2, 3.45, booth);   // door
  K.box(1.5, 0.6, 0.25, boothMat, -1.35, 2.9, 3.45, booth); K.box(1.5, 0.6, 0.25, boothMat, 1.35, 2.9, 3.45, booth);
  K.box(1.4, 2.4, 0.25, boothMat, -1.3, 1.2, 3.45, booth); K.box(1.4, 2.4, 0.25, boothMat, 1.3, 1.2, 3.45, booth);
  var lockSign = K.plane(2.4, 0.8, K.sign("🔒 LOCK", CSS.coral, 600, 200, 104), 0, 3.95, 3.62, 0, booth);
  var openSign = K.plane(2.4, 0.8, K.sign("OPEN", CSS.mint, 600, 200, 110), 0, 3.95, 3.63, 0, booth);
  var qSign = K.plane(0.9, 0.9, K.sign("?", CSS.amber, 200, 200, 150), 0, 5.1, 3.6, 0, booth);

  // ---------- crew: 20 small hard-hat robots ----------
  var hatMat = K.std(C.amber, { r: 0.5 });
  function crewBot(accent) {
    var b = K.makeRobot({ accent: accent || C.cyan });
    K.cyl(0.46, 0.52, 0.26, 12, hatMat, 0, 0.52, 0, b.userData.head);
    K.cyl(0.6, 0.6, 0.04, 14, hatMat, 0, 0.41, 0.08, b.userData.head);
    b.scale.setScalar(0.42);
    return b;
  }
  var crew = [];
  for (var i = 0; i < 20; i++) crew.push(crewBot());
  var key = K.sphere(0.16, K.std(C.amber, { e: C.amber, ei: 0.9 }), 0, 0, 0, null, 0);
  var lostKey = K.sphere(0.16, K.std(C.coral, { e: C.coral, ei: 0.9 }), 3.2, 0.2, 5.5, null, 0);
  var dust = [0, 1, 2, 3].map(function () { return K.sphere(0.35, K.glow(0xd8c8b0, 0.35), 0, 0, 0, null, 0); });

  // planner, judge and task cards
  var planner = K.makeRobot({ accent: C.violet }); planner.scale.setScalar(0.7); planner.position.set(-7.4, 0, -1.5); planner.rotation.y = 0.5;
  var judge = K.makeRobot({ accent: C.amber }); judge.scale.setScalar(0.7); judge.position.set(7.4, 0, -1.5); judge.rotation.y = -0.5;
  var board = K.plane(2.6, 2.0, K.sign("TASKS", CSS.violet, 520, 400, 90), -7.4, 2.6, -3.0, 0.4);
  var stamp = K.cyl(0.32, 0.32, 0.3, 12, K.std(C.amber, { e: C.amber, ei: 0.4 }), 0, 0, 0);
  var stampMark = K.plane(1.2, 1.2, K.sign("✓", CSS.mint, 200, 200, 160), 6.6, 3.0, -2.4, -0.4);
  var cards = [0, 1, 2, 3, 4].map(function (i) {
    return K.plane(0.7, 0.5, K.sign("task " + (i + 1), CSS.violet, 260, 180, 56), 0, 0, 0, 0);
  });

  // ---------- helpers ----------
  function eyesOn(b, on) { b.userData.eyes.forEach(function (e) { e.material.color.setHex(on ? C.cyan : 0x4a5068); }); }
  function resetCrew(t) {
    crew.forEach(function (b, i) {
      b.visible = true; b.rotation.set(0, 0, 0); eyesOn(b, true); K.robotIdle(b, t + i * 0.37, 0);
    });
  }
  function jamPos(i, t) {   // crowd squeezed at the door, facing it (-z)
    var row = Math.floor(i / 6), col = i % 6;
    var x = (col - 2.5) * (0.95 - row * 0.05) + 0.12 * Math.sin(t * 2.3 + i);
    return V(x, 0, 4.3 + row * 0.95 + 0.06 * Math.sin(t * 3 + i * 1.7));
  }
  function sitePos(i) {      // spread around the site
    var a = i * 2.39996, rr = 3.2 + (i % 5) * 1.1;
    return V(Math.sin(a) * rr * 1.4, 0, 1.0 + Math.cos(a) * rr * 0.7);
  }
  function workPos(i, n) { return V(-5 + (i + 0.5) * (10 / n), 0, WZ + 2.3); }
  function panelFill(k, flicker, t) {
    panels.forEach(function (m, i) {
      var on = clamp(k * 12 - i, 0, 1);
      m.visible = on > 0.02;
      var f = flicker ? (0.55 + 0.45 * Math.abs(Math.sin(t * (3 + i * 0.7) + i))) : 1;
      m.material.opacity = on * f;
      m.position.copy(m.userData.home); m.rotation.z = 0;
    });
    winLight.intensity = 2.2 * k;
  }

  var wide = { pos: V(0, 9.5, 24), look: V(0, 4.0, -2) };

  K.frame(function (t, p) {
    var out = {};
    resetCrew(t);
    key.visible = lostKey.visible = false;
    dust.forEach(function (d) { d.visible = false; });
    cards.forEach(function (c) { c.visible = false; });
    stamp.visible = false; stampMark.visible = false;
    planner.visible = judge.visible = board.visible = false;
    lockSign.visible = true; openSign.visible = false; qSign.visible = false;
    expSign.position.y = 13; expSign.visible = SHOT === 8;
    booth.visible = SHOT <= 3 || SHOT === 10;
    panelFill(0.15, false, t);
    K.robotIdle(planner, t, 0); K.robotIdle(judge, t + 1, 0);

    if (SHOT === 1) {           // jam at the LOCK door
      crew.forEach(function (b, i) { b.position.copy(jamPos(i, t)); b.rotation.y = Math.PI + 0.25 * Math.sin(t * 2 + i); });
      lockSign.scale.setScalar(1 + 0.08 * Math.sin(t * 7));
      K.cam(lerpV(V(4.2, 5.2, 13.0), V(3.0, 4.4, 10.2), sm(p)), V(0, 1.6, 4.2));
      K.tag(0, V(-1.6, 1.6, 5.5), "20 agents", CSS.cyan, seg(p, 0.15, 0.3));
      K.tag(1, V(-2.6, 3.2, 3.6), "1 shared lock", CSS.coral, seg(p, 0.45, 0.6));
    } else if (SHOT === 2) {    // pull back + rise: the browser being built
      crew.forEach(function (b, i) { b.position.copy(jamPos(i, t)); b.rotation.y = Math.PI; });
      qSign.visible = true; qSign.scale.setScalar(K.pop(p, 0.15) || 0.001);
      K.cam(lerpV(V(3.0, 3.1, 9.0), wide.pos, sm(p)), lerpV(V(0, 1.9, 3.6), wide.look, sm(p)));
      panelFill(0.15 + 0.3 * seg(p, 0.4, 1), false, t);
      K.tag(0, V(0, 11, WZ), "a browser, from scratch", CSS.mint, seg(p, 0.55, 0.7));
    } else if (SHOT === 3) {    // single-file queue; one holds the key, one forgot it
      crew.forEach(function (b, i) {
        var step = Math.floor(t * 0.8) * 0.0; // queue barely moves
        if (i === 0) { b.position.set(0, 0, 4.3); b.rotation.y = Math.PI; }
        else { b.position.set(0.95 * i, 0, 4.6 + 0.1 * Math.sin(i * 1.9)); b.rotation.y = -Math.PI / 2; }
      });
      var lead = crew[0];
      lead.userData.arms[1].sh.rotation.x = -1.2;
      key.visible = true; key.position.set(lead.position.x + 0.3, 1.25, lead.position.z - 0.3);
      key.material.emissiveIntensity = 0.6 + 0.5 * Math.sin(t * 5);
      lostKey.visible = p > 0.45; lostKey.material.emissiveIntensity = (Math.floor(t * 4) % 2) ? 1.2 : 0.2;
      crew[7].position.set(3.2, 0, 6.6); crew[7].rotation.y = 0.4;
      lostKey.position.set(3.9, 0.2, 6.9);
      K.cam(lerpV(V(3.5, 3.4, 13.5), V(4.5, 3.0, 11.5), sm(p)), V(4.0, 1.1, 4.6));
      K.tag(0, V(0.0, 1.8, 4.2), "holds the lock", CSS.amber, seg(p, 0.1, 0.25));
      K.tag(1, V(5.6, 0.5, 7.4), "forgot to release", CSS.coral, seg(p, 0.5, 0.65));
    } else if (SHOT === 4) {    // 17 idle (dim), 3 working
      crew.forEach(function (b, i) {
        if (i < 3) { b.position.copy(workPos(i + 1, 5)); b.rotation.y = Math.PI; b.userData.arms.forEach(function (a) { a.sh.rotation.x = -1.6 + 0.4 * Math.sin(t * 8 + i); }); }
        else { b.position.copy(sitePos(i)); b.rotation.y = Math.PI * 0.2 * (i % 3 - 1); var d = seg(p, 0.1, 0.4); if (d > 0.5) eyesOn(b, false); b.userData.head.rotation.x = 0.35 * d; }
      });
      panelFill(0.3, false, t);
      K.cam(lerpV(V(0, 7.5, 19), V(0, 6.5, 16), sm(p)), V(0, 2.5, -1));
      var n = Math.round(lerp(20, 3, seg(p, 0.15, 0.7)));
      var k4 = seg(p, 0.15, 0.6);
      out.counter = k4 >= 1 ? "2-3 working" : (Math.round(lerp(20, 3, k4)) + " working"); out.counterColor = k4 >= 1 ? CSS.coral : CSS.cyan;
      K.tag(0, V(0, 2.6, WZ + 2.3), "3 actually working", CSS.mint, seg(p, 0.6, 0.75));
    } else if (SHOT === 5) {    // churn: panels placed, knocked off, redone
      crew.forEach(function (b, i) {
        if (i < 5) { b.position.copy(workPos(i, 5)); b.rotation.y = Math.PI; b.userData.arms.forEach(function (a) { a.sh.rotation.x = -1.5 + 0.5 * Math.sin(t * 7 + i); }); }
        else b.visible = false;
      });
      panelFill(0.45, false, t);
      var cyc = (t * 0.9) % 1;
      [4, 5, 6, 7].forEach(function (pi, j) {
        var m = panels[pi], ph = (cyc + j * 0.25) % 1;
        m.visible = true; m.material.opacity = 1;
        if (ph > 0.55) { var f = seg(ph, 0.55, 1); m.position.y = m.userData.home.y - 6.5 * f * f; m.rotation.z = 0.9 * f * (j % 2 ? 1 : -1); }
        var d = dust[j]; d.visible = ph > 0.9; d.position.set(m.userData.home.x, 0.4, WZ + 0.8); d.scale.setScalar(1 + 2 * seg(ph, 0.9, 1));
      });
      K.cam(lerpV(V(-3, 6.0, 9), V(3, 6.0, 8), sm(p)), V(0, 4.5, WZ));
      K.tag(0, V(0, 9.0, WZ + 1), "redo, redo, redo", CSS.coral, seg(p, 0.2, 0.35));
    } else if (SHOT === 7) {    // orderly site: planner -> workers -> judge, window fills
      planner.visible = judge.visible = board.visible = true;
      crew.forEach(function (b, i) {
        if (i < 8) { b.position.copy(workPos(i, 8)); b.rotation.y = Math.PI; b.userData.arms.forEach(function (a) { a.sh.rotation.x = -1.5 + 0.45 * Math.sin(t * 9 + i * 1.3); }); }
        else b.visible = false;
      });
      cards.forEach(function (c, i) {
        var ph = (t * 0.7 + i * 0.2) % 1; c.visible = true;
        var a = V(-7.0, 2.6, -2.6), b = workPos((i * 3) % 8, 8).add(V(0, 1.6, 0.4));
        c.position.copy(lerpV(a, b, ph)); c.position.y += 2.2 * Math.sin(ph * Math.PI); K.billboard(c);
      });
      stamp.visible = true; var thump = Math.abs(Math.sin(t * 2.4));
      stamp.position.set(6.7, 1.6 + 0.6 * thump, -1.6);
      stampMark.visible = true; stampMark.scale.setScalar(0.6 + 0.4 * (1 - thump));
      panelFill(0.35 + 0.65 * seg(p, 0.05, 0.95), false, t);
      var orb = sm(clamp(p * 1.15, 0, 1));
      K.cam(V(Math.sin(-0.45 + 0.9 * orb) * 16, 6.8, Math.cos(-0.45 + 0.9 * orb) * 16 - 2), V(0, 3.6, -4));
      K.tag(0, V(-7.4, 4.2, -1.5), "Planner", CSS.violet, seg(p, 0.05, 0.15));
      K.tag(1, V(-3.2, 3.4, WZ + 2.4), "Workers", CSS.cyan, seg(p, 0.12, 0.22));
      K.tag(2, V(7.4, 4.2, -1.5), "Judge", CSS.amber, seg(p, 0.2, 0.3));
      out.counter = p > 0.55 ? "1M+ lines" : "";
      out.counterColor = CSS.mint;
    } else if (SHOT === 8) {    // callback: the window lights up, unevenly; experiment sign lowers
      crew.forEach(function (b, i) {
        if (i < 10) { b.position.copy(workPos(i, 10)).add(V(0, 0, 3.2)); b.rotation.y = Math.PI; b.rotation.x = -0.18 * seg(p, 0.2, 0.5); }
        else b.visible = false;
      });
      panelFill(1, true, t);
      expSign.position.y = lerp(13, 11.6, seg(p, 0.25, 0.6));
      K.cam(lerpV(V(0, 4.0, 14), V(0, 5.0, 11), sm(p)), V(0, 6.8, WZ));
    } else if (SHOT === 10) {   // outro: door now OPEN, crew waves
      lockSign.visible = false; openSign.visible = true; openSign.scale.setScalar(1 + 0.05 * Math.sin(t * 5));
      panelFill(1, false, t);
      crew.forEach(function (b, i) {
        var q = jamPos(i, 0); b.position.set(q.x * 1.6, 0, q.z + 1.2); b.rotation.y = 0;
        K.robotIdle(b, t + i * 0.3, seg(p, 0.15 + (i % 5) * 0.04, 0.35 + (i % 5) * 0.04));
      });
      K.cam(lerpV(V(3.0, 3.6, 13.5), V(4.0, 6.5, 19), sm(p)), lerpV(V(0, 2.2, 3.6), V(0, 3.6, 0), sm(p)));
    } else {                    // fallback (B-roll scenes do not use this page)
      K.cam(wide.pos, wide.look);
    }
    return out;
  });
})();
