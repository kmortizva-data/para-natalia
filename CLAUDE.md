# Para Natalia — memoria del proyecto

> Regalo de despedida para Natalia, amiga de kei: una hoja carta con 10 códigos QR y un sitio
> web en GitHub Pages con mensaje, fotos y los mismos 10 juegos para seguir jugando a distancia.
> Nació el 2026-09-24. Carpeta `Documents\02_Personal\Natalia` (personal, no portafolio).

## Decisiones (2026-09-24)

- Jugadores: **solo Natalia y kei**; todo juego debe funcionar bien a dos con sala privada por link.
- Fotos: kei las suelta en `fotos_originales/` (fuera de git). `tools/prepare_photos.py` las
  redimensiona a 1600 px, **borra EXIF (incluida ubicación GPS)** y escribe `site/photos/manifest.json`.
- Privacidad: repo público (GitHub Pages gratis lo exige) + **clave sencilla** (palabra que elige
  kei, comparada por SHA-256 en el JS; no es seguridad real) + `noindex` + `robots.txt`.
  **La clave se pide en cada visita** (pedido de kei 2026-09-25: que nadie en el PC de ella la
  encuentre abierta); no se guarda nada en localStorage sobre el desbloqueo.
- Mensaje: borrador de Claude en `site/message.md`; kei lo edita ahí y solo ahí.
- Los 10 juegos viven en `site/games.json` (fuente única para la hoja QR y el sitio).
- Repo: `para-natalia` en la cuenta `kmortizva-data` → `https://kmortizva-data.github.io/para-natalia/`.
- Código en inglés; textos visibles, README y este archivo en español.
- Fuentes de la hoja PDF: Georgia + Segoe UI (del sistema; la red a 35 KB/s no da para bajar TTF).
- **Música (2026-09-25): NO se publica el MP3** de `Downloads\Bad Bunny - DtMF.mp3` (repo público
  = distribución con derechos; GitHub baja el repo entero por DMCA y se pierde el regalo). Suena
  el visualizer oficial de YouTube, canal "Bad Bunny", ID `v9T_MGfzq7I` (constante `VIDEO_ID` en
  `script.js`), en una tarjeta fija de 200×200 (mínimo que exige YouTube; no se puede esconder).
  Arranca dentro del clic de Entrar: la clave se hashea mientras escribe para que el `playVideo`
  quede dentro del gesto. Si el navegador lo bloquea, aparece "Toca la pantalla para que suene" y
  el primer toque la arranca. Volumen y silencio se recuerdan en localStorage.

## Los 10 juegos (verificados 2026-09-24: gratis, navegador, sirven a dos)

Orden pedido por kei el 2026-09-24: los escape rooms van primero.
1. Enchambered · Alone Together (navegador, gratis) · 2. Escape Lab (navegador o app, gratis,
1-2 h) · 3. Unsolved Case de Eleven Puzzles (app gratis sin anuncios, 30-60 min; NO es navegador,
avisado) · 4. Codenames Duet · 5. skribbl.io · 6. JKLM.fun BombParty · 7. Board Game Arena ·
8. jigsawpuzzles.io · 9. PlayingCards.io · 10. Teleparty.
Salieron el 2026-09-24 a pedido de kei: Geotastic y Lichess (quería más escape rooms).
Descartados: Among Us (mínimo 4), Gartic Phone (rinde con 4+), Jackbox (pago), Escape Team (DNS
caído), Together Apart de Enchambered (mínimo 5 USD), Parallel Lab (de pago).

## Estructura

```
site/            lo que se publica: index.html, styles.css, script.js, games.json, message.md,
                 photos/ (generado), robots.txt, favicon.svg, qr_natalia.pdf (copia para descargar)
qr/              make_qr_sheet.py → out/qr_natalia.pdf y .png (carta, 300 dpi)
tools/           prepare_photos.py
fotos_originales/  originales de kei, ignorada por git
```

## Cómo se corre

```
python qr/make_qr_sheet.py          # regenera la hoja
python tools/prepare_photos.py      # tras soltar fotos en fotos_originales/
cd site && python -m http.server 8551   # ver local en http://localhost:8551
```

## Pendientes de kei

- [x] Palabra clave elegida (2026-09-24).
- [ ] Soltar fotos en `fotos_originales/` y correr `prepare_photos.py`.
- [x] Mensaje definitivo de kei puesto el 2026-09-25 (texto suyo, literal).
- [x] Repo público creado y primer push hecho (2026-09-24).
- [x] Pages se publica con `.github/workflows/pages.yml` (Actions, carpeta `site/`); se activa solo.
- [ ] Confirmar la lista de juegos o cambiar alguno en `games.json`.

## Inventario de UI (para auditar tras refactors)

- Puerta: campo "Dime un número de 3 dígitos que traiga buena suerte" (teclado numérico) + botón
  Entrar + error "Ese no es. Piensa en un número nuestro." con sacudida.
- Barra: solo la marca. Sin botón de tema (siempre oscura, decisión de kei 2026-09-25). Los menús
  de arriba se quitaron el 2026-09-25: los reemplaza el **panel lateral** (Inicio / Mensaje /
  Fotos / Juegos, fijo arriba a la derecha bajo la barra, resalta la sección actual, pestaña
  para esconderlo y recuerda la elección). Se puso arriba porque a media altura lo tapaba la
  tarjeta de música.
