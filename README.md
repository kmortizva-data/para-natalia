# Para Natalia

Un regalo de despedida en dos partes:

1. **Hoja carta con 10 códigos QR** (`qr/out/qr_natalia.pdf`), uno por juego, para imprimir y guardar.
2. **Sitio web** (`site/`) publicado en GitHub Pages: un mensaje, fotos y los mismos 10 juegos con
   botones. Está detrás de una palabra clave y no aparece en buscadores.

Los 10 juegos son gratis, corren en el navegador y sirven para dos personas a distancia.
La lista vive en un solo lugar, `site/games.json`, y de ahí salen tanto la hoja como la web.

## Cómo actualizar

| Quiero… | Hago… |
|---|---|
| Cambiar el mensaje | Edito `site/message.md` (línea en blanco = párrafo nuevo). |
| Poner o cambiar fotos | Suelto jpg/png en `fotos_originales/` y corro `python tools/prepare_photos.py`. Se achican a 1600 px y pierden los metadatos (ubicación incluida). Los originales nunca se suben. |
| Cambiar un juego | Edito `site/games.json` y corro `python qr/make_qr_sheet.py` para regenerar la hoja (copia el PDF nuevo a `site/`). |
| Cambiar la palabra clave | `python -c "import hashlib;print(hashlib.sha256(b'palabra').hexdigest())"` y pego el hash en `PASS_HASH` de `site/script.js`. La palabra se compara sin tildes, sin mayúsculas y sin espacios sobrantes. |
| Verla en local | `python -m http.server 8551 --directory site` y abro `http://localhost:8551`. |
| Publicar | `git add -A && git commit && git push`; GitHub Pages se actualiza solo en uno o dos minutos. |

## Publicación (una sola vez)

1. Crear en github.com un repo **público** vacío llamado `para-natalia`.
2. `git remote add origin https://github.com/kmortizva-data/para-natalia.git` y `git push -u origin main`.
3. En el repo: Settings → Pages → Source "Deploy from a branch" → rama `main`, carpeta `/site`.
   Si GitHub solo ofrece `/(root)` o `/docs`, renombrar `site/` a `docs/` y elegir `/docs`.
4. La página queda en `https://kmortizva-data.github.io/para-natalia/`.

Requisitos: Python 3 con `Pillow`, `qrcode` y `zxing-cpp` (este último solo para verificar los QR).
