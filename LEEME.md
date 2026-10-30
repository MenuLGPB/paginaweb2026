# La Gran Parrillada Boyacense: sitio v2

La estructura nueva, con animaciones, está pensada **primero para celular**.

Para verla en tu PC, abre la carpeta en VS Code y usa la extensión *Live Server*. Si abres `index.html` con doble clic, los íconos y las fuentes no cargan bien.

## Qué tiene cada sección

| Sección | Celular | PC |
|---|---|---|
| **Pantalla de carga** | No aparece, para que abra más rápido | Contador 0→100 y una cortina que sube (solo la primera visita) |
| **Portada** | Los platos rotan cada 3 s, con nombre y precio. Título gigante que sube desde una máscara | Igual, más título a la izquierda, plato a la derecha y cursor personalizado |
| **Manifiesto** | Las palabras se van "encendiendo" a medida que bajas | Igual |
| **Parrillada** | La foto se abre desde el centro, los ingredientes aparecen uno a uno y la carta gira | Igual + parallax |
| **¿Qué se le antoja?** | Tarjetas tipo historia de Instagram que se deslizan con el dedo, con barra de progreso | 5 tarjetas en fila |
| **Carta** | Pestañas fijas que siguen la sección, nombres gigantes que se deslizan y botón *Pedir* en cada plato | La foto del plato sigue al mouse al pasar por cada fila |
| **Galería** | Dos cintas de fotos en sentidos opuestos | 4 columnas que se mueven a distinta velocidad |
| **Cifras** | Los números cuentan al aparecer | Igual |
| **Visítanos** | Horario con el día de hoy marcado y estado "Hoy abrimos", más mapa bajo demanda | Igual |
| **Final + pie** | "¿Nos vemos, sumercé?" y la palabra PARRILLADA gigante en contorno | Botones magnéticos |
| **Barra tipo app** | Inicio · Carta · **WhatsApp** · Llegar · Llamar, siempre visible | Se oculta, porque el header ya tiene la navegación |

Si el celular tiene activado *"reducir movimiento"*, las animaciones se apagan solas. Si las librerías no cargan, la página se ve completa sin animar.

## Google (Lighthouse)

- **Celular:** SEO 100 · Buenas prácticas 100 · Accesibilidad 95 · Velocidad ~86.
- **PC:** SEO 100 · Buenas prácticas 100 · Accesibilidad 95 · Velocidad 97.

Incluye los datos estructurados de restaurante con toda la carta y los precios, las preguntas frecuentes, el sitemap y la imagen para compartir en WhatsApp y Facebook.

## Dónde cambiar tus cosas

- **Tu logo:** en `_generador/generar.py`, función `top()`, cambia el texto de `.logo` por `<img src="img/logo.png" alt="La Gran Parrillada Boyacense" height="44">`.
- **Tus fotos:** ponlas en `img/` con el mismo nombre (formato `.webp`, en 360 px y 720 px de ancho), o cambia los nombres en `HERO_PLATOS`, `STORIES` y `GALERIA`.
- **Videos de IA (Flow):**
  - En la **portada**, descomenta la etiqueta `<video>` en `index()` y pon tu video en `video/hero.mp4`.
  - En las **historias**, pon la ruta del `.mp4` vertical en `STORIES` (último campo). Se reproduce solo cuando la tarjeta está en pantalla.
- **Carta, precios, dirección, horario y redes:** en `_generador/datos.py`.
- Después de editar, ejecuta `python _generador/generar.py` y se regeneran `index.html`, `privacidad.html`, `404.html` y `sitemap.xml`.

## Pendiente

Dirección exacta, horas de apertura y cierre, links de redes y precios de la parrillada Junior, Mediana y Grande.

## Publicar en GitHub Pages

1. Crea un repositorio público.
2. Sube **todo el contenido** de esta carpeta. Incluye `CNAME` y `.nojekyll`.
3. Ve a **Settings → Pages → Deploy from branch → main / root**.
4. En **Custom domain** escribe `lagranparrilladaboyacense.com`.
5. En tu dominio, configura el DNS:
   - Registros **A**: `185.199.108.153`, `185.199.109.153`, `185.199.110.153` y `185.199.111.153`.
   - **CNAME** `www` → `TU-USUARIO.github.io`.
6. Activa **Enforce HTTPS**.
7. Luego registra el sitio en Google Search Console, envía el `sitemap.xml` y completa tu Perfil de Empresa en Google.
