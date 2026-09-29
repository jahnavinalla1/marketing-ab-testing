import random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import write_csv

def generate():
    rng=random.Random(3303);rows=[]
    for i in range(6000):
        variant='B' if rng.random()<.5 else 'A';device=rng.choice(['Desktop','Mobile'])
        probability=.11+(.014 if variant=='B' else 0)+(.02 if device=='Desktop' else 0)
        converted=int(rng.random()<probability)
        rows.append(dict(user_id=f'U{i:05}',variant=variant,device=device,converted=converted,
            revenue_cents=converted*rng.choice([4900,7900,9900]),acquisition_cents=220))
    write_csv(Path(__file__).with_name('data.csv'),rows)
if __name__=='__main__':generate()
