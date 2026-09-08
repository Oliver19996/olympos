from app.matching import simulate

def p(i,role,gender,target):
    return {'id':i,'role':role,'gender_identity':gender,'target_gender':target,'age_band':'25-29','area':'東京23区','required_age_bands':['25-29'],'preferred_age_bands':['25-29'],'availability':['a','b','c']}

def test_forms_zeus_with_six_candidates():
    data=[p('h','host','male','female')]+[p(f'c{i}','candidate','female','male') for i in range(6)]
    groups,assigned=simulate(data)
    assert len(groups)==1 and groups[0].display_name=='ZEUS'
    assert len(groups[0].candidate_ids)==6 and assigned==7

def test_does_not_form_with_five_candidates():
    data=[p('h','host','male','female')]+[p(f'c{i}','candidate','female','male') for i in range(5)]
    groups,assigned=simulate(data)
    assert groups==[] and assigned==0
