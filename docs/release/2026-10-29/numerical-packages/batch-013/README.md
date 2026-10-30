# Retained numerical reconstruction

This local review package reconstructs seven release-critical arithmetic groups
from the retained data. It draws no new samples and makes no new causal, native
package, bank-validation or independent-acceptance claim. It does not regenerate
every original simulation or reproduce every number in the monograph.

Run with Python and the NumPy/SciPy versions in manifest.json:

    python3 /path/to/package/reconstruct.py --external-root /path/to/supplied-inputs --output /path/to/new-result

The output directory must not exist. The external root must contain the two
repository-relative public-data paths listed in manifest.json. Supply the
retained originals whose hashes match the provenance receipts; the runner makes
no network requests. These public experimental files are excluded because their
data-specific commercial redistribution terms are unresolved. This package
grants no rights over them. No papers or vendor documents are bundled.

All project data, the unchanged numerical verifier, expected results and their
hashes are included. The runner verifies bytes before reconstruction, compares
all result structures with the reference using declared numerical tolerances,
and checks that inputs remain unchanged. The original verifier itself checks
claims against retained results and exact rational constructions. Environment
differences are reported. The surrounding assignment, observation, selection and
transport assumptions require scientific evidence beyond arithmetic agreement.