- Portada: eyebrow, "Te extraño,", **burbujas** (Natalia grande + gold nugget, la esmeralda que
  más brilla, mi parcera, china mk, ojitos lindos; física propia en `initBubbles`, arrastrables,
  estáticas si `prefers-reduced-motion`), subtítulo, flecha "Baja".
- Mensaje: tarjeta con comillas, párrafos de `message.md`, firma en cursiva.
- Fotos ("Debí Tirar Más Fotos"): mosaico de columnas con las primeras 24 + botón "Ver las
  otras N"; visor a pantalla completa tipo carrusel (contador, cerrar, flechas en escritorio,
  deslizar con el dedo, toque en los bordes, arrastre hacia abajo cierra, Esc, teclado).
  El lead de la sección es la línea de `index.html` comentada "Cambia esta línea": kei pidió
  poner letra de la canción y NO se hace (no se reproducen letras); él la pega si quiere.
- Juegos: 10 tarjetas (icono por categoría, categoría, nombre, sitio, número, texto, botón Jugar
  en pestaña nueva, desplegable "¿Cómo entramos a dos?"), link a la hoja QR en la intro.
- Pie: firma y aviso de no indexado.
- Tarjeta de música (fija, abajo a la derecha; en móvil a lo ancho): punto que late, etiqueta
  "Sonando · DtMF, Bad Bunny", plegar (oculta controles, el video sigue), cerrar (para la música
  y esconde la tarjeta), reproductor 200×200, botones bajar / silenciar / subir, barras de nivel,
  aviso "Toca la pantalla para que suene" cuando el navegador bloquea el arranque.

## Bitácora

- 2026-09-25 (fotos): kei soltó 81 fotos y 15 videos de WhatsApp en `fotos_originales/`.
  `prepare_photos.py` ahora deduplica (md5 exacto + hash perceptual a distancia ≤ 2): quitó 10
  repetidas → 71 fotos, 13.5 MB en `site/photos/`. Quedan 2 pares casi iguales (distancia 3-4,
  posibles ráfagas) que se le mostraron a kei para que decida. Los **videos no se procesan**
  (123 MB en total, 2 repetidos): pendiente de decisión de kei (comprimir con ffmpeg a ~40 MB y
  meterlos al carrusel, o dejarlos fuera). Sección renombrada "Debí Tirar Más Fotos", mosaico
  con 24 + "Ver las otras N", visor carrusel a pantalla completa con deslizamiento.
  Nota: el servidor local de Python corta las fotos grandes (ERR_CONNECTION_RESET, ver memoria
  "servidor Python en trozos"); en GitHub Pages no pasa.

- 2026-09-25 (noche): mensaje definitivo de kei con firma "Con cariño, Kevin" (los saltos de
  línea sueltos se respetan con `<br>`). Música: kei pidió el MP3 de DtMF tras la clave con
  botones de volumen y mute; se le explicó el riesgo legal y eligió YouTube oficial. Hecho y
  verificado en local: arranca al pulsar Entrar, botones cambian volumen de 10 en 10 y silencian,
  se recuerdan; móvil revisado. Después, en ráfaga: párrafo del "Polo Norte" ampliado
  ("recordandonos el calor del hogar estando tan lejos", literal, sin tilde como él lo escribió),
  **tema claro eliminado** (tokens oscuros en `:root`, sin toggle) y la puerta pregunta "Dime un
  número de 3 dígitos que traiga buena suerte" (la clave sigue siendo la misma).

- 2026-09-25: kei pidió dinamismo en la portada: burbujas flotando que chocan e intercambian
  lugar, Natalia la más grande y sus apodos alrededor. Hecho con DOM + física simple (rebote en
  paredes, choques elásticos con masa ∝ r², deriva aleatoria, arrastre con el dedo). Bug real
  cazado con medición: el `padding: 12%` inflaba todas las burbujas pequeñas a 236 px (el
  porcentaje es del ancho de la caja), por eso se montaban; ahora el padding va en función de
  `--d`. Verificado en escritorio, móvil 375 px y modo oscuro.
  Luego pidió burbujas y letra más pequeñas y más rebote: radio base 14 % del ancho (19 % en
  pantallas < 600 px para que quepan las etiquetas), letra 0.115·d con piso de 11 px, velocidad
  70-170 px/s. Perillas en `initBubbles` (`base`, `MAX`, `MIN`) y en `.bubble` del CSS.

- 2026-09-24: plan aprobado. Hecho el mismo día: estructura, `games.json`, hoja QR (los 11 códigos
  se decodifican con zxing-cpp desde el PNG), sitio completo y verificado en local con capturas
  (clave mala rechazada, clave buena con mayúsculas/espacios aceptada, 10 botones con la URL
  correcta, galería vacía y con 5 fotos de prueba + visor, tema claro/oscuro, móvil 375 px sin
  scroll horizontal). Las fotos de prueba se borraron; `manifest.json` quedó en `[]`.
  Clave elegida por kei el 2026-09-24 (solo el hash vive en el repo). Servidor local registrado
  como `natalia` en `~/.claude/launch.json`. Proyecto registrado en `_INDICE/projects.json`.
  Repo creado por kei y primer push el mismo día. Pages: el primer intento de activarlo desde el workflow falló (GitHub no deja que el token del repo lo encienda); se activó a mano en Settings → Pages → Source: GitHub Actions y se relanzó con un push.
