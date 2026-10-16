#!/usr/bin/env python3
"""Static site generator for EnterpriseMCP. python3 site/build.py -> site/dist"""
import json, pathlib, html, shutil, sys, re
R=pathlib.Path(__file__).resolve().parent; ROOT=R.parent
sys.path.insert(0,str(ROOT/'scripts')); from score import RUBRIC
PREFIX='/enterprisemcp'  # GitHub Pages project subpath
BASE='https://diegocroce.github.io'+PREFIX
D=json.load(open(ROOT/'data/servers.json')); S=sorted(D['servers'],key=lambda s:-s['score'])
OUT=R/'dist'; shutil.rmtree(OUT,ignore_errors=True); OUT.mkdir()
e=lambda x:html.escape(str(x if x is not None else 'unknown'))
slug=lambda x:re.sub(r'[^a-z0-9]+','-',x.lower()).strip('-')
systems=sorted({s['system'] for s in S}); pages=[]
CSS="""*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;color:#0f172a;background:#f8fafc}
a{color:#1d4ed8;text-decoration:none}a:hover{text-decoration:underline}header{background:#0f172a;color:#fff}header .w{display:flex;gap:20px;align-items:center;padding:14px 20px}
header a{color:#cbd5e1}header .logo{color:#fff;font-weight:700;font-size:18px;margin-right:auto}.w{max-width:1120px;margin:0 auto;padding:0 20px}
.hero{padding:36px 0 12px}.hero h1{margin:0 0 6px;font-size:30px}.muted{color:#64748b}.filters{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}
input,select,button,textarea{font:inherit;padding:8px 10px;border:1px solid #cbd5e1;border-radius:8px;background:#fff}input[type=search]{flex:1;min-width:220px}
button{background:#1d4ed8;color:#fff;border:0;cursor:pointer}table{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 2px #0001}
th,td{padding:9px 10px;border-bottom:1px solid #e2e8f0;text-align:left;vertical-align:top}th{background:#f1f5f9;font-size:13px}
.b{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;background:#e2e8f0}.off{background:#dcfce7;color:#166534}.sc{font-weight:700;padding:2px 8px;border-radius:6px;color:#fff}
.card{background:#fff;border-radius:10px;padding:20px;box-shadow:0 1px 2px #0001;margin:16px 0}dl{display:grid;grid-template-columns:180px 1fr;gap:6px 12px}dt{color:#64748b}
footer{margin:40px 0 0;padding:24px 0;background:#0f172a;color:#94a3b8}footer form{display:flex;gap:8px;margin-top:8px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}"""
(OUT/'style.css').write_text(CSS)
def col(n): return '#16a34a' if n>=70 else '#ca8a04' if n>=45 else '#dc2626'
def badge(s): return f'<span class="sc" style="background:{col(s["score"])}">{s["score"]}</span>'
def page(path,title,desc,body):
    nav='<a href="/">Directory</a><a href="/systems/">Systems</a><a href="/methodology/">Methodology</a><a href="/submit/">Submit</a><a href="/sponsor/">Sponsor</a><a href="https://buttondown.com/enterprisemcp">Subscribe</a>'
    doc=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<link rel="stylesheet" href="/style.css"></head><body><header><div class="w"><a class="logo" href="/">EnterpriseMCP</a>{nav}</div></header>
