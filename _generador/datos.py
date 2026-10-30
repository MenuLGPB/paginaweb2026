# -*- coding: utf-8 -*-
"""
DATOS del sitio: configuración, carta, precios, preguntas frecuentes y SEO (schema.org).
Edita aquí y luego ejecuta:  python generar.py
"""
import json, os, datetime
from html import escape as e
from urllib.parse import quote

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

# ======================= CONFIGURACIÓN (EDITAR AQUÍ) =======================
CONFIG = {
    "nombre": "La Gran Parrillada Boyacense",
    "dominio": "https://lagranparrilladaboyacense.com",
    "telefono": "+57 312 4411166",
    "whatsapp": "573124411166",
    "ciudad": "Sogamoso",
    "departamento": "Boyacá",
    "direccion": "",          # EDITAR: ej. "Calle 11 # 10-20, Barrio Centro"  (vacío = no se muestra)
    "codigo_postal": "",      # EDITAR: ej. "152210"
    "lat": "", "lng": "",     # EDITAR: coordenadas de Google Maps (vacío = no se usan)
    "maps_link": "https://www.google.com/maps/search/?api=1&query=" + quote("La Gran Parrillada Boyacense Sogamoso"),
    "maps_embed": "https://www.google.com/maps?q=" + quote("La Gran Parrillada Boyacense, Sogamoso, Boyacá") + "&output=embed",
    "fundado": "2015",
    # Horario: (día schema, nombre, abre, cierra). abre/cierra vacíos = "Abierto" sin hora.
    "horario": [
        ("Monday", "Lunes", None, None),
        ("Tuesday", "Martes", None, None),
        ("Wednesday", "Miércoles", None, None),
        ("Thursday", "Jueves", None, None),
        ("Friday", "Viernes", None, None),
        ("Saturday", "Sábado", "", ""),   # EDITAR: ej. "11:00", "18:00"
        ("Sunday", "Domingo", "", ""),    # EDITAR
    ],
    "redes": {   # EDITAR: pega los links; los vacíos no se muestran
        "instagram": "",
        "facebook": "",
        "tiktok": "",
    },
    "precios_parrillada": {"Junior": "", "Mediana": "", "Grande": ""},  # EDITAR: ej. "45000"
}

DIA_NUM = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}

