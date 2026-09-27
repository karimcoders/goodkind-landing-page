# Goodkind — Indigo & Gold Corporate Gifting

Live website: https://karimcoders.github.io/goodkind-landing-page/

A single-page corporate gifting landing website, using the client-supplied RE emblem with Goodkind branding. The layout follows the marketing-page composition of the supplied CorporateGift reference, without its ecommerce, blog, account or checkout features.

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
`https://began-backed-conferencing-stopping.trycloudflare.com/api/enquiry`

The backend permits the GitHub Pages origin `https://karimcoders.github.io`. If the temporary backend or tunnel stops, the website still displays on GitHub Pages, but submitting the form will report that the service is unavailable. Email notifications are not connected.

Before production use, deploy `server.py` to persistent hosting, update the API URL in `index.html`, confirm the CORS origin, and connect an email or CRM destination if needed.

## Privacy and security
Enquiries are stored in `landing-private/enquiries.sqlite3` and `landing-private/enquiries.csv` on the backend host. Those files are excluded from Git and are not served by the web application. No enquiry records, passwords or GitHub tokens are present in this repository.

Replace illustrative reviews with approved customer testimonials before commercial use. The client-supplied logo remains the property of its owner. `robots.txt` currently discourages indexing of the prototype; update it when the production site is ready.
