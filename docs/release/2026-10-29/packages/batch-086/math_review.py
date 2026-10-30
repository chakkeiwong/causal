"""Validate exact additive-only mathematical review records against edit bytes."""
from collections import Counter
from pathlib import Path
import hashlib
import re


def validate_additions(reviews, edits, root, pattern):
    approved = Counter()
    issues = []
    seen = set()
    def occurrences(text):
        return Counter(re.sub(r'\s+', ' ', m[0]) for m in pattern.finditer(text))
    for review in reviews:
        local = []
        before, after = Counter(), Counter()
        if review.get('status') != 'reviewed_additions_only' or review.get('allowed_removed'):
            local.append('Mathematical review is not additions-only')
        if not review.get('derivation') or not review.get('reviewed_assumptions'):
            local.append('Mathematical review lacks derivation or assumptions')
        for row in review.get('edits', []):
            index = row.get('edit', 0)
            if not isinstance(index, int) or index < 1 or index > len(edits) or index in seen:
                local.append('Invalid or repeated mathematical-review edit')
                continue
            seen.add(index)
            edit = edits[index - 1]
            if edit['file'] != row.get('file'):
                local.append('Mathematical-review file differs from ledger')
            for field in ['before', 'after']:
                if hashlib.sha256(edit[field].encode()).hexdigest() != row.get(field + '_sha256'):
                    local.append('Mathematical-review text differs from ledger')
            before.update(occurrences(edit['before']))
            after.update(occurrences(edit['after']))
        if before - after:
            local.append('An additions-only review contains a mathematical removal')
        delta = after - before
        if dict(delta) != review.get('allowed_added'):
            local.append('Reviewed additions differ from exact edit mathematics')
        for field in ['witness', 'source_audit']:
            binding = review.get(field, {})
            p = Path(root) / binding.get('path', '')
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != binding.get('sha256'):
                local.append('Mathematical-review evidence identity changed: ' + field)
        if local:
            issues.extend(local)
        else:
            approved.update(delta)
    return approved, issues
