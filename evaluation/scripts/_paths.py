"""
Shared path constants for evaluation scripts.

Import from category scripts (run from repo root or the script's category folder):

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _paths import MODEL_RESULTS, API_ROOT, repo_path

Prefer repo_path(MODEL_RESULTS) when opening files so paths work regardless of CWD.
"""

from pathlib import Path

# Repo root (youtube-comment-reader/)
REPO_ROOT = Path(__file__).resolve().parents[2]

# evaluation/ tree
EVAL_ROOT = REPO_ROOT / "evaluation"
REPORTS = EVAL_ROOT / "01_reports"
GRAPHS = EVAL_ROOT / "02_graphs"
DATA = EVAL_ROOT / "03_data"
GUIDES = EVAL_ROOT / "05_guides"
ARCHIVED = EVAL_ROOT / "06_archived"

# Domain output folders (unchanged in v1 reorganisation)
MODEL_ANALYSIS = EVAL_ROOT / "model_analysis"
MODEL_RESULTS = MODEL_ANALYSIS / "results"
MODEL_GRAPHS = MODEL_ANALYSIS / "graphs"
MODEL_DATA = MODEL_ANALYSIS / "data"
MODEL_REPORTS = MODEL_ANALYSIS / "reports"

API_ROOT = EVAL_ROOT / "api_load_testing"
API_RESULTS = API_ROOT / "results"
API_GRAPHS = API_ROOT / "graphs"
API_CONSOLIDATED_GRAPHS = API_ROOT / "consolidated_graphs"

MODEL_COMPARISON = EVAL_ROOT / "model_comparison"
MODEL_COMPARISON_SCRIPTS = MODEL_COMPARISON / "scripts"
MODEL_COMPARISON_RESULTS = MODEL_COMPARISON / "results"

SCRIPTS_ROOT = EVAL_ROOT / "scripts"
MODEL_EVAL_SCRIPTS = SCRIPTS_ROOT / "01_model_evaluation"
API_PERF_SCRIPTS = SCRIPTS_ROOT / "02_api_performance"
API_E2E_SCRIPTS = SCRIPTS_ROOT / "03_api_e2e"


def repo_path(path: Path) -> Path:
    """Return absolute path; relative paths are resolved from REPO_ROOT."""
    p = Path(path)
    return p if p.is_absolute() else REPO_ROOT / p
