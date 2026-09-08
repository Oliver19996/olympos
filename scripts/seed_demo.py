"""起動済みAPIへZEUS/APHRODITE各1クール分の匿名データを投入する。"""
import json, urllib.request
API='http://localhost:8000'

def post(path,data):
    req=urllib.request.Request(API+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'},method='POST')
    return json.load(urllib.request.urlopen(req))

def participant(gender,role,band='25-29'):
    return {'gender_identity':gender,'target_gender':'female' if gender=='male' else 'male','age_band':band,'area':'東京23区','role':role,'required_age_bands':['25-29'],'preferred_age_bands':['25-29'],'availability':['2026-10-03T10','2026-10-04T13','2026-10-10T10'],'portrait_opt_in':False}

ids=[]
ids.append(post('/v1/participants',participant('male','host'))['id'])
for _ in range(7): ids.append(post('/v1/participants',participant('female','candidate'))['id'])
ids.append(post('/v1/participants',participant('female','host'))['id'])
for _ in range(7): ids.append(post('/v1/participants',participant('male','candidate'))['id'])
for pid in ids:
    post('/v1/surveys',{'participant_id':pid,'participation_intent':4,'payment_intent':4,'price_plan':'iap-baseline','usability_score':4,'comment':'デモ回答'})
print(json.dumps(post('/v1/simulations',{}),ensure_ascii=False,indent=2))
