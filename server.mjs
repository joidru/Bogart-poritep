import {createReadStream, existsSync, statSync} from 'node:fs';
import {createServer} from 'node:http';
import {extname, join, normalize, resolve, sep} from 'node:path';

const staticDirectory = resolve('dist');
const port = Number(process.env.LOCAL_SITE_PORT) || 4173;
const mimeTypes = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.js': 'text/javascript; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp'
};

createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, `http://${request.headers.host}`).pathname);
  const requestedPath = pathname === '/' ? '/index.html' : pathname;
  const withExtension = extname(requestedPath) ? requestedPath : `${requestedPath}.html`;
  const filePath = normalize(join(staticDirectory, withExtension));

  if (!filePath.startsWith(`${staticDirectory}${sep}`) || !existsSync(filePath) || !statSync(filePath).isFile()) {
    response.writeHead(404, {'content-type': 'text/plain; charset=utf-8'});
    response.end('Страница не найдена');
    return;
  }

  response.writeHead(200, {
    'cache-control': 'no-store',
    'content-type': mimeTypes[extname(filePath).toLowerCase()] || 'application/octet-stream'
  });
  createReadStream(filePath).pipe(response);
}).listen(port, '127.0.0.1', () => {
  console.log(`Poritep Partner: http://127.0.0.1:${port}`);
});
