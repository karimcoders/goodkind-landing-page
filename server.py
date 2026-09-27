"""Goodkind single-page website and private enquiry storage. Python standard library only."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, deque
import csv, io, json, os, re, sqlite3, threading, time, uuid

ROOT=Path(__file__).resolve().parent
SITE=ROOT
PRIVATE=ROOT/'landing-private'
PRIVATE.mkdir(exist_ok=True,mode=0o700)
os.chmod(PRIVATE,0o700)
DB=PRIVATE/'enquiries.sqlite3'
LOCK=threading.Lock()
RATES=defaultdict(deque)
OCCASIONS={'Employee welcome','Festive gifting','Client appreciation','Team milestone','Something custom'}
BUDGETS={'Under ₹1,000','₹1,000 – ₹2,500','₹2,500 – ₹5,000','₹5,000+',"Let's discuss"}
FIELDS=['reference','created_utc','name','company','email','occasion','quantity','budget','notes']
with sqlite3.connect(DB) as con:
    con.execute('CREATE TABLE IF NOT EXISTS enquiries (reference TEXT PRIMARY KEY,created_utc TEXT,name TEXT,company TEXT,email TEXT,occasion TEXT,quantity INTEGER,budget TEXT,notes TEXT)')
os.chmod(DB,0o600)

def save(data):
    ref='GK-'+uuid.uuid4().hex[:10].upper()
    values=[ref,datetime.now(timezone.utc).isoformat(),data['name'],data['company'],data['email'],data['occasion'],data['quantity'],data['budget'],data['notes']]
    with LOCK:
        with sqlite3.connect(DB) as con:
            con.execute('INSERT INTO enquiries VALUES (?,?,?,?,?,?,?,?,?)',values)
            rows=con.execute('SELECT '+','.join(FIELDS)+' FROM enquiries ORDER BY created_utc').fetchall()
        # A workspace-only export for the site owner. Never exposed as a web route.
        path=PRIVATE/'enquiries.csv';tmp=PRIVATE/'enquiries.csv.tmp'
        def safe(v):
            if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')):return "'"+v
            return v
        with tmp.open('w',newline='',encoding='utf-8-sig') as f:
            writer=csv.writer(f);writer.writerow(FIELDS)
            writer.writerows([[safe(v) for v in row] for row in rows])
        os.chmod(tmp,0o600);tmp.replace(path)
    return ref

class Handler(BaseHTTPRequestHandler):
    server_version='Goodkind/1.0'
    def log_message(self,format,*args):
        # Do not log personal form values.
        super().log_message(format,*args)
    def respond(self,status,body,kind='application/json; charset=utf-8',head=False):
        if isinstance(body,dict):body=json.dumps(body,ensure_ascii=False).encode()
        if isinstance(body,str):body=body.encode()
        self.send_response(status)
        self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        origin=self.headers.get('Origin','')
        if origin=='https://karimcoders.github.io':
            self.send_header('Access-Control-Allow-Origin',origin)
            self.send_header('Vary','Origin')
            self.send_header('Access-Control-Allow-Methods','POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy','camera=(), microphone=(), geolocation=()')
        self.send_header('Content-Security-Policy',"default-src 'self'; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; form-action 'self'; base-uri 'none'; object-src 'none'")
        self.end_headers()
        if not head:self.wfile.write(body)
    def do_OPTIONS(self):
        if self.path=='/api/enquiry' and self.headers.get('Origin')=='https://karimcoders.github.io':
            return self.respond(204,b'')
        return self.respond(403,{'error':'Origin not allowed'})
    def do_HEAD(self):self.do_GET(head=True)
    def do_GET(self,head=False):
        path=self.path.split('?',1)[0]
        if path in ['/','/index.html']:
            return self.respond(200,(SITE/'index.html').read_bytes(),'text/html; charset=utf-8',head)
        if path=='/api/health':return self.respond(200,{'ok':True,'service':'goodkind'},head=head)
        if path=='/favicon.ico':return self.respond(204,b'','image/x-icon',head)
        if path=='/robots.txt':return self.respond(200,'User-agent: *\nDisallow: /\n','text/plain; charset=utf-8',head)
        return self.respond(404,{'error':'Not found'},head=head)
    def do_POST(self):
        if self.path!='/api/enquiry':return self.respond(404,{'error':'Not found'})
        try:length=int(self.headers.get('Content-Length','0'))
        except ValueError:return self.respond(400,{'error':'Invalid request.'})
        if length<1 or length>16000:return self.respond(413,{'error':'Please keep your enquiry shorter.'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.respond(415,{'error':'Please submit through the website form.'})
        try:data=json.loads(self.rfile.read(length))
        except (json.JSONDecodeError,UnicodeDecodeError):return self.respond(400,{'error':'Please check your enquiry and try again.'})
        if not isinstance(data,dict):return self.respond(400,{'error':'Invalid enquiry.'})
        if data.get('website'):return self.respond(400,{'error':'Unable to accept this enquiry.'})
        clean={}
        for name,limit in [('name',80),('company',100),('email',150),('occasion',80),('budget',80),('notes',1500)]:
            value=data.get(name,'')
            if not isinstance(value,str) or len(value)>limit:return self.respond(400,{'error':'Please check the '+name+' field.'})
            clean[name]=value.strip()
        if not clean['name'] or not clean['company']:return self.respond(400,{'error':'Please enter your name and company.'})
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',clean['email']):return self.respond(400,{'error':'Please enter a valid email address.'})
        if clean['occasion'] not in OCCASIONS or clean['budget'] not in BUDGETS:return self.respond(400,{'error':'Please select an occasion and budget.'})
        if isinstance(data.get('quantity'),bool):return self.respond(400,{'error':'Please enter a valid number of gifts.'})
        try:
            q=str(data.get('quantity',''))
            if not q.isdigit():raise ValueError()
            quantity=int(q)
            if not 1<=quantity<=100000:raise ValueError()
        except (TypeError,ValueError):return self.respond(400,{'error':'Please enter a gift quantity between 1 and 100,000.'})
        clean['quantity']=quantity
        ip=self.headers.get('CF-Connecting-IP') or self.client_address[0]
        with LOCK:
            now=time.time();history=RATES[ip]
            while history and history[0]<now-3600:history.popleft()
            if len(history)>=10:return self.respond(429,{'error':'Too many enquiries. Please try again in an hour.'})
            history.append(now)
        try:reference=save(clean)
        except Exception:
            return self.respond(500,{'error':'Your enquiry could not be recorded. Please try again shortly.'})
        return self.respond(201,{'ok':True,'reference':reference})

if __name__=='__main__':
    print('Goodkind website and enquiry form listening on 0.0.0.0:3000',flush=True)
    ThreadingHTTPServer(('0.0.0.0',3000),Handler).serve_forever()
