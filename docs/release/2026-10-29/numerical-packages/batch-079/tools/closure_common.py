"""Receipts for the C revision; scientific outcomes are not pass flags."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))


def digest(path):
    with (ROOT / path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def default(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(type(value).__name__)


def save(path, result, inputs):
    result['input_sha256'] = {p: digest(p) for p in sorted(set(inputs))}
    (ROOT / path).write_text(json.dumps(result, default=default, indent=2, allow_nan=False)+'\n')


def coverage(count, total):
    from scipy.stats import beta
    return {'count': int(count), 'requests': int(total), 'frequency': count/total,
            'mc95': [float(beta.ppf(.025,count,total-count+1)) if count else 0.,
                     float(beta.ppf(.975,count+1,total-count)) if count<total else 1.]}
