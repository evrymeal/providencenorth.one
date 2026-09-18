#!/usr/bin/env python3
# Providence North LLC static site generator.
# Emits the HTML pages from one template so the header/footer never drift.
# Brand tokens live in assets/css/main.css.
import os, datetime, hashlib

DOMAIN = "providencenorth.one"
BASE   = f"https://{DOMAIN}"
EMAIL  = "inquiries@providencenorth.one"
YEAR   = 2026
OUT    = os.path.dirname(os.path.abspath(__file__))

# Cache-busting stamp: the stylesheet URL changes whenever the CSS changes, so a
# returning visitor never gets a stale stylesheet after a deploy.
_css_path = os.path.join(OUT, "assets", "css", "main.css")
CSS_V = hashlib.sha256(open(_css_path, "rb").read()).hexdigest()[:8]

NAV = [("index.html","Overview"),("portfolio.html","Portfolio"),
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

def head(page_title, desc, canonical, page_css=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}/{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Providence North LLC">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}/{canonical}">
<meta property="og:image" content="{BASE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0D0C0A">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/bodoni-moda-latin-400_700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/manrope-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/main.css?v={CSS_V}">
{page_css}<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Providence North LLC","url":"{BASE}","logo":"{BASE}/assets/img/providence-north-logo.png","email":"{EMAIL}","address":{{"@type":"PostalAddress","streetAddress":"30 N Gould St, STE R","addressLocality":"Sheridan","addressRegion":"WY","postalCode":"82801","addressCountry":"US"}},"subOrganization":[{{"@type":"Organization","name":"The Faithful Business","url":"https://www.thefaithfulbusiness.com"}},{{"@type":"Organization","name":"The Science of Wellness"}}]}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(active):
    links = "".join(
        f'<a href="/{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a>' for h,t in NAV)
    mlinks = "".join(
        f'<a href="/{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a>' for h,t in NAV)
    return f'''<header class="hdr">
  <div class="wrap hdr-in">
    <a class="brand" href="/" aria-label="Providence North LLC, home">
      <img class="brand-mark" src="/assets/img/brand-mark@2x.png" alt="" width="40" height="40">
      <span class="brand-txt">
        <span class="brand-name">Providence North</span>
        <span class="brand-sub">Holdings Group</span>
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
          <img src="/assets/img/brand-mark@2x.png" alt="" width="44" height="44">
          <span class="n">Providence<br>North LLC</span>
        </div>
        <p class="body" style="max-width:34ch">A private holding company. Long horizon stewardship of two operating businesses in faith driven commerce and health media.</p>
      </div>
      <div>
        <h5>Portfolio</h5>
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
          <li><a href="/governance.html#disclosure">Disclosures</a></li>
          <li><a href="/contact.html">Registered Office</a></li>
        </ul>
      </div>
      <div>
        <h5>Contact</h5>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span class="f">Registered office<br>30 N Gould St, STE R<br>Sheridan, WY 82801<br>United States</span></li>
          <li><span class="f">Operations<br>Bangkok, Thailand</span></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p class="small">Providence North LLC is a Wyoming limited liability company. This website is published for general information about the company and the businesses it operates. Nothing on this site is an offer to sell, or a solicitation of an offer to buy, any security, and nothing on this site is investment, legal, tax or medical advice. Providence North LLC is not a registered broker dealer or investment adviser. Investments involve risk. Advertising and directory listing services provided by The Faithful Business are not investment advice, and both parties and their counsel carry out their own due diligence. Content published by The Science of Wellness is educational and is not medical advice.</p>
      <div class="copy">
        <span class="small">&copy; {YEAR} Providence North LLC. All rights reserved.</span>
        <span class="small">Registered in Wyoming, United States. Operating from Bangkok, Thailand.</span>
      </div>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body></html>
'''

def page(fname, title, desc, body, active, page_css="", extra_js=""):
    html = head(title, desc, fname, page_css) + header(active) + body + footer()
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
    <p class="lead">Providence North is a private holding company. It owns and operates The Faithful Business and The Science of Wellness.</p>
    <div class="hero-pill"><span class="dot"></span>Wyoming LLC &middot; No outside LP capital</div>
    <div class="hero-cta">
      <a class="btn btn-primary" href="/portfolio.html">Explore the portfolio</a>
      <a class="btn btn-ghost" href="/contact.html">Partner Inquiry</a>
    </div>
  </div>
  <div class="hairline"></div>
</section>
'''

pillars = f'''<section aria-label="Company at a glance">
  <div class="pillars">
      <div class="pillar"><div class="label">Operating Companies</div><div class="k">Two</div><div class="v">Faith and health</div><div class="u">Two focused businesses, one standard</div></div>
      <div class="pillar"><div class="label">Stewardship Horizon</div><div class="k">Generational</div><div class="v">Multi decade alignment</div><div class="u">Built to be held, not flipped</div></div>
      <div class="pillar"><div class="label">Capital Structure</div><div class="k">Privately Funded</div><div class="v">No outside LP capital</div><div class="u">No fund, no outside partners</div></div>
      <div class="pillar"><div class="label">Ethical Mandate</div><div class="k">Biblical and Scientific</div><div class="v">Fiduciary discipline</div><div class="u">Honest books, honest claims</div></div>
  </div>
</section>
'''

portfolio = f'''<section class="sec" id="portfolio">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Portfolio</span></div>
    <h2 class="h2" style="max-width:24ch">Two operating companies, held with patience.</h2>
    <p class="lead mt-s" style="max-width:62ch">Each business is managed on its own terms and held to the same rule: say what is true, deliver what is promised, and keep the books clean.</p>

    <div class="grid2 mt-xl">
      <article class="card" id="faithful-business">
        <div class="entity-head">
          <img src="/assets/img/the-faithful-business-logo.png" alt="The Faithful Business logo">
          <div><span class="label">Operating Company I</span><h3 class="h3 mt-s">The Faithful Business</h3></div>
        </div>
        <span class="chip">Faith driven commerce &middot; Legal directory</span>
        <p class="body mt-m">A network that connects Christians with businesses, founders and professional advisers who share their convictions. The church verifies the founder, not the entity.</p>
        {feat("users","Faith verified marketplace","Browse businesses and professionals whose founders are active members of their local church.")}
        {feat("scale","VC Corner","Founders publish a listing and accredited investors subscribe to see it. This is an advertising and listing service. We do not recommend or give investment advice, and due diligence is carried out by both parties and their counsel.")}
        {feat("book","The Law Connect","A directory where Christian attorneys publish a listing for their own practice.")}
        <a class="tlink mt-l" href="https://www.thefaithfulbusiness.com" rel="noopener" target="_blank" style="display:inline-flex">www.thefaithfulbusiness.com {IC["arrow"]}</a>
      </article>

      <article class="card" id="science-of-wellness">
        <div class="entity-head">
          <img src="/assets/img/the-science-of-wellness-logo.png" alt="The Science of Wellness logo">
          <div><span class="label">Operating Company II</span><h3 class="h3 mt-s">The Science of Wellness</h3></div>
        </div>
        <span class="chip chip-mute">Frontier health &middot; Longevity media</span>
        <p class="body mt-m">A digital broadcast brand that translates research on metabolic health, cellular ageing and preventive medicine for a general audience.</p>
        {feat("pulse","Plain language, real studies","Coverage of peer reviewed research on metabolic health, cellular repair and healthy ageing, written for people who are not scientists.")}
        {feat("play","Documentary and short form","Long form documentaries and short form video, published on YouTube.")}
        {feat("sun","Built for a general audience","Written for ordinary viewers who want to understand their own health, not only for clinicians.")}
        <span class="chip chip-mute mt-l" style="display:inline-flex">Educational content &middot; Not medical advice</span>
      </article>
    </div>
  </div>
</section>
'''

governance_teaser = f'''<section class="sec" id="governance">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Governance &amp; Standards</span></div>
    <h2 class="h2" style="max-width:26ch">The triad of Providence stewardship.</h2>
    <p class="lead mt-s" style="max-width:62ch">Providence North does not treat capital as a transaction. It stewards the businesses it owns so that they last, stay lawful, and serve the people who depend on them.</p>
    <div class="grid3 mt-xl">
      <div class="card">
        <span class="triad-no">I</span>
        <span class="label mt-s" style="display:block">Pillar One</span>
        <h3 class="h3 mt-s">Patient Stewardship</h3>
        <p class="body mt-s">Long horizon capital preservation anchored in balance sheet patience. We decline short cycle speculation in favour of compounding structural value alongside honest enterprises.</p>
      </div>
      <div class="card">
        <span class="triad-no">II</span>
        <span class="label mt-s" style="display:block">Pillar Two</span>
        <h3 class="h3 mt-s">Governance</h3>
        <p class="body mt-s">Regulatory care and contractual integrity across both operating companies. Statutory conformity and continuous legal oversight underwrite every partnership we form.</p>
      </div>
      <div class="card">
        <span class="triad-no">III</span>
        <span class="label mt-s" style="display:block">Pillar Three</span>
        <h3 class="h3 mt-s">Purpose and Flourishing</h3>
        <p class="body mt-s">Commitment to the spiritual vitality and physical wellbeing of the people our companies serve. We back ordinary ventures that honour God and help families thrive.</p>
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
          <p class="body">A diner, a burger shop, a media brand, or something much larger. The size is not the point. What matters is that the business is real, the work is honest, and the family behind it is provided for.</p>
          <p class="body">The church verifies the founder. Providence North holds the business to a standard of lawful, transparent dealing.</p>
        </div>
        <a class="tlink mt-l" href="/mission.html" style="display:inline-flex;margin-top:2.2rem">Our mission in full {IC["arrow"]}</a>
      </div>
      <div class="ivory">
        <span class="label">Statement of Purpose</span>
        <p style="font-family:var(--font-display);font-size:1.5rem;line-height:1.4;margin-top:1.2rem;color:#0D0C0A">
          &ldquo;We are stewards, not owners. The businesses are held for the people they serve, the families they employ, and the churches they strengthen.&rdquo;
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
     "Providence North LLC is a private Wyoming holding company operating The Faithful Business and The Science of Wellness.",
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
      <div><span class="label label-gold">Operating Company I</span><h2 class="h2 mt-s">The Faithful Business</h2></div>
    </div>
    <p class="lead" style="max-width:66ch">A network that connects Christians with businesses, founders and professional advisers who share their convictions. The church verifies the founder, not the entity.</p>
    <div class="grid3 mt-xl">
      <div class="card">
        <span class="chip">Marketplace</span>
        <h3 class="h3 mt-m">Faith verified businesses and professionals</h3>
        <p class="body mt-s">Business owners and professionals list themselves in the network. Verification is limited to identity, active church membership and document completeness. We do not evaluate the financial merit, viability or investment potential of any company.</p>
      </div>
      <div class="card">
        <span class="chip">VC Corner</span>
        <h3 class="h3 mt-m">Founders list, accredited investors subscribe</h3>
        <p class="body mt-s">VC Corner is an advertising and listing service. Founders publish a listing, and accredited investors subscribe to see those listings and contact founders directly. We do not recommend or give investment advice, and due diligence is carried out by both parties and their counsel.</p>
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
      <div><span class="label label-gold">Operating Company II</span><h2 class="h2 mt-s">The Science of Wellness</h2></div>
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
          <p style="font-size:1rem;line-height:1.7;color:#0D0C0A">Providence North is not a fund and does not take outside limited partner capital. It is not a registered broker dealer or investment adviser, and it does not offer securities. Nothing on this website is an offer to sell or a solicitation of an offer to buy any security.</p>
        </div>
        <div>
          <p style="font-size:1rem;line-height:1.7;color:#0D0C0A">Providence North is not affiliated with any government, sovereign body or state investment vehicle. It is a private company owned by its member, registered in Wyoming and operating from Bangkok, Thailand.</p>
        </div>
      </div>
    </div>
  </div>
</section>'''

page("portfolio.html","Portfolio | Providence North LLC",
  "The two operating companies of Providence North LLC: The Faithful Business and The Science of Wellness.",
  pagehead("Portfolio","Two operating companies, held with patience.",
    "Each business is managed on its own terms and held to the same rule: say what is true, deliver what is promised, and keep the books clean.")+tfb+sow+what_we_are_not,
  "portfolio.html")

# ================================================================ GOVERNANCE
gov_body = pagehead("Governance &amp; Standards","How the company is run.",
  "Providence North holds two operating businesses to one standard of dealing. The standard is written down so that it can be checked.")+f'''
<section class="sec">
  <div class="wrap">
    <div class="grid3">
      <div class="card">
        <span class="triad-no">I</span>
        <span class="label mt-s" style="display:block">Pillar One</span>
        <h3 class="h3 mt-s">Patient Stewardship</h3>
        <p class="body mt-s">Long horizon capital preservation anchored in balance sheet patience. We decline short cycle speculation in favour of compounding structural value alongside honest enterprises.</p>
        <p class="body mt-s">In practice: no leverage taken against the operating companies, no growth bought with borrowed money, and no sale of a business simply because a buyer appears.</p>
      </div>
      <div class="card">
        <span class="triad-no">II</span>
        <span class="label mt-s" style="display:block">Pillar Two</span>
        <h3 class="h3 mt-s">Governance</h3>
        <p class="body mt-s">Regulatory care and contractual integrity across both operating companies. Statutory conformity and continuous legal oversight underwrite every partnership we form.</p>
        <p class="body mt-s">In practice: written agreements for every material dealing, counsel retained on retainer, and statutory filings kept current in every jurisdiction where we are registered.</p>
      </div>
      <div class="card">
        <span class="triad-no">III</span>
        <span class="label mt-s" style="display:block">Pillar Three</span>
        <h3 class="h3 mt-s">Purpose and Flourishing</h3>
        <p class="body mt-s">Commitment to the spiritual vitality and physical wellbeing of the people our companies serve. We back ordinary ventures that honour God and help families thrive.</p>
        <p class="body mt-s">In practice: we choose businesses that provide real work for real families, and we measure them by whether those families are better off.</p>
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
      {feat("scale","Written agreements","Every material dealing is documented, and each party keeps its own counsel where it needs one.")}</div>
      <div class="card">{feat("bank","Clean books","Accounts kept current and reconciled. Filings made on time in every jurisdiction where we are registered.")}
      {feat("compass","No outside capital","Providence North is privately funded. There is no fund, no outside limited partner capital and no investment offering.")}</div>
    </div>
    <div class="card mt-l" style="max-width:none">{feat("users","The church verifies the founder","For businesses in The Faithful Business network, verification covers identity, active church membership and document completeness. It is not an endorsement, and it is not a review of the business itself.")}</div>
  </div>
</section>

<section class="sec" id="disclosure">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Disclosures</span></div>
    <h2 class="h2" style="max-width:24ch">Regulatory and legal disclosure.</h2>
    <div class="stack mt-m" style="max-width:76ch">
      <p class="body">Providence North LLC is a limited liability company registered in the State of Wyoming, United States. It is privately held and is not affiliated with any government, sovereign body or state investment vehicle.</p>
      <p class="body">Providence North LLC is not a registered broker dealer, investment adviser, fund, or pooled investment vehicle. It does not offer, sell or solicit the purchase of any security, and it does not manage money for third parties.</p>
      <p class="body">Nothing on this website is an offer to sell, or a solicitation of an offer to buy, any security, nor is it investment, legal, tax, accounting or medical advice. Any figures, descriptions or forward looking statements on this site are general in nature and subject to change without notice.</p>
      <p class="body">The Faithful Business operates advertising and directory listing services. Verification of a business or a professional is limited to identity, active church membership and document completeness. Providence North LLC does not evaluate the financial merit, viability or investment potential of any company, does not recommend or give investment advice, and due diligence is carried out by both parties and their counsel.</p>
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
        <p class="lead">A diner, a burger shop, a media brand, or something much larger. The size is not the point. What matters is that the business is real, the work is honest, and the family behind it is provided for.</p>
        <p class="body">Faith in business is not a slogan and it is not a guarantee of success. It is a way of dealing with people. Pay what you agreed to pay. Do not overstate what you have. Do not hide a problem to close a deal. When you are wrong, say so and put it right.</p>
        <p class="body">That is the whole of our doctrine, and it is harder to keep than it sounds. It is also the reason we can hold a business for twenty years and still look a partner in the eye.</p>
      </div>
      <div class="ivory">
        <span class="label">The frame we work inside</span>
        <p style="font-family:var(--font-display);font-size:1.35rem;line-height:1.45;margin-top:1.1rem;color:#0D0C0A">The church verifies the founder, not the entity. Providence North holds the business to a standard of lawful, transparent dealing.</p>
        <p class="small" style="margin-top:1.25rem;color:#5A5049">Verification is limited to identity, active church membership and document completeness. It is not an endorsement of a business, a product or an investment.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="eyebrow-row"><span class="label label-gold">Two audiences</span></div>
    <h2 class="h2" style="max-width:26ch">Who we build for.</h2>
    <div class="grid2 mt-xl">
      <div class="card">
        <span class="chip">Founders and families</span>
        <h3 class="h3 mt-m">People who want to build something honest</h3>
        <p class="body mt-s">If the business is real and the work is honest, we want to know about it. We are not looking for the next unicorn. We are looking for a business that will still be standing in twenty years and still paying the family that runs it.</p>
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
          <span class="label">Operations</span>
          <p class="mt-s" style="display:flex;gap:.7rem;align-items:flex-start">{IC["compass"]}<span class="body" style="color:var(--bone)">Bangkok, Thailand</span></p>
          <p class="small mt-s">Providence North has no public office and does not receive visitors without an appointment.</p>
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
  "Contact Providence North LLC. Registered office in Sheridan, Wyoming. Operations in Bangkok, Thailand.",
  contact_body, "contact.html")

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
page("404.html","Page not found | Providence North LLC","That page is not here.", notfound, "")

# ================================================================ static files
open(os.path.join(OUT,"CNAME"),"w").write(DOMAIN+"\n")
open(os.path.join(OUT,".nojekyll"),"w").write("")
open(os.path.join(OUT,"robots.txt"),"w").write(
f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
""")
today=datetime.date(2026,9,17).isoformat()
urls="".join(f"  <url><loc>{BASE}/{'' if p=='index.html' else p}</loc><lastmod>{today}</lastmod>"
             f"<priority>{'1.0' if p=='index.html' else '0.8'}</priority></url>\n"
             for p,_ in NAV if p!="contact.html")
urls+=f"  <url><loc>{BASE}/contact.html</loc><lastmod>{today}</lastmod><priority>0.7</priority></url>\n"
open(os.path.join(OUT,"sitemap.xml"),"w").write(
  f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

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
print("pages:", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith('.html'))))
