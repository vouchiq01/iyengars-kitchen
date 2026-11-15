"""Builds menu.html from the menu below, reusing the header, icons and footer from index.html.

Edit a price or dish here, then run:  python tools/build_menu.py
Each item is (name, price) or (name, price, description). A price can be "₹150 / 300" for two sizes.
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

MENU = [
    ("All Day Feast", None, [
        ("Avalakki Upma (Poha)", 80), ("Gojju Avalakki (Tamarind Poha)", 80), ("Shavige Bath", 80),
        ("Akki Rotti (2 pcs)", 80), ("Ambode (1 pc)", 10), ("Ghee Pongal", 70), ("Bisi Bele Bath", 70),
        ("Vada (1 pc)", 40), ("Poori Bhaji", 80), ("Raagi Rotti (2 pcs)", 80), ("Nucchina Unde (3 pcs)", 100),
        ("Khara Bath", 70), ("Dahl Vada", 50), ("Idiyappam (3 pcs) with Veg Kurma", 100), ("Chow Chow Bath", 80),
        ("Curd Avalakki", 70),
    ], None),
    ("Idly Varieties", None, [
        ("Idly (2 pcs)", 40), ("Pudi Idly (2 pcs)", 60), ("Masala Idly (2 pcs) · Sunday", 60), ("Button Idly (12 pcs)", 50),
        ("Kanchipuram Idly (2 pcs)", 80), ("Idly (1 pc) Vada (1 pc)", 60), ("Idly (2 pcs) Vada (1 pc)", 80),
        ("Pudi Button Idly (12 pcs)", 60),
    ], "Seasoning of ghee / butter ₹15 extra"),
    ("Dosa Varieties", None, [
        ("Plain Dosa", 50), ("Masala Dosa", 80), ("Podi Dosa", 60), ("Podi Masala Dosa", 90), ("Upma Pesarattu Dosa", 100),
        ("Adai Dosa", 100), ("Paneer Plain Dosa", 90), ("Cheese Plain Dosa", 90), ("Paneer Masala Dosa", 150),
        ("Cheese Masala Dosa", 150), ("Raagi Dosa", 70), ("Rava Dosa", 80), ("Rava Masala Dosa", 120),
        ("Plain Pesarattu", 70), ("Neer Dosa (3 pcs)", 70), ("Kali Dosa", 70),
    ], None),
    ("Dosa Specials", None, [
        ("Iyengar's Special Dosa", 150), ("Mushroom Masala Dosa", 150), ("Beetroot Masala Dosa", 150),
        ("Paneer Matar Masala Dosa", 180), ("Mix Veg Masala Dosa", 150), ("Shivage Bath Masala Dosa", 120),
        ("Tomato Masala Dosa", 150), ("Pudina Masala Dosa", 150), ("Carrot Masala Dosa", 150),
    ], None),
    ("Meals", None, [
        ("Iyengar's Oota", 240, "Rice, poriyal, kosambari, sambar, flavoured rice, rasam, curd, papad, mor kulzhambu or kootu, sweet & ambode"),
        ("Obbattu Oota", 280, "One obbattu, rice, poriyal, kosambari, sambar, flavoured rice, rasam, curd, papad, mor kulzhambu or kootu, sweet & ambode"),
        ("Executive Meal", 180, "1 chapathi, poriyal, kosambari, sambar, rasam, flavoured rice, ambode & papad"),
        ("Quick Meal", 140, "Poriyal, sambar, rasam, curd, rice, kosambari, ambode and papad"),
        ("Jolada Rotti Oota", 160, "Two rotti, curry, palya, sambar, rasam, curd, rice, kosambari & papad"),
        ("Mudde Oota", 160, "One mudde, palya, sambar, rasam, curd, rice, kosambari, ambode and papad"),
        ("Chapathi Meal", 120, "3 chapathi, poriyal, kootu / dal and kosambari"),
        ("Pulka Meal", 120, "3 pulka, poriyal, kootu / dal and kosambari"),
        ("Anna Sambar", 80), ("Mor Kulzhambu with Rice", 100), ("Milagu Rasam with Rice", 80), ("Kootu with Rice", 100),
    ], None),
    ("Rice Varieties", None, [
        ("Puliyogre", 70), ("Aloo Bath", 70), ("Raw Mango Rice", 70), ("Capsicum Rice", 70), ("Lemon Rice", 70),
        ("Coconut Rice", 70), ("Kadugu Ogare (Mustard Rice)", 70), ("Vangi Bath", 70), ("Curry Leaf Rice", 70),
        ("Tomato Rice", 70), ("Curd Rice", 70), ("Avakaya Pappu Rice", 70), ("Pickle Rice", 70), ("Pudina Rice", 70),
        ("Carrot Rice", 70), ("Sabakki Soppu Bath", 70), ("Dal Khichadi", 70), ("Weekend Pulao Special", 140),
        ("Ghee Rice", 150), ("Jeera Rice", 150), ("Palak Khichdi", 120),
    ], None),
    ("Main Course", "250 ml / 450 ml", [
        ("Paneer Bhurji", "150 / 300"), ("Palak Paneer", "140 / 280"), ("Paneer Butter Masala", "140 / 280"),
        ("Kadai Paneer", "140 / 280"), ("Matar Paneer Masala", "140 / 280"), ("Achari Paneer", "140 / 280"),
        ("Methi Matar Paneer", "130 / 260"), ("Methi Matar Corn", "130 / 260"), ("Palak Cream Corn", "120 / 240"),
        ("Methi Matar Masala", "120 / 240"), ("Dum Aloo", "120 / 240"), ("Veg Kadai", "120 / 240"),
        ("Aloo Matar Curry", "100 / 200"), ("Aloo Gobi Curry", "100 / 200"), ("Aloo Tomato Curry", "100 / 200"),
        ("Veg Kurma", "100 / 200"), ("Mix Veg Curry", "100 / 200"), ("Bhindi Masala", "100 / 200"),
        ("Aloo Palak", "100 / 200"), ("Dahi Aloo", "100 / 200"), ("Dahi Bhindi", "100 / 200"), ("Achari Aloo", "100 / 200"),
        ("Aloo Methi Dry", "100 / 200"), ("Plain Palak", "90 / 180"), ("Bhandare Wale Aloo Sabji", "90 / 180"),
        ("Aloo Jeera Dry", "80 / 160"), ("Bhindi Fry", "80 / 160"), ("Gobhi Masala Fry", "80 / 160"),
        ("Aloo Bhindi Fry", "80 / 160"), ("Aloo Fry", "80 / 160"),
    ], None),
    ("Dal Varieties", "250 ml / 450 ml", [
        ("Dal", "80 / 160"), ("Dal Tadka", "90 / 180"), ("Ghee Dal Tadka", "120 / 220"),
    ], None),
    ("Roti Varieties", None, [
        ("Phulka", 25), ("Chapati", 25), ("Wheat Paratha", 35), ("Jolada Rotti", 25), ("Lacha Paratha", 35), ("Ajwain Chapati", 35),
    ], None),
    ("Evening Varieties", None, [
        ("Paddu (6 pcs)", 80), ("Vada Rasam", 70), ("Aloo Bonda (1 pc)", 10), ("Chilli Bajji (1 pc)", 15),
        ("Palak Pakoda", 40), ("Susla", 50), ("Bonda Soup", 70), ("Bonda Rasam", 70), ("Idly 65", 120), ("Chilly Idly", 120),
    ], None),
    ("Starters", None, [
        ("Veg Ball Manchurian", 120), ("Gobi Manchurian", 100), ("Mushroom Manchurian", 140), ("Baby Corn Manchurian", 140),
        ("Gobi Manchurian Masala", 140), ("Veg 65", 140), ("Mushroom 65", 150), ("Paneer 65", 200), ("Chilli Paneer", 220),
        ("Paneer Manchurian", 220), ("Gobi 65", 120), ("Mushroom Pepper", 140), ("Paneer Pepper", 200),
    ], "Gravy item ₹20 extra"),
    ("Fried Rice", None, [
        ("Veg Fried Rice", 150), ("Schezwan Rice", 160), ("Manchurian Rice", 220), ("Paneer Fried Rice", 220),
        ("Mushroom Fried Rice", 180), ("Corn Stir Fried Rice", 180), ("Baby Corn Fried Rice", 180),
    ], None),
    ("Noodles", None, [
        ("Veg Noodles", 120), ("Schezwan Noodles", 160), ("Manchurian Noodles", 240), ("Paneer Noodles", 200),
        ("Mushroom Noodles", 180), ("Baby Corn Noodles", 180),
    ], None),
    ("Desserts", None, [
        ("Rice Payasam (250 ml)", 100), ("Hayagreeva · Chana Dal (250 ml)", 100), ("Sakkarai Pongal (250 ml)", 100),
        ("Semiya Payasam (250 ml)", 100), ("Rava Kaseri (250 ml)", 100), ("Parippu Payasam (250 ml)", 100),
        ("Sabudana Payasam (250 ml)", 100), ("Gasa Gase Payasam (100 ml)", 50), ("Carrot Halwa (250 ml)", 100),
        ("Sweet Avalakki (250 ml)", 80), ("Idiyappam with Coconut Jaggery Milk", 100), ("Idiyappam with Gasa Gasa Payasam", 120),
        ("Peanut Obbattu", 60), ("Dal Obbattu", 60), ("Kayi Obbattu", 60), ("Dry Jamun (1 pc)", 20), ("Gulab Jamun (1 pc)", 20),
    ], None),
    ("Iyengar Special Add-ons", None, [
        ("Kulzhambu · Sambar (450 ml)", 80), ("Mor Kuzhambu · Curd Sambar (225 ml)", 80), ("Rasam (450 ml)", 80),
        ("Kootu (225 ml)", 80), ("Parippu · Tovve (225 ml)", 80), ("Milagu · Pepper Rasam (450 ml)", 80),
        ("Gojju Curry of the Day (225 ml)", 80), ("Kosambari · Salad (225 ml)", 80), ("Poriyal · Palya (225 ml)", 80),
        ("White Rice", 40), ("Ragi Mudde (1 pc)", 25), ("Ennegayi (250 ml)", 90), ("Papad (1 pc)", 5), ("Fried Curd Chilly (2 pcs)", 5),
    ], None),
    ("Parcel Combos", None, [
        ("Meal for Two (without rice)", 240, "Poriyal, kosambari, sambar, rasam, curd, papad, ambode 2 pcs"),
        ("Meal for Two", 520, "Rice, poriyal, kosambari, sambar, rasam, flavoured rice, milagu rasam, curd, papad, mor kulzhambu, ambode 4 pcs and sweet"),
        ("Family Combo (serves 3 to 4)", 780, "Rice, poriyal, kosambari, sambar, rasam, flavoured rice, milagu rasam, curd, papad, mor kulzhambu, ambode 8 pcs and sweet"),
    ], "Parcel charges ₹5 extra per item · meal parcel ₹15 per meal"),
    ("Hot Beverages", None, [
        ("Tea", 25), ("Coffee", 25), ("Lemon Tea", 25), ("Masala Tea", 30), ("Masala Jaggery Tea", 30), ("Jaggery Honey Tea", 30),
        ("Ginger Tea", 25), ("Elaichi Tea", 30), ("Ginger Coffee", 30), ("Hot Badam Milk", 30), ("Water Bottle 500 ml", 10),
    ], None),
    ("Lassi & Buttermilk", None, [
        ("Butter Milk", 30), ("Sweet Lassi", 60), ("Salt Lassi", 60), ("Salt & Sweet Lassi", 70), ("Mango Lassi", 90),
        ("Strawberry Lassi", 80), ("Rose Lassi", 80),
    ], None),
    ("Juices & Beverages", None, [
        ("Water Melon", 60), ("Mosambi", 75), ("Muskmelon", 80), ("Pineapple", 60), ("Apple Juice", 80), ("Orange Juice", 75),
        ("Pulpy Grape Juice", 65), ("Fresh Lime Salt", 45), ("Fresh Lime Sweet", 45), ("Fresh Lime Soda Salt", 60),
        ("Fresh Lime Soda Sweet", 60), ("Fresh Lime Salt & Sweet Soda", 70), ("Mint Lime Soda", 50), ("Pomegranate", 75),
        ("Mojito Juice", 70), ("Blue Curacao Juice", 80), ("Black Currant Juice", 70),
    ], None),
    ("Milkshakes", None, [
        ("Apple Milk Shake", 90), ("Chikoo Milk Shake", 80), ("Banana Milk Shake", 70), ("Pomegranate Milk Shake", 100),
        ("Butter Fruit Milk Shake", 120), ("Musk Melon Milk Shake", 80), ("Papaya Milk Shake", 90),
        ("Chocolate Milk Shake", 100), ("Dry Fruit Milk Shake", 120), ("Rose Milk Shake", 70), ("Mango Milk Shake", 90),
    ], None),
]

FEATURED = [
    ("meals-board.jpg", "Iyengar's Oota", "₹240", "Iyengar meal spread"),
    ("akki-rotti.jpg", "Akki Rotti", "₹80", "Akki rotti on a banana leaf"),
    ("puliyogare-plates.jpg", "Puliyogre", "₹70", "Puliyogare on areca plates"),
    ("sakkarai-pongal.jpg", "Sakkarai Pongal", "₹100", "Sakkarai pongal with cashews"),
]

def slug(s): return "m-" + re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def price(p): return f"₹{p}" if p is not None else ""
e = html.escape

def build():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    grab = lambda tag: re.search(rf"<!--{tag}-->.*?<!--/{tag}-->", src, re.S).group(0)
    svg, navb, foot = grab("SVG"), grab("NAV"), grab("FOOTER")
    count = sum(len(items) for _, _, items, _ in MENU)

    chips = "\n".join(f'        <a href="#{slug(n)}">{e(n)}</a>' for n, *_ in MENU)
    cats = []
    for name, size, items, note in MENU:
        lis = []
        for it in items:
            n, p, *d = it
            big = ' big' if d else ''
            desc = f'<span class="d">{e(d[0])}</span>' if d else ''
            lis.append(f'          <li class="mi{big}"><span class="n">{e(n)}</span><span class="dots"></span><span class="p">{price(p)}</span>{desc}</li>')
        size_tag = f'<span class="mtime">{e(size)}</span>' if size else ''
        foot_note = f'\n        <p class="mfoot">* {e(note)}</p>' if note else ''
        cats.append(f'''      <div class="mcat" id="{slug(name)}">
        <div class="mcat-head"><h3>{e(name)}</h3>{size_tag}</div>
        <ul>
{chr(10).join(lis)}
        </ul>{foot_note}
      </div>''')
    feats = "\n".join(f'      <figure class="feat reveal"><img src="images/{i}" alt="{e(a)}" loading="lazy"><figcaption><b>{e(n)}</b><span>{p}</span></figcaption></figure>' for i, n, p, a in FEATURED)

    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Menu | Mrs. Iyengar's Kitchen, KR Puram</title>
<meta name="description" content="Full menu of Mrs. Iyengar's Kitchen: Iyengar meals, puliyogre, akki rotti, dosas, idly, rice varieties, sweets and drinks. Pure veg, no onion, no garlic. KR Puram, Bengaluru.">
<meta name="theme-color" content="#4a0c0c">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="Menu | Mrs. Iyengar's Kitchen">
<meta property="og:description" content="Satvik Iyengar home food. No onion, no garlic. KR Puram, Bengaluru.">
<meta property="og:image" content="images/meals-board.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,500&family=Inter:wght@400;500;600;700&family=Noto+Sans+Kannada:wght@600&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="styles.css?v=1">
</head>
<body>

<!-- generated by tools/build_menu.py — edit the menu there, not here -->
{svg}

{navb}

<section class="page-hero">
  <svg class="mandala" style="color:#f5c83a"><use href="#mandala"/></svg>
  <div class="wrap">
    <a class="back" href="./"><svg width="18" height="18"><use href="#i-left"/></svg>Back to home</a>
    <span class="kannada">ಊಟದ ಪಟ್ಟಿ</span>
    <h1>Our <em>Menu</em></h1>
    <p class="lead">Iyengar home-style tiffins, dosas, full meals, rice varieties and sweets. All pure vegetarian, all cooked without onion or garlic.</p>
    <div class="page-hero-meta">
      <span class="chip"><i class="dot"></i>Open daily · 7:30 am – 10:30 pm</span>
      <span class="chip"><b>No</b> onion · <b>No</b> garlic</span>
      <span class="chip">₹1–200 per person</span>
    </div>
    <div class="cta">
      <a class="btn btn-primary" data-order href="#" target="_blank" rel="noopener"><svg><use href="#i-bag"/></svg>Order online</a>
      <a class="btn btn-glass" href="tel:+919880186251"><svg><use href="#i-phone"/></svg>Call to order</a>
    </div>
  </div>
  <div class="wave" aria-hidden="true"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path fill="#fbf1dc" d="M0 40c240 30 480 30 720 0s480-30 720 0v30H0z"/></svg></div>
</section>

<section id="full-menu" class="menu-page">
  <div class="wrap">
    <div class="featured">
{feats}
    </div>

    <div class="menu-tools">
      <label class="msearch"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="menuSearch" type="search" placeholder="Search {count} dishes… e.g. dosa, payasam, rice" autocomplete="off" aria-label="Search the menu"></label>
      <nav class="mchips" aria-label="Menu sections">
{chips}
      </nav>
    </div>

    <div class="mnote"><span>All dishes are pure veg &amp; cooked without onion or garlic</span><span>Prices in ₹, may change without notice</span></div>

    <div class="mgrid" id="mgrid">
{chr(10).join(cats)}
    </div>
    <p class="mnone" id="mnone" hidden>No dishes match your search. Try another word, or call us on <a href="tel:+919880186251">098801 86251</a>.</p>
  </div>
</section>

{foot}

<script src="script.js?v=1"></script>
</body>
</html>
'''
    # the menu page has no hero buttons, so the phone bar should always show
    (ROOT / "menu.html").write_text(page, encoding="utf-8")
    print(f"menu.html written: {len(MENU)} sections, {count} dishes")

if __name__ == "__main__":
    build()
