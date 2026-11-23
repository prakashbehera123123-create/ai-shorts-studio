/* AI Shorts Studio world kit (2026-11-22). Original procedural low-poly building blocks: renderer, lights, text textures,
   a seated/standing person with a visible face, a friendly robot helper, DOM label pills. No third-party models or logos.
   Deterministic: seeded RNG; every frame is drawn from one GSAP timeline value st.t (seconds). */
var KIT = (function () {
  var CFG = window.WORLD;
  var W = 1080, H = 1920;
  window.__timelines = window.__timelines || {};

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rng = mulberry32(7);
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
  function sm(x) { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); }
  function seg(p, a, b) { return sm((p - a) / (b - a)); }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function V(x, y, z) { return new THREE.Vector3(x, y, z); }
  function lerpV(a, b, k) { return a.clone().lerp(b, k); }
  function pop(p, a) { var k = clamp((p - a) / 0.08, 0, 1); return k <= 0 ? 0 : 1 + 0.18 * Math.sin(k * Math.PI) ; }

  var C = { navy: 0x0b1020, cyan: 0x4cc9f0, amber: 0xffb703, mint: 0x3ddc97, coral: 0xff5d73, violet: 0x9b7bff, ink: 0xffffff, muted: 0xaab4cf };
  var CSS = { cyan: "#4CC9F0", amber: "#FFB703", mint: "#3DDC97", coral: "#FF5D73", violet: "#9B7BFF", navy: "#0B1020", navy2: "#121A33", ink: "#FFFFFF", muted: "#AAB4CF" };
  var FONT = "'Segoe UI', sans-serif";

  var renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("w-canvas"), antialias: true });
  renderer.setSize(W, H, false);
  renderer.setPixelRatio(1);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(48, W / H, 0.1, 400);

  function lights(bg, fogNear, fogFar) {
    scene.background = new THREE.Color(bg);
    scene.fog = new THREE.Fog(bg, fogNear, fogFar);
    scene.add(new THREE.HemisphereLight(0x9fc0ff, 0x1a1430, 0.5));
    var key = new THREE.DirectionalLight(0xffe2b8, 1.2); key.position.set(8, 14, 10); scene.add(key);
    var rim = new THREE.DirectionalLight(0x4cc9f0, 0.8); rim.position.set(-10, 6, -12); scene.add(rim);
  }

  function std(color, o) {
    o = o || {};
    return new THREE.MeshStandardMaterial({ color: color, roughness: o.r === undefined ? 0.7 : o.r, metalness: o.m || 0,
      flatShading: o.flat === undefined ? true : o.flat, emissive: o.e || 0x000000, emissiveIntensity: o.ei === undefined ? 1 : o.ei,
      transparent: !!o.op, opacity: o.op || 1 });
  }
  function glow(color, op) { return new THREE.MeshBasicMaterial({ color: color, transparent: op !== undefined, opacity: op === undefined ? 1 : op }); }
  function add(m, x, y, z, parent) { m.position.set(x, y, z); (parent || scene).add(m); return m; }
  function box(w, h, d, mat, x, y, z, parent) { return add(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat), x, y, z, parent); }
  function cyl(rt, rb, h, seg, mat, x, y, z, parent) { return add(new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg || 12), mat), x, y, z, parent); }
  function sphere(r, mat, x, y, z, parent, d) { return add(new THREE.Mesh(new THREE.IcosahedronGeometry(r, d === undefined ? 1 : d), mat), x, y, z, parent); }

  function textCanvas(w, h, draw) {
    var cv = document.createElement("canvas"); cv.width = w; cv.height = h;
    var g = cv.getContext("2d"); if (draw) draw(g, w, h);
    var tx = new THREE.CanvasTexture(cv); tx.anisotropy = 4; tx.encoding = THREE.sRGBEncoding;
    return { canvas: cv, ctx: g, tex: tx };
  }
  function roundRect(g, x, y, w, h, r) {
    g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
  }
  function signTex(text, color, w, h, size, bg, sub) {
    return textCanvas(w, h, function (g) {
      g.fillStyle = bg || "rgba(11,16,32,0.94)"; roundRect(g, 6, 6, w - 12, h - 12, Math.min(40, h / 5)); g.fill();
      g.strokeStyle = color; g.lineWidth = 10; g.stroke();
      g.fillStyle = color; g.font = "900 " + size + "px " + FONT; g.textAlign = "center"; g.textBaseline = "middle";
      g.fillText(text, w / 2, sub ? h * 0.4 : h / 2 + 4);
      if (sub) { g.fillStyle = CSS.muted; g.font = "700 " + Math.round(size * 0.5) + "px " + FONT; g.fillText(sub, w / 2, h * 0.74); }
    });
  }
  function sign(text, color, w, h, size, bg, sub) {
    return new THREE.MeshBasicMaterial({ map: signTex(text, color, w, h, size, bg, sub).tex, transparent: true });
  }
  function plane(w, h, mat, x, y, z, ry, parent) {
    var m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat); m.rotation.y = ry || 0; return add(m, x, y, z, parent);
  }
  function billboard(m) { m.quaternion.copy(camera.quaternion); }

  // ---------- person (faces +z by default) ----------
  function makePerson(o) {
    o = o || {};
    var g = new THREE.Group();
    var skin = std(o.skin || 0xc98f6a), shirt = std(o.shirt || 0x2b4a8a), pants = std(0x1f2638), hair = std(o.hair || 0x1b1410);
    var seated = o.seated !== false;
    var hip = seated ? 1.05 : 1.75;
    if (seated) {
      box(0.95, 0.22, 0.9, pants, 0, hip, 0.1, g);                                 // thighs
      [-0.25, 0.25].forEach(function (x) { box(0.3, 1.0, 0.3, pants, x, 0.5, 0.5, g); box(0.34, 0.14, 0.5, std(0x111111), x, 0.07, 0.6, g); });
    } else {
      [-0.25, 0.25].forEach(function (x) { box(0.32, 1.7, 0.32, pants, x, 0.85, 0, g); box(0.36, 0.14, 0.5, std(0x111111), x, 0.07, 0.08, g); });
    }
    var torso = box(1.0, 1.1, 0.55, shirt, 0, hip + 0.65, 0, g);
    box(0.3, 0.2, 0.3, skin, 0, hip + 1.28, 0, g);                                  // neck
    var headG = new THREE.Group(); headG.position.set(0, hip + 1.65, 0); g.add(headG);
    sphere(0.36, skin, 0, 0, 0, headG);
    var hc = sphere(0.38, hair, 0, 0.1, -0.06, headG); hc.scale.set(1, 0.8, 0.95);
    if (o.long) { var hb = box(0.7, 0.7, 0.2, hair, 0, -0.2, -0.25, headG); }
    var eyeM = glow(0x161616);
    sphere(0.05, eyeM, -0.13, 0.02, 0.33, headG, 0); sphere(0.05, eyeM, 0.13, 0.02, 0.33, headG, 0);
    var smile = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.022, 6, 12, Math.PI), glow(0x5a2a22));
    smile.rotation.z = Math.PI; smile.position.set(0, -0.12, 0.33); headG.add(smile);
    box(0.08, 0.1, 0.08, skin, 0, -0.03, 0.37, headG);                              // nose
    var arms = [];
    [-1, 1].forEach(function (s) {
      var sh = new THREE.Group(); sh.position.set(s * 0.6, hip + 1.1, 0); g.add(sh);
      box(0.24, 0.8, 0.26, shirt, 0, -0.38, 0, sh);
      var el = new THREE.Group(); el.position.set(0, -0.78, 0); sh.add(el);
      box(0.22, 0.7, 0.24, shirt, 0, -0.33, 0, el);
      box(0.22, 0.22, 0.22, skin, 0, -0.75, 0, el);
      arms.push({ sh: sh, el: el, s: s });
    });
    if (o.badge) box(0.22, 0.14, 0.02, glow(C.cyan), 0.25, hip + 0.95, 0.29, g);
    g.userData = { head: headG, arms: arms, torso: torso, hip: hip };
    if (o.parent) o.parent.add(g); else scene.add(g);
    return g;
  }
  // pose helpers: typing (arms forward), wave (right arm up), nod
  function poseTyping(p, t, amt) {
    p.userData.arms.forEach(function (a, i) {
      a.sh.rotation.x = -1.05 * amt; a.sh.rotation.z = 0;
      a.el.rotation.x = -0.35 * amt + 0.06 * amt * Math.sin(t * 18 + i * 2.1);
    });
  }
  function poseWave(p, t, k) {
    var a = p.userData.arms[1];
    a.sh.rotation.z = lerp(0, 2.5, k) * a.s; a.sh.rotation.x = lerp(-1.05, 0, k);
    a.el.rotation.x = 0; a.el.rotation.z = k * 0.5 * Math.sin(t * 9) * a.s;
  }
  function poseRest(p) { p.userData.arms.forEach(function (a) { a.sh.rotation.set(-0.2, 0, 0.08 * a.s); a.el.rotation.set(-0.3, 0, 0); }); }

  // ---------- robot helper (faces +z) ----------
  function makeRobot(o) {
    o = o || {};
    var g = new THREE.Group();
    var body = std(0xe8edf7, { r: 0.35, m: 0.1 }), dark = std(0x1d2540, { r: 0.4 }), accent = std(o.accent || C.cyan, { e: o.accent || C.cyan, ei: 0.45 });
    cyl(0.28, 0.36, 0.25, 12, dark, 0, 0.12, 0, g);                                 // base wheel
    var torso = box(1.0, 0.95, 0.8, body, 0, 0.85, 0, g);
    var chest = plane(0.62, 0.44, glow(0x0f1830), 0, 0.92, 0.405, 0, g);
    var belt = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.07, 6, 24), accent); belt.rotation.x = Math.PI / 2; belt.position.set(0, 0.45, 0); g.add(belt);
    belt.visible = !!o.belt;
    var headG = new THREE.Group(); headG.position.set(0, 1.72, 0); g.add(headG);
    box(1.05, 0.78, 0.82, body, 0, 0, 0, headG);
    var visor = box(0.86, 0.5, 0.05, glow(0x0a1226), 0, 0, 0.42, headG);
    var eyeL = box(0.16, 0.2, 0.02, glow(C.cyan), -0.2, 0.02, 0.45, headG), eyeR = box(0.16, 0.2, 0.02, glow(C.cyan), 0.2, 0.02, 0.45, headG);
    cyl(0.03, 0.03, 0.35, 6, dark, 0, 0.55, 0, headG);
    var tip = sphere(0.08, glow(C.amber), 0, 0.75, 0, headG, 0);
    var brain = sphere(0.33, new THREE.MeshStandardMaterial({ color: 0xc8a8ff, emissive: C.violet, emissiveIntensity: 0.9, transparent: true, opacity: 0.92, roughness: 0.3, flatShading: true }), 0, 0.5, 0, headG, 1);
    brain.visible = !!o.brain;
    var arms = [];
    [-1, 1].forEach(function (s) {
      var sh = new THREE.Group(); sh.position.set(s * 0.62, 1.15, 0); g.add(sh);
      box(0.2, 0.62, 0.2, dark, 0, -0.3, 0, sh);
      var hand = sphere(0.14, accent, 0, -0.66, 0, sh, 0);
      arms.push({ sh: sh, s: s, hand: hand });
    });
    g.userData = { head: headG, brain: brain, belt: belt, eyes: [eyeL, eyeR], tip: tip, arms: arms, chest: chest };
    if (o.parent) o.parent.add(g); else scene.add(g);
    return g;
  }
  function robotIdle(r, t, wave) {
    var u = r.userData;
    u.head.rotation.y = 0.12 * Math.sin(t * 1.3);
    u.head.position.y = 1.72 + 0.03 * Math.sin(t * 3.1);
    var blink = (t % 3.1) < 0.12 ? 0.15 : 1;
    u.eyes.forEach(function (e) { e.scale.y = blink; });
    u.tip.material.color.setHex((Math.floor(t * 2) % 2) ? C.amber : 0xffe08a);
    u.arms.forEach(function (a) { a.sh.rotation.z = 0.15 * a.s; a.sh.rotation.x = 0.1 * Math.sin(t * 2 + a.s); });
    if (wave) { var a = u.arms[1]; a.sh.rotation.z = (2.4 + 0.35 * Math.sin(t * 10)) * a.s * wave + 0.15 * a.s * (1 - wave); }
  }

  // ---------- DOM overlay ----------
  var pill = document.getElementById("w-pill"); pill.textContent = CFG.pill;
  if (CFG.pill.length > 34) pill.style.fontSize = "44px"; else if (CFG.pill.length > 27) pill.style.fontSize = "50px";
  document.getElementById("w-src").textContent = CFG.src;
  if (!CFG.src) document.getElementById("w-src").style.display = "none";
  var tags = [0, 1, 2, 3].map(function (i) { return document.getElementById("w-tag" + i); });
  var counter = document.getElementById("w-counter");
  var flash = document.getElementById("w-flash");
  var used = {};
  function tag(i, world, text, color, show) {
    var el = tags[i]; used[i] = show;
    el.textContent = text; el.style.borderColor = color; el.style.color = color;
    var pp = world.clone().project(camera);
    var x = (pp.x * 0.5 + 0.5) * W, y = (-pp.y * 0.5 + 0.5) * H;
    var bw = el.offsetWidth, bh = el.offsetHeight;
    x = clamp(x - bw / 2, 40, W - bw - 40); y = clamp(y - bh / 2, 320, 1180);
    el.style.transform = "translate(" + x + "px," + y + "px) scale(" + (0.8 + 0.2 * show) + ")";
    el.style.opacity = show; el.style.visibility = show > 0.01 ? "visible" : "hidden";
  }

  var st = { t: 0 };
  var tl = gsap.timeline({ paused: true });
  tl.to(st, { t: CFG.dur, duration: CFG.dur, ease: "none" }, 0);
  window.__timelines["main"] = tl;

  function frame(draw) {
    function render() {
      var ph = CFG.phase || [0, 1];
      var t = st.t, p = ph[0] + clamp(t / CFG.dur, 0, 1) * (ph[1] - ph[0]);
      used = {};
      var o = draw(t, p) || {};
      tags.forEach(function (el, i) { if (!used[i]) { el.style.opacity = 0; el.style.visibility = "hidden"; } });
      var ctr = o.counter || "";
      counter.style.opacity = ctr ? 1 : 0; counter.style.visibility = ctr ? "visible" : "hidden"; counter.textContent = ctr;
      if (o.counterColor) counter.style.color = o.counterColor;
      flash.style.opacity = o.flash || 0;
      pill.style.opacity = seg(t, 0.05, 0.35);
      if (CFG.clean) ["w-pill", "w-tag0", "w-tag1", "w-tag2", "w-tag3", "w-src", "w-ill", "w-flash", "w-counter"].forEach(function (id) { document.getElementById(id).style.display = "none"; });
      renderer.render(scene, camera);
    }
    tl.eventCallback("onUpdate", render);
    render();
  }
  function cam(pos, look) { camera.position.copy(pos); camera.lookAt(look); }

  return { CFG: CFG, SHOT: CFG.shot, D: CFG.dur, rng: rng, clamp: clamp, sm: sm, seg: seg, lerp: lerp, V: V, lerpV: lerpV, pop: pop,
    C: C, CSS: CSS, FONT: FONT, THREE: THREE, scene: scene, camera: camera, lights: lights, std: std, glow: glow, add: add, box: box,
    cyl: cyl, sphere: sphere, textCanvas: textCanvas, roundRect: roundRect, signTex: signTex, sign: sign, plane: plane, billboard: billboard,
    makePerson: makePerson, poseTyping: poseTyping, poseWave: poseWave, poseRest: poseRest, makeRobot: makeRobot, robotIdle: robotIdle,
    tag: tag, frame: frame, cam: cam };
})();
