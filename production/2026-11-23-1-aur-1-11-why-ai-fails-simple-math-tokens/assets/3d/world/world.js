/* "Why AI fumbles long sums: tokens" world (2026-11-23, original, procedural).
   A daylight classroom: green-slate chalkboard on the back wall (z -4), a robot student standing beside it (x 3.4),
   a wooden table in front (z 1.2) where token tiles slide in. The board is a canvas redrawn every frame (chalk writing).
   Shots: 1 hook board, 2 glasses, 3 left-to-right cut, 4 comma re-cut, 5 result + paper, 6 callback tick, 7 outro wave. */
(function () {
  var K = KIT, THREE = K.THREE, V = K.V, seg = K.seg, sm = K.sm, lerp = K.lerp, lerpV = K.lerpV, clamp = K.clamp;
  var C = K.C, CSS = K.CSS, SHOT = K.SHOT, scene = K.scene;
  K.lights(0x2a3a3a, 30, 90);
  var sun = new THREE.DirectionalLight(0xfff1d6, 0.9); sun.position.set(-12, 16, 14); scene.add(sun);
  scene.add(new THREE.AmbientLight(0xffffff, 0.35));
  var CHALK = "#F4F1E8", GREEN = "#7CF0A8", WOOD = 0x9a6a42;

  // ---------- room ----------
  K.box(60, 0.1, 40, K.std(0xa77b52, { r: 0.8 }), 0, -0.05, 0);                    // wooden floor
  K.box(40, 16, 0.3, K.std(0xe9e0cc, { r: 0.9 }), 0, 8, -4.6);                      // back wall
  K.box(0.3, 16, 30, K.std(0xdcd2bc, { r: 0.9 }), -11, 8, 6);                       // left wall
  // window on the left wall (daylight)
  var winTex = K.textCanvas(512, 512, function (g, w, h) {
    var gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#8fd0ff"); gr.addColorStop(1, "#d8f0ff"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "#ffffff"; [[120, 140], [330, 220]].forEach(function (c) { g.beginPath(); g.arc(c[0], c[1], 50, 0, 7); g.arc(c[0] + 50, c[1] + 10, 40, 0, 7); g.fill(); });
    g.strokeStyle = "#f5efe2"; g.lineWidth = 22; g.strokeRect(0, 0, w, h); g.beginPath(); g.moveTo(w / 2, 0); g.lineTo(w / 2, h); g.moveTo(0, h / 2); g.lineTo(w, h / 2); g.stroke();
  });
  K.plane(5, 5, new THREE.MeshBasicMaterial({ map: winTex.tex }), -10.8, 6.5, 2, Math.PI / 2);
  // chalkboard
  K.box(7.6, 6.8, 0.25, K.std(0x6b4a2e), 0, 6.0, -4.35);                             // frame (portrait board for 9:16)
  K.box(7.4, 0.18, 0.5, K.std(0x6b4a2e), 0, 2.6, -4.1);                              // chalk ledge
  var boardC = K.textCanvas(1100, 920);
  var boardMesh = K.plane(7.2, 6.2, new THREE.MeshBasicMaterial({ map: boardC.tex }), 0, 6.0, -4.2, 0);
  // clock + poster (classroom cues)
  K.cyl(0.7, 0.7, 0.1, 24, K.std(0xffffff), 8.5, 9.4, -4.4).rotation.x = Math.PI / 2;
  K.plane(2.4, 3.0, K.sign("A B C", CSS.coral, 400, 500, 110, "#fdf6e3"), -8.6, 6.0, -4.4, 0);

  // ---------- robot student ----------
  var bot = K.makeRobot({ accent: C.mint });
  bot.scale.setScalar(1.05); bot.position.set(1.95, 0, 3.1); bot.rotation.y = -0.25;
  // glasses (thick, the "eyes" metaphor)
  var glasses = new THREE.Group(); bot.userData.head.add(glasses); glasses.position.set(0, 0.03, 0.48);
  var gMat = K.std(0x222833, { r: 0.3 });
  [-0.22, 0.22].forEach(function (x) { var r = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.035, 8, 20), gMat); r.position.set(x, 0, 0); glasses.add(r); });
  K.box(0.12, 0.03, 0.03, gMat, 0, 0.02, 0, glasses);
  var lensCut = [-0.22, 0.22].map(function (x) { return K.box(0.02, 0.32, 0.02, K.glow(C.coral), x, 0, 0.02, glasses); });

  // ---------- table + token tiles ----------
  var tbl = K.std(WOOD, { r: 0.6 });
  K.box(6.0, 0.25, 2.0, tbl, -0.4, 1.9, 1.2);
  [[-3.2, 0.4], [2.4, 0.4], [-3.2, 2.0], [2.4, 2.0]].forEach(function (q) { K.box(0.2, 1.9, 0.2, tbl, q[0], 0.95, q[1]); });
  function tile(label, color) {
    var g = new THREE.Group(); scene.add(g);
    var w = 0.55 + 0.42 * label.length;
    K.box(w, 0.9, 0.35, K.std(0xd9b27c, { r: 0.7 }), 0, 0, 0, g);
    K.plane(w - 0.1, 0.8, K.sign(label, color, Math.round(160 + 110 * label.length), 220, 140, "#fff6e6"), 0, 0, 0.18, 0, g);
    g.userData.w = w; return g;
  }
  var L2R = [tile("830", CSS.coral), tile("244", CSS.coral), tile("7", CSS.coral)];
  var R2L = [tile("8", "#2a9d6a"), tile("302", "#2a9d6a"), tile("447", "#2a9d6a")];
  var place = ["millions", "thousands", "ones"].map(function (s) { return K.plane(1.8, 0.42, K.sign(s, CSS.muted, 420, 100, 52, "rgba(11,16,32,0.85)"), 0, 0, 0, 0); });
  // paper + model name plates (shot 5), calculator + code props (shot 6/7)
  var paper = K.plane(1.6, 2.0, K.sign("PAPER", CSS.navy, 320, 400, 64, "#fbfaf5", "arXiv 2024"), -2.4, 2.1, 1.3, 0);
  paper.rotation.x = -Math.PI / 2 + 0.25;
  var plates = [K.plane(1.8, 0.6, K.sign("GPT-3.5", CSS.cyan, 420, 140, 76), -0.6, 2.35, 1.9, 0), K.plane(1.8, 0.6, K.sign("GPT-4", CSS.violet, 420, 140, 76), 1.4, 2.35, 1.9, 0)];
  var calc = new THREE.Group(); scene.add(calc);
  K.box(0.9, 0.18, 1.2, K.std(0x2b3560), 0, 0, 0, calc);
  K.plane(0.7, 0.3, K.glow(C.mint), 0, 0.1, -0.3, 0, calc).rotation.x = -Math.PI / 2;
  calc.position.set(-2.0, 2.1, 1.4);
  var codeCard = K.plane(1.4, 0.9, K.sign("</>", CSS.cyan, 300, 200, 110), 0.4, 2.6, 1.6, 0);

  // ---------- chalk board drawing ----------
  function chalkText(g, text, x, y, size, color, k, align) {
    var n = Math.round(text.length * clamp(k, 0, 1)); if (n <= 0) return;
    g.font = "700 " + size + "px 'Segoe Print', 'Comic Sans MS', " + K.FONT; g.fillStyle = color || CHALK;
    g.textAlign = align || "center"; g.textBaseline = "middle"; g.shadowColor = "rgba(255,255,255,0.35)"; g.shadowBlur = 6;
    g.fillText(text.slice(0, n), x, y); g.shadowBlur = 0;
  }
  function board(draw) {
    var g = boardC.ctx, w = 1100, h = 920;
    g.fillStyle = "#2f4a3e"; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,0.05)"; for (var i = 0; i < 40; i++) g.fillRect((i * 397) % w, (i * 211) % h, 180, 6);   // eraser smudges
    draw(g, w, h);
    boardC.tex.needsUpdate = true;
  }
  function cutMarks(g, xs, y, k) {
    g.strokeStyle = CSS.coral; g.lineWidth = 10; g.setLineDash([22, 14]);
    xs.forEach(function (x, i) { var kk = seg(k, i * 0.3, i * 0.3 + 0.3); if (kk <= 0) return; g.beginPath(); g.moveTo(x, y - 110); g.lineTo(x, y - 110 + 220 * kk); g.stroke(); });
    g.setLineDash([]);
  }
  function tick(g, x, y, k) {
    if (k <= 0) return; g.strokeStyle = GREEN; g.lineWidth = 26; g.lineCap = "round";
    g.beginPath(); g.moveTo(x - 70, y); g.lineTo(x - 20, y + 60 * Math.min(1, k * 2)); if (k > 0.5) g.lineTo(x - 20 + 140 * (k - 0.5) * 2, y + 60 - 150 * (k - 0.5) * 2); g.stroke();
  }

  function tileRow(tiles, k, xs, z, stagger) {
    tiles.forEach(function (t, i) {
      var kk = seg(k, i * stagger, i * stagger + 0.35);
      t.visible = kk > 0;
      t.position.set(lerp(xs[i] + 5, xs[i], kk), 2.5 + 0.6 * Math.sin(kk * Math.PI), z);
      t.rotation.set(0, 0, 0);
    });
  }
  // x (canvas px) of the cut after character n of `text` drawn centred at cx
  function cutX(g, text, cx, size, n) {
    g.font = "700 " + size + "px 'Segoe Print', 'Comic Sans MS', " + K.FONT;
    var full = g.measureText(text).width; return cx - full / 2 + g.measureText(text.slice(0, n)).width;
  }
  var BIG = 190, CX = 550;
  var camBoard = { pos: V(0.4, 5.0, 9.6), look: V(0.2, 4.6, -3.0) };
  var TX = [-1.9, -0.3, 1.2], TX2 = [-1.9, -0.6, 1.1];

  K.frame(function (t, p) {
    var out = {};
    L2R.concat(R2L).forEach(function (m) { m.visible = false; });
    place.forEach(function (m) { m.visible = false; });
    paper.visible = false; plates.forEach(function (m) { m.visible = false; });
    calc.visible = false; codeCard.visible = false;
    glasses.visible = SHOT >= 2; glasses.scale.setScalar(1); glasses.position.y = 0.03;
    lensCut.forEach(function (m) { m.visible = false; });
    K.robotIdle(bot, t, 0);
    bot.rotation.y = -0.25;

    if (SHOT === 1) {            // hook: the long sum, puzzled robot
      board(function (g) { chalkText(g, "8302447", CX, 250, BIG, CHALK, 1); chalkText(g, "+ 2", CX, 470, BIG, CHALK, 1); chalkText(g, "= ?", CX, 690, BIG, CSS.amber, 1); });
      var a = bot.userData.arms[1]; a.sh.rotation.z = 2.6 * a.s * seg(p, 0.35, 0.55); a.sh.rotation.x = -0.4 * seg(p, 0.35, 0.55);
      bot.userData.head.rotation.z = 0.25 * Math.sin(t * 3) * (1 - seg(p, 0.35, 0.55));
      K.cam(lerpV(V(0.6, 5.2, 11.6), camBoard.pos, sm(p)), camBoard.look);
      K.tag(0, V(1.95, 3.1, 3.1), "???", CSS.amber, seg(p, 0.1, 0.25));
    } else if (SHOT === 2) {     // the glasses: lenses slice the number into pieces
      board(function (g) {
        chalkText(g, "8302447", CX, 330, BIG, CHALK, 1);
        cutMarks(g, [cutX(g, "8302447", CX, BIG, 3), cutX(g, "8302447", CX, BIG, 6)], 330, seg(p, 0.45, 0.95));
      });
      var drop = seg(p, 0.05, 0.3);
      glasses.position.y = 0.03 + 0.8 * (1 - drop); glasses.scale.setScalar(1.25);
      lensCut.forEach(function (m) { m.visible = p > 0.45 && (Math.floor(t * 6) % 2 === 0); });
      var kc = sm(seg(p, 0, 0.6));
      K.cam(lerpV(camBoard.pos, V(2.45, 2.2, 7.4), kc), lerpV(camBoard.look, V(1.95, 1.85, 3.1), kc));
      K.tag(0, V(1.95, 2.9, 3.1), "the eyes", CSS.coral, seg(p, 0.55, 0.7));
    } else if (SHOT === 3) {     // left-to-right chunks [830][244][7]
      board(function (g) {
        chalkText(g, "8302447", CX, 330, BIG, CHALK, seg(p, 0, 0.25));
        cutMarks(g, [cutX(g, "8302447", CX, BIG, 3), cutX(g, "8302447", CX, BIG, 6)], 330, seg(p, 0.3, 0.75));
        chalkText(g, "cut left → right", CX, 640, 84, CSS.coral, seg(p, 0.35, 0.5));
      });
      tileRow(L2R, seg(p, 0.35, 1), TX, 1.5, 0.22);
      K.cam(lerpV(camBoard.pos, V(0.2, 4.7, 9.8), sm(p)), V(-0.2, 4.2, -2.4));
      K.tag(0, V(-0.3, 3.4, 1.5), "chunks ignore place value", CSS.coral, seg(p, 0.8, 0.92));
    } else if (SHOT === 4) {     // commas: cut moves right to left [8][302][447]
      var cm = seg(p, 0.2, 0.45);
      board(function (g) {
        if (cm > 0.5) {
          chalkText(g, "8,302,447", CX, 330, BIG - 20, GREEN, 1);
          cutMarks(g, [cutX(g, "8,302,447", CX, BIG - 20, 1) + 18, cutX(g, "8,302,447", CX, BIG - 20, 5) + 18], 330, seg(p, 0.45, 0.7));
        } else chalkText(g, "8302447", CX, 330, BIG, CHALK, 1);
        chalkText(g, "commas: cut right ← left", CX, 640, 74, GREEN, seg(p, 0.45, 0.6));
      });
      L2R.forEach(function (m, i) { var o = seg(p, 0.0, 0.2); m.visible = o < 1; m.position.set(TX[i] + 0.25 * Math.sin(t * 30 + i) * (1 - o), 2.5 - 2.4 * o, 1.5); m.rotation.z = 0.6 * o * (i - 1); });
      tileRow(R2L, seg(p, 0.45, 0.95), TX2, 1.5, 0.2);
      place.forEach(function (m, i) { m.visible = p > 0.8; m.position.set(TX2[i], 1.75, 1.9); });
      K.cam(V(0.2, 4.7, 9.8), V(-0.2, 4.2, -2.4));
      K.tag(0, V(-0.4, 3.5, 1.5), "lines up with place value", CSS.mint, seg(p, 0.85, 0.95));
    } else if (SHOT === 5) {     // the result: sum lit green, paper + model plates
      board(function (g) {
        chalkText(g, "8,302,447", CX, 210, 150, GREEN, seg(p, 0, 0.15)); chalkText(g, "+ 2", CX, 390, 150, GREEN, seg(p, 0.1, 0.2));
        chalkText(g, "= 8,302,449", CX, 570, 150, GREEN, seg(p, 0.15, 0.3)); chalkText(g, "commas → better accuracy", CX, 780, 62, CHALK, seg(p, 0.4, 0.7));
      });
      paper.visible = true; paper.position.y = 2.1 + 3 * (1 - seg(p, 0.15, 0.35));
      plates.forEach(function (m, i) { m.visible = seg(p, 0.3 + i * 0.08, 0.4 + i * 0.08) > 0; });
      K.cam(lerpV(V(0.2, 4.7, 9.8), V(0.4, 5.0, 10.6), sm(p)), V(0.0, 4.2, -2.6));
    } else if (SHOT === 6 || SHOT === 7) {   // callback board with tick (6: tools appear, 7: wave + pull back)
      board(function (g) {
        chalkText(g, "8,302,447", CX - 60, 210, 150, CHALK, 1); chalkText(g, "+ 2", CX - 60, 390, 150, CHALK, 1);
        chalkText(g, "= 8,302,449", CX - 60, 570, 150, CHALK, 1); tick(g, 960, 720, SHOT === 7 ? 1 : seg(p, 0.15, 0.45));
      });
      if (SHOT === 6) {
        calc.visible = seg(p, 0.45, 0.55) > 0; calc.scale.setScalar(Math.max(0.01, K.pop(p, 0.45)));
        codeCard.visible = p > 0.62; codeCard.scale.setScalar(Math.max(0.01, K.pop(p, 0.62)));
        var a6 = bot.userData.arms[0]; a6.sh.rotation.x = -1.4 * seg(p, 0.05, 0.2) * (1 - seg(p, 0.3, 0.45));
        K.cam(lerpV(V(0.6, 5.2, 11.6), camBoard.pos, sm(p)), camBoard.look);
        K.tag(0, V(-2.0, 2.9, 1.4), "calculator", CSS.mint, seg(p, 0.5, 0.6));
        K.tag(1, V(0.4, 3.3, 1.6), "code tool", CSS.cyan, seg(p, 0.66, 0.76));
      } else {
        calc.visible = codeCard.visible = true;
        K.robotIdle(bot, t, seg(p, 0.1, 0.3));
        K.cam(lerpV(camBoard.pos, V(0.6, 5.2, 11.6), sm(p)), camBoard.look);
      }
    } else {
      board(function () {}); K.cam(camBoard.pos, camBoard.look);
    }
    return out;
  });
})();
