"""One-click reproduction of the Causal Transformer (CT) paper.

Run from the package root after unzip:

    python run_all.py

This script (1) regenerates every figure referenced by the manuscript and the
electronic supplementary material into ./figures/, (2) compiles manuscript.tex
and ESM_1.tex into PDFs, and (3) sanity-checks that required data files and the
pdflatex/LaTeX toolchain are present.

All paths are resolved relative to this script so the package runs on any
machine. No absolute paths (e.g. D:/NO.1 or a specific Desktop folder) are used.

Figures produced (must match the paper's filenames):
  - fig2_results.pdf / .png          (main text, Fig 2, 2x2)
  - fig3_ablation.pdf / .png         (main text, Fig 3, 1x3)
  - esm_fig1_scaling_law.pdf / .png  (ESM Fig 1)
  - esm_fig2_tcga_validation.pdf/.png(ESM Fig 2)
"""
import os
import shutil
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = _HERE
SCRIPTS = os.path.join(ROOT, 'scripts')
DATA = os.path.join(ROOT, 'data')
FIGURES = os.path.join(ROOT, 'figures')
BOLD = '\033[1m'
RESET = '\033[0m'


def info(msg):
    print(f'{BOLD}[run_all]{RESET} {msg}')


def has_pdftex():
    return shutil.which('pdflatex') is not None


def run_py(script):
    info(f'>> Generating figure from {os.path.basename(script)} ...')
    env = dict(os.environ)
    env['MPLBACKEND'] = 'Agg'   # headless matplotlib, no display needed
    r = subprocess.run([sys.executable, script], cwd=SCRIPTS, env=env)
    if r.returncode != 0:
        raise RuntimeError(f'Figure script failed: {script} (rc={r.returncode})')


def run_pdf(tex):
    info(f'>> Compiling {tex} (pass 1) ...')
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex],
                       cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f'pdflatex failed on {tex} (pass 1)')
    # bibtex for manuscript
    info(f'>> Running bibtex for {tex} ...')
    subprocess.run(['bibtex', tex.replace('.tex', '')], cwd=ROOT)
    info(f'>> Compiling {tex} (pass 2) ...')
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex],
                       cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f'pdflatex failed on {tex} (pass 2)')


def check_data():
    need = [os.path.join(DATA, 'ct_results.json')]
    missing = [p for p in need if not os.path.isfile(p)]
    if missing:
        raise FileNotFoundError('Missing required data: ' + ', '.join(missing))
    info('data/ct_results.json present.')


def main():
    info('Package root: ' + ROOT)
    check_data()

    # ---- 1. Regenerate all figures (relative paths only) ----
    fig_scripts = ['gen_fig2.py', 'gen_fig3.py', 'gen_esm_fig2.py', 'gen_esm_fig3.py']
    os.makedirs(FIGURES, exist_ok=True)
    for s in fig_scripts:
        run_py(os.path.join(SCRIPTS, s))

    # ---- 2. Compile manuscript + ESM ----
    if has_pdftex():
        run_pdf('manuscript.tex')
        run_pdf('ESM_1.tex')
        info('Compiled manuscript.pdf and ESM_1.pdf into the package root.')
    else:
        info('pdflatex not found on PATH: skipping PDF compilation '
             '(figures still generated). Install a TeX distribution to build the PDFs.')

    # ---- 3. Final check ----
    expect_figs = ['fig2_results', 'fig3_ablation',
                   'esm_fig1_scaling_law', 'esm_fig2_tcga_validation']
    for f in expect_figs:
        for ext in ('.pdf', '.png'):
            p = os.path.join(FIGURES, f + ext)
            if not os.path.isfile(p):
                raise RuntimeError(f'Expected figure missing: {p}')
    info('All 4 figures generated (PDF + PNG).')

    info('=== REPRODUCTION COMPLETE ===')
    return 0


if __name__ == '__main__':
    sys.exit(main())