# ======================= CARTA =======================
CARTA = [
    {"id": "sopas", "titulo": "Sopas típicas", "icono": "🥣", "sub": "Como en la casa de la abuela", "clase": "grupo--sopas", "platos": [
        ("Cuchuco de trigo", "Sopa campesina de trigo molido con espinazo de cerdo, papa, habas y arvejas.", 12000, "cuchuco-de-trigo"),
        ("Mondongo", "Sopa de menudo cocinada lentamente con papa pastusa, habas, cilantro y especias.", 12000, "mondongo"),
        ("Mute de mazorca", "Sopa tradicional que celebra el sabor y la textura de la mazorca en cada cucharada.", 12000, "mute-de-mazorca"),
    ]},
    {"id": "barra-de-tota", "titulo": "La Barra de Tota", "icono": "🐟", "sub": "Truchas y pescados", "clase": "", "platos": [
        ("Mojarra frita", "Mojarra fresca frita hasta lograr un dorado perfecto, tierna y jugosa por dentro.", 38000, "mojarra-frita"),
        ("Bagre en salsa", "Bagre fresco cocido en salsa con especias, cebolla y tomate.", 38000, "bagre-en-salsa"),
        ("Cachama frita", "Cachama frita: crujiente por fuera y suave por dentro.", 38000, "cachama-frita"),
        ("Trucha marinera", "Filete de trucha fresca bañado en cremosa salsa marinera con frutos del mar.", 48000, "trucha-marinera"),
        ("Viudo de capaz", "Capaz fresco cocido lentamente en un sudado con especias.", 40000, "viudo-de-capaz"),
        ("Trucha boyacense", "Filete de trucha fresca en suave y cremosa salsa de mazorca.", 39000, "trucha-boyacense"),
        ("Trucha al ajillo", "Filete de trucha fresca con una exquisita y cremosa salsa de ajo.", 38000, "trucha-al-ajillo"),
        ("Trucha a la plancha", "Filete de trucha fresca a la plancha para resaltar su sabor natural.", 35000, "trucha-a-la-plancha"),
    ]},
    {"id": "carnes", "titulo": "Nuestras carnes", "icono": "🥩", "sub": "Asadas a la perfección", "clase": "grupo--carnes", "platos": [
        ("Churrasco", "Corte jugoso de res, asado a la perfección para resaltar su sabor y ternura.", 38000, "churrasco"),
        ("Lomo de cerdo", "Corte tierno y jugoso de cerdo, cocinado para resaltar su sabor natural.", 38000, "lomo-de-cerdo"),
        ("Pechuga asada", "Pechuga de pollo tierna y jugosa, asada a la perfección.", 36000, "pechuga-asada"),
        ("Tabla churrasco y lomo", "Una dupla irresistible: jugoso churrasco de res y tierno lomo de cerdo.", 38000, "tabla-churrasco-lomo"),
        ("Tabla churrasco y pechuga", "Jugoso churrasco de res y tierna pechuga de pollo asada, servidos juntos.", 38000, "tabla-churrasco-pechuga"),
        ("Tabla lomo y pechuga", "Tierno lomo de cerdo y pechuga de pollo asada en un solo plato.", 38000, "tabla-lomo-pechuga"),
    ]},
    {"id": "picadas", "titulo": "Picadas de carne", "icono": "🔥", "sub": "450 g para disfrutar", "clase": "grupo--sopas", "platos": [
        ("Picada carne mixta", "450 g de carne de res y cerdo con rellena tradicional, papa salada, yuca sudada y guacamole fresco.", 45000, "picada-carne-mixta"),
        ("Picada carne de cerdo", "450 g de carne de cerdo con rellena tradicional, papa salada, yuca sudada y guacamole fresco.", 45000, "picada-carne-de-cerdo"),
        ("Picada carne de res", "450 g de jugosa carne de res con rellena tradicional, papa salada, yuca sudada y guacamole fresco.", 45000, "picada-carne-de-res"),
    ]},
]
ACOMPANAMIENTOS = [
    ("Arepa boyacense", 3500), ("Envuelto de mazorca", 4000), ("Plátano maduro", 7000),
    ("Chorizo artesanal 100 % cerdo", 8000), ("Longaniza amarilla", 8000), ("Longaniza roja", 8000),
    ("Rellena boyacense", 4000), ("Papa salada", 5000), ("Papa criolla", 5000), ("Yuca sudada", 5000),
    ("Guacamole", 7000), ("Patacón", 5000), ("Arroz", 4000), ("Ensalada", 5000), ("Papa a la francesa", 4000),
]
BEBIDAS = [
    ("Preparada especial de la casa (jarra)", 12000), ("Cerveza Club Colombia", 6000), ("Cerveza nacional", 5000),
    ("Gaseosa personal", 4500), ("Jugo natural en agua", 6000), ("Jugo natural en leche", 7000),
    ("Gaseosa Postobón 1.5 L", 9500), ("Agua en botella", 3000),
]
PARRILLADA_INCLUYE = ["Res", "Cerdo", "Longaniza amarilla", "Longaniza roja", "Chorizo artesanal", "Rellena",
                      "Arepa boyacense", "Envuelto de queso y bocadillo", "Plátano maduro", "Papa criolla",
                      "Papa salada", "Yuca sudada", "Guacamole"]

