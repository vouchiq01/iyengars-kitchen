// ---- Settings ----
const WA_NUMBER = "919880186251";          // restaurant, party hall and catering line
const ORDER_URL = "https://mrs-iyengars-kitchen.order.food-pe.com/#fpc=StlWQJb27epVhzxj130AltFt";
const DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&destination=Mrs+Iyengar%27s+Kitchen+The+Terminal+Hoodi+Main+Rd+Ayyappa+Nagar+Krishnarajapuram+Bengaluru";
const HOURS = { open: 7 * 60 + 30, close: 22 * 60 + 30 }; // 7:30 am to 10:30 pm, every day (IST)
const WA_MESSAGES = {
  hello: "Hi Mrs. Iyengar's Kitchen! I have a question.",
  parcel: "Hi Mrs. Iyengar's Kitchen! I'd like to order a meal combo parcel.\n\nCombo (Meal for Two / Family Combo):\nPickup or delivery:\nTime:",
  party: "Hi Mrs. Iyengar's Kitchen! I'd like to book the Sabhagrha Party Hall.\n\nOccasion:\nDate:\nNumber of guests:",
  catering: "Hi Mrs. Iyengar's Kitchen! I'm interested in outdoor catering.\n\nEvent type:\nDate:\nNumber of guests:\nLocation:"
};
const waLink = text => `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`;
document.querySelectorAll('[data-wa]').forEach(a => a.href = waLink(WA_MESSAGES[a.dataset.wa] || WA_MESSAGES.hello));
document.querySelectorAll('[data-order]').forEach(a => a.href = ORDER_URL);
document.querySelectorAll('[data-dir]').forEach(a => a.href = DIRECTIONS_URL);

// Open / closed right now, by Bengaluru time
(() => {
  const el = document.querySelector('[data-open-status]');
  if (!el) return;
  const t = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));
  const m = t.getHours() * 60 + t.getMinutes();
  const open = m >= HOURS.open && m < HOURS.close;
  el.querySelector('span').textContent = open ? 'Open now · till 10:30 pm' : 'Closed now · opens 7:30 am';
  el.querySelector('.live').classList.toggle('closed', !open);
})();

// In-page links: smooth scroll without adding #section to the address bar
document.querySelectorAll('a[href^="#"], a[href^="./#"]').forEach(a => a.addEventListener('click', e => {
  const id = a.getAttribute('href').split('#')[1];
  const target = id && document.getElementById(id);
  if (!target) return;
  e.preventDefault();
  if (id === 'top') window.scrollTo({ top: 0, behavior: 'smooth' });
  else target.scrollIntoView({ behavior: 'smooth' });
}));
if (location.hash && !document.getElementById('menuSearch')) {
  const t = document.getElementById(location.hash.slice(1));
  history.replaceState(null, '', location.pathname);
  if (t) setTimeout(() => t.scrollIntoView(), 60);
}

// Nav turns solid after scrolling; phone action bar stays away until you scroll past the hero buttons
const nav = document.getElementById('topnav');
const mbar = document.querySelector('.mbar');
const heroCta = document.querySelector('.hero .cta');
const onScroll = () => {
  nav.classList.toggle('scrolled', scrollY > 40);
  if (heroCta && mbar) mbar.classList.toggle('away', heroCta.getBoundingClientRect().bottom > 0);
};
addEventListener('scroll', onScroll, { passive: true });
addEventListener('resize', onScroll);
onScroll();

// Gallery slideshow: swipe, arrows, dots, autoplay while visible
const track = document.getElementById('slides');
if (track) {
  const slides = [...track.children];
  const dotsBox = document.getElementById('dots');
  slides.forEach((_, i) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', `Show photo ${i + 1}`);
    b.addEventListener('click', () => { go(i); restart(); });
    dotsBox.appendChild(b);
  });
  const dots = [...dotsBox.children];
  let current = 0, timer = null, inView = false;
  const setActive = i => {
    current = i;
    slides.forEach((s, k) => s.classList.toggle('active', k === i));
    dots.forEach((d, k) => d.classList.toggle('on', k === i));
  };
  const go = i => {
    i = (i + slides.length) % slides.length;
    const s = slides[i];
    track.scrollTo({ left: s.offsetLeft - (track.clientWidth - s.clientWidth) / 2, behavior: 'smooth' });
    setActive(i);
  };
  let scrollT;
  track.addEventListener('scroll', () => {
    clearTimeout(scrollT);
    scrollT = setTimeout(() => {
      const mid = track.scrollLeft + track.clientWidth / 2;
      let best = 0, dist = Infinity;
      slides.forEach((s, k) => { const d = Math.abs(s.offsetLeft + s.clientWidth / 2 - mid); if (d < dist) { dist = d; best = k; } });
      setActive(best);
    }, 80);
  }, { passive: true });
  const restart = () => { clearInterval(timer); if (inView) timer = setInterval(() => go(current + 1), 4200); };
  document.getElementById('prev').addEventListener('click', () => { go(current - 1); restart(); });
  document.getElementById('next').addEventListener('click', () => { go(current + 1); restart(); });
  track.addEventListener('pointerdown', () => clearInterval(timer), { passive: true });
  track.addEventListener('touchend', () => setTimeout(restart, 1500), { passive: true });
  new IntersectionObserver(([e]) => { inView = e.isIntersecting; restart(); }, { threshold: .35 }).observe(track);
  setActive(0);
}

