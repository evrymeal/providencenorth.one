#!/usr/bin/env python3
# Providence North LLC static site generator.
# Emits the HTML pages from one template so the header/footer never drift,
# plus robots.txt, sitemap.xml, llms.txt, and llms-full.txt.
# Brand tokens live in assets/css/main.css.
import os, hashlib, json

DOMAIN = "providencenorth.one"
BASE   = f"https://{DOMAIN}"
EMAIL  = "inquiries@providencenorth.one"
YEAR   = 2026
OUT    = os.path.dirname(os.path.abspath(__file__))
ORG_ID = f"{BASE}/#organization"
SITE_ID = f"{BASE}/#website"
# Bump when indexable page content changes. Date is UTC.
SITEMAP_LASTMOD = "2026-10-20"
# Homepage meta description, and the Organization description. The namesake
# sentence is identity disambiguation only; it does not describe those entities.
ORG_DESCRIPTION = (
    "Providence North LLC is the Wyoming private holding company that operates "
    "The Faithful Business and The Science of Wellness. Not a fund, broker-dealer, "
    "or investment adviser. Not a Florida D&B entity, California nursing homes, or Tennessee townhomes."
)

# Cache-busting stamp: the stylesheet URL changes whenever the CSS changes, so a
# returning visitor never gets a stale stylesheet after a deploy.
_css_path = os.path.join(OUT, "assets", "css", "main.css")
CSS_V = hashlib.sha256(open(_css_path, "rb").read()).hexdigest()[:8]

NAV = [("index.html","Overview"),("portfolio.html","Businesses"),
       ("governance.html","Governance"),("mission.html","Mission"),
       ("contact.html","Contact")]

MONTH = "September 2026"

# ---------------------------------------------------------------- inline icons
IC = {
 "users":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13A4 4 0 0 1 16 11"/></svg>',
 "scale":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><path d="M12 3v18M7 21h10M3 8l4-2 4 2M13 8l4-2 4 2"/><path d="M3 8l-2 5h4zM19 8l-2 5h4z"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 "pulse":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><path d="M3 12h4l2-6 3 12 3-8 2 2h4"/></svg>',
 "play":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><rect x="2" y="4" width="20" height="16"/><path d="M10 8.5l6 3.5-6 3.5z"/></svg>',
 "book":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><path d="M4 4h9a3 3 0 0 1 3 3v13H7a3 3 0 0 1-3-3z"/><path d="M20 4h-4v16h1a3 3 0 0 0 3-3z"/></svg>',
 "bank":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><path d="M3 10l9-6 9 6M4 10v9M20 10v9M8 10v9M12 10v9M16 10v9M2 21h20"/></svg>',
 "compass":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/></svg>',
 "sun":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg>',
 "mail":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><rect x="2" y="5" width="20" height="14"/><path d="M2 6l10 7L22 6"/></svg>',
 "pin":'<svg viewBox="0 0 24 24" fill="none" stroke="#E5A93C" stroke-width="1.4" stroke-linecap="square"><path d="M12 21s7-6 7-11a7 7 0 1 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "arrow":'<svg class="chev" viewBox="0 0 20 12" width="18" height="11" fill="none" stroke="#E5A93C" stroke-width="1.4"><path d="M0 6h17M12 1l5 5-5 5"/></svg>',
}

def star(size=46, cls="hero-star"):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true">'
            f'<defs><linearGradient id="sg{size}" x1="0" y1="1" x2="0" y2="0">'
            f'<stop offset="0" stop-color="#E5A93C"/><stop offset="1" stop-color="#FFF3D6"/></linearGradient></defs>'
            f'<path d="M12 1 L13.7 10.3 L23 12 L13.7 13.7 L12 23 L10.3 13.7 L1 12 L10.3 10.3 Z" '
            f'fill="url(#sg{size})"/></svg>')

def feat(icon, title, body):
    return (f'<div class="feat">{IC[icon]}<div><div class="ft">{title}</div>'
            f'<div class="fb">{body}</div></div></div>')

def html_text(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def html_attr(s):
    return html_text(s).replace('"', "&quot;")

def canonical_url(fname):
    if fname == "index.html":
        return f"{BASE}/"
    return f"{BASE}/{fname}"

def nav_href(slug):
    return "/" if slug == "index.html" else f"/{slug}"

def schema_graph(fname, title, desc):
    url = canonical_url(fname)
    org = {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Providence North LLC",
        "legalName": "Providence North LLC",
        "url": BASE,
        "description": ORG_DESCRIPTION,
        "logo": f"{BASE}/assets/img/providence-north-logo.png",
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "30 N Gould St, STE R",
            "addressLocality": "Sheridan",
            "addressRegion": "WY",
            "postalCode": "82801",
            "addressCountry": "US",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "Partner inquiries",
            "email": EMAIL,
            "url": f"{BASE}/contact.html",
        },
        "subOrganization": [
            {
                "@type": "Organization",
                "name": "The Faithful Business",
                "url": "https://www.thefaithfulbusiness.com",
            },
            {
                "@type": "Organization",
                "name": "The Science of Wellness",
            },
        ],
    }
    graph = [org]
    if fname == "index.html":
        graph.append({
            "@type": "WebSite",
            "@id": SITE_ID,
            "url": f"{BASE}/",
            "name": "Providence North LLC",
            "description": ORG_DESCRIPTION,
            "publisher": {"@id": ORG_ID},
            "inLanguage": "en",
        })
    page_type = "ContactPage" if fname == "contact.html" else "WebPage"
    graph.append({
        "@type": page_type,
        "@id": f"{url}#webpage",
        "name": title,
        "description": desc,
        "url": url,
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": ORG_ID},
        "inLanguage": "en",
    })
    return json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        separators=(",", ":"),
    )

def head(page_title, desc, fname, page_css="", robots=None):
    url = canonical_url(fname)
    robots_tag = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html_text(page_title)}</title>
