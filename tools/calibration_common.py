"""Durable records for the registered V9 investigations."""
import json
from closure_common import ROOT, save, digest, default
from reliability_common import summarize

SPEC = 'docs/studies/calibration-repair-spec.json'


class Journal:
    def __init__(self, name, inputs, pilot=False):
        self.inputs = sorted(set(inputs+[SPEC, 'tools/calibration_common.py',
            'tools/closure_common.py', 'tools/reliability_common.py']))
        self.path = ROOT / ('docs/studies/calibration-'+name+('-pilot' if pilot else '-final')+'.jsonl')
        identity = {p: digest(p) for p in self.inputs}
        self.rows = {}
        if self.path.exists():
            lines = self.path.read_text().splitlines()
            if json.loads(lines[0])['input_sha256'] != identity:
                raise ValueError('Changed inputs: preserve the old journal and register fresh evaluation')
            for line in lines[1:]:
                row = json.loads(line)
                if row['key'] in self.rows:
                    raise ValueError('Duplicate contribution')
                self.rows[row['key']] = row['result']
        else:
            self.path.write_text(json.dumps({'input_sha256': identity})+'\n')

    def run(self, key, compute):
        if key not in self.rows:
            result = compute()
            encoded = json.dumps({'key': key, 'result': result}, default=default, allow_nan=False)
            with self.path.open('a') as stream:
                stream.write(encoded+'\n')
                stream.flush()
            self.rows[key] = json.loads(encoded)['result']
            if len(self.rows) % 50 == 0:
                print(json.dumps({'journal': self.path.stem, 'saved': len(self.rows)}), flush=True)
        return self.rows[key]

    def finish(self, result):
        name = str(self.path.relative_to(ROOT)).replace('-final.jsonl', '-results.json').replace('.jsonl', '.json')
        save(name, result, self.inputs+[str(self.path.relative_to(ROOT))])
        print(json.dumps({'saved': name, 'requests': len(self.rows)}), flush=True)
