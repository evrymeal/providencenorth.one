# providencenorth.one

Static marketing site for **Providence North LLC**, a private Wyoming holding company.
Two operating companies: The Faithful Business and The Science of Wellness.

Plain HTML + one hand written CSS file. No framework, no build step needed to serve it,
no Tailwind CDN.

## Deploy

Hosted on GitHub Pages from the `main` branch, repo root, under the account `evrymeal`.
Custom domain is configured in `CNAME`.

## Editing content

The six HTML pages are **generated** by `build.py` so the header, footer and navigation
never drift between pages. Edit `build.py`, then:

```bash
python3 build.py
```

That rewrites `index.html`, `portfolio.html`, `governance.html`, `mission.html`,
`contact.html` and `404.html` in place. Edit the HTML directly only if you are happy for
it to be overwritten on the next build.

## Design tokens

All colours, type sizes and spacing live as CSS custom properties at the top of
`assets/css/main.css`. The palette is sampled from the Providence North brand mark
(gold hour sky over an obsidian ridgeline).

- Obsidian canvas `#0D0C0A`
- Warm gold `#E5A93C`, champagne `#F4D389`, bronze `#C2841E`
- Ivory ink `#FBF9F5`, muted `#A69F91`
- Zero border radius throughout
- Bodoni Moda for display, Manrope for body and labels

## Assets

- `assets/img/brand-mark*.png` is the star and ridgeline mark derived from the master logo
- `assets/img/sky-field.jpg` is the hero field, gradient mapped to the brand ramp
- `assets/img/the-faithful-business-logo.png` and `the-science-of-wellness-logo.png` are
  the master logos, unmodified

## Contact form

There is no server. The form composes a `mailto:` with the field values, so nothing is
transmitted through the website and no claim of encryption is made.

## DNS

The domain's nameservers are Google (`ns-cloud-d*.googledomains.com`). To point the domain
at GitHub Pages:

- Replace the four apex `A` records with `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`
- Change the `www` CNAME from `ext-sq.squarespace.com` to `evrymeal.github.io`

Leave the `MX` and `TXT` records alone so Google Workspace mail keeps working.
