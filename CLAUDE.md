# Knoxville Roofing Leads - Project Notes

## Google Analytics + AdSense

Every HTML page gets the GA tag and the AdSense verification meta tag at the top of `<head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RPJS68684E"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-RPJS68684E');
</script>
<meta name="google-adsense-account" content="ca-pub-5819445292295786">
```

The AdSense ad script goes on **blog pages only** (end of `<head>`). Keep it off the homepage, location pages, and thank-you page so ads don't pull visitors away from the quote form:

```html
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5819445292295786" crossorigin="anonymous"></script>
```

## Lead form

- Form posts to Formspree `https://formspree.io/f/xdeawzlj`. When adding a new location page, copy the full `<form id="leadForm">` block from an existing location page and update the hidden `source`, `location`, `_subject` values and the ZIP placeholder.
- `script.js` turns it into a 3-step form, submits via fetch, and redirects to `/thank-you/`, which fires the GA `generate_lead` event.

## Content rules

- Use the inline SVG icons (`<svg class="icon">`), never emojis.
- Don't add made-up stats, ratings, or testimonials. Only add real customer reviews.

## Website Info

- **Domain**: knoxvilleroofingquotes.com
- **Hosting**: GitHub Pages (deploys from `main`)
- **Google Search Console**: Verified
