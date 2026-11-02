import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url));
const host = '0.0.0.0';
const port = Number(process.env.PORT || 8080);
const mime = { '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.css':'text/css; charset=utf-8', '.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.png':'image/png', '.svg':'image/svg+xml', '.json':'application/json; charset=utf-8', '.md':'text/markdown; charset=utf-8' };
const visible = new Set(['/','/index.html','/app.js','/styles.css','/assets/sourcewell_rfp_logo.jpg','/healthz']);
const server = http.createServer(async (req,res)=>{
  try {
    if(req.method!=='GET' && req.method!=='HEAD') {res.writeHead(405);res.end('Method not allowed');return;}
    let url=new URL(req.url,`http://${req.headers.host || 'localhost'}`);
    let route=decodeURIComponent(url.pathname);
    if(route==='/healthz') {res.writeHead(200,{'Content-Type':'text/plain; charset=utf-8'});res.end('ok');return;}
    if(!visible.has(route)) {res.writeHead(404);res.end('Not found');return;}
    let filename=path.join(root,route==='/'?'index.html':route.slice(1));
    const payload=await readFile(filename);
    res.writeHead(200,{'Content-Type':mime[path.extname(filename)]||'application/octet-stream','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});
    if(req.method==='HEAD')res.end();else res.end(payload);
  }catch(e){res.writeHead(500,{'Content-Type':'text/plain'});res.end('Server error');}
});
server.listen(port,host,()=>console.log(`Sourcewell demonstration running on http://localhost:${port}`));
