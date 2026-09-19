# Domain Binding｜自定义域名

Dharma Atlas public preview is built from the `docs/` directory.

## First publish on GitHub Pages

Repository:
`minyajing-rgb/Buddhist`

One-time setting:
1. Settings
2. Pages
3. Build and deployment → Deploy from a branch
4. Branch: `main`
5. Folder: `/docs`
6. Save

The default project-site address will follow GitHub Pages' normal project URL pattern.

## Bind a custom domain later

When the final domain is chosen:
1. Add the domain in **Settings → Pages → Custom domain**.
2. Create `docs/CNAME` containing only the domain.
3. Configure DNS:
   - subdomain: CNAME → `minyajing-rgb.github.io`
   - apex domain: use GitHub Pages' documented A/AAAA records.
4. Enable **Enforce HTTPS** after DNS resolves.

The site uses relative page/asset URLs, so moving from the GitHub Pages project URL to a custom domain does not require rewriting the HTML.
