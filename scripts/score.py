"""Enterprise-readiness rubric (0-100). Unknown always scores 0 for that criterion."""
import math, datetime
TODAY=datetime.date.today()
def _date(s):
    try: return datetime.date.fromisoformat(s[:10])
    except Exception:
        try: return datetime.date(int(s[:4]),int(s[5:7]),1)
        except Exception: return None
RUBRIC=[('official','Official / vendor-maintained',25),('maintenance','Recently maintained (<=30d 20, <=90d 14, <=365d 6)',20),
 ('auth','Auth model: OAuth/Entra/IAM 20, tokens/keys 12, none/unknown 0',20),('governance','Scoped access: read-only or configurable permissions 10, read-write 4',10),
 ('audit','Audit logging documented',10),('adoption','Adoption: log10(stars) scaled, max 10; vendor-hosted 8',10),('license','Clear license (OSI or vendor service) 5',5)]
def score(s):
    b={}
    b['official']=25 if s['official'] else 0
    d=_date(s.get('last_updated') or ''); age=(TODAY-d).days if d else None
    b['maintenance']=0 if age is None else 20 if age<=30 else 14 if age<=90 else 6 if age<=365 else 0
    a=(s.get('auth') or '').lower()
    b['auth']=20 if any(k in a for k in ['oauth','entra','iam','azure ad','xsuaa']) else 12 if any(k in a for k in ['token','key','credential','connection','pat','basic']) else 0
    w=(s.get('access') or '').lower()
    b['governance']=10 if ('read-only' in w or 'configurable' in w) else 4 if 'read-write' in w else 0
    b['audit']=10 if s.get('audit_logging')=='yes' else 0
    st=s.get('stars')
    b['adoption']=min(10,round(2.5*math.log10(st+1),1)) if st is not None else (8 if 'hosted' in s['hosting'] else 0)
    b['license']=5 if s.get('license') not in (None,'unknown','NOASSERTION') else 0
    t=sum(b.values())
    if s.get('archived'): t-=30; b['archived_penalty']=-30
    return max(0,round(t)),b
