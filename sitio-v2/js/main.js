/* =====================================================================
   La Gran Parrillada Boyacense — interacciones y animaciones
   Si GSAP no carga, todo el contenido se ve normal (sin animación).
   ===================================================================== */
(function () {
  'use strict';
  var d = document, html = d.documentElement, w = window;
  var reduce = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var esPC = w.matchMedia('(min-width:1024px)').matches;
  var mouse = w.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* ---------- texto que llena el ancho ---------- */
  function ajustar() {
    $$('[data-fit]').forEach(function (el) {
      el.style.fontSize = ''; el.style.display = 'inline-block'; el.style.whiteSpace = 'nowrap';
      var p = el.parentElement, cs = getComputedStyle(p);
      var ancho = p.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      var fs = parseFloat(getComputedStyle(el).fontSize);
      el.style.fontSize = Math.floor(fs * ancho / el.scrollWidth * 0.99) + 'px';
    });
  }
  ajustar();
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(ajustar);
  var rt; w.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { ajustar(); if (w.ScrollTrigger) ScrollTrigger.refresh(); }, 150); });

  /* ---------- año ---------- */
  var anio = $('#anio'); if (anio) anio.textContent = new Date().getFullYear();

  /* ---------- estado abierto / horario ---------- */
  var cfg = w.LGPB || { dias: [6, 0], diciembre: true };
  var hoy = new Date(), dia = hoy.getDay(), abreHoy = cfg.dias.indexOf(dia) > -1 || (cfg.diciembre && hoy.getMonth() === 11);
  $$('[data-estado]').forEach(function (el) {
    el.classList.toggle('abierto', abreHoy);
    el.querySelector('span').textContent = abreHoy ? 'Hoy abrimos' : (dia === 5 ? 'Abre mañana' : 'Abre sábado');
  });
  var fh = $('.horario [data-dia="' + dia + '"]'); if (fh) fh.classList.add('hoy');

  /* ---------- menú ---------- */
  var burger = $('.burger'), menu = $('#menu');
  function menuToggle(abrir) {
    d.body.classList.toggle('menu-on', abrir);
    burger.setAttribute('aria-expanded', abrir); menu.setAttribute('aria-hidden', !abrir);
  }
  if (burger) {
    burger.addEventListener('click', function () { menuToggle(!d.body.classList.contains('menu-on')); });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { menuToggle(false); }); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') menuToggle(false); });
  }

  /* ---------- mapa bajo demanda ---------- */
  var mb = $('.mapa__btn');
  if (mb) mb.addEventListener('click', function () {
    var f = d.createElement('iframe'); f.src = mb.dataset.src; f.title = 'Mapa: La Gran Parrillada Boyacense, Sogamoso';
    f.loading = 'lazy'; f.allowFullscreen = true; mb.replaceWith(f);
  });

  /* ---------- header: se esconde al bajar, aparece al subir ---------- */
  var top = $('#top'), ultimo = 0;
  function onScroll(y) {
    if (!top) return;
    top.classList.toggle('solido', y > 40);
    top.classList.toggle('esconde', y > 300 && y > ultimo && !d.body.classList.contains('menu-on'));
    ultimo = y;
  }
  w.addEventListener('scroll', function () { onScroll(w.scrollY); }, { passive: true });

  /* ---------- sin GSAP o con movimiento reducido: fin ---------- */
  var loader = $('.loader');
  if (!w.gsap || !w.ScrollTrigger || reduce) $$('.hero__plato img[data-src]').forEach(function (im) { im.src = im.dataset.src; });
  if (!w.gsap || !w.ScrollTrigger || reduce) {
    if (loader) loader.classList.add('oculto');
    $$('.story').forEach(function (s) { s.classList.add('visto'); });
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  html.classList.add('anim');

  /* ---------- scroll suave (solo PC con mouse) ---------- */
  var lenis = null;
  if (mouse && esPC && w.Lenis) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', function (e) { ScrollTrigger.update(); onScroll(e.scroll); });
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href'); if (id.length < 2) return;
        var t = $(id); if (!t) return; e.preventDefault(); lenis.scrollTo(t, { offset: -20, duration: 1.4 });
      });
    });
  }

  /* platos del hero: se cargan después de la página (más rápido) */
  w.addEventListener('load', function () { $$('.hero__plato img[data-src]').forEach(function (im) { im.src = im.dataset.src; }); });

  /* ---------- LOADER (solo PC) + entrada del hero ---------- */
  if (!esPC && loader) { loader.classList.add('oculto'); loader = null; }
  var visto = false; try { visto = sessionStorage.getItem('lgpb') === '1'; sessionStorage.setItem('lgpb', '1'); } catch (e) {}
  var tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
  if (loader && !visto) {
    var num = $('[data-loader]'), o = { v: 0 };
    tl.to(o, { v: 100, duration: 1.1, ease: 'power2.inOut', onUpdate: function () { num.textContent = Math.round(o.v); } })
      .to(loader, { yPercent: -100, duration: 0.9, ease: 'expo.inOut' })
      .set(loader, { display: 'none' });
  } else if (loader) { loader.classList.add('oculto'); }

  tl.from('.hero__titulo .linea > span', { yPercent: 110, duration: 1.2, stagger: 0.09 }, visto ? 0 : '-=0.45')
    .from('.hero__escena', { scale: 0.4, rotate: -40, duration: 1.4 }, '<0.1')
    .from('.hero__meta, .hero__info, .hero__ctas .btn, .cinta', { y: 30, opacity: 0, duration: 1, stagger: 0.08 }, '<0.3');

  /* ---------- platos que rotan en el hero ---------- */
  var platos = $$('.hero__plato'), i = 0, total = platos.length;
  var nNombre = $('[data-hero-nombre]'), nPrecio = $('[data-hero-precio]'), nNum = $('[data-hero-num]');
  gsap.set(platos, { opacity: 0 }); gsap.set(platos[0], { opacity: 1 });
  function siguiente() {
    var a = platos[i]; i = (i + 1) % total; var b = platos[i];
    gsap.to(a, { opacity: 0, scale: 1.15, rotate: 30, duration: 0.8, ease: 'power3.in' });
    gsap.fromTo(b, { opacity: 0, scale: 0.55, rotate: -35 }, { opacity: 1, scale: 1, rotate: 0, duration: 1.2, ease: 'expo.out', delay: 0.45 });
    gsap.to([nNombre, nPrecio], { yPercent: -60, opacity: 0, duration: 0.35, stagger: 0.05, onComplete: function () {
      nNombre.textContent = b.dataset.nombre; nPrecio.textContent = b.dataset.precio;
      nNum.textContent = ('0' + (i + 1)).slice(-2) + ' / ' + ('0' + total).slice(-2);
      gsap.fromTo([nNombre, nPrecio], { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.6, stagger: 0.06, ease: 'expo.out' });
    } });
  }
  var rot = gsap.delayedCall(3.4, function rep() { siguiente(); rot.restart(true); });
  ScrollTrigger.create({ trigger: '.hero', start: 'top top', end: 'bottom top', onLeave: function () { rot.pause(); }, onEnterBack: function () { rot.resume(); } });

  /* hero al hacer scroll: el título sube, el plato crece */
  gsap.to('.hero__titulo', { yPercent: -25, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.to('.hero__escena', { scale: 1.25, yPercent: esPC ? -10 : -5, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

  /* ---------- títulos que suben desde una máscara ---------- */
  $$('h2 .linea > span').forEach(function (s) {
    gsap.from(s, { yPercent: 110, duration: 1.1, ease: 'expo.out', scrollTrigger: { trigger: s.closest('h2'), start: 'top 88%' } });
  });

  /* ---------- aparición suave ---------- */
  ScrollTrigger.batch('.revela', {
    start: 'top 90%',
    onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, duration: 0.9, stagger: 0.07, ease: 'expo.out', overwrite: true }); }
  });

  /* ---------- manifiesto: las palabras se "encienden" ---------- */
  var pals = $$('[data-manifiesto] .pal, [data-manifiesto] .pill');
  if (pals.length) {
    gsap.set(pals, { opacity: 0.12 });
    gsap.to(pals, { opacity: 1, stagger: 0.1, ease: 'none', scrollTrigger: { trigger: '[data-manifiesto]', start: 'top 80%', end: 'bottom 45%', scrub: 0.6 } });
  }

  /* ---------- parrillada: la foto se abre ---------- */
  var clip = $('[data-clip]');
  if (clip) {
    gsap.fromTo(clip, { clipPath: 'inset(18% 14% 18% 14% round 22px)' }, { clipPath: 'inset(0% 0% 0% 0% round 22px)', ease: 'none', scrollTrigger: { trigger: clip, start: 'top 95%', end: 'top 35%', scrub: true } });
    gsap.fromTo('[data-parallax]', { scale: 1.3 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: clip, start: 'top bottom', end: 'bottom top', scrub: true } });
  }
  gsap.from('.ingr li', { scale: 0, opacity: 0, duration: 0.6, stagger: 0.04, ease: 'back.out(2)', scrollTrigger: { trigger: '.ingr', start: 'top 88%' } });

  /* ---------- historias ---------- */
  $$('.story').forEach(function (s, k) {
    ScrollTrigger.create({ trigger: s, start: 'left 95%', horizontal: false, onEnter: function () { setTimeout(function () { s.classList.add('visto'); }, k * 250); } });
    var v = $('video', s);
    if (v) ScrollTrigger.create({ trigger: s, start: 'top bottom', end: 'bottom top', onToggle: function (st) { st.isActive ? v.play().catch(function () {}) : v.pause(); } });
  });

  /* ---------- carta: nombres gigantes se deslizan + chip activo ---------- */
  $$('.cat__nombre h3').forEach(function (h) {
    gsap.from(h, { xPercent: 18, ease: 'none', scrollTrigger: { trigger: h, start: 'top bottom', end: 'top 55%', scrub: true } });
  });
  var chips = $$('.chips a'), chipsBar = $('.chips');
  chips.forEach(function (c) {
    var sec = $(c.getAttribute('href')); if (!sec) return;
    ScrollTrigger.create({ trigger: sec, start: 'top 45%', end: 'bottom 45%', onToggle: function (st) {
      if (!st.isActive) return;
      chips.forEach(function (x) { x.classList.remove('on'); }); c.classList.add('on');
      chipsBar.scrollTo({ left: c.offsetLeft - 20, behavior: 'smooth' });
    } });
  });

  /* imagen que sigue al cursor sobre la carta (PC) */
  var flota = $('.flota');
  if (flota && mouse && esPC) {
    var fimg = $('img', flota);
    var fx = gsap.quickTo(flota, 'left', { duration: 0.6, ease: 'power3' }), fy = gsap.quickTo(flota, 'top', { duration: 0.6, ease: 'power3' });
    $$('.fila[data-img]').forEach(function (f) {
      f.addEventListener('mouseenter', function () { fimg.src = f.dataset.img; flota.classList.add('on'); });
      f.addEventListener('mouseleave', function () { flota.classList.remove('on'); });
    });
    w.addEventListener('mousemove', function (e) { fx(e.clientX + 160); fy(e.clientY); });
  }

  /* ---------- galería: columnas a distinta velocidad (PC) ---------- */
  $$('.gal__col').forEach(function (c) {
    gsap.to(c, { yPercent: parseFloat(c.dataset.vel), ease: 'none', scrollTrigger: { trigger: '.gal', start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- cifras que cuentan ---------- */
  $$('[data-count]').forEach(function (el) {
    var fin = +el.dataset.count, ini = +(el.dataset.desde || 0), suf = el.dataset.suf || '', o = { v: ini };
    el.textContent = ini + suf;
    ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: function () {
      gsap.to(o, { v: fin, duration: 1.8, ease: 'expo.out', onUpdate: function () { el.textContent = Math.round(o.v) + suf; } });
    } });
  });

  /* ---------- botones magnéticos + cursor (PC con mouse) ---------- */
  if (mouse && esPC) {
    $$('.magnet').forEach(function (b) {
      var bx = gsap.quickTo(b, 'x', { duration: 0.5, ease: 'power3' }), by = gsap.quickTo(b, 'y', { duration: 0.5, ease: 'power3' });
      b.addEventListener('mousemove', function (e) { var r = b.getBoundingClientRect(); bx((e.clientX - r.left - r.width / 2) * 0.3); by((e.clientY - r.top - r.height / 2) * 0.4); });
      b.addEventListener('mouseleave', function () { bx(0); by(0); });
    });
    var cur = $('.cursor'), cl = $('span', cur);
    var cx = gsap.quickTo(cur, 'left', { duration: 0.25, ease: 'power3' }), cy = gsap.quickTo(cur, 'top', { duration: 0.25, ease: 'power3' });
    w.addEventListener('mousemove', function (e) { cx(e.clientX); cy(e.clientY); });
    $$('[data-cursor]').forEach(function (el) {
      el.addEventListener('mouseenter', function () { cl.textContent = el.dataset.cursor; cur.classList.add('grande'); });
      el.addEventListener('mouseleave', function () { cur.classList.remove('grande'); });
    });
  }

  w.addEventListener('load', function () { ajustar(); ScrollTrigger.refresh(); });
})();
