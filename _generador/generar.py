# -*- coding: utf-8 -*-
"""
Generador v2 — La Gran Parrillada Boyacense
Datos (CONFIG, CARTA, precios, FAQ, schema SEO) en datos.py · Diseño en este archivo.
Uso:  python generar.py   → crea index.html, privacidad.html, 404.html, sitemap.xml
"""
import os, sys
from html import escape as e
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from datos import (CONFIG, CARTA, ACOMPANAMIENTOS, BEBIDAS, PARRILLADA_INCLUYE, FAQ, ICONOS,
                   schema, sitemap, cop, wa, WA_GENERAL, WA_PARRILLADA, TEL, D, dir_txt)

# ---------- contenido editable del diseño ----------
HERO_PLATOS = [  # (imagen, nombre, precio) — rotan en la portada
    ("picada-carne-de-cerdo", "Picada de cerdo con rellena", 45000),
    ("trucha-boyacense", "Trucha boyacense en salsa de mazorca", 39000),
    ("cuchuco-de-trigo", "Cuchuco de trigo con espinazo", 12000),
    ("tabla-churrasco-lomo", "Tabla churrasco y lomo", 38000),
    ("picada-carne-mixta", "Picada mixta 450 g", 45000),
]
# Historias (tipo Instagram). "video": ruta a un .mp4 vertical (ej. "video/sopas.mp4") — vacío = usa la foto
STORIES = [
    ("sopas", "Sopas típicas", "3 sopas", "cuchuco-de-trigo", "s2", ""),
    ("parrillada-carta", "La Parrillada", "Plato insignia", "picada-carne-mixta", "s1", ""),
    ("barra-de-tota", "Barra de Tota", "8 platos", "trucha-boyacense", "s3", ""),
    ("carnes", "Carnes", "6 cortes", "tabla-churrasco-lomo", "s4", ""),
    ("picadas", "Picadas", "450 g", "picada-carne-de-res", "s5", ""),
]
GALERIA = [  # (imagen, clase fondo, es_foto)
    ("parrillada-boyacense-640", "t2", True), ("cuchuco-de-trigo-360", "t4", False), ("trucha-marinera-360", "t3", False),
    ("picada-carne-mixta-360", "t1", False), ("carta-de-boyaca-600", "t4", True), ("mondongo-360", "t2", False),
    ("churrasco-360", "t1", False), ("mojarra-frita-360", "t3", False), ("preparada-especial-360", "t2", False),
    ("pechuga-asada-360", "t4", False), ("picada-carne-de-cerdo-360", "t3", False), ("viudo-de-capaz-360", "t1", False),
    ("mute-de-mazorca-360", "t2", False), ("trucha-al-ajillo-360", "t4", False), ("tabla-lomo-pechuga-360", "t3", False),
    ("cachama-frita-360", "t1", False),
]
DIAS_ABIERTO = [6, 0]   # 0=domingo … 6=sábado
DICIEMBRE_TODOS = True

NAV = [("#parrillada", "Parrillada"), ("#carta", "Carta"), ("#galeria", "Galería"), ("#visitanos", "Visítanos")]

def ico(i): return f'<svg aria-hidden="true"><use href="#{i}"/></svg>'

def head(titulo, desc, url, extra="", base=""):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0e0a08">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="{base}fonts/bigshoulders-900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}css/estilos.css">
<script>document.documentElement.classList.add('js')</script>
{extra}"""

def top(base=""):
    nav = "".join(f'<a href="{base}{h}">{t}</a>' for h, t in NAV)
    return f"""<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="top" id="top">
  <div class="wrap">
    <a class="logo" href="{base or './'}">La Gran Parrillada<b>Boyacense</b></a>
    <nav class="top__nav" aria-label="Principal">{nav}</nav>
    <div class="top__der">
      <span class="estado" data-estado><i></i><span>Sáb y dom</span></span>
      <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span></button>
    </div>
  </div>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <ul class="menu__links">{''.join(f'<li><a href="{base}{h}"><span>{t}</span></a></li>' for h, t in NAV + [('#preguntas', 'Preguntas')])}</ul>
  <div class="menu__pie"><a href="{WA_GENERAL}" target="_blank" rel="noopener">WhatsApp ↗</a><a href="{TEL}">{CONFIG['telefono']}</a><a href="{CONFIG['maps_link']}" target="_blank" rel="noopener">Cómo llegar ↗</a></div>
