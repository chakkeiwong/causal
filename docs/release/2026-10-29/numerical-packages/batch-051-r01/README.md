# Retained numerical reconstruction

This local review package reconstructs the release-critical arithmetic groups listed in manifest.json
from the retained data. It draws no new samples and makes no new causal, native
package, bank-validation or independent-acceptance claim. It does not regenerate
every original simulation or reproduce every number in the monograph.

Run with Python and the NumPy/SciPy versions in manifest.json:

    python3 /path/to/package/reconstruct.py --external-root /path/to/supplied-inputs --output /path/to/new-result

The output directory must not exist. The external root must contain the five
repository-relative external-data paths listed in manifest.json: two public
experimental subset files and three saved benchmark-result CSVs. Supply the
retained originals whose hashes match the provenance receipts; the runner makes
no network requests. External source identities and acquisition receipts are in
evidence/external-input-provenance.json. The benchmark tables originate from the
pinned third-party repository, not this project's authored simulations. Its root
MIT notice does not close the retained review's inherited-data and provider-terms
questions. All five originals are supplied separately; this package grants no
rights over them. No papers or vendor documents are bundled.

All project data, the unchanged numerical verifier, expected results and their
hashes are included. The runner verifies bytes before reconstruction, compares
all result structures with the reference using declared numerical tolerances,
and checks that inputs remain unchanged. The original verifier itself checks
claims against retained results and exact rational constructions. Environment
differences are reported. The surrounding assignment, observation, selection and
transport assumptions require scientific evidence beyond arithmetic agreement.