# ======================= utilidades =======================
def cop(n): return "$" + f"{int(n):,}".replace(",", ".")
def wa(texto): return f"https://wa.me/{CONFIG['whatsapp']}?text=" + quote(texto)
WA_GENERAL = wa("¡Hola! 👋 Quiero hacer un pedido / reserva en La Gran Parrillada Boyacense 🔥")
WA_PARRILLADA = wa("¡Hola! 🔥 Quiero pedir la Auténtica Parrillada Boyacense. ¿Qué tamaños tienen disponibles hoy?")
TEL = "tel:" + CONFIG["telefono"].replace(" ", "")
D = CONFIG["dominio"]
dir_txt = ", ".join(x for x in [CONFIG["direccion"], CONFIG["ciudad"] + ", " + CONFIG["departamento"]] if x)

def img(slug, alt, sizes="(min-width:1000px) 300px, 118px", eager=False, w=360, h=None):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="img/{slug}-360.webp" srcset="img/{slug}-360.webp 360w, img/{slug}-720.webp 720w" '
            f'sizes="{sizes}" alt="{e(alt)}" width="{w}" height="{h or int(w*0.53)}" {loading}>')

ICONOS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
 <symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.2h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm5.8 14.03c-.24.68-1.42 1.31-1.96 1.36-.5.05-1.12.07-1.81-.11a16.4 16.4 0 0 1-1.64-.6c-2.88-1.25-4.76-4.15-4.9-4.34-.14-.19-1.17-1.56-1.17-2.97s.74-2.11 1-2.4c.27-.29.58-.36.78-.36h.56c.18 0 .42-.07.66.5.24.58.82 2 .89 2.15.07.14.12.31.02.5-.1.19-.14.31-.29.48-.14.17-.3.38-.43.51-.14.14-.29.3-.13.59.17.29.74 1.22 1.59 1.98 1.09.97 2.01 1.27 2.3 1.42.29.14.46.12.63-.07.17-.19.72-.84.92-1.13.19-.29.38-.24.65-.14.26.1 1.68.79 1.97.94.29.14.48.22.55.34.07.12.07.7-.17 1.38Z"/></symbol>
 <symbol id="i-tel" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></symbol>
 <symbol id="i-pin" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
 <symbol id="i-reloj" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 6v6l4 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
 <symbol id="i-carta" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5v14ZM8 7h8M8 11h6"/></symbol>
 <symbol id="i-fuego" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2s1 3-1.5 6S7 12.5 7 15a5 5 0 0 0 10 0c0-2-1-3.5-1-3.5s-.5 2-2 2.5c0 0 1.5-3-1-6.5C12.2 6.4 12 4 12 2Zm0 20a7 7 0 0 1-7-7c0-3.4 2.2-5.6 3.8-7.6C10.3 5.6 11 4 11 2c0 0 6.5 3.4 6.5 9.3 0 0 1.5-1 1.5-3 0 0 2 2.6 2 6.7a9 9 0 0 1-9 7Z" opacity=".95"/></symbol>
 <symbol id="i-familia" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></symbol>
 <symbol id="i-pez" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M2 12s4-6 11-6c4 0 7 3 9 6-2 3-5 6-9 6-7 0-11-6-11-6Zm0 0 -1-4m1 4-1 4M16 11h.01"/></symbol>
 <symbol id="i-cal" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 2v4M8 2v4M3 10h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
 <symbol id="i-ig" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></symbol>
 <symbol id="i-fb" viewBox="0 0 24 24"><path fill="currentColor" d="M14 8V6.5c0-.8.2-1.3 1.4-1.3H17V2.1A22 22 0 0 0 14.6 2C12.2 2 10.6 3.4 10.6 6.1V8H8v3.4h2.6V22H14V11.4h2.7L17 8h-3Z"/></symbol>
 <symbol id="i-tt" viewBox="0 0 24 24"><path fill="currentColor" d="M16.6 2h-3.3v13.4a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V9.2a6.3 6.3 0 1 0 5.3 6.2V8.6a7.9 7.9 0 0 0 4.4 1.4V6.7a4.6 4.6 0 0 1-4.4-4.7Z"/></symbol>