// Policy dialogs
document.querySelectorAll('[data-open]').forEach(b => b.addEventListener('click', () => document.getElementById(b.dataset.open).showModal()));
document.querySelectorAll('dialog').forEach(d => {
  d.querySelector('.dlg-close').addEventListener('click', () => d.close());
  d.addEventListener('click', e => { if (e.target === d) d.close(); });
});

// Year
const yr = new Date().getFullYear();
document.querySelectorAll('#yr, .yr').forEach(el => el.textContent = yr);

// Scroll reveal with a small stagger inside each group
const groups = new Map();
document.querySelectorAll('.reveal').forEach(el => {
  const n = groups.get(el.parentElement) || 0;
  el.style.transitionDelay = (n % 3) * 50 + 'ms';
  groups.set(el.parentElement, n + 1);
});
const io = new IntersectionObserver(entries => entries.forEach(en => {
  if (en.isIntersecting) { const t = en.target; t.classList.add('in'); io.unobserve(t); setTimeout(() => t.style.transitionDelay = '', 700); }
}), { threshold: 0, rootMargin: '0px 0px 20% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Full menu: search box and section chips that follow your scroll
const menuSearch = document.getElementById('menuSearch');
if (menuSearch) {
  const cats = [...document.querySelectorAll('.mcat')];
  const none = document.getElementById('mnone');
  menuSearch.addEventListener('input', () => {
    const t = menuSearch.value.trim().toLowerCase();
    let any = false;
    cats.forEach(c => {
      const catMatch = t && c.querySelector('h3').textContent.toLowerCase().includes(t);
      let shown = 0;
      c.querySelectorAll('.mi').forEach(li => {
        const ok = !t || catMatch || li.textContent.toLowerCase().includes(t);
        li.classList.toggle('hide', !ok);
        if (ok) shown++;
      });
      c.classList.toggle('hide', !shown);
      if (shown) any = true;
    });
    none.hidden = any;
  });

  const chipBox = document.querySelector('.mchips');
  const chips = [...chipBox.querySelectorAll('a')];
  let ticking = false;
  const markChip = () => {
    ticking = false;
    let cur = null;
    cats.forEach(c => { if (!c.classList.contains('hide') && c.getBoundingClientRect().top < 240) cur = c.id; });
    chips.forEach(a => {
      const on = a.getAttribute('href') === '#' + cur;
      if (on && !a.classList.contains('on')) chipBox.scrollTo({ left: a.offsetLeft - chipBox.clientWidth / 2 + a.clientWidth / 2, behavior: 'smooth' });
      a.classList.toggle('on', on);
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(markChip); } }, { passive: true });
  if (location.hash) { const t = document.getElementById(location.hash.slice(1)); if (t) setTimeout(() => t.scrollIntoView(), 80); }
}

// Live Google reviews (served by /api/reviews). If it isn't set up or fails, the page keeps its built-in text.
fetch('/api/reviews').then(r => r.ok ? r.json() : null).then(g => {
  if (!g || !g.ok) return;
  if (g.url) document.querySelectorAll('[data-greviews]').forEach(a => a.href = g.url);

  const card = document.getElementById('gquote');
  if (!card || !g.reviews || !g.reviews.length) return;
  const stars = card.querySelector('.stars');
  const quote = card.querySelector('blockquote');
  const avatar = card.querySelector('.avatar');
  const name = card.querySelector('.who b');
  const meta = card.querySelector('.who small');
  card.querySelector('.g-src').hidden = false;
  const show = v => {
    stars.textContent = '★'.repeat(Math.round(v.rating));
    quote.textContent = v.text;
    avatar.textContent = v.name.charAt(0).toUpperCase();
    if (v.photo) {
      const img = new Image();
      img.alt = '';
      img.referrerPolicy = 'no-referrer';
      img.onerror = () => img.remove();
      img.src = v.photo;
      avatar.appendChild(img);
    }
    name.textContent = '';
    if (v.profile) {
      const a = document.createElement('a');
      a.href = v.profile; a.target = '_blank'; a.rel = 'noopener';
      a.textContent = v.name;
      name.appendChild(a);
    } else name.textContent = v.name;
    meta.textContent = v.when ? `${v.when} · Google` : 'Google review';
  };
  let i = Math.floor(Math.random() * g.reviews.length);
  show(g.reviews[i]);
  if (g.reviews.length > 1 && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    setInterval(() => {
      card.classList.add('swap');
      setTimeout(() => { i = (i + 1) % g.reviews.length; show(g.reviews[i]); card.classList.remove('swap'); }, 400);
    }, 8000);
  }
}).catch(() => {});
