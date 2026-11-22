// Link mời có tên khách (/?xh=Anh&ten=Minh) được vercel.json chuyển về đây.
// Trả về index.html với tiêu đề / mô tả / og:url chứa tên khách để Zalo, Messenger,
// Facebook hiển thị bản xem trước đúng tên khách mời.
const fs = require('fs');
const path = require('path');

const SITE = 'https://lamanhphuchieu.site/';
const COUPLE = 'Lâm Anh - Phúc Hiếu';
const WEDDING_DATE_TEXT = 'Chủ nhật, 20.12.2026';
const INDEX_PATH = path.join(process.cwd(), 'index.html');

const esc = (s) =>
  s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

const clean = (v) =>
  String(Array.isArray(v) ? v[0] : v || '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 50);

function guestLabel(q) {
  const to = clean(q.to);
  let xh = clean(q.xh);
  const ten = clean(q.ten);
  if (xh) xh = xh.charAt(0).toUpperCase() + xh.slice(1);
  return to || [xh, ten].filter(Boolean).join(' ');
}

module.exports = (req, res) => {
  const q = req.query || {};
  const label = guestLabel(q);
  let out = fs.readFileSync(INDEX_PATH, 'utf8');

  const proto = (req.headers && req.headers['x-forwarded-proto']) || 'https';
  const host = req.headers && req.headers.host;
  const siteBase = host ? `${proto}://${host}/` : SITE;

  if (label) {
    const params = new URLSearchParams();
    ['xh', 'ten', 'to'].forEach((k) => {
      const v = clean(q[k]);
      if (v) params.set(k, v);
    });
    const url = esc(siteBase + '?' + params.toString());
    const ogImg = esc(siteBase + 'assets/images/og_share.jpg');
    const title = esc(`Thân mời ${label} | Lễ Cưới ${COUPLE}`);
    const desc = esc(
      `Trân trọng kính mời ${label} đến chung vui cùng ${COUPLE} - ${WEDDING_DATE_TEXT}`
    );

    out = out
      .replace(/<title>[^<]*<\/title>/, `<title>${title}</title>`)
      .replace(/(<meta property="og:title" content=")[^"]*/, `$1${title}`)
      .replace(/(<meta property="og:description" content=")[^"]*/, `$1${desc}`)
      .replace(/(<meta name="description" content=")[^"]*/, `$1${desc}`)
      .replace(/(<meta property="og:url" content=")[^"]*/, `$1${url}`)
      .replace(/(<link rel="canonical" href=")[^"]*/, `$1${url}`)
      .replace(/(<meta property="og:image" content=")[^"]*/, `$1${ogImg}`)
      .replace(/(<meta name="twitter:image" content=")[^"]*/, `$1${ogImg}`);
  }

  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader(
    'Cache-Control',
    'public, max-age=0, s-maxage=86400, stale-while-revalidate=604800'
  );
  res.status(200).send(out);
};
