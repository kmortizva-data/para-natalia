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
- Mensaje: borrador de Claude en `site/message.md`; kei lo edita ahí y solo ahí.
- Los 10 juegos viven en `site/games.json` (fuente única para la hoja QR y el sitio).
- Repo: `para-natalia` en la cuenta `kmortizva-data` → `https://kmortizva-data.github.io/para-natalia/`.
- Código en inglés; textos visibles, README y este archivo en español.
- Fuentes de la hoja PDF: Georgia + Segoe UI (del sistema; la red a 35 KB/s no da para bajar TTF).

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
- [ ] Revisar `site/message.md`.
- [x] Repo público creado y primer push hecho (2026-09-24).
- [x] Pages se publica con `.github/workflows/pages.yml` (Actions, carpeta `site/`); se activa solo.
- [ ] Confirmar la lista de juegos o cambiar alguno en `games.json`.

## Inventario de UI (para auditar tras refactors)

- Puerta: input "La palabra" + botón Entrar + mensaje de error con sacudida.
- Barra: marca, nav (Mensaje/Fotos/Juegos, solo ≥720 px), botón de tema.
- Portada: eyebrow, "Te extraño,", **burbujas** (Natalia grande + gold nugget, la esmeralda que
  más brilla, mi parcera, china mk, ojitos lindos; física propia en `initBubbles`, arrastrables,
  estáticas si `prefers-reduced-motion`), subtítulo, flecha "Baja".
- Mensaje: tarjeta con comillas, párrafos de `message.md`, firma en cursiva.
- Fotos: mosaico de columnas + visor (cerrar, anterior, siguiente, flechas del teclado, Esc).
- Juegos: 10 tarjetas (icono por categoría, categoría, nombre, sitio, número, texto, botón Jugar
  en pestaña nueva, desplegable "¿Cómo entramos a dos?"), link a la hoja QR en la intro.
- Pie: firma y aviso de no indexado.

## Bitácora

- 2026-09-25: kei pidió dinamismo en la portada: burbujas flotando que chocan e intercambian
  lugar, Natalia la más grande y sus apodos alrededor. Hecho con DOM + física simple (rebote en
  paredes, choques elásticos con masa ∝ r², deriva aleatoria, arrastre con el dedo). Bug real
  cazado con medición: el `padding: 12%` inflaba todas las burbujas pequeñas a 236 px (el
  porcentaje es del ancho de la caja), por eso se montaban; ahora el padding va en función de
  `--d`. Verificado en escritorio, móvil 375 px y modo oscuro.

- 2026-09-24: plan aprobado. Hecho el mismo día: estructura, `games.json`, hoja QR (los 11 códigos
  se decodifican con zxing-cpp desde el PNG), sitio completo y verificado en local con capturas
  (clave mala rechazada, clave buena con mayúsculas/espacios aceptada, 10 botones con la URL
  correcta, galería vacía y con 5 fotos de prueba + visor, tema claro/oscuro, móvil 375 px sin
  scroll horizontal). Las fotos de prueba se borraron; `manifest.json` quedó en `[]`.
  Clave elegida por kei el 2026-09-24 (solo el hash vive en el repo). Servidor local registrado
  como `natalia` en `~/.claude/launch.json`. Proyecto registrado en `_INDICE/projects.json`.
  Repo creado por kei y primer push el mismo día. Pages: el primer intento de activarlo desde el workflow falló (GitHub no deja que el token del repo lo encienda); se activó a mano en Settings → Pages → Source: GitHub Actions y se relanzó con un push.