</svg>"""

LOGO_SVG = """<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="lg-f" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e8571e"/><stop offset=".6" stop-color="#ff8a2f"/><stop offset="1" stop-color="#ffd36b"/></linearGradient></defs><rect x="2" y="2" width="60" height="60" rx="16" fill="#5b2f17"/><rect x="5" y="5" width="54" height="54" rx="13" fill="none" stroke="#f6b732" stroke-width="2" opacity=".55"/><path d="M32 9c2 7-6 10-6 18 0 3 1.5 5 3 6-4-1-8-5-8-10-5 5-7 10-7 15 0 9 8 15 18 15s18-6 18-15c0-8-6-12-8-18-1 5-3 7-5 8 2-6-1-14-5-19Z" fill="url(#lg-f)"/><path d="M32 30c1 4-3 6-3 10a4.5 4.5 0 0 0 9 0c0-4-3-6-6-10Z" fill="#fff2d6"/><rect x="12" y="49" width="40" height="7" rx="3.5" fill="#7a4220" transform="rotate(-8 32 52)"/><rect x="12" y="49" width="40" height="7" rx="3.5" fill="#8f5228" transform="rotate(8 32 52)"/></svg>"""

# ======================= JSON-LD =======================
def schema():
    horas = []
    for dia, _, a, c in CONFIG["horario"]:
        if a is None: continue
        o = {"@type": "OpeningHoursSpecification", "dayOfWeek": f"https://schema.org/{dia}"}
        if a and c: o["opens"], o["closes"] = a, c
        if a and c: horas.append(o)
    secciones = []
    for g in CARTA:
        secciones.append({"@type": "MenuSection", "name": g["titulo"], "hasMenuItem": [
            {"@type": "MenuItem", "name": n, "description": d, "image": f"{D}/img/{s}-720.webp",
             "offers": {"@type": "Offer", "price": p, "priceCurrency": "COP"}} for n, d, p, s in g["platos"]]})
    secciones.insert(1, {"@type": "MenuSection", "name": "La Parrillada", "hasMenuItem": [{
        "@type": "MenuItem", "name": "Auténtica Parrillada Boyacense",
        "description": "Cortes de res y cerdo, longaniza amarilla y roja, chorizo artesanal, rellena, arepa boyacense, envuelto, plátano maduro, papa criolla, papa salada, yuca sudada y guacamole. Tamaños Junior, Mediana y Grande.",
        "image": f"{D}/img/parrillada-boyacense-1200.webp"}]})
    secciones.append({"@type": "MenuSection", "name": "Acompañamientos", "hasMenuItem": [
        {"@type": "MenuItem", "name": n, "offers": {"@type": "Offer", "price": p, "priceCurrency": "COP"}} for n, p in ACOMPANAMIENTOS]})
    secciones.append({"@type": "MenuSection", "name": "Bebidas", "hasMenuItem": [
        {"@type": "MenuItem", "name": n, "offers": {"@type": "Offer", "price": p, "priceCurrency": "COP"}} for n, p in BEBIDAS]})

    direccion = {"@type": "PostalAddress", "addressLocality": CONFIG["ciudad"], "addressRegion": CONFIG["departamento"], "addressCountry": "CO"}
    if CONFIG["direccion"]: direccion["streetAddress"] = CONFIG["direccion"]
    if CONFIG["codigo_postal"]: direccion["postalCode"] = CONFIG["codigo_postal"]
    rest = {
        "@type": "Restaurant", "@id": f"{D}/#restaurante",
        "name": CONFIG["nombre"], "alternateName": ["LGPB", "La Gran Parrillada", "Parrillada Boyacense Sogamoso"],
        "description": "Restaurante familiar de comida típica boyacense en Sogamoso desde 2015. Parrillada boyacense, cuchuco, mondongo, mute, truchas, carnes asadas y picadas.",
        "url": f"{D}/", "telephone": CONFIG["telefono"], "image": [f"{D}/img/og-lgpb.jpg", f"{D}/img/parrillada-boyacense-1200.webp"],
        "logo": f"{D}/icon-512.png", "address": direccion,
        "areaServed": [{"@type": "City", "name": "Sogamoso"}, {"@type": "AdministrativeArea", "name": "Boyacá"}],
        "servesCuisine": ["Comida típica boyacense", "Comida colombiana", "Parrilla", "Asados", "Trucha"],
        "priceRange": "$$", "currenciesAccepted": "COP", "foundingDate": CONFIG["fundado"],
        "hasMenu": {"@type": "Menu", "name": "La Carta de Boyacá", "url": f"{D}/#carta", "inLanguage": "es-CO", "hasMenuSection": secciones},
        "potentialAction": {"@type": "OrderAction", "target": {"@type": "EntryPoint", "urlTemplate": f"https://wa.me/{CONFIG['whatsapp']}", "actionPlatform": ["https://schema.org/MobileWebPlatform", "https://schema.org/DesktopWebPlatform"]}},
    }
    if horas: rest["openingHoursSpecification"] = horas
    if CONFIG["lat"] and CONFIG["lng"]: rest["geo"] = {"@type": "GeoCoordinates", "latitude": CONFIG["lat"], "longitude": CONFIG["lng"]}
    redes = [u for u in CONFIG["redes"].values() if u]
    if redes: rest["sameAs"] = redes
    rest["hasMap"] = CONFIG["maps_link"]
    web = {"@type": "WebSite", "@id": f"{D}/#web", "url": f"{D}/", "name": CONFIG["nombre"], "inLanguage": "es-CO", "publisher": {"@id": f"{D}/#restaurante"}}
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return json.dumps({"@context": "https://schema.org", "@graph": [rest, web, faq]}, ensure_ascii=False, indent=1)

