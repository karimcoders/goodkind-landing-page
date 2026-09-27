# Rare Enterprises — Indigo & Gold Corporate Gifting

Live website: https://karimcoders.github.io/rare-enterprises/

A single-page corporate gifting landing website, using the client-supplied RE emblem with Rare Enterprises branding. The layout follows the marketing-page composition of the supplied CorporateGift reference, without a live ecommerce checkout, blog or user accounts. Collection tiles are enquiry links, not purchase flows.

## Current design
- White base, deep indigo `#39317d`, warm gold `#a77a27`, pale indigo `#f0eef8`, and champagne `#faf5e9`.
- Client-provided logo in the header, footer and favicon. Background removed without redrawing the mark.
- Large mixed-weight hero typography, six-feature grid and two alternating image/accordion sections.
- Newly AI-generated gifting photography, not imagery copied from the reference website.
- Two-card desktop / one-card mobile review carousel with arrows, dots, keyboard and touch controls.
- Clearly labelled illustrative reviews and generated reviewer portraits, not verified endorsements.
- One enquiry form and a compact footer.
- Responsive layout checked from 320px to 1440px.

## Run locally
Python 3.10+ is sufficient; no third-party Python libraries are required.

```sh
python server.py
```

Open http://localhost:3000. `index.html` is self-contained: fonts, images, CSS and JavaScript are embedded. The separately included `assets/brand-logo.png` and `assets/favicon.png` are editable branding source assets.

## GitHub Pages and form hosting
GitHub Pages publishes the static website from the root of the `main` branch.

**The form backend is temporary and separate from GitHub Pages.** It currently uses:
`https://mod-outcome-freight-impossible.trycloudflare.com/api/enquiry`

The backend permits the GitHub Pages origin `https://karimcoders.github.io`. If the temporary backend or tunnel stops, the website still displays on GitHub Pages, but submitting the form will report that the service is unavailable. Email notifications are not connected.

Before production use, deploy `server.py` to persistent hosting, update the API URL in `index.html`, confirm the CORS origin, and connect an email or CRM destination if needed.

## Privacy and security
Enquiries are stored in `landing-private/enquiries.sqlite3` and `landing-private/enquiries.csv` on the backend host. Those files are excluded from Git and are not served by the web application. No enquiry records, passwords or GitHub tokens are present in this repository.

Replace illustrative reviews with approved customer testimonials before commercial use. The client-supplied logo remains the property of its owner. `robots.txt` currently discourages indexing of the prototype; update it when the production site is ready.

## Newly added reference sections
- Exact requested “Designed for frequent gifters” heading and platform copy, with hover-shadow cards. These are displayed as capability previews, not proof that those platform modules are implemented. Confirm actual business service scope before removing the visible availability note.
- “Shop our Most Popular Collections”: original generated photographs in a six-tile tall/square/wide mosaic. Tapping a tile preselects an occasion and includes the collection in the enquiry. No cart or checkout is added.
- “Our latest awards”: five visibly labelled placeholder badge slots. No G2 or other awards are claimed by Rare Enterprises. Replace these only with verified awards.

## Client domain
The client supplied `rareenterprisessolution.com`. At the time of this update it returned a Hostinger parked-domain page. This repository update does not change its DNS or hosting, and no custom-domain mapping has been configured. The repository and GitHub Pages project URL have been renamed to `rare-enterprises` at the client’s request. Use the new URL; old GitHub Pages links may no longer resolve.

## Bold typography update
Hero text is now 102px / weight 700 on large desktop viewports. Main section headings use a 58–70px bold scale, feature titles 24–26px, and reading text 15–18px. Responsive overrides keep the layout within the viewport down to 320px. Branding, sections, imagery, cards and enquiry flow are unchanged.

## Motion and interaction update
- Continuous, seamless occasion marquee with pause/play, pause-on-hover and keyboard-focus pause.
- One-time staggered scroll reveals, a subtle page-progress line and active section navigation.
- Improved card and button hover effects plus a short hero entrance.
- Reviews rotate every 6.5 seconds only while visible, and pause on interaction or a hidden browser tab. A dedicated control pauses automatic rotation.
- Reduced-motion preferences disable nonessential animation and review autoplay.

Repository: https://github.com/karimcoders/rare-enterprises
Live page: https://karimcoders.github.io/rare-enterprises/
