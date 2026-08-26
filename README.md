# EN PIE — puesta en marcha (10 minutos, gratis)

No necesitas saber programar. Sigue estos pasos una sola vez.

## 1. Crea tu cuenta de GitHub
Ve a **github.com** → *Sign up* → crea una cuenta gratuita con tu correo.

## 2. Crea el repositorio
1. Arriba a la derecha, pulsa el **+** → **New repository**.
2. Nómbralo, por ejemplo `en-pie`.
3. Márcalo como **Public** (tiene que ser público para que Pages y Actions sean gratis).
4. Pulsa **Create repository**.

## 3. Sube estos archivos
En la página del repositorio recién creado, pulsa **uploading an existing file** (o el botón *Add file → Upload files*) y arrastra **todos** los archivos y carpetas de este proyecto (incluida la carpeta `.github` con el archivo `actualizar.yml` dentro). Confirma con **Commit changes**.

> Importante: la carpeta `.github/workflows/actualizar.yml` tiene que conservar exactamente esa ruta. Si tu navegador no sube carpetas, usa GitHub Desktop (gratis) o pídeme el paso a paso con ese programa.

## 4. Activa GitHub Pages
1. En el repositorio, ve a **Settings → Pages**.
2. En "Build and deployment", elige **Source: GitHub Actions**.

## 5. Lanza la primera actualización
1. Ve a la pestaña **Actions** del repositorio.
2. Verás el flujo "Actualizar noticias diarias". Ábrelo y pulsa **Run workflow** (botón a la derecha) para lanzarlo manualmente la primera vez.
3. Espera 1-2 minutos. Cuando termine en verde, tu web ya está publicada.

## 6. Encuentra tu web
En **Settings → Pages** verá arriba la URL pública, algo como:
`https://tu-usuario.github.io/en-pie/`

A partir de aquí, el robot se ejecuta **solo, cada día a las 7:00 (hora de España)**, sin que tengas que hacer nada ni pagar nada. Añade noticias buscando en `fetch_noticias.py` y ajustando la lista `FUENTES` si quieres sumar o quitar medios.

## Notas importantes
- Todo funciona dentro de los límites gratuitos de GitHub (repos públicos: Pages y Actions ilimitados en la práctica para un proyecto de este tamaño).
- El robot **enlaza siempre a la fuente original** — no copia artículos completos, solo el titular y un resumen corto, para respetar los derechos de los medios.
- El texto de "Cómo actuar hoy" es deliberadamente genérico (escribir a representantes, verificar información, organizarse localmente) porque no incluye fechas de manifestaciones concretas sin confirmar — puedes editarlo a mano en `index.html` si quieres añadir convocatorias reales y verificadas.
- Si algún día un medio cambia su URL de RSS y deja de funcionar, el sitio no se rompe: ese medio simplemente no aportará noticias nuevas ese día (verás un aviso en el registro de "Actions").
