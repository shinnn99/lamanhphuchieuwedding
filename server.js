const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');
const inviteHandler = require('./api/invite.js');

const PORT = Number(process.env.PORT) || 8088;
const ROOT = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.mp3': 'audio/mpeg',
  '.otf': 'font/otf',
  '.ttf': 'font/ttf',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
};

const server = http.createServer((req, res) => {
  const parsed = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = decodeURIComponent(parsed.pathname);

  // Route SSR cá nhân hóa tên khách giống cấu hình vercel.json
  if (
    (pathname === '/' || pathname === '/api/invite') &&
    (parsed.searchParams.has('xh') ||
      parsed.searchParams.has('ten') ||
      parsed.searchParams.has('to'))
  ) {
    const query = Object.fromEntries(parsed.searchParams.entries());
    return inviteHandler(
      { query },
      {
        setHeader: (k, v) => res.setHeader(k, v),
        status: (code) => ({
          send: (body) => {
            res.statusCode = code;
            res.end(body);
          },
        }),
      }
    );
  }

  const relPath = pathname === '/' ? '/index.html' : pathname;
  const safePath = path.normalize(path.join(ROOT, relPath));
  if (!safePath.startsWith(ROOT)) {
    res.writeHead(403);
    return res.end('Forbidden');
  }

  fs.stat(safePath, (err, stat) => {
    if (err || !stat.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('404 Not Found');
    }

    const ext = path.extname(safePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // Hỗ trợ HTTP Range cho file nhạc MP3 tua/phát mượt trên mọi trình duyệt
    const range = req.headers.range;
    if (range && ext === '.mp3') {
      const parts = range.replace(/bytes=/, '').split('-');
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stat.size - 1;
      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${stat.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': end - start + 1,
        'Content-Type': contentType,
      });
      return fs.createReadStream(safePath, { start, end }).pipe(res);
    }

    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Length': stat.size,
      'Cache-Control': 'no-cache',
    });
    fs.createReadStream(safePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log(`Wedding server running at http://localhost:${PORT}/`);
});
