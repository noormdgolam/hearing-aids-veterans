# Hearing Aids Veterans Guide - Static Site Generator

This is a custom, zero-dependency Python static site generator built specifically for the "Hearing Aids Veterans Guide" project. It generates a high-performance, AdSense-ready, and SEO-optimized website capable of handling massive traffic spikes.

## Prerequisites

- Python 3.8+ (No external dependencies required)

## How to Build the Site

To generate the site, simply run:

```bash
python build_site.py
```

This will create an `out/` directory containing the fully built static site.

## Testing Locally

You can test the site locally using Python's built-in HTTP server:

```bash
cd out
python -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.

## Adding New Content

To add or modify articles:
1. Open `content.py`.
2. Add a new tuple to the `raw_articles` list or modify existing entries.
3. If you want a completely unique article body, you can modify `generate_article_body()` or override it for specific slugs.
4. Run `python build_site.py` again to regenerate the site, RSS feed, Sitemap, and Search index.

## Google AdSense & Analytics integration

1. Open `templates/base.html`.
2. Look for the `<!-- Placeholder: Google AdSense -->` comment in the `<head>` and uncomment the script tag, replacing `ca-pub-XXXXXXXXXXXX` with your Publisher ID.
3. Look for the `<!-- Placeholder: GA4 -->` comment in the `<head>` and replace `G-XXXXXXXX` with your GA4 Measurement ID.
4. Ad placeholders are already placed in `base.html` (top and bottom) and `article.html` (sidebar).
5. Run `python build_site.py` to apply changes.

## Newsletter Integration

1. The site contains a placeholder form (`<form action="/subscribe-placeholder" method="POST">`).
2. Replace `/subscribe-placeholder` with your email marketing provider's endpoint (e.g., Mailchimp, ConvertKit).

## Deployment

Since the output in the `out/` directory is purely static (HTML, CSS, JS), you can deploy it to any static hosting provider (e.g., GitHub Pages, Cloudflare Pages, Netlify, Vercel) or a traditional CDN. All routing is file-based (e.g., `/va-benefits/index.html`).
