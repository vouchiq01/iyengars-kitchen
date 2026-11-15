# Mrs. Iyengar's Kitchen website

Static site (HTML/CSS/JS) for Mrs. Iyengar's Kitchen, KR Puram, Bengaluru. Hosted on Vercel.

- `index.html` – home page
- `menu.html` – full menu, **generated** from `tools/build_menu.py`. To change a dish or price, edit the `MENU` list there and run `python tools/build_menu.py`.
- `script.js` – phone/WhatsApp number, online-order link and opening hours are at the top.
- `api/reviews.js` – optional live Google reviews (Vercel function). Set `GOOGLE_PLACES_API_KEY` and `GOOGLE_PLACE_ID` in the Vercel project; without them the page shows its built-in review.

No database or separate backend is needed.
