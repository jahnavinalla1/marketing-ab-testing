import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import database,queries,publish
F=Path(__file__).resolve().parent
SCHEMA='user_id TEXT PRIMARY KEY,variant TEXT CHECK(variant IN("A","B")),device TEXT,converted INTEGER CHECK(converted IN(0,1)),revenue_cents INTEGER CHECK(revenue_cents>=0),acquisition_cents INTEGER'
def compare(xa,na,xb,nb):
    if min(na,nb)<=0:raise ValueError('Both variants need observations')
    if not (0<=xa<=na and 0<=xb<=nb):raise ValueError('Invalid conversion counts')
    pa,pb=xa/na,xb/nb;delta=pb-pa;pooled=(xa+xb)/(na+nb)
    se=math.sqrt(pa*(1-pa)/na+pb*(1-pb)/nb)
    pooled_se=math.sqrt(pooled*(1-pooled)*(1/na+1/nb))
    p=math.erfc(abs(delta/pooled_se)/math.sqrt(2)) if pooled_se else 1.0
    expected=(na+nb)/2;chi=(na-expected)**2/expected+(nb-expected)**2/expected
    srm=math.erfc(math.sqrt(chi/2))
    adequate=min(xa,na-xa,xb,nb-xb)>=10
    low,high=delta-1.96*se,delta+1.96*se
    decision='Investigate assignment' if srm<.01 else ('Insufficient counts' if not adequate else ('Evidence of improvement' if low>0 else ('Evidence of harm' if high<0 else 'Inconclusive')))
    return {'lift_pp':round(delta*100,3),'ci_low_pp':round(low*100,3),'ci_high_pp':round(high*100,3),
       'two_sided_p':round(p,6),'srm_p':round(srm,6),'normal_approximation_valid':adequate,'decision':decision}
def run():
    db=database(F,'experiment',SCHEMA);t=queries(db,F/'analysis.sql');a,b=t['variants'];s=compare(a['conversions'],a['users'],b['conversions'],b['users']);t['inference']=[s]
    assert a['users']+b['users']==6000
    assert db.execute('SELECT COUNT(*) FROM experiment WHERE converted=0 AND revenue_cents>0').fetchone()[0]==0
    publish(F,'Marketing landing-page A/B experiment','Does variant B improve conversion enough to justify a rollout?',
    {'Participants':'6,000','Absolute lift':f"{s['lift_pp']:+.2f} pp",'95% lift interval':f"[{s['ci_low_pp']:.2f}, {s['ci_high_pp']:.2f}] pp",'Decision':s['decision']},t,
    [f"A converts at {a['conversion_pct']:.2f}%; B converts at {b['conversion_pct']:.2f}%.",
     f"Two-sided pooled z-test p={s['two_sided_p']}; 50/50 sample-ratio mismatch p={s['srm_p']}.",
     'Revenue per user is a descriptive secondary metric; device cuts are exploratory and are not separately tested.'],
    [f"Current statistical assessment: {s['decision'].lower()}. Decide practical value against an agreed minimum effect before rollout.",
     'For a real trial, pre-register sample size, stopping rule, primary conversion event and refund/latency guardrails.',
     'Do not extend the same experiment until significance appears; plan a separately powered follow-up if needed.'],
    'Simulated independent user-level assignment, one observation per user and one fixed analysis. Uses a two-sided pooled z-test and unpooled normal 95% confidence interval; count adequacy is checked. No commercial results are claimed. Costs are illustrative and gross revenue is not profit.',
    {'title':'Conversion rate by variant','note':'Primary metric: converting users / all assigned users (intention to treat).','unit':'%',
     'rows':[{'label':'Variant '+r['variant'],'value':r['conversion_pct']} for r in t['variants']]})
    return t
if __name__=='__main__':run()
