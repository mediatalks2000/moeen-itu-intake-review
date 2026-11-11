"""Offline audit of historical output; no LLM or network calls."""
import json
from pathlib import Path
from intake_sandbox import review
p=Path(__file__).resolve().parent
config=json.loads((p/'experiment.json').read_text())
policies=json.loads((p/'public_policy_seed.json').read_text())
integrated=json.loads((p/'results.json').read_text())['cases']
baseline=json.loads((p/'baseline-results.json').read_text())['cases']
assert len(config['cases'])==len(integrated)==len(baseline)==4
code_map={'DEMO_DOCUMENT_MISSING':'missing_document','DOCUMENT_CONFLICT':'document_conflict','AUTHORITY_LIMIT':'authority_limit','SOURCE_RECHECK':'source_recheck','NO_CURRENT_GUIDANCE':'no_current_guidance'}
for case,record,raw in zip(config['cases'],integrated,baseline):
    assert case['id']==record['id']==raw['id']
    fixture={k:v for k,v in case.items() if k not in ('expected','stale')}
    assert record['input']==raw['input']==fixture
    sources=[dict(s,checked='2025-01-01') for s in policies] if case.get('stale') else policies
    result=review(dict(fixture,synthetic=True),{'role':'reviewer','allowed_cases':[case['id']]},sources,'2026-11-04')
    assert set(code_map[f['code']] for f in result['findings'])==set(case['expected'])
    saved=record['review_output']
    assert result['findings']==saved['findings']
    assert set(s['id'] for s in result['citations'])==set(saved['citation_ids'])
    assert saved['human_review_required'] is True
    assert saved['eligibility_decision'] is None
    assert saved['payment_executed'] is False
    assert record['pass'] is all(record['checks'].values())
    assert raw['pass'] is all(raw['checks'].values())
assert sum(r['pass'] for r in integrated)==4
assert sum(r['pass'] for r in baseline)==0
print('PASS: 4 historical cases audited and deterministic review replayed; no new model calls.')
