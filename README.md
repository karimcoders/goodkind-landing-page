# Goodkind — Corporate Gifting Landing Page

A clean, single-page Goodkind website with white, violet, lavender and apricot colours, oversized typography, newly AI-generated imagery, and an enquiry form.

## Features
- Goodkind branding throughout.
- Reference-inspired homepage composition without a shopping cart, catalogue, account login, checkout or blog.
- Responsive layout, navigation and six benefits.
- Testimonials carousel with arrows, dots, keyboard navigation and mobile swipe.
- Clearly labelled illustrative reviews and AI-generated portraits, not verified endorsements.
- Enquiry form with server-side validation, private SQLite storage and a private CSV export.
- No advertising trackers. Images, fonts, styles and JavaScript are embedded in `index.html`.

## Hosting and enquiry service
The HTML is deployed through GitHub Pages from the repository's default branch, at its root.

**Important:** GitHub Pages serves only the static landing page. The form currently calls a temporary Cloudflare-hosted Python API. Form submission depends on that temporary backend remaining online. Email notifications are not configured. Replace the enquiry endpoint with a permanently hosted backend before production use.

Current temporary API origin: `https://casino-matter-scheduling-mortgage.trycloudflare.com`
Allowed GitHub Pages form origin: `https://karimcoders.github.io`

No GitHub credentials are stored in this repository, its website, or its form.

## Local use
With Python 3.10 or later:

```sh
python server.py
```

Open http://localhost:3000. Only the homepage and API routes are publicly served by the Python server. Enquiries are stored in `landing-private/`, which is ignored by Git and is not served through the web server.

The production GitHub Pages form uses the temporary API URL in the JavaScript at the end of `index.html`. On localhost, the form uses `/api/enquiry` from the local Python server.

## Theme
The final style block contains the current theme overrides:
- Primary violet: `#6045d8`
- Text: `#242036`
- Soft lavender: `#f0edff`
- Secondary apricot: `#fff0e4`

The final CSS rules also define the responsive typography scale.

## Before production
1. Replace illustrative reviews with approved real customer testimonials.
2. Deploy the enquiry backend on persistent infrastructure and update the API URL and allowed CORS origin.
3. Connect a recipient email or CRM, if required.
4. Confirm privacy/retention requirements and keep the private enquiry directory out of public deployments.
5. Remove the crawler restriction in `robots.txt` when ready for indexing.
