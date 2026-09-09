import json, uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import CORS_ALLOW_ALL, CORS_ORIGINS, WEB_DIR
from .database import init_db, db
from .models import ParticipantIn, SurveyIn, PortraitRequest, PortraitDecision, SimulationResult
from .matching import simulate
from .portrait import provider

now=lambda: datetime.now(timezone.utc).isoformat()
app=FastAPI(title='OLYMPOS Phase 0 API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'] if CORS_ALLOW_ALL else CORS_ORIGINS,allow_methods=['*'],allow_headers=['*'])

@app.middleware('http')
async def no_store_web(request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path.endswith(('.css', '.js', '.html')) or path in ('/', ''):
        response.headers['Cache-Control'] = 'no-store, max-age=0'
        response.headers['Pragma'] = 'no-cache'
    return response

@app.on_event('startup')
def startup(): init_db()

@app.get('/health')
def health(): return {'status':'ok','service':'OLYMPOS','phase':'0'}

@app.post('/v1/participants',status_code=201)
def create_participant(x:ParticipantIn):
    pid=str(uuid.uuid4())
    with db() as c:
        c.execute('''INSERT INTO participants(id,consent_version,consented_at,gender_identity,target_gender,age_band,area,role,required_json,preferred_json,availability_json,portrait_opt_in,interested_json,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(
          pid,x.consent_version,now(),x.gender_identity,json.dumps(x.target_genders),x.age_band,x.area,x.role,
          json.dumps(x.required_age_bands),json.dumps(x.preferred_age_bands),json.dumps(x.availability),int(x.portrait_opt_in),json.dumps(x.interested_modes),now()))
    return {'id':pid,'anonymous':True}

@app.post('/v1/surveys',status_code=201)
def create_survey(x:SurveyIn):
    with db() as c:
        if x.participant_id and not c.execute('SELECT 1 FROM participants WHERE id=?',(x.participant_id,)).fetchone():
            raise HTTPException(404,'participant not found')
        c.execute('INSERT INTO survey_responses(participant_id,participation_intent,payment_intent,price_plan,usability_score,comment,created_at) VALUES(?,?,?,?,?,?,?)',
          (x.participant_id,x.participation_intent,x.payment_intent,x.price_plan,x.usability_score or 0,x.comment,now()))
    return {'status':'recorded'}

def participants():
    with db() as c: rows=c.execute('SELECT * FROM participants ORDER BY created_at').fetchall()
    result=[]
    for r in rows:
        d=dict(r); d['required_age_bands']=json.loads(d.pop('required_json')); d['preferred_age_bands']=json.loads(d.pop('preferred_json')); d['availability']=json.loads(d.pop('availability_json'))
        raw=d.get('target_gender') or '[]'
        d['target_genders']=json.loads(raw) if isinstance(raw,str) and raw.startswith('[') else [raw]
        d['interested_modes']=json.loads(d.pop('interested_json') or '[]')
        result.append(d)
    return result

@app.post('/v1/simulations',response_model=SimulationResult)
def run_simulation():
    data=participants(); groups,assigned=simulate(data); rid=str(uuid.uuid4()); rate=(assigned/len(data)) if data else 0
    metrics={'formation_rate':rate,'formed_groups':len(groups),'threshold':0.70,'passed':rate>=0.70}
    with db() as c:c.execute('INSERT INTO simulation_runs VALUES(?,?,?,?,?,?,?)',(rid,now(),'phase0-match-v1',len(data),assigned,json.dumps([g.model_dump() for g in groups]),json.dumps(metrics)))
    return SimulationResult(run_id=rid,applications=len(data),assigned=assigned,formation_rate=rate,groups=groups)

@app.get('/v1/kpis')
def kpis():
    with db() as c:
        n=c.execute('SELECT COUNT(*) n FROM participants').fetchone()['n']; surveys=c.execute('SELECT * FROM survey_responses').fetchall(); portraits=c.execute('SELECT * FROM portrait_trials').fetchall(); last=c.execute('SELECT metrics_json FROM simulation_runs ORDER BY created_at DESC LIMIT 1').fetchone()
    def ratio(items,pred): return sum(1 for x in items if pred(x))/len(items) if items else 0
    return {'participants':n,'participation_intent_rate':ratio(surveys,lambda x:x['participation_intent']>=4),'payment_intent_rate':ratio(surveys,lambda x:x['payment_intent']>=4),'portrait_approval_rate':ratio([x for x in portraits if x['approved'] is not None],lambda x:x['approved']==1),'formation_rate':json.loads(last['metrics_json'])['formation_rate'] if last else 0,'thresholds':{'participation_intent_rate':.60,'payment_intent_rate':.40,'portrait_approval_rate':.80,'formation_rate':.70}}

@app.post('/v1/portraits',status_code=201)
async def generate_portrait(x:PortraitRequest):
    with db() as c:
        p=c.execute('SELECT portrait_opt_in FROM participants WHERE id=?',(x.participant_id,)).fetchone()
        if not p: raise HTTPException(404,'participant not found')
        if not p['portrait_opt_in']: raise HTTPException(403,'portrait consent required')
        attempt=c.execute('SELECT COUNT(*) n FROM portrait_trials WHERE participant_id=?',(x.participant_id,)).fetchone()['n']+1
        if attempt>2: raise HTTPException(409,'free generation limit reached; use unified avatar')
    pp=provider(); out=await pp.generate(x.source_reference,attempt); await pp.delete_source(x.source_reference)
    with db() as c:
        cur=c.execute('INSERT INTO portrait_trials(participant_id,attempt,provider,status,asset_ref,created_at,deleted_at) VALUES(?,?,?,?,?,?,?)',(x.participant_id,attempt,out.provider,out.status,out.asset_ref,now(),now()))
    return {'id':cur.lastrowid,'attempt':attempt,'asset_ref':out.asset_ref,'source_deleted':True}

@app.post('/v1/portraits/{trial_id}/decision')
def decide_portrait(trial_id:int,x:PortraitDecision):
    with db() as c:
        if not c.execute('SELECT 1 FROM portrait_trials WHERE id=?',(trial_id,)).fetchone(): raise HTTPException(404,'trial not found')
        c.execute('UPDATE portrait_trials SET approved=?,rejection_reason=? WHERE id=?',(int(x.approved),x.rejection_reason,trial_id))
    return {'status':'approved' if x.approved else 'rejected'}

if WEB_DIR.is_dir():
    app.mount('/', StaticFiles(directory=WEB_DIR, html=True), name='web')
