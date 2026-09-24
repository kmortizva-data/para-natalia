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

1. Enchambered · Alone Together (escape room para 2) · 2. Codenames Duet · 3. skribbl.io ·
4. JKLM.fun BombParty · 5. Board Game Arena · 6. Lichess · 7. jigsawpuzzles.io · 8. Geotastic ·
9. PlayingCards.io · 10. Teleparty.
Descartados: Among Us (mínimo 4), Gartic Phone (rinde con 4+), Jackbox (pago), Escape Team (DNS caído).

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
- [ ] Settings → Pages → Deploy from a branch → `main` / `site` (o raíz si no aparece).
- [ ] Confirmar la lista de juegos o cambiar alguno en `games.json`.

## Bitácora

- 2026-09-24: plan aprobado. Hecho el mismo día: estructura, `games.json`, hoja QR (los 11 códigos
  se decodifican con zxing-cpp desde el PNG), sitio completo y verificado en local con capturas
  (clave mala rechazada, clave buena con mayúsculas/espacios aceptada, 10 botones con la URL
  correcta, galería vacía y con 5 fotos de prueba + visor, tema claro/oscuro, móvil 375 px sin
  scroll horizontal). Las fotos de prueba se borraron; `manifest.json` quedó en `[]`.
  Clave elegida por kei el 2026-09-24 (solo el hash vive en el repo). Servidor local registrado
  como `natalia` en `~/.claude/launch.json`. Proyecto registrado en `_INDICE/projects.json`.
  Pendiente: repo en GitHub + Pages (solo kei puede crearlo) y primer push.
