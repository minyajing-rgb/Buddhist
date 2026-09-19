# Publish the HTML site with GitHub Pages

The site is already prepared under `docs/`.

One-time repository setting:

1. Open **Settings**
2. Open **Pages**
3. Under **Build and deployment**, choose **Deploy from a branch**
4. Branch: **main**
5. Folder: **/docs**
6. Save

The expected public URL will follow GitHub Pages' normal project-site pattern for this repository.

No build step is required. The site is static HTML + SVG and includes `docs/.nojekyll`.