<main class="w">{body}</main><footer><div class="w"><strong style="color:#fff">The EnterpriseMCP newsletter</strong> — new and re-rated enterprise MCP servers, monthly.
<form action="https://buttondown.com/api/emails/embed-subscribe/enterprisemcp" method="post" target="_blank"><input type="email" name="email" required placeholder="you@company.com" aria-label="Email"><button type="submit">Subscribe</button></form>
</div></footer></body></html>"""
    f=OUT/path.strip('/')/'index.html' if path.endswith('/') else OUT/path; f.parent.mkdir(parents=True,exist_ok=True); doc=re.sub(r'(href|src|action)="/(?!/)',lambda m:f'{m.group(1)}="{PREFIX}/',doc).replace('href="{BASE}'.replace('{BASE}',BASE+PREFIX),'href="'+BASE); f.write_text(doc); pages.append(path)
def row(s):
    return f'<tr><td>{badge(s)}</td><td><a href="/servers/{s["id"]}/">{e(s["name"])}</a><div class="muted">{e(s["maintainer"])}</div></td><td><a href="/systems/{slug(s["system"])}/">{e(s["system"])}</a></td><td>{"<span class=\'b off\'>official</span>" if s["official"] else "<span class=b>community</span>"}</td><td>{e(s["auth"])}</td><td>{e(s["access"])}</td><td>{e(s["hosting"])}</td><td>{e(s["stars"] if s["stars"] is not None else "—")}</td></tr>'
TH='<table><thead><tr><th>Score</th><th>Server</th><th>System</th><th>Type</th><th>Auth</th><th>Access</th><th>Hosting</th><th>★</th></tr></thead><tbody id="rows">'
lean=[{k:s[k] for k in ('id','name','maintainer','system','official','auth','access','hosting','stars','score')} for s in S]
opt=lambda xs:''.join(f'<option>{e(x)}</option>' for x in xs)
home=f"""<section class="hero"><h1>The rated directory of enterprise MCP servers</h1><p class="muted">{len(S)} MCP servers for Salesforce, SAP, Oracle Siebel/Fusion, ServiceNow, Dynamics, Workday, HubSpot, Zendesk, Atlassian, ERP and databases — each scored 0–100 for enterprise readiness. <a href="/methodology/">How we score</a>.</p></section>
<div class="filters"><input type="search" id="q" placeholder="Search servers, vendors, systems…" aria-label="Search">
<select id="fs"><option value="">All systems</option>{opt(systems)}</select>
<select id="fa"><option value="">Any auth</option><option value="oauth">OAuth / SSO</option><option value="token">Token / API key</option><option value="unknown">Unknown</option></select>
<select id="fw"><option value="">Any access</option><option value="read-only">Read-only</option><option value="read-write">Read-write</option><option value="configurable">Configurable</option></select>
<select id="fo"><option value="">Official + community</option><option value="1">Official only</option><option value="0">Community only</option></select></div>
<p class="muted" id="cnt"></p>{TH}{''.join(row(s) for s in S)}</tbody></table>
<script>const D={json.dumps(lean)};const $=i=>document.getElementById(i);const esc=t=>String(t??'unknown').replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
const sl=t=>t.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');const col=n=>n>=70?'#16a34a':n>=45?'#ca8a04':'#dc2626';
function r(){{const q=$('q').value.toLowerCase(),fs=$('fs').value,fa=$('fa').value,fw=$('fw').value,fo=$('fo').value;
const x=D.filter(s=>(!q||(s.name+s.maintainer+s.system).toLowerCase().includes(q))&&(!fs||s.system==fs)&&(!fo||String(+s.official)==fo)&&(!fw||s.access.toLowerCase().includes(fw))
&&(!fa||(fa=='oauth'?/oauth|entra|iam|azure ad|xsuaa/i.test(s.auth):fa=='token'?/token|key|credential|connection|pat|basic/i.test(s.auth):s.auth=='unknown')));
$('cnt').textContent=x.length+' of '+D.length+' servers';$('rows').innerHTML=x.map(s=>`<tr><td><span class=sc style="background:${{col(s.score)}}">${{s.score}}</span></td><td><a href="/servers/${{s.id}}/">${{esc(s.name)}}</a><div class=muted>${{esc(s.maintainer)}}</div></td><td><a href="/systems/${{sl(s.system)}}/">${{esc(s.system)}}</a></td><td>${{s.official?'<span class="b off">official</span>':'<span class=b>community</span>'}}</td><td>${{esc(s.auth)}}</td><td>${{esc(s.access)}}</td><td>${{esc(s.hosting)}}</td><td>${{s.stars??'—'}}</td></tr>`).join('')}}
['q','fs','fa','fw','fo'].forEach(i=>$(i).addEventListener('input',r));r();</script>"""
page('/','EnterpriseMCP — Rated directory of enterprise MCP servers','Find and compare MCP servers for Salesforce, SAP, Oracle Siebel, ServiceNow, Dynamics, Workday, HubSpot, Zendesk, Jira and databases, scored for enterprise readiness.',home)
for s in S:
    bd=''.join(f'<tr><td>{e(k)}</td><td>{v}</td></tr>' for k,v in s['score_breakdown'].items())
    rows=[('System',f'<a href="/systems/{slug(s["system"])}/">{e(s["system"])}</a>'),('Maintainer',e(s['maintainer'])),('Official',"yes" if s['official'] else "no (community)"),
     ('Repo / docs',f'<a href="{e(s["url"])}" rel="nofollow noopener">{e(s["url"])}</a>'),('Auth model',e(s['auth'])),('Access',e(s['access'])),('Hosting',e(s['hosting'])),
     ('Audit logging',e(s['audit_logging'])),('Last updated',e(s['last_updated'])),('GitHub stars',e(s['stars'] if s['stars'] is not None else 'n/a')),('License',e(s['license'])),('Archived','yes' if s.get('archived') else 'no')]
    body=f'<section class="hero"><h1>{e(s["name"])} {badge(s)}</h1><p class="muted">{e(s["notes"]) if s["notes"] else ""}</p></section><div class="card"><dl>{"".join(f"<dt>{a}</dt><dd>{b}</dd>" for a,b in rows)}</dl></div><div class="card"><h2>Score breakdown</h2><table>{bd}</table><p><a href="/methodology/">Rubric</a> · Something wrong? <a href="/submit/">Send a correction</a>.</p></div>'
    page(f'/servers/{s["id"]}/',f'{s["name"]} — {s["system"]} MCP server review | EnterpriseMCP',f'{s["name"]} ({s["system"]}, {"official" if s["official"] else "community"}): auth {s["auth"]}, {s["access"]}, enterprise-readiness score {s["score"]}/100.',body)
cards=''
for sy in systems:
    xs=[s for s in S if s['system']==sy]; cards+=f'<a class="card" href="/systems/{slug(sy)}/"><strong>{e(sy)}</strong><div class="muted">{len(xs)} servers · top score {xs[0]["score"]}</div></a>'
    page(f'/systems/{slug(sy)}/',f'Best {sy} MCP servers ({len(xs)}) | EnterpriseMCP',f'Compare {len(xs)} MCP servers for {sy}: official vs community, auth, read/write access and enterprise-readiness scores.',f'<section class="hero"><h1>{e(sy)} MCP servers</h1></section>{TH}{"".join(row(s) for s in xs)}</tbody></table>')
page('/systems/','MCP servers by enterprise system | EnterpriseMCP','Browse enterprise MCP servers by system.',f'<section class="hero"><h1>Systems</h1></section><div class="grid">{cards}</div>')
rub=''.join(f'<tr><td>{e(d)}</td><td>{p}</td></tr>' for _,d,p in RUBRIC)
page('/methodology/','Methodology & scoring rubric | EnterpriseMCP','How EnterpriseMCP scores MCP servers for enterprise readiness (0–100).',f'''<section class="hero"><h1>Methodology</h1></section><div class="card">
<p>Every entry links to a verified GitHub repo or vendor documentation page. GitHub stars, last push date, license and archived status come from the GitHub API (refreshed by <code>scripts/refresh</code>). Auth, access and hosting come from READMEs and vendor docs. <strong>Anything we could not verify is recorded as "unknown" and scores 0</strong> for that criterion — a low score can mean "undocumented", not "bad".</p>
<h2>Enterprise-readiness score (0–100)</h2><table><tr><th>Criterion</th><th>Max points</th></tr>{rub}<tr><td>Archived repository</td><td>−30</td></tr></table>
<p>For vendor-hosted services without a public repo, "last updated" is the documentation page's date, and adoption is a flat 8.</p></div>''')
page('/submit/','Submit an MCP server | EnterpriseMCP','Suggest an enterprise MCP server or a correction.','''<section class="hero"><h1>Submit a server</h1><p class="muted">Placeholder form — nothing is sent yet.</p></section><form class="card" onsubmit="event.preventDefault();this.innerHTML='<p>Thanks! (placeholder — no data was sent)</p>'" style="display:grid;gap:10px;max-width:560px">
<input required placeholder="Server name"><input required type="url" placeholder="Repo or docs URL"><input placeholder="System (e.g. Siebel, SAP S/4HANA)"><select><option>Community</option><option>Official / vendor</option></select><textarea rows="4" placeholder="Auth model, read/write, hosting, audit logging…"></textarea><input type="email" placeholder="Your email (optional)"><button>Submit</button></form>''')
page('/sponsor/','Sponsor EnterpriseMCP','Reach enterprise architects and integration teams evaluating MCP servers.','''<section class="hero"><h1>Sponsor EnterpriseMCP</h1></section><div class="card"><p>EnterpriseMCP is read by architects and integration teams choosing how to connect AI assistants to CRM, ERP and ITSM systems.</p>
<ul><li><strong>Featured listing</strong> — clearly labelled "Sponsored"; never affects scores.</li><li><strong>Newsletter placement</strong> in the monthly digest.</li><li><strong>Integration services</strong> — Siebel, Oracle and CRM MCP rollouts.</li></ul><p>Contact: placeholder (form coming soon).</p></div>''')
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{p}</loc><lastmod>{D["generated"]}</lastmod></url>' for p in pages)+'</urlset>\n')
(OUT/'servers.json').write_text(json.dumps(D))
print(len(pages),'pages')