<meta name="description" content="{html_attr(desc)}">
{robots_tag}<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Providence North LLC">
<meta property="og:title" content="{html_attr(page_title)}">
<meta property="og:description" content="{html_attr(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og-image.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html_attr(page_title)}">
<meta name="twitter:description" content="{html_attr(desc)}">
<meta name="twitter:image" content="{BASE}/og-image.jpg">
<meta name="theme-color" content="#0D0C0A">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/bodoni-moda-latin-400_700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/manrope-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/main.css?v={CSS_V}">
{page_css}<script type="application/ld+json">{schema_graph(fname, page_title, desc)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def nav_link(slug, label, active):
    current = ' aria-current="page"' if slug == active else ""
    return f'<a href="{nav_href(slug)}"{current}>{label}</a>'

def header(active):
    links = "".join(nav_link(h, t, active) for h, t in NAV)
    mlinks = "".join(nav_link(h, t, active) for h, t in NAV)
    return f'''<header class="hdr">
  <div class="wrap hdr-in">
    <a class="brand" href="/" aria-label="Providence North LLC, home">
      <img class="brand-mark" src="/assets/img/brand-mark@2x.png" alt="" width="72" height="72">
      <span class="brand-txt">
        <span class="brand-name"><span class="ln1">Providence</span><span class="ln2">North</span></span>
        <span class="brand-sub">LLC</span>
      </span>
    </a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <a class="btn btn-ghost hdr-cta" href="/contact.html">Partner Inquiry</a>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i><i></i></button>
  </div>
  <nav class="mnav" id="mnav" aria-label="Mobile">{mlinks}<a href="/contact.html">Partner Inquiry</a></nav>
</header>
'''

def footer():
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <div class="ftr-brand">
          <img src="/assets/img/brand-mark@2x.png" alt="Providence North LLC" width="64" height="64">
          <span class="n">Providence<br>North LLC</span>
        </div>
        <p class="body" style="max-width:34ch">A private holding company. Long horizon stewardship of two lines of business in faith driven commerce and health media.</p>
      </div>
      <div>
        <h5>Lines of Business</h5>
        <p class="small" style="margin:.35rem 0 .6rem">Within Providence North LLC. Trade&nbsp;names.</p>
        <ul>
          <li><a href="/portfolio.html#faithful-business">The Faithful Business</a></li>
          <li><a href="/portfolio.html#science-of-wellness">The Science of Wellness</a></li>
          <li><a href="/governance.html">Governance &amp; Standards</a></li>
          <li><a href="/mission.html">Mission</a></li>
        </ul>
      </div>
      <div>
        <h5>Company</h5>
        <ul>
          <li><a href="/contact.html">Partner Inquiry</a></li>
          <li><a href="/legal.html">Legal &amp; Disclosures</a></li>
          <li><a href="/governance.html#disclosure">Regulatory Disclosure</a></li>
          <li><a href="/contact.html">Registered Office</a></li>
        </ul>
      </div>
      <div>
        <h5>Contact</h5>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span class="f">Registered office<br>30 N Gould St, STE R<br>Sheridan, WY 82801<br>United States</span></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p class="small">Providence North LLC is a Wyoming limited liability company. The Faithful Business and The Science of Wellness are lines of business of Providence North LLC, operated under trade names. They are not separate legal entities and are not subsidiaries, funds or investment vehicles.</p>
      <p class="small"><strong>The Faithful Business is not a broker-dealer or investment advisor.</strong> It is not registered under Section 15(a) of the Securities Exchange Act of 1934 or under the Investment Advisers Act of 1940, and it does not effect securities transactions, hold customer funds or securities, or give investment advice. It operates as a platform under Section 4(b) of the Securities Act of 1933, a status that is conditional on each offering complying with Rule 506 of Regulation D. Listings published on The Faithful Business are advertising by the issuing company, which makes any offer in reliance on exemptions from registration under the Securities Act of 1933, including Section 4(a)(2) and Rule 506(c) of Regulation D, 17 CFR 230.506(c). That rule permits general solicitation and general advertising where every purchaser is a verified accredited investor. <a href="/legal.html">Read the full legal notice</a>.</p>
      <p class="small">Nothing on this site is an offer to sell, or a solicitation of an offer to buy, any security, and nothing on this site is investment, legal, tax or medical advice. Investments involve risk. Advertising and directory listing services provided by The Faithful Business are not investment advice, and both parties and their counsel carry out their own due diligence. Content published by The Science of Wellness is educational and is not medical advice.</p>
      <div class="copy">
        <span class="small">&copy; {YEAR} Providence North LLC. All rights reserved.</span>
        <span class="small">Registered in Wyoming, United States.</span>
      </div>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body></html>
'''

def page(fname, title, desc, body, active, page_css="", extra_js="", robots=None):
    html = head(title, desc, fname, page_css, robots=robots) + header(active) + body + footer()
    open(os.path.join(OUT, fname), "w").write(html)
    return fname

# ================================================================ INDEX
hero = f'''<section class="hero">
  <div class="hero-bg"><picture>
    <source type="image/webp" sizes="100vw" srcset="/assets/img/sky-field-760.webp 760w, /assets/img/sky-field-1280.webp 1280w, /assets/img/sky-field-2400.webp 2400w">
    <source type="image/jpeg" sizes="100vw" srcset="/assets/img/sky-field-760.jpg 760w, /assets/img/sky-field-1280.jpg 1280w, /assets/img/sky-field-2400.jpg 2400w">
    <img src="/assets/img/sky-field-1280.jpg" alt="" role="presentation" fetchpriority="high" width="2400" height="1300">
  </picture></div>
  <div class="hero-scrim" aria-hidden="true"></div>
  <div class="wrap hero-in">
    {star(64)}
    <span class="label label-gold">Private holding company</span>
    <h1 class="display">Enduring value, built on faith, capital and human wellbeing.</h1>
    <p class="lead">Providence North is a private holding company. It operates two lines of business: The Faithful Business and The Science of Wellness.</p>
    <div class="hero-pill"><span class="dot"></span>Wyoming LLC &middot; Member-funded &middot; No outside investors</div>
    <div class="hero-cta">
      <a class="btn btn-primary" href="/portfolio.html">Explore the businesses</a>
      <a class="btn btn-ghost" href="/contact.html">Partner Inquiry</a>
    </div>
  </div>
  <div class="hairline"></div>
</section>
'''

pillars = f'''<section aria-label="Company at a glance">
  <div class="pillars">
      <div class="pillar"><div class="label">Lines of Business</div><div class="k">Two</div><div class="v">Faith and health</div><div class="u">Two focused businesses, one standard</div></div>
      <div class="pillar"><div class="label">Stewardship Horizon</div><div class="k">Generational</div><div class="v">Multi decade alignment</div><div class="u">Built to be held, not flipped</div></div>
      <div class="pillar"><div class="label">Capital Structure</div><div class="k">Member-Funded</div><div class="v">No outside investors</div><div class="u">Not a fund &middot; provides capital to no one</div></div>
      <div class="pillar"><div class="label">Compliance Standard</div><div class="k">Lawful and Accurate</div><div class="v">Regulatory discipline</div><div class="u">Clean books, accurate claims</div></div>
  </div>
</section>
'''

portfolio = f'''<section class="sec" id="portfolio">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Lines of Business</span><span class="label">Within Providence North LLC &middot; Trade Names</span></div>
    <h2 class="h2" style="max-width:24ch">Two lines of business, held with patience.</h2>
    <p class="lead mt-s" style="max-width:62ch">Each business is managed on its own terms and held to the same rule: say what is true, deliver what is promised, and keep the books clean. Both are lines of business of Providence North LLC, operated under trade names.</p>

    <div class="grid2 mt-xl">
      <article class="card" id="faithful-business">
        <div class="entity-head">
          <img src="/assets/img/the-faithful-business-logo.png" alt="The Faithful Business logo">
          <div><span class="label">Line of Business I</span><h3 class="h3 mt-s">The Faithful Business</h3></div>
        </div>
        <span class="chip">Faith driven commerce &middot; Legal directory</span>
        <p class="body mt-m">A network that connects Christians with businesses, founders and professional advisers who share their convictions. We verify the founder’s identity and church membership status. We do not verify a business’s financial merit.</p>
        {feat("users","Identity-verified network","Browse businesses and professionals whose founders are active members of their local church.")}
        {feat("scale","VC Corner","Founders publish a listing and accredited investors subscribe to see it. This is an advertising and listing service. We do not recommend or give investment advice, and due diligence is carried out by both parties and their counsel.")}
        {feat("book","The Law Connect","A directory where Christian attorneys publish a listing for their own practice.")}
        <a class="tlink mt-l" href="https://www.thefaithfulbusiness.com" rel="noopener" target="_blank" style="display:inline-flex">www.thefaithfulbusiness.com {IC["arrow"]}</a>
      </article>

      <article class="card" id="science-of-wellness">
        <div class="entity-head">
          <img src="/assets/img/the-science-of-wellness-logo.png" alt="The Science of Wellness logo">
          <div><span class="label">Line of Business II</span><h3 class="h3 mt-s">The Science of Wellness</h3></div>
        </div>
        <span class="chip chip-mute">Frontier health &middot; Longevity media</span>
        <p class="body mt-m">A digital broadcast brand that translates research on metabolic health, cellular ageing and preventive medicine for a general audience.</p>
        {feat("pulse","Plain language, real studies","Coverage of peer reviewed research on metabolic health, cellular repair and healthy ageing, written for people who are not scientists.")}
        {feat("play","Documentary and short form","Long form documentaries and short form video, published on YouTube.")}
        {feat("sun","Built for a general audience","Written for ordinary viewers who want to understand their own health, not only for clinicians.")}
        <span class="chip chip-mute mt-l" style="display:inline-flex">Educational content &middot; Not medical advice</span>
      </article>
    </div>
    <p class="small mt-l">The Faithful Business and The Science of Wellness are lines of business of Providence North LLC, operated under trade names. Neither is a separate legal entity, a subsidiary, a fund or an investment vehicle.</p>
  </div>
</section>
'''

governance_teaser = f'''<section class="sec" id="governance">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Governance &amp; Standards</span></div>
    <h2 class="h2" style="max-width:26ch">The triad of Providence stewardship.</h2>
    <p class="lead mt-s" style="max-width:62ch">Providence North does not treat capital as a transaction. It stewards the two lines of business it owns so that they last, stay lawful, and serve the people who depend on them. It does not take a stake in the ventures it connects.</p>
    <div class="grid3 mt-xl">
      <div class="card">
        <span class="triad-no">I</span>
        <span class="label mt-s" style="display:block">Pillar One</span>
        <h3 class="h3 mt-s">Patient Stewardship</h3>
        <p class="body mt-s">We connect Christian founders with accredited investors and Christian advisers. There is no requirement that an accredited investor be Christian. We are a listing and connection service: we do not intermediate, we do not negotiate on anyone's behalf, and we are not a party to any deal.</p>
      </div>
      <div class="card">
        <span class="triad-no">II</span>
        <span class="label mt-s" style="display:block">Pillar Two</span>
        <h3 class="h3 mt-s">Governance</h3>
        <p class="body mt-s">Regulatory care, honest dealing and contractual integrity across both lines of business. Our listings are transparent, our agreements with participants are clear and put in writing, and we keep our own filings current and compliant in every jurisdiction where we are registered.</p>
      </div>
      <div class="card">
        <span class="triad-no">III</span>
        <span class="label mt-s" style="display:block">Pillar Three</span>
        <h3 class="h3 mt-s">Purpose and Flourishing</h3>
        <p class="body mt-s">We aim to be one of God’s many ways of answering the prayers of Christians by connecting capital to their business ventures.</p>
      </div>
    </div>
    <a class="tlink mt-l" href="/governance.html" style="display:inline-flex;margin-top:2.5rem">Read the full standard {IC["arrow"]}</a>
  </div>
</section>
'''

mission_band = f'''<section class="sec" id="mission">
  <div class="wrap">
    <div class="split">
      <div>
        <div class="eyebrow-row"><span class="label label-gold">Mission</span></div>
        <h2 class="h2">Why the company exists.</h2>
        <div class="stack mt-m">
          <p class="lead">Providence North exists to build ordinary, honest, profitable businesses that let Christians provide for their families and make an impact at their church and in God's kingdom.</p>
          <p class="body">The next big SaaS, App or Media Brand, or something much smaller like a Diner or Burger Shop. What matters is that the business is real, the work is honest, and the family behind it is provided for.</p>
          <p class="body">We verify the founder’s identity and church membership status. We do not verify a business’s financial merit. Providence North holds the business to a standard of lawful, transparent dealing.</p>
        </div>
        <a class="tlink mt-l" href="/mission.html" style="display:inline-flex;margin-top:2.2rem">Our mission in full {IC["arrow"]}</a>
      </div>
      <div class="ivory">
        <span class="label">Statement of Purpose</span>
        <p style="font-family:var(--font-display);font-size:1.5rem;line-height:1.4;margin-top:1.2rem;color:#0D0C0A">
          &ldquo;We are stewards, not owners. The two lines of business we hold are held for the people they serve, the families they employ, and the churches they strengthen. The ventures we connect are owned by their founders, not by us.&rdquo;
        </p>
        <hr class="mt-l" style="border:0;height:1px;background:rgba(13,12,10,.18);margin:1.75rem 0 1.1rem">
        <span class="label">Providence North LLC</span>
      </div>
    </div>
  </div>
</section>
'''

cta_band = f'''<section class="sec">
  <div class="wrap center">
    <span class="label label-gold">Partner Inquiry</span>
    <h2 class="h2 mt-s" style="max-width:22ch;margin-left:auto;margin-right:auto">Speak with Providence North.</h2>
    <p class="lead mt-s" style="max-width:56ch;margin-left:auto;margin-right:auto">We welcome serious enquiries from partners, suppliers, professional advisers and operators, and from investors who want to understand what we own and how we run it.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="/contact.html">Send an inquiry</a>
      <a class="btn btn-ghost" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</section>
'''

page("index.html",
     "Providence North LLC | Private holding company",
     ORG_DESCRIPTION,
     hero+pillars+portfolio+governance_teaser+mission_band+cta_band, "index.html")

# ================================================================ PORTFOLIO
def pagehead(label, h1, lead):
    return f'''<section class="page-head">
  <div class="wrap">
    <span class="label label-gold">{label}</span>
    <h1 class="display mt-s" style="max-width:22ch">{h1}</h1>
    <p class="lead mt-m" style="max-width:62ch">{lead}</p>
  </div>
</section>'''

tfb = f'''<section class="sec" id="faithful-business">
  <div class="wrap">
    <div class="entity-head">
      <img src="/assets/img/the-faithful-business-logo.png" alt="The Faithful Business logo" style="width:88px;height:88px">
      <div><span class="label label-gold">Line of Business I</span><h2 class="h2 mt-s">The Faithful Business</h2></div>
    </div>
    <p class="lead" style="max-width:66ch">A network that connects Christians with businesses, founders and professional advisers who share their convictions. We verify the founder’s identity and church membership status. We do not verify a business’s financial merit.</p>
    <div class="grid3 mt-xl">
      <div class="card">
        <span class="chip">Marketplace</span>
        <h3 class="h3 mt-m">Verified member directory</h3>
        <p class="body mt-s">Business owners and professionals list themselves in the network. Verification is limited to identity, active church membership and document completeness. We do not evaluate the financial merit, viability or investment potential of any company.</p>
      </div>
      <div class="card">
        <span class="chip">VC Corner</span>
        <h3 class="h3 mt-m">Founders list, accredited investors subscribe</h3>
        <p class="body mt-s">VC Corner is an advertising and listing service. Founders publish a listing, and accredited investors subscribe to see those listings and contact founders directly. Investors need not be Christian; the accredited standard is what governs. We do not recommend or give investment advice, and due diligence is carried out by both parties and their counsel.</p>
      </div>
      <div class="card">
        <span class="chip chip-mute">The Law Connect</span>
        <h3 class="h3 mt-m">A directory of Christian attorneys</h3>
        <p class="body mt-s">Attorneys publish a listing for their own practice. The directory is advertising, not a curated or recommended panel. Any engagement is between the attorney and the client.</p>
      </div>
    </div>
    <a class="tlink" href="https://www.thefaithfulbusiness.com" rel="noopener" target="_blank" style="display:inline-flex;margin-top:2.5rem">www.thefaithfulbusiness.com {IC["arrow"]}</a>
  </div>
</section>'''

sow = f'''<section class="sec" id="science-of-wellness">
  <div class="wrap">
    <div class="entity-head">
      <img src="/assets/img/the-science-of-wellness-logo.png" alt="The Science of Wellness logo" style="width:88px;height:88px">
      <div><span class="label label-gold">Line of Business II</span><h2 class="h2 mt-s">The Science of Wellness</h2></div>
    </div>
    <p class="lead" style="max-width:66ch">A digital broadcast brand that translates research on metabolic health, cellular ageing and preventive medicine into plain language for a general audience.</p>
    <div class="grid3 mt-xl">
      <div class="card">
        <span class="chip chip-mute">Longevity media</span>
        <h3 class="h3 mt-m">Research, translated</h3>
        <p class="body mt-s">Coverage of peer reviewed work on metabolic health, cellular repair and healthy ageing, written for people who are not scientists.</p>
      </div>
      <div class="card">
        <span class="chip chip-mute">Broadcast</span>
        <h3 class="h3 mt-m">Documentary and short form video</h3>
        <p class="body mt-s">Long form documentaries and short form video, published on YouTube. Free to watch, open to anyone.</p>
      </div>
      <div class="card">
        <span class="chip chip-mute">Standard</span>
        <h3 class="h3 mt-m">Educational only</h3>
        <p class="body mt-s">Our content is educational and is not medical advice. Viewers should consult their own physician before changing anything about their health.</p>
      </div>
    </div>
  </div>
</section>'''

what_we_are_not = f'''<section class="sec">
  <div class="wrap">
    <div class="ivory">
      <span class="label">What we are not</span>
      <div class="grid2 mt-m" style="gap:1.5rem">
        <div>
          <p style="font-size:1rem;line-height:1.7;color:#0D0C0A">Providence North is not a fund and does not take outside investment. It does not invest in or provide capital to the businesses it lists, and it is a privately held listing and directory service operator. It is not a registered broker dealer or investment adviser, and it does not offer securities. Nothing on this website is an offer to sell or a solicitation of an offer to buy any security.</p>
        </div>
        <div>
          <p style="font-size:1rem;line-height:1.7;color:#0D0C0A">Providence North is a private company with no public funding. It is a private company owned by its member, registered in the State of Wyoming, United States.</p>
        </div>
      </div>
      <p class="small mt-m" style="color:#5A5049">The Faithful Business and The Science of Wellness are lines of business of Providence North LLC, operated under trade names. They are not separate legal entities and are not subsidiaries, funds or investment vehicles.</p>
    </div>
  </div>
</section>'''

page("portfolio.html","Lines of Business | Providence North LLC",
  "The two lines of business of Providence North LLC: The Faithful Business and The Science of Wellness, operated under trade names.",
  pagehead("Lines of Business within Providence North LLC (Trade Names)","Two lines of business, held with patience.",
    "Each business is managed on its own terms and held to the same rule: say what is true, deliver what is promised, and keep the books clean. Both are lines of business of Providence North LLC, operated under trade names.")+tfb+sow+what_we_are_not,
  "portfolio.html")

# ================================================================ GOVERNANCE
gov_body = pagehead("Governance &amp; Standards","How the company is run.",
  "Providence North holds its two lines of business to one standard of dealing. The standard is written down so that it can be checked.")+f'''
<section class="sec">
  <div class="wrap">
    <div class="grid3">
      <div class="card">
        <span class="triad-no">I</span>
        <span class="label mt-s" style="display:block">Pillar One</span>
        <h3 class="h3 mt-s">Patient Stewardship</h3>
        <p class="body mt-s">We connect Christian founders with accredited investors and Christian advisers. There is no requirement that an accredited investor be Christian. We are a listing and connection service: we do not intermediate, we do not negotiate on anyone's behalf, and we are not a party to any deal.</p>
      </div>
      <div class="card">
        <span class="triad-no">II</span>
        <span class="label mt-s" style="display:block">Pillar Two</span>
        <h3 class="h3 mt-s">Governance</h3>
        <p class="body mt-s">Regulatory care, honest dealing and contractual integrity across both lines of business. Our listings are transparent, our agreements with participants are clear and put in writing, and we keep our own filings current and compliant in every jurisdiction where we are registered.</p>
        <p class="body mt-s">In practice: our listing terms are published and plainly written, our agreements with participants are documented, and we hold no position in any business we list.</p>
      </div>
      <div class="card">
        <span class="triad-no">III</span>
        <span class="label mt-s" style="display:block">Pillar Three</span>
        <h3 class="h3 mt-s">Purpose and Flourishing</h3>
        <p class="body mt-s">We aim to be one of God’s many ways of answering the prayers of Christians by connecting capital to their business ventures.</p>
        <p class="body mt-s">In practice: we favour businesses that provide real work for real families, and we judge our own service by whether those families are better off.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Operating Standards</span></div>
    <h2 class="h2" style="max-width:26ch">Five rules we hold ourselves to.</h2>
    <div class="grid2 mt-xl">
      <div class="card">{feat("shield","Say what is true","No claim about a business, a product or a result that we cannot point to in the records.")}
      {feat("scale","Written agreements","Our agreements with participants are documented, and each party keeps its own counsel where it needs one.")}</div>
      <div class="card">{feat("bank","Clean books","Accounts kept current and reconciled. Filings made on time in every jurisdiction where we are registered.")}
      {feat("compass","No outside capital","Providence North is privately funded. There is no fund, no outside investment and no investment offering.")}</div>
    </div>
    <div class="card mt-l" style="max-width:none">{feat("users","We verify the founder’s identity and church membership status","For businesses in The Faithful Business network, verification covers identity, active church membership and document completeness. It is not an endorsement, and it is not a review of the business itself.")}</div>
  </div>
</section>

<section class="sec" id="disclosure">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Disclosures</span></div>
    <h2 class="h2" style="max-width:24ch">Regulatory and legal disclosure.</h2>
    <div class="stack mt-m" style="max-width:76ch">
      <p class="body">Providence North LLC is a limited liability company registered in the State of Wyoming, United States. It is privately held by its member and has no public funding.</p>
      <p class="body">Providence North LLC is not a registered broker dealer, investment adviser, fund, or pooled investment vehicle. It does not offer, sell or solicit the purchase of any security, and it does not manage money for third parties.</p>
      <p class="body">Nothing on this website is an offer to sell, or a solicitation of an offer to buy, any security, nor is it investment, legal, tax, accounting or medical advice. Any figures, descriptions or forward looking statements on this site are general in nature and subject to change without notice.</p>
      <p class="body">The Faithful Business operates advertising and directory listing services. Verification of a business or a professional is limited to identity, active church membership and document completeness. Providence North LLC does not evaluate the financial merit, viability or investment potential of any company, does not recommend or give investment advice, and due diligence is carried out by both parties and their counsel.</p>
      <p class="body"><strong style="color:var(--bone)">The Faithful Business is not a broker dealer or an investment adviser.</strong> It is not registered under Section 15(a) of the Securities Exchange Act of 1934 or under the Investment Advisers Act of 1940, and it does not effect securities transactions, hold customer funds or securities, or give investment advice. Any offering published on The Faithful Business is made by the issuing company in reliance on exemptions from registration under the Securities Act of 1933, including Section 4(a)(2) and Rule 506(c) of Regulation D, 17 CFR 230.506(c), which permits general solicitation and general advertising where every purchaser is a verified accredited investor. Listings on The Faithful Business are advertising only.</p>
      <p class="body">Content published by The Science of Wellness is educational and is not medical advice, diagnosis or treatment. Viewers should consult a qualified physician about their own health.</p>
      <p class="body">Investments involve risk, including the risk of total loss. Any investment activity described on this site is intended only for accredited investors who qualify in their own jurisdiction.</p>
    </div>
  </div>
</section>'''

page("governance.html","Governance & Standards | Providence North LLC",
  "The stewardship standard, operating rules and regulatory disclosures of Providence North LLC.",
  gov_body, "governance.html")

# ================================================================ MISSION
mission_body = pagehead("Mission","Why the company exists.",
  "Providence North exists to build ordinary, honest, profitable businesses that let Christians provide for their families and make an impact at their church and in God's kingdom.")+f'''
<section class="sec">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="lead">The next big SaaS, App or Media Brand, or something much smaller like a Diner or Burger Shop. What matters is that the business is real, the work is honest, and the family behind it is provided for.</p>
        <p class="body">Faith in business is not a slogan and it is not a guarantee of success. It is a way of dealing with people. Pay what you agreed to pay. Do not overstate what you have. Do not hide a problem to make a sale. When you are wrong, say so and put it right.</p>
        <p class="body">That is the whole of our doctrine, and it is harder to keep than it sounds. It is also the reason we can stand by a founder for twenty years and still look a partner in the eye.</p>
      </div>
      <div class="ivory">
        <span class="label">The frame we work inside</span>
        <p style="font-family:var(--font-display);font-size:1.35rem;line-height:1.45;margin-top:1.1rem;color:#0D0C0A">We verify the founder’s identity and church membership status. We do not verify a business’s financial merit. Providence North holds the business to a standard of lawful, transparent dealing.</p>
        <p class="small" style="margin-top:1.25rem;color:#5A5049">Verification is limited to identity, active church membership and document completeness. It is not an endorsement of a business, a product or an investment.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Three audiences</span></div>
    <h2 class="h2" style="max-width:26ch">Who we build for.</h2>
    <div class="grid3 mt-xl">
      <div class="card">
        <span class="chip">Founders and families</span>
        <h3 class="h3 mt-m">People who want to build something honest</h3>
        <p class="body mt-s">If the business is real and the work is honest, we want to know about it.</p>
      </div>
      <div class="card">
        <span class="chip">Founders producing apps and SaaS</span>
        <h3 class="h3 mt-m">People shipping a product right now</h3>
        <p class="body mt-s">We serve Christian founders across every sector. Founders producing apps and SaaS, product builders and entrepreneurs launching new ventures are as welcome here as a diner or a trades business. If you are building something real and you need investors, advisers and a community behind you, we want to hear from you.</p>
      </div>
      <div class="card">
        <span class="chip">Partners and advisers</span>
        <h3 class="h3 mt-m">People who hold the same standard</h3>
        <p class="body mt-s">Attorneys, accountants, operators and suppliers who care about doing the work properly. We would rather move slowly with the right partner than quickly with the wrong one.</p>
      </div>
    </div>
  </div>
</section>'''

page("mission.html","Mission | Providence North LLC",
  "The mission and doctrine of Providence North LLC: ordinary, honest, profitable businesses that let Christians provide for their families.",
  mission_body, "mission.html")

# ================================================================ CONTACT
FORM_JS = '''<script>
document.getElementById('inquiry').addEventListener('submit',function(e){
  e.preventDefault();
  var f=e.target, g=function(n){return (f.querySelector('[name="'+n+'"]').value||'').trim();};
  var body = 'Name and title: '+g('name')+'\\nEmail: '+g('email')+'\\nOrganisation: '+g('org')+
             '\\nArea of interest: '+g('area')+'\\n\\n'+g('message')+'\\n';
  window.location.href = 'mailto:inquiries@providencenorth.one?subject='+
    encodeURIComponent('Partner Inquiry - '+g('org'))+'&body='+encodeURIComponent(body);
  document.getElementById('sent').style.display='block';
  document.getElementById('sent').scrollIntoView({block:'nearest'});
});
</script>'''

contact_body = pagehead("Partner Inquiry","Speak with Providence North.",
  "We read every message. Expect a reply within five business days.")+f'''
<section class="sec">
  <div class="wrap">
    <div class="split">
      <div>
        <form id="inquiry" novalidate>
          <div class="field"><label class="label" for="f-name">Name and title</label>
            <input id="f-name" name="name" type="text" placeholder="Your full name and title" required></div>
          <div class="field"><label class="label" for="f-email">Email</label>
            <input id="f-email" name="email" type="email" placeholder="name@organisation.com" required></div>
          <div class="field"><label class="label" for="f-org">Organisation</label>
            <input id="f-org" name="org" type="text" placeholder="Company or firm"></div>
          <div class="field"><label class="label" for="f-area">Area of interest</label>
            <select id="f-area" name="area">
              <option>The Faithful Business</option>
              <option>The Science of Wellness</option>
              <option>Supplying or partnering with a Providence North company</option>
              <option>Professional services</option>
              <option>Media or press</option>
              <option>Something else</option>
            </select></div>
          <div class="field"><label class="label" for="f-msg">Message</label>
            <textarea id="f-msg" name="message" placeholder="Tell us briefly what you need and the timescale."></textarea></div>
          <button class="btn btn-primary" type="submit">Send an inquiry</button>
          <p class="small mt-m">This form opens your own email application with the details filled in, so that nothing is transmitted through this website.</p>
          <div id="sent" style="display:none" class="card mt-m">
            <span class="label label-gold">Ready to send</span>
            <p class="body mt-s">Your email application should now be open with the message prepared. If it did not open, write to <a href="mailto:{EMAIL}" style="color:var(--gold)">{EMAIL}</a> directly.</p>
          </div>
        </form>
      </div>
      <div>
        <div class="card">
          <span class="label">Email</span>
          <p class="mt-s" style="display:flex;gap:.7rem;align-items:flex-start">{IC["mail"]}<a href="mailto:{EMAIL}" style="color:var(--ivory);font-size:.9375rem">{EMAIL}</a></p>
        </div>
        <div class="card mt-m">
          <span class="label">Registered office</span>
          <p class="mt-s" style="display:flex;gap:.7rem;align-items:flex-start">{IC["pin"]}<span class="body" style="color:var(--bone)">Providence North LLC<br>30 N Gould St, STE R<br>Sheridan, WY 82801<br>United States</span></p>
          <p class="small mt-s">Mail sent to the registered office is received and forwarded.</p>
        </div>
        <div class="card mt-m">
          <span class="label">What we cannot help with</span>
          <p class="small mt-s">We are not a broker dealer or investment adviser and do not offer securities. We do not give investment, legal, tax or medical advice, and we do not respond to investment solicitations.</p>
        </div>
      </div>
    </div>
  </div>
</section>
'''+FORM_JS

page("contact.html","Partner Inquiry | Providence North LLC",
  "Contact Providence North LLC at inquiries@providencenorth.one. Registered office in Sheridan, Wyoming, United States.",
  contact_body, "contact.html")

# ================================================================ LEGAL
legal_body = pagehead("Legal &amp; Disclosures","Legal notice.",
  "Company status, regulatory position and the terms on which this website is published.")+f'''
<section class="sec">
  <div class="wrap wrap-narrow">
    <div class="stack">

      <h2 class="h2">The company</h2>
      <p class="body">Providence North LLC is a limited liability company registered in the State of Wyoming, United States. Its registered office is 30 N Gould St, STE R, Sheridan, WY 82801, United States. The company is privately held by its member and has no public funding.</p>

      <h2 class="h2 mt-xl">Lines of business and trade names</h2>
      <p class="body">The Faithful Business and The Science of Wellness are lines of business of Providence North LLC, operated under trade names. They are not separate legal entities. They are not subsidiaries, partnerships, funds, pooled investment vehicles or joint ventures, and they do not have their own directors, officers or members. Obligations arising in either line of business are obligations of Providence North LLC.</p>

      <h2 class="h2 mt-xl">Securities and regulatory position</h2>
      <p class="body"><strong style="color:var(--bone)">The Faithful Business is not a broker dealer or an investment adviser.</strong> It is not registered under Section 15(a) of the Securities Exchange Act of 1934 or under the Investment Advisers Act of 1940. It does not effect or execute securities transactions, does not hold or custody customer funds or securities, does not negotiate the terms of any transaction between a founder and an investor, and does not give investment advice of any kind.</p>
      <p class="body">Any offering published on The Faithful Business is made by the issuing company itself, and not by Providence North LLC or by any of its lines of business. Those offerings are made in reliance on exemptions from registration under the Securities Act of 1933, as amended, including Section 4(a)(2) and Rule 506(c) of Regulation D, 17 CFR 230.506(c). Rule 506(c) permits general solicitation and general advertising where every purchaser is a verified accredited investor. Offers made under that rule are securities that are subject to transfer restrictions, and investors must satisfy applicable eligibility and verification requirements in the jurisdiction where they qualify.</p>
      <p class="body">Providence North LLC is not a registered broker dealer, investment adviser, fund or pooled investment vehicle. It does not offer, sell or solicit the purchase of any security, does not manage money for any third party and does not take outside investment.</p>

      <h3 class="h3 mt-l">Basis of the platform position</h3>
      <p class="body">The Faithful Business operates as a platform. Its regulatory position rests on Section 4(b) of the Securities Act of 1933, 15 U.S.C. 77d(b), which was added by Title II of the JOBS Act. That section provides that a person who satisfies its conditions is not required to register as a broker under Section 15(a)(1) of the Securities Exchange Act of 1934 solely because of defined platform activity carried out in connection with an offering made under Rule 506 of Regulation D.</p>
      <p class="body">The exemption is self-executing. It requires no application, filing or approval by the Securities and Exchange Commission, and no registration. It is also conditional, and it is narrow. It applies only where the offering itself complies with Rule 506; where neither the platform nor any associated person receives compensation in connection with the purchase or sale of a security; and where neither the platform nor any associated person is subject to statutory disqualification under Section 3(a)(39) of the Securities Exchange Act of 1934. If those conditions are not met for a given offering, the platform position does not apply to that offering.</p>
      <p class="body">Accordingly, The Faithful Business charges a flat subscription fee for advertising and listing services only. It takes no success fee, commission, carried interest, referral fee or other transaction-based compensation from any offering, and no fee that varies with the size of an offering or with whether a transaction closes. It does not negotiate the terms of any transaction, does not handle or hold investor funds or securities, does not sponsor or manage any investment vehicle, and does not give investment advice or recommend any offering. It does not curate, rank, score or selectively promote issuers. A listing appears because the issuer published it.</p>
      <p class="body">Compliance with Rule 506, including the reasonable steps required to verify that every purchaser is an accredited investor, remains the responsibility of the issuing company making the offering. That verification may be performed through an independent third-party verification service, but the legal burden of it is not assumed by Providence North LLC or by The Faithful Business. Investors are responsible for confirming that they qualify in their own jurisdiction.</p>

      <h2 class="h2 mt-xl">Advertising and listing services</h2>
      <p class="body">VC Corner is an advertising and listing service. Founders publish a listing describing their own business, and accredited investors subscribe to see those listings and to contact founders directly. Investors need not be Christian; the accredited standard is what governs. A listing is advertising. It is not a recommendation, an endorsement, a valuation or an offer. Providence North LLC does not evaluate the financial merit, viability or investment potential of any company. Due diligence is carried out by both parties and their counsel.</p>
      <p class="body">The Law Connect is a directory in which attorneys publish a listing for their own practice. The directory is advertising. It is not a curated or recommended panel, it is not a lawyer referral service, and nothing in it is legal advice. Any engagement is between the attorney and the client.</p>
      <p class="body">Verification of a business, founder or professional is limited to identity, active church membership and document completeness. It is not an endorsement of a business, a product or an investment, and it is not a review of the business itself.</p>

      <h2 class="h2 mt-xl">Health content</h2>
      <p class="body">Content published by The Science of Wellness is educational and is not medical advice, diagnosis or treatment. It is written for a general audience and is not a substitute for care from a qualified physician. Viewers should consult their own physician before making any change to their health, medication or diet.</p>

      <h2 class="h2 mt-xl">No offer, no advice</h2>
      <p class="body">Nothing on this website is an offer to sell, or a solicitation of an offer to buy, any security, nor is anything on this website investment, legal, tax, accounting or medical advice. Any figures, descriptions, statements of intent or forward looking statements on this site are general in nature, are not commitments and are subject to change without notice. Investments involve risk, including the risk of total loss. Any investment activity referred to on this site is intended only for accredited investors, and each investor must also qualify under the law of their own jurisdiction.</p>

      <h2 class="h2 mt-xl">Contact</h2>
      <p class="body">Questions about this notice, or about the status of any business named on this site, may be addressed to <a href="mailto:{EMAIL}" style="color:var(--gold)">{EMAIL}</a>.</p>

      <p class="small mt-xl">Last updated {MONTH}. This page is the full legal notice referred to in the footer of every page of this website.</p>
    </div>
  </div>
</section>'''

page("legal.html","Legal & Disclosures | Providence North LLC",
  "Legal notice for Providence North LLC: company status, lines of business and trade names, securities and regulatory position, advertising services and disclaimers.",
  legal_body, "legal.html")

# ================================================================ 404
notfound = f'''<section class="page-head">
  <div class="wrap center">
    {star(56)}
    <span class="label label-gold">404</span>
    <h1 class="display mt-s">That page is not here.</h1>
    <p class="lead mt-m" style="max-width:46ch;margin-left:auto;margin-right:auto">The link may be old or mistyped. Use the navigation above, or start from the overview.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="/">Back to the overview</a>
    <a class="btn btn-ghost" href="/contact.html">Contact us</a></div>
  </div>
</section>'''
page("404.html","Page not found | Providence North LLC","That page is not here.", notfound, "",
     robots="noindex, follow")

# ================================================================ static files
# Indexable HTML only. 404 is noindex and is omitted.
INDEXABLE = [
    ("index.html", "1.0"),
    ("portfolio.html", "0.8"),
    ("governance.html", "0.8"),
    ("mission.html", "0.8"),
    ("contact.html", "0.7"),
    ("legal.html", "0.4"),
]

def sitemap_xml():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for fname, priority in INDEXABLE:
        lines += [
            "  <url>",
            f"    <loc>{canonical_url(fname)}</loc>",
            f"    <lastmod>{SITEMAP_LASTMOD}</lastmod>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"

ROBOTS = f"""# Canonical host: {BASE}/
# www.{DOMAIN} permanently redirects (301) to the apex.
# One sitemap covers the site; do not submit a separate www sitemap.
User-agent: *
Allow: /

# Plain-text summaries for AI crawlers (see https://llmstxt.org):
# {BASE}/llms.txt
# {BASE}/llms-full.txt

Sitemap: {BASE}/sitemap.xml
"""

LLMS = f"""# Providence North LLC

> {ORG_DESCRIPTION}

Providence North LLC is a limited liability company registered in the State of Wyoming, United States. It is privately held by its member, member-funded, and has no outside investors and no public funding. It is a private holding company with two lines of business, operated under trade names: The Faithful Business and The Science of Wellness. Those lines of business are not separate legal entities, and they are not subsidiaries, funds, or investment vehicles.

This website is published by that Wyoming company. Canonical host: {BASE}/ . www.{DOMAIN} permanently redirects (301) to the apex.

## Lines of business

- [The Faithful Business](https://www.thefaithfulbusiness.com): A network that connects Christians with businesses, founders, and professional advisers who share their convictions. Verification is limited to founder identity, active church membership, and document completeness. It does not verify a business’s financial merit. VC Corner is an advertising and listing service: founders publish a listing, and accredited investors subscribe to see it. The Law Connect is a directory where Christian attorneys publish a listing for their own practice. The Faithful Business is not a broker-dealer or an investment adviser. It does not effect securities transactions, hold customer funds or securities, or give investment advice. Listings are advertising by the issuing company.
- The Science of Wellness: A digital broadcast brand that translates research on metabolic health, cellular ageing, and preventive medicine for a general audience. Documentary and short-form video are published on YouTube. This site does not publish a separate URL for The Science of Wellness. Its content is educational and is not medical advice.

## What this company is not

- Not a fund, and it does not take outside investment. It does not invest in or provide capital to the businesses it lists.
- Not a registered broker-dealer, investment adviser, fund, or pooled investment vehicle. It does not offer, sell, or solicit the purchase of any security, and it does not manage money for third parties.
- Nothing on this site is an offer to sell, or a solicitation of an offer to buy, any security, and nothing on this site is investment, legal, tax, or medical advice.
- Not a Florida D&B entity, not California nursing homes, and not Tennessee townhomes.

## Key pages

- [Overview]({BASE}/): Holding company overview.
- [Lines of business]({BASE}/portfolio.html): The Faithful Business and The Science of Wellness.
- [Governance and standards]({BASE}/governance.html): Stewardship standard, operating rules, and regulatory disclosures.
- [Mission]({BASE}/mission.html): Why the company exists.
- [Partner inquiry]({BASE}/contact.html): Inquiry form, email, and registered office.
- [Legal notice]({BASE}/legal.html): Controlling legal notice for company status, securities position, advertising services, and disclaimers.
- [Extended summary]({BASE}/llms-full.txt): Longer plain-text summary for AI crawlers.

## Contact

- Email: {EMAIL}
- Registered office: Providence North LLC, 30 N Gould St, STE R, Sheridan, WY 82801, United States
"""

LLMS_FULL = f"""# Providence North LLC

> {ORG_DESCRIPTION}

This file restates facts already published on {BASE}/ . The controlling legal notice is {BASE}/legal.html . Do not treat this summary as an offer, a solicitation, or advice.

## Identity

Providence North LLC is a limited liability company registered in the State of Wyoming, United States. Registered office: 30 N Gould St, STE R, Sheridan, WY 82801, United States. The company is privately held by its member and has no public funding. It is member-funded and has no outside investors.

Canonical website: {BASE}/
www.{DOMAIN} permanently redirects (301) to that apex. Do not cite a www URL as canonical.

The Faithful Business and The Science of Wellness are lines of business of Providence North LLC, operated under trade names. They are not separate legal entities. They are not subsidiaries, partnerships, funds, pooled investment vehicles, or joint ventures, and they do not have their own directors, officers, or members. Obligations arising in either line of business are obligations of Providence North LLC.

There are no public social-profile URLs on this site. Do not invent any.

## The Faithful Business

Public site: https://www.thefaithfulbusiness.com

A network that connects Christians with businesses, founders, and professional advisers who share their convictions. Providence North verifies the founder’s identity and church membership status. It does not verify a business’s financial merit. Verification covers identity, active church membership, and document completeness. It is not an endorsement, and it is not a review of the business itself.

Three published services:

- Verified member directory. Business owners and professionals list themselves. Verification is limited to identity, active church membership, and document completeness.
- VC Corner. An advertising and listing service. Founders publish a listing, and accredited investors subscribe to see those listings and contact founders directly. Investors need not be Christian. Providence North does not recommend or give investment advice. Due diligence is carried out by both parties and their counsel.
- The Law Connect. A directory where attorneys publish a listing for their own practice. The directory is advertising, not a curated or recommended panel, and not a lawyer referral service. Any engagement is between the attorney and the client.

The Faithful Business is not a broker-dealer or an investment adviser. It is not registered under Section 15(a) of the Securities Exchange Act of 1934 or under the Investment Advisers Act of 1940. It does not effect or execute securities transactions, does not hold or custody customer funds or securities, does not negotiate the terms of any transaction between a founder and an investor, and does not give investment advice.

It operates as a platform under Section 4(b) of the Securities Act of 1933, a status that is conditional on each offering complying with Rule 506 of Regulation D. Any offering published on The Faithful Business is made by the issuing company, not by Providence North LLC. Listings are advertising only. Compliance with Rule 506, including verification that every purchaser is an accredited investor, remains the responsibility of the issuing company.

## The Science of Wellness

No separate official URL is published on this site. Do not invent one.

A digital broadcast brand that translates research on metabolic health, cellular ageing, and preventive medicine into plain language for a general audience. Coverage includes peer-reviewed work on metabolic health, cellular repair, and healthy ageing. Long-form documentaries and short-form video are published on YouTube. This site does not name a channel URL.

Content is educational and is not medical advice, diagnosis, or treatment. It is not a substitute for care from a qualified physician.

## What Providence North is not

- Not a fund. It does not take outside investment, does not invest in or provide capital to the businesses it lists, and provides capital to no one.
- Not a registered broker-dealer, investment adviser, fund, or pooled investment vehicle.
- It does not offer, sell, or solicit the purchase of any security, and it does not manage money for third parties.
- Nothing on providencenorth.one is an offer to sell, or a solicitation of an offer to buy, any security.
- Nothing on this site is investment, legal, tax, accounting, or medical advice.
- Not a Florida D&B entity.
- Not California nursing homes.
- Not Tennessee townhomes.

## How the company describes its standard

Providence North states three stewardship pillars: patient stewardship, governance, and purpose and flourishing. It describes itself as a listing and connection service: it does not intermediate, does not negotiate on anyone’s behalf, and is not a party to any deal. Operating rules published on the site include saying what is true, written agreements, clean books, no outside capital, and identity-and-membership verification that is not an endorsement.

## Contact

- Partner inquiries: {EMAIL}
- The contact form opens the visitor’s own email application. Nothing is transmitted through the website.
- Registered office: Providence North LLC, 30 N Gould St, STE R, Sheridan, WY 82801, United States. Mail sent to the registered office is received and forwarded.
- The company states that it does not respond to investment solicitations, and that it does not give investment, legal, tax, or medical advice.

## Key URLs

- {BASE}/
- {BASE}/portfolio.html
- {BASE}/governance.html
- {BASE}/mission.html
- {BASE}/contact.html
- {BASE}/legal.html
- {BASE}/llms.txt
- https://www.thefaithfulbusiness.com
"""

open(os.path.join(OUT,"CNAME"),"w").write(DOMAIN+"\n")
open(os.path.join(OUT,".nojekyll"),"w").write("")
open(os.path.join(OUT,"robots.txt"),"w").write(ROBOTS)
open(os.path.join(OUT,"sitemap.xml"),"w").write(sitemap_xml())
open(os.path.join(OUT,"llms.txt"),"w").write(LLMS)
open(os.path.join(OUT,"llms-full.txt"),"w").write(LLMS_FULL)

open(os.path.join(OUT,"assets/js/main.js"),"w").write('''(function(){
  var b=document.getElementById('burger'), m=document.getElementById('mnav');
  if(!b||!m) return;
  b.addEventListener('click',function(){
    var open=m.classList.toggle('open');
    b.setAttribute('aria-expanded', open?'true':'false');
  });
  m.addEventListener('click',function(e){ if(e.target.tagName==='A'){ m.classList.remove('open'); b.setAttribute('aria-expanded','false'); }});
})();
''')

def verify_build():
    import xml.etree.ElementTree as ET

    def read(name):
        with open(os.path.join(OUT, name), encoding="utf-8") as fh:
            return fh.read()

    def graph(html):
        raw = html.split('<script type="application/ld+json">', 1)[1].split("</script>", 1)[0]
        return json.loads(raw)

    idx = read("index.html")
    assert 'rel="canonical" href="https://providencenorth.one/"' in idx
    assert 'property="og:url" content="https://providencenorth.one/"' in idx
    assert "providencenorth.one/index.html" not in idx
    assert 'href="/index.html"' not in idx
    assert 'content="https://providencenorth.one/og-image.jpg"' in idx
    assert os.path.isfile(os.path.join(OUT, "og-image.jpg"))
    home = graph(idx)
    assert [n["@type"] for n in home["@graph"]] == ["Organization", "WebSite", "WebPage"]
    org = home["@graph"][0]
    assert org["@id"] == ORG_ID
    assert org["legalName"] == "Providence North LLC"
    assert org["url"] == BASE
    assert org["description"] == ORG_DESCRIPTION
    assert "sameAs" not in org
    assert org["address"]["streetAddress"] == "30 N Gould St, STE R"
    assert org["address"]["addressRegion"] == "WY"
    assert org["subOrganization"][0]["url"] == "https://www.thefaithfulbusiness.com"
    assert "url" not in org["subOrganization"][1]
    assert org["subOrganization"][1]["name"] == "The Science of Wellness"
    site = home["@graph"][1]
    assert site["@id"] == SITE_ID
    assert site["url"] == f"{BASE}/"
    assert site["publisher"] == {"@id": ORG_ID}
    assert "potentialAction" not in site
    assert "SearchAction" not in idx
    page_node = home["@graph"][2]
    assert page_node["url"] == f"{BASE}/"
    assert page_node["isPartOf"] == {"@id": SITE_ID}
    assert page_node["about"] == {"@id": ORG_ID}
    assert page_node["description"] == ORG_DESCRIPTION

    for fname, _prio in INDEXABLE:
        if fname == "index.html":
            continue
        html = read(fname)
        url = canonical_url(fname)
        assert f'rel="canonical" href="{url}"' in html
        assert f'property="og:url" content="{url}"' in html
        assert 'href="/index.html"' not in html
        data = graph(html)
        types = [n["@type"] for n in data["@graph"]]
        assert "WebSite" not in types
        assert data["@graph"][0]["legalName"] == "Providence North LLC"
        assert data["@graph"][0]["url"] == BASE
        assert data["@graph"][-1]["url"] == url
        assert data["@graph"][-1]["name"]
        assert data["@graph"][-1]["description"]
        assert 'lang="en"' in html

    contact = graph(read("contact.html"))
    assert contact["@graph"][-1]["@type"] == "ContactPage"
    assert contact["@graph"][0]["contactPoint"]["email"] == EMAIL

    nf = read("404.html")
    assert 'name="robots" content="noindex, follow"' in nf
    assert 'href="/index.html"' not in nf

    sm = read("sitemap.xml")
    ET.fromstring(sm)
    assert sm.count("<loc>") == len(INDEXABLE)
    assert f"<loc>{BASE}/</loc>" in sm
    assert "index.html" not in sm
    assert "404" not in sm
    assert sm.count(f"<lastmod>{SITEMAP_LASTMOD}</lastmod>") == len(INDEXABLE)

    robots = read("robots.txt")
    assert "Allow: /" in robots
    assert f"Sitemap: {BASE}/sitemap.xml" in robots
    assert f"{BASE}/llms.txt" in robots

    llms = read("llms.txt")
    for needle in (
        "Wyoming",
        "The Faithful Business",
        "The Science of Wellness",
        "not a fund",
        "Florida D&B entity",
        "California nursing homes",
        "Tennessee townhomes",
        "not medical advice",
        EMAIL,
        "30 N Gould St, STE R",
        "https://www.thefaithfulbusiness.com",
        f"{BASE}/",
    ):
        assert needle.lower() in llms.lower(), needle
    assert "youtube.com" not in llms.lower()
    assert "linkedin.com" not in llms.lower()
    full = read("llms-full.txt")
    assert "Section 4(b)" in full
    assert "not medical advice" in full
    assert "Florida D&B entity" in full

verify_build()
print("pages:", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith('.html'))))
