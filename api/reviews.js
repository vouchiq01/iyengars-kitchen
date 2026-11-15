// Live Google rating and reviews for the site, via Places API (New).
// Needs GOOGLE_PLACES_API_KEY and GOOGLE_PLACE_ID in the Vercel project settings.
// Responses are cached on Vercel's edge for a day, so Google is called at most a few times a day.
module.exports = async (req, res) => {
  const key = process.env.GOOGLE_PLACES_API_KEY;
  const placeId = process.env.GOOGLE_PLACE_ID;
  if (!key || !placeId) return res.status(503).json({ ok: false, error: 'not configured' });

  try {
    const r = await fetch(`https://places.googleapis.com/v1/places/${encodeURIComponent(placeId)}?languageCode=en`, {
      headers: {
        'X-Goog-Api-Key': key,
        'X-Goog-FieldMask': 'rating,userRatingCount,googleMapsUri,reviews'
      }
    });
    if (!r.ok) throw new Error(`Google responded ${r.status}`);
    const p = await r.json();

    const reviews = (p.reviews || [])
      .map(v => ({
        name: v.authorAttribution?.displayName || '',
        profile: v.authorAttribution?.uri || '',
        photo: v.authorAttribution?.photoUri || '',
        rating: v.rating || 0,
        text: (v.text?.text || v.originalText?.text || '').trim(),
        when: v.relativePublishTimeDescription || '',
        link: v.googleMapsUri || ''
      }))
      // keep short, positive reviews that fit the quote card
      .filter(v => v.name && v.rating >= 4 && v.text.length >= 20 && v.text.length <= 320);

    res.setHeader('Cache-Control', 'public, s-maxage=86400, stale-while-revalidate=604800');
    res.status(200).json({
      ok: true,
      rating: p.rating || null,
      count: p.userRatingCount || null,
      url: p.googleMapsUri || '',
      reviews
    });
  } catch (e) {
    res.setHeader('Cache-Control', 'public, s-maxage=600');
    res.status(502).json({ ok: false, error: 'google unavailable' });
  }
};
