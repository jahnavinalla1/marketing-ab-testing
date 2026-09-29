"""Standard-library utilities shared by the five reproducible case studies."""
import csv, html, json, sqlite3
from pathlib import Path

def write_csv(path, rows):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def database(folder, table, schema):
    """Load the full CSV into a typed, constrained, ephemeral SQLite database."""
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE '+table+' ('+schema+')')
    with (folder/'data.csv').open(newline='') as f:
        reader=csv.DictReader(f); columns=reader.fieldnames
        db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in columns)+')',
                       ([r[c] for c in columns] for r in reader))
    return db

def queries(db,path):
    """Execute the actual reviewed SQL file; each -- name: block is one query."""
    result={}
    for part in path.read_text().split('-- name: ')[1:]:
        name,sql=part.split('\n',1)
        result[name.strip()]=[dict(r) for r in db.execute(sql)]
    return result

def publish(folder,title,question,kpis,tables,findings,actions,limitations,chart):
    out=folder/'results';out.mkdir(exist_ok=True)
    payload={'title':title,'question':question,'kpis':kpis,'tables':tables,
             'findings':findings,'actions':actions,'limitations':limitations,'chart':chart}
    (out/'metrics.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    for name,rows in tables.items():
        if rows: write_csv(out/(name+'.csv'),rows)
    report='# '+title+'\n\n**Simulated portfolio case study — no client data or measured commercial impact.**\n\n'
    report+='## Decision\n\n'+question+'\n\n## Results\n\n'
    report+='\n'.join('- **'+k+':** '+str(v) for k,v in kpis.items())+'\n\n## Findings\n\n'
    report+='\n'.join('- '+v for v in findings)+'\n\n## Recommended next steps\n\n'
    report+='\n'.join('- '+v for v in actions)+'\n\n## Limits\n\n'+limitations+'\n'
    (out/'report.md').write_text(report)
    template=(folder/'dashboard-template.html').read_text()
    safe=json.dumps(payload,allow_nan=False).replace('<','\\u003c')
    page=template.replace('__TITLE__',html.escape(title)).replace('__DATA__',safe)
    (folder/'index.html').write_text(page)
