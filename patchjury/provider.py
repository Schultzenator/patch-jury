"""One bounded Token Factory call; conservative durable budget reservations."""
import json, os, pathlib, sqlite3, urllib.request, urllib.parse
from contextlib import contextmanager, closing
from .fixtures import FIXTURES, validate_cases
MODEL='nvidia/Nemotron-3_5-Lightning'
BASE_URL='https://api.tokenfactory.nebius.com/v1'

def configuration():
    base=os.environ.get('NEBIUS_BASE_URL',BASE_URL).rstrip('/')
    url=urllib.parse.urlsplit(base)
    if (url.scheme!='https' or not url.hostname or url.username or url.password
            or url.query or url.fragment or url.path!='/v1'):
        raise ValueError('NEBIUS_BASE_URL must be an HTTPS API base ending in /v1, without credentials or query')
    model=os.environ.get('MODEL',MODEL)
    if not model.startswith('nvidia/'):
        raise ValueError('MODEL must select an NVIDIA model from the Token Factory catalog')
    return base+'/chat/completions',model


@contextmanager
def connection(path):
    # SQLite's transaction context does not close its connection.
    with closing(sqlite3.connect(path,timeout=20)) as db:
        with db:
            yield db

class Budget:
    def __init__(self, path='.state/budget.sqlite3'):
        self.path=pathlib.Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        with connection(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS calls(id INTEGER PRIMARY KEY, reserved_cents INTEGER NOT NULL, usage TEXT)')
    def reserve(self):
        with connection(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            used=db.execute('SELECT coalesce(sum(reserved_cents),0) FROM calls').fetchone()[0]
            if used>=1000: raise ValueError('Hard $10 budget reached')
            return db.execute('INSERT INTO calls(reserved_cents) VALUES(1)').lastrowid
    def record(self, id, usage):
        with connection(self.path) as db: db.execute('UPDATE calls SET usage=? WHERE id=?',(json.dumps(usage),id))
    def status(self):
        with connection(self.path) as db:
            n,c=db.execute('SELECT count(*),coalesce(sum(reserved_cents),0) FROM calls').fetchone()
        return {'attempts':n,'reserved_usd':c/100,'cap_usd':10,'note':'Reservations include failures; not a provider invoice. Preserve this ledger across restarts.'}

def generate(fixture, budget=None):
    if os.environ.get('NEBIUS_CREDITS_CONFIRMED')!='yes': raise ValueError('Free credits must be confirmed before live calls')
    key=os.environ.get('NEBIUS_API_KEY')
    if not key: raise ValueError('Missing NEBIUS_API_KEY')
    endpoint,model_id=configuration()
    f=FIXTURES[fixture]
    # Fail closed if current official prices exceed the reservation assumptions.
    catalog_req=urllib.request.Request('https://tokenfactory.nebius.com/api/public/models_info')
    with urllib.request.urlopen(catalog_req,timeout=15) as response:
        catalog=json.loads(response.read(2000000))
    flavors=[flavor for model in catalog for flavor in model.get('flavors',[]) if flavor.get('model_id')==model_id]
    if len(flavors)!=1 or flavors[0].get('input_price_per_million_tokens',float('inf'))>0.06 or flavors[0].get('output_price_per_million_tokens',float('inf'))>0.24:
        raise ValueError('Model catalog or pricing changed; live calls disabled pending review')
    prompt='Return only JSON: {"cases": [[arguments], ...]}. Propose 3 to 8 diverse boundary inputs to reveal bugs under this specification. Do not return code, expected outputs, or prose. '+f['spec']+'\nImplementation:\n'+f['base']
    body=json.dumps({'model':model_id,'messages':[{'role':'user','content':prompt}],'temperature':0,'max_tokens':4096,'response_format':{'type':'json_object'}}).encode()
    if len(body)>20000: raise ValueError('Prompt exceeds budget bound')
    budget=budget or Budget(); reservation=budget.reserve()
    req=urllib.request.Request(endpoint,data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    # No automatic retries. Reserve 1 cent even on timeout. At catalog prices,
    # <=20k input bytes plus <=4096 output tokens is less than this reservation.
    with urllib.request.urlopen(req,timeout=60) as response:
        raw=response.read(1000001)
    if len(raw)>1000000: raise ValueError('Response too large')
    data=json.loads(raw); usage=data.get('usage',{}); budget.record(reservation,usage)
    if data.get('model')!=model_id: raise ValueError('Provider returned an unexpected model ID')
    content=data['choices'][0]['message']['content']
    cases=validate_cases(fixture,json.loads(content)['cases'])
    return cases, {'mode':'live','provider':'Nebius Token Factory','model':data['model'],'request_id':data.get('id'),'usage':usage,'endpoint':endpoint,'budget':budget.status()}