</div>"""

def app(base=""):
    return f"""<nav class="app" aria-label="Accesos rápidos">
  <a href="{base}#inicio" class="activo">{ico('i-fuego')}Inicio</a>
  <a href="{base}#carta">{ico('i-carta')}Carta</a>
  <a class="app__wa" href="{WA_GENERAL}" target="_blank" rel="noopener" aria-label="Pedir por WhatsApp" data-evento="wa_app">{ico('i-wa')}</a>
  <a href="{CONFIG['maps_link']}" target="_blank" rel="noopener">{ico('i-pin')}Llegar</a>
  <a href="{TEL}">{ico('i-tel')}Llamar</a>
</nav>"""

def pie(base=""):
    redes = [(k, u) for k, u in CONFIG["redes"].items() if u]
    redes_html = f'<div><p class="pie__t">Redes</p><ul>{"".join(f"<li><a href=\"{e(u)}\" target=\"_blank\" rel=\"noopener\">{k.capitalize() if k != 'tiktok' else 'TikTok'} ↗</a></li>" for k, u in redes)}</ul></div>' if redes else ""
    return f"""<footer class="pie">
  <div class="wrap">
    <div class="pie__grid">
      <div><a class="logo" href="{base or './'}">La Gran Parrillada<b>Boyacense</b></a>
        <p style="margin-top:14px;max-width:36ch">Comida típica boyacense en {CONFIG['ciudad']}, {CONFIG['departamento']}, desde {CONFIG['fundado']}.</p></div>
      <div><p class="pie__t">Visítanos</p><ul><li>{e(dir_txt)}</li><li><a href="{TEL}">{CONFIG['telefono']}</a></li><li><a href="{CONFIG['maps_link']}" target="_blank" rel="noopener">Cómo llegar ↗</a></li></ul></div>
      <div><p class="pie__t">Explora</p><ul>{''.join(f'<li><a href="{base}{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
      {redes_html}
    </div>
    <div class="pie__marca" aria-hidden="true" data-fit>Parrillada</div>
    <div class="pie__legal"><span>© <span id="anio">2026</span> {CONFIG['nombre']}</span><a href="{base}privacidad.html">Aviso de privacidad</a></div>
  </div>
</footer>
<div class="cursor" aria-hidden="true"><span></span></div>"""

def scripts(base=""):
    return f"""<script src="{base}js/vendor/gsap.min.js" defer></script>
<script src="{base}js/vendor/ScrollTrigger.min.js" defer></script>
<script src="{base}js/vendor/lenis.min.js" defer></script>
<script src="{base}js/main.js" defer></script>"""

def src(slug, w=360): return f"img/{slug}-{w}.webp"
def srcset(slug): return f"img/{slug}-360.webp 360w, img/{slug}-720.webp 720w"

# ============================== INDEX ==============================
def index():
    titulo = "La Gran Parrillada Boyacense | Restaurante de comida típica en Sogamoso, Boyacá"
    desc = "Restaurante de comida típica boyacense en Sogamoso desde 2015. Parrillada boyacense, cuchuco, mondongo, trucha y carnes asadas. ¡Pide por WhatsApp!"
    seo = f"""<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="CO-BOY"><meta name="geo.placename" content="Sogamoso">
<meta property="og:type" content="restaurant.restaurant"><meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="{CONFIG['nombre']}">
<meta property="og:title" content="La Gran Parrillada Boyacense – Comida típica en Sogamoso">
<meta property="og:description" content="Auténtica parrillada boyacense, sopas típicas, truchas y carnes asadas. Desde 2015 en Sogamoso.">
<meta property="og:url" content="{D}/"><meta property="og:image" content="{D}/img/og-lgpb.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{D}/img/og-lgpb.jpg">
<link rel="preload" as="image" href="{src(HERO_PLATOS[0][0], 720)}" fetchpriority="high">
<script type="application/ld+json">
{schema()}
</script>"""

    # HERO
    platos = ""
    for i, (s, n, p) in enumerate(HERO_PLATOS):
        att = 'fetchpriority="high"' if i == 0 else 'decoding="async"'
        fuente = f'src="{src(s, 720)}"' if i == 0 else f'data-src="{src(s, 720)}"'
        platos += f'<div class="hero__plato" data-nombre="{e(n)}" data-precio="{cop(p)}"><img {fuente} alt="{e(n)} – La Gran Parrillada Boyacense" width="565" height="557" {att}></div>'
    cinta = "".join(f"<span>{x}</span>" for x in ["Parrillada boyacense", "Cuchuco", "Mondongo", "Mute", "Longaniza", "Rellena", "Arepa boyacense", "Trucha", "Envuelto", "Picadas"])

    # MANIFIESTO
    def pill(s): return f'<span class="pill"><img src="{src(s)}" alt="" loading="lazy" width="80" height="40"></span>'
    manif = (f'Aquí la parrilla se prende cada fin de semana desde 2015. Cuchuco {pill("cuchuco-de-trigo")} longaniza, rellena '
             f'{pill("picada-carne-de-cerdo")} y arepa boyacense, <span class="it">como se come en Boyacá,</span> sumercé.')
    import re
    # envolver palabras para el efecto de encendido (sin romper etiquetas)
    partes = re.split(r'(<[^>]+>)', manif); out = []; dentro_tag = 0
    for pz in partes:
        if pz.startswith('<'): out.append(pz); continue
        out.append(re.sub(r'(\S+)', r'<span class="pal">\1</span>', pz))
    manif = "".join(out)

    # PARRILLADA
    pp = CONFIG["precios_parrillada"]
    tam = "".join(f'<li><b>{t}</b><span>{cop(pp[t]) if pp[t] else ("Personal" if t == "Junior" else "Para compartir")}</span></li>' for t in ["Junior", "Mediana", "Grande"])

    # STORIES
    st = ""
    for ancla, t, sub, img, cls, vid in STORIES:
        fondo = f'<video src="{vid}" muted loop playsinline preload="none" aria-hidden="true"></video>' if vid else f'<img src="{src(img, 720)}" alt="" loading="lazy" width="565" height="557">'
        st += f'<a class="story {cls} revela" href="#{ancla}" data-cursor="Ver"><div class="story__bg">{fondo}</div><div class="story__barra"><i></i></div><small>{e(sub)}</small><h3>{e(t)}</h3><span>Ver en la carta</span></a>'

    # CARTA
    chips = [("sopas", "Sopas"), ("parrillada-carta", "Parrillada"), ("barra-de-tota", "Barra de Tota"), ("carnes", "Carnes"), ("picadas", "Picadas"), ("acompanamientos", "Acompañamientos"), ("bebidas", "Bebidas")]
    chips_html = "".join(f'<a href="#{i}">{t}</a>' for i, t in chips)
    def fila(n, d, p, s):
        return (f'<a class="fila revela" href="{wa(f"¡Hola! Quiero pedir: {n} 🔥")}" target="_blank" rel="noopener" data-img="{src(s, 720)}" data-cursor="Pedir">'
                f'<div class="fila__img"><img src="{src(s)}" alt="{e(n)} – comida típica en Sogamoso" loading="lazy" decoding="async" width="360" height="190"></div>'
                f'<div><h4>{e(n)}</h4><p>{e(d)}</p></div>'
                f'<div class="fila__der"><span class="precio">{cop(p)}</span><span class="pedir">{ico("i-wa")}Pedir</span></div></a>')
    def cat(id_, t, sub, filas):
        return f'<section class="cat" id="{id_}" aria-labelledby="h-{id_}"><div class="cat__nombre"><h3 id="h-{id_}" data-x>{e(t)}</h3><span>{e(sub)}</span></div>{filas}</section>'
    cartas = ""
    for g in CARTA:
        cartas += cat(g["id"], g["titulo"], g["sub"], "".join(fila(*p) for p in g["platos"]))
        if g["id"] == "sopas":
            parr = (f'<a class="fila revela" href="{WA_PARRILLADA}" target="_blank" rel="noopener" data-img="img/parrillada-boyacense-640.webp" data-cursor="Pedir">'
                    f'<div class="fila__img"><img src="img/parrillada-boyacense-640.webp" alt="Auténtica Parrillada Boyacense" loading="lazy" width="640" height="317" style="object-fit:cover;width:100%;height:100%"></div>'
                    f'<div><h4>Auténtica Parrillada Boyacense</h4><p>Junior, Mediana o Grande. {e(", ".join(PARRILLADA_INCLUYE).capitalize())}.</p></div>'
                    f'<div class="fila__der"><span class="precio">{("Desde " + cop(min(int(v) for v in pp.values() if v))) if any(pp.values()) else "Consultar"}</span><span class="pedir">{ico("i-wa")}Pedir</span></div></a>')
            cartas += cat("parrillada-carta", "La Parrillada", "plato insignia", parr)
    acomp = "".join(f"<li><span>{e(n)}</span><b>{cop(p)}</b></li>" for n, p in ACOMPANAMIENTOS)
    beb = "".join(f"<li><span>{e(n)}</span><b>{cop(p)}</b></li>" for n, p in BEBIDAS)

    # GALERÍA
    def fig(s, cls, foto, lazy=True):
        alt = s.rsplit('-', 1)[0].replace('-', ' ').capitalize() + " – La Gran Parrillada Boyacense"
        return f'<figure class="{cls}{" foto" if foto else ""}"><img src="img/{s}.webp" alt="{e(alt)}" loading="lazy" decoding="async" width="360" height="360"></figure>'
    mitad = len(GALERIA) // 2
    fila1 = "".join(fig(*g) for g in GALERIA[:mitad]); fila2 = "".join(fig(*g) for g in GALERIA[mitad:])
    filas_movil = f'<div class="gal__filas" aria-hidden="false"><div class="gal__fila">{fila1}{fila1.replace("<img", "<img aria-hidden=\"true\"")}</div><div class="gal__fila">{fila2}{fila2.replace("<img", "<img aria-hidden=\"true\"")}</div></div>'
    cols = ["", "", "", ""]
    for i, g in enumerate(GALERIA): cols[i % 4] += fig(*g)
    cols_pc = '<div class="gal__cols" aria-hidden="true">' + "".join(f'<div class="gal__col" data-vel="{v}">{c}</div>' for c, v in zip(cols, [-12, 18, -20, 14])) + '</div>'

    # HORARIO
    hor = ""
    for dia, nom, a, c in CONFIG["horario"]:
        from datos import DIA_NUM
        n = DIA_NUM[dia]
        if a is None: hor += f'<li data-dia="{n}"><span>{nom}</span><span>Cerrado</span></li>'
        else: hor += f'<li class="abre" data-dia="{n}"><span>{nom}</span><b>{(a + " – " + c) if a and c else "Abierto"}</b></li>'

    faq = "".join(f'<details class="revela"><summary>{e(q)}<i></i></summary><p>{e(r)}</p></details>' for q, r in FAQ)

    return f"""<!doctype html>
<html lang="es-CO">
<head>
{head(titulo, desc, D + "/", seo)}
</head>
<body>
{ICONOS}
<div class="loader" aria-hidden="true"><div class="loader__num"><span data-loader>0</span><small>%</small></div><div class="loader__txt"><svg class="loader__llama"><use href="#i-fuego"/></svg><span class="eti" style="justify-content:center">Prendiendo la parrilla</span></div></div>
<div class="grano" aria-hidden="true"></div>
{top()}

<main id="contenido">

<!-- ============ HERO ============ -->
<section class="hero" id="inicio" aria-labelledby="h1">
  <div class="hero__fondo" aria-hidden="true"></div>
  <!-- VIDEO OPCIONAL: descomenta y pon tu video vertical/horizontal en /video/hero.mp4
  <video class="hero__video" autoplay muted loop playsinline poster="img/og-lgpb.jpg"><source src="video/hero.mp4" type="video/mp4"></video> -->
  <div class="wrap hero__meta"><span>Sogamoso · Boyacá<br><b>Desde 2015</b></span><span style="text-align:right">Abrimos<br><b>sábados y domingos</b></span></div>
  <div class="hero__escena" aria-hidden="false"><div class="hero__aro" aria-hidden="true"></div>{platos}</div>
  <div class="wrap">
    <h1 class="hero__titulo mega" id="h1">
      <span class="linea l1"><span>La Gran</span></span>
      <span class="linea l2"><span data-fit>Parrillada</span></span>
      <span class="linea l3"><span><span class="it">Boyacense</span> — comida típica en Sogamoso</span></span>
    </h1>
    <div class="hero__abajo">
      <div class="hero__info"><div class="hero__plato-nombre" aria-live="polite"><small data-hero-num>01 / 0{len(HERO_PLATOS)}</small><strong data-hero-nombre>{e(HERO_PLATOS[0][1])}</strong><em data-hero-precio>{cop(HERO_PLATOS[0][2])}</em></div></div>
      <div class="hero__ctas">
        <a class="btn btn--wa magnet" href="{WA_GENERAL}" target="_blank" rel="noopener" data-evento="wa_hero">{ico('i-wa')}Pedir ya</a>
        <a class="btn btn--linea magnet" href="#carta">Ver carta</a>
      </div>
    </div>
  </div>
  <div class="cinta" aria-hidden="true"><div class="cinta__pista">{cinta}{cinta}</div></div>
</section>

<!-- ============ MANIFIESTO ============ -->
<section class="manifiesto" aria-label="Quiénes somos">
  <div class="wrap"><span class="eti">La casa</span><p data-manifiesto>{manif}</p></div>
</section>

<!-- ============ PARRILLADA ============ -->
<section class="parri" id="parrillada" aria-labelledby="h-parri">
  <div class="wrap parri__grid">
    <div class="parri__titulo"><span class="eti">Plato insignia</span><h2 class="mega" id="h-parri" style="margin-top:18px"><span class="linea"><span>La auténtica</span></span><span class="linea"><span><span class="it">parrillada</span></span></span></h2></div>
    <figure class="parri__foto" style="margin:0" data-clip>
      <img src="img/parrillada-boyacense-1200.webp" srcset="img/parrillada-boyacense-640.webp 640w, img/parrillada-boyacense-1200.webp 1200w" sizes="(min-width:1024px) 55vw, 92vw" alt="Auténtica Parrillada Boyacense con longaniza, rellena, arepa, envuelto y papa criolla" width="1200" height="595" loading="lazy" decoding="async" data-parallax>
      <div class="parri__sello" aria-hidden="true"><svg viewBox="0 0 100 100"><defs><path id="circ" d="M50 50 m-38 0 a38 38 0 1 1 76 0 a38 38 0 1 1 -76 0"/></defs><text font-size="9.5" font-weight="800" letter-spacing="3" fill="#0e0a08"><textPath href="#circ">ANTÓJATE DE UNA PARRILLADA · ANTÓJATE ·</textPath></text></svg><span>Desde<b>2015</b></span></div>
    </figure>
    <div class="parri__txt">
      <p class="revela">Cortes de res y cerdo, longaniza amarilla y roja, chorizo artesanal y rellena, con todo lo que la acompaña en Boyacá. Para uno, para dos o para toda la familia.</p>
      <ul class="ingr">{''.join(f'<li>{x}</li>' for x in PARRILLADA_INCLUYE)}</ul>
      <ul class="tam revela">{tam}</ul>
      <a class="btn btn--brasa magnet" href="{WA_PARRILLADA}" target="_blank" rel="noopener" data-evento="wa_parrillada">{ico('i-wa')}Quiero mi parrillada</a>
    </div>
  </div>
</section>

<!-- ============ HISTORIAS ============ -->
<section class="stories" aria-labelledby="h-stories">
  <div class="wrap">
    <div class="stories__cab"><h2 class="mega" id="h-stories"><span class="linea"><span>¿Qué se le</span></span><span class="linea"><span><span class="it">antoja?</span></span></span></h2></div>
    <div class="stories__pista">{st}</div>
  </div>
</section>

<!-- ============ CARTA ============ -->
<section class="carta" id="carta" aria-labelledby="h-carta">
  <div class="wrap">
    <div class="carta__cab"><span class="eti">La carta de Boyacá</span><h2 class="mega" id="h-carta"><span class="linea"><span>La <span class="it">carta</span></span></span></h2><p>Toque cualquier plato y le llega el pedido listo a WhatsApp.</p></div>
    <nav class="chips" aria-label="Secciones de la carta">{chips_html}</nav>
    {cartas}
    <div class="listas">
      <section class="cat" id="acompanamientos" aria-labelledby="h-acomp"><div class="cat__nombre"><h3 id="h-acomp">Para acompañar</h3></div><ul class="lista">{acomp}</ul></section>
      <section class="cat" id="bebidas" aria-labelledby="h-beb"><div class="cat__nombre"><h3 id="h-beb">Bebidas</h3></div><ul class="lista">{beb}</ul></section>
    </div>
    <p class="nota">Precios en pesos colombianos. Pueden cambiar sin previo aviso.</p>
  </div>
  <div class="flota" aria-hidden="true"><img alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACw="></div>
</section>

<!-- ============ GALERÍA ============ -->
<section class="gal" id="galeria" aria-labelledby="h-gal">
  <div class="wrap gal__cab"><span class="eti">Se le hace agua la boca</span><h2 class="mega" id="h-gal"><span class="linea"><span>Así se ve</span></span><span class="linea"><span><span class="it">lo boyacense</span></span></span></h2></div>
  {filas_movil}
  <div class="wrap">{cols_pc}</div>
</section>

<!-- ============ CIFRAS ============ -->
<section class="cifras" aria-label="La Gran Parrillada en números">
  <div class="wrap"><ul>
    <li><b data-count="2015" data-desde="1990">2015</b><span>Desde</span></li>
    <li><b data-count="10" data-suf="+">10+</b><span>Años</span></li>
    <li><b data-count="40" data-suf="+">40+</b><span>Platos y bebidas</span></li>
  </ul></div>
</section>

<!-- ============ VISITA ============ -->
<section class="visita" id="visitanos" aria-labelledby="h-visita">
  <div class="wrap">
    <span class="eti">Lo esperamos</span>
    <h2 class="mega" id="h-visita"><span class="linea"><span>Venga a</span></span><span class="linea"><span><span class="it">Sogamoso</span></span></span></h2>
    <div class="visita__grid">
      <div class="caja revela"><h3>Horario <span class="estado" data-estado><i></i><span>Sáb y dom</span></span></h3><ul class="horario">{hor}</ul><p class="aviso">En diciembre abrimos todos los días. Confirme por WhatsApp.</p></div>
      <div class="caja revela"><h3>Contacto</h3><ul class="datos">
        <li>{ico('i-pin')}<span>{e(dir_txt)}<br><a href="{CONFIG['maps_link']}" target="_blank" rel="noopener">Abrir en Google Maps ↗</a></span></li>
        <li>{ico('i-tel')}<a href="{TEL}">{CONFIG['telefono']}</a></li>
        <li>{ico('i-wa')}<a href="{WA_GENERAL}" target="_blank" rel="noopener">Pedidos y reservas</a></li></ul>
        <a class="btn btn--crema" style="width:100%;margin-top:14px" href="{CONFIG['maps_link']}" target="_blank" rel="noopener">{ico('i-pin')}Cómo llegar</a></div>
      <div class="mapa revela"><button class="mapa__btn" type="button" data-src="{e(CONFIG['maps_embed'])}"><span class="mapa__pin">{ico('i-pin')}</span>Ver mapa</button></div>
    </div>
  </div>
</section>

<!-- ============ FAQ ============ -->
<section class="faq" id="preguntas" aria-labelledby="h-faq">
  <div class="wrap faq__grid">
    <div><span class="eti">Dudas</span><h2 class="mega" id="h-faq"><span class="linea"><span>Preguntas</span></span><span class="linea"><span><span class="it">frecuentes</span></span></span></h2></div>
    <div>{faq}</div>
  </div>
</section>

<!-- ============ FINAL ============ -->
<section class="final" aria-labelledby="h-final">
  <div class="wrap">
    <span class="eti" style="justify-content:center">Este fin de semana</span>
    <h2 class="mega" id="h-final" style="margin-top:18px"><span class="linea"><span>¿Nos vemos,</span></span><span class="linea"><span><span class="it">sumercé?</span></span></span></h2>
    <p>Reserve su mesa o pida para llevar en un par de toques.</p>
    <div class="final__ctas">
      <a class="btn btn--wa magnet" href="{WA_GENERAL}" target="_blank" rel="noopener" data-evento="wa_final">{ico('i-wa')}Pedir por WhatsApp</a>
      <a class="btn btn--linea magnet" href="{TEL}">{ico('i-tel')}Llamar</a>
    </div>
  </div>
</section>

</main>
{pie()}
{app()}
<script>window.LGPB={{dias:{DIAS_ABIERTO},diciembre:{str(DICIEMBRE_TODOS).lower()}}}</script>
{scripts()}
</body>
</html>
"""

def privacidad():
    return f"""<!doctype html>
<html lang="es-CO">
<head>
{head("Aviso de privacidad | La Gran Parrillada Boyacense", "Aviso de privacidad del sitio web de La Gran Parrillada Boyacense, Sogamoso.", D + "/privacidad.html")}
</head>
<body>
{ICONOS}
{top('./')}
<main id="contenido" class="simple"><div class="wrap">
  <span class="eti" style="color:var(--rojo)">Legal</span>
  <h1 class="mega">Aviso de privacidad</h1>
  <p><b>Responsable:</b> {CONFIG['nombre']}, {e(dir_txt)}. Contacto: {CONFIG['telefono']}.</p>
  <h2>Qué datos recogemos</h2><p>Este sitio no tiene formularios ni registro. Si nos escribe por WhatsApp o nos llama, recibimos solo lo que usted comparta (nombre, teléfono, dirección de entrega y su pedido).</p>
  <h2>Para qué</h2><p>Para atender su pedido o reserva y responder sus preguntas. Si lo autoriza, para avisarle de promociones. No vendemos ni cedemos sus datos.</p>
  <h2>Sus derechos</h2><p>Según la Ley 1581 de 2012 y el Decreto 1377 de 2013, puede conocer, actualizar, rectificar o pedir que borremos sus datos escribiendo al {CONFIG['telefono']}.</p>
  <h2>Servicios de terceros</h2><p>Solo si toca “Ver mapa” se carga Google Maps. Los botones de WhatsApp abren la aplicación de Meta.</p>
  <p style="margin-top:30px"><a class="btn btn--brasa" href="./">← Volver al inicio</a></p>
</div></main>
{pie('./')}
{app('./')}
<script>window.LGPB={{dias:{DIAS_ABIERTO},diciembre:{str(DICIEMBRE_TODOS).lower()}}}</script>
{scripts()}
</body></html>"""

def p404():
    return f"""<!doctype html>
<html lang="es-CO">
<head>
{head("Página no encontrada | La Gran Parrillada Boyacense", "Esta página no existe.", D + "/404.html", '<meta name="robots" content="noindex">', base="/")}
</head>
<body>
{ICONOS}
<main id="contenido" class="simple" style="text-align:center;background:var(--noche);color:var(--crema)"><div class="wrap">
  <h1 class="mega" style="font-size:clamp(6rem,40vw,20rem);color:var(--brasa)">404</h1>
  <p style="color:#bfae98;font-size:1.2rem">Esta página se nos quemó en la parrilla.</p>
  <p style="margin-top:26px"><a class="btn btn--crema" href="/">Volver al inicio</a></p>
</div></main>
</body></html>"""

if __name__ == "__main__":
    for nombre, f in [("index.html", index), ("privacidad.html", privacidad), ("404.html", p404), ("sitemap.xml", sitemap)]:
        with open(os.path.join(RAIZ, nombre), "w", encoding="utf-8") as fh: fh.write(f())
        print("✔", nombre)