FAQ = [
    ("¿Dónde comer comida típica boyacense en Sogamoso?",
     "En La Gran Parrillada Boyacense, restaurante familiar en Sogamoso desde 2015. Servimos la Auténtica Parrillada Boyacense, sopas típicas como cuchuco de trigo, mondongo y mute de mazorca, truchas, carnes asadas y picadas."),
    ("¿Qué días abre el restaurante?",
     "Abrimos los fines de semana (sábado y domingo). En temporada de diciembre abrimos todos los días. Escríbenos por WhatsApp al +57 312 4411166 para confirmar el horario del día."),
    ("¿Cómo hago un pedido o una reserva?",
     "Por WhatsApp al +57 312 4411166. Toca cualquier botón verde de esta página y te llega el mensaje listo para enviar."),
    ("¿Qué trae la Auténtica Parrillada Boyacense?",
     "Cortes de res y cerdo, longaniza amarilla, longaniza roja, chorizo artesanal 100 % cerdo y rellena tradicional, acompañados de arepa boyacense, envuelto de queso y bocadillo, plátano maduro, papa criolla, papa salada, yuca sudada y guacamole fresco. Viene en tamaño Junior, Mediana y Grande."),
    ("¿Cuánto cuesta comer en La Gran Parrillada Boyacense?",
     "Las sopas típicas cuestan $12.000, los platos fuertes entre $35.000 y $48.000 y los acompañamientos desde $3.500 (precios en pesos colombianos, sujetos a cambios)."),
]

def sitemap():
    hoy = datetime.date.today().isoformat()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url><loc>{D}/</loc><lastmod>{hoy}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority>
    <image:image><image:loc>{D}/img/parrillada-boyacense-1200.webp</image:loc></image:image>
    <image:image><image:loc>{D}/img/og-lgpb.jpg</image:loc></image:image>
  </url>
  <url><loc>{D}/privacidad.html</loc><lastmod>{hoy}</lastmod><changefreq>yearly</changefreq><priority>0.2</priority></url>
</urlset>
"""

