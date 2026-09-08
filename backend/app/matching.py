import json
from collections import defaultdict
from .models import MatchGroup

AGE_ORDER = {'20-24':0,'25-29':1,'30-34':2,'35-39':3}

def _as_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.startswith('['):
        return json.loads(value)
    return [value] if value else []

def _wants(targets, identity):
    return 'anyone' in targets or identity in targets

def _hard_match(host, candidate):
    host_wants = _as_list(host.get('target_genders') or host.get('target_gender'))
    cand_wants = _as_list(candidate.get('target_genders') or candidate.get('target_gender'))
    return (
        host['role'] == 'host' and candidate['role'] == 'candidate'
        and _wants(host_wants, candidate['gender_identity'])
        and _wants(cand_wants, host['gender_identity'])
        and candidate['age_band'] in host['required_age_bands']
        and host['age_band'] in candidate['required_age_bands']
        and host['area'] == candidate['area']
        and len(set(host['availability']) & set(candidate['availability'])) >= 1
    )

def _score(host, candidate):
    shared = len(set(host['availability']) & set(candidate['availability']))
    preference = int(candidate['age_band'] in host['preferred_age_bands']) + int(host['age_band'] in candidate['preferred_age_bands'])
    age_distance = abs(AGE_ORDER[host['age_band']] - AGE_ORDER[candidate['age_band']])
    return (shared * 10) + (preference * 5) - age_distance

def simulate(participants):
    """申込順を基本に、必須条件を満たす6〜7名を編成する。入力順=申込順。"""
    hosts = [p for p in participants if p['role'] == 'host']
    candidates = [p for p in participants if p['role'] == 'candidate']
    used = set(); groups=[]
    for host in hosts:
        pool = [c for c in candidates if c['id'] not in used and _hard_match(host,c)]
        pool.sort(key=lambda c: _score(host,c), reverse=True)
        selected = pool[:7]
        if len(selected) < 6:
            continue
        shared_count = defaultdict(int)
        for c in selected:
            for slot in set(host['availability']) & set(c['availability']): shared_count[slot] += 1
        viable = sorted([s for s,n in shared_count.items() if n >= 1])
        modes = _as_list(host.get('interested_modes'))
        if host['gender_identity']=='male' or ('ZEUS' in modes and 'APHRODITE' not in modes):
            ctype, name = 'MALE_HOST', 'ZEUS'
        elif host['gender_identity']=='female' or 'APHRODITE' in modes:
            ctype, name = 'FEMALE_HOST', 'APHRODITE'
        else:
            ctype, name = 'MALE_HOST', 'ZEUS'
        groups.append(MatchGroup(course_type=ctype, display_name=name, host_id=host['id'], candidate_ids=[c['id'] for c in selected], shared_slots=viable[:5]))
        used.update(c['id'] for c in selected); used.add(host['id'])
    assigned = sum(1+len(g.candidate_ids) for g in groups)
    return groups, assigned
