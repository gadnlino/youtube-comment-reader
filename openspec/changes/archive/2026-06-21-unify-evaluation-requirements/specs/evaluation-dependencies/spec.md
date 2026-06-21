## ADDED Requirements

### Requirement: Canonical evaluation requirements file exists

The repository SHALL provide a single canonical Python requirements file at `evaluation/requirements.txt` that lists all third-party packages required to run canonical evaluation and analysis scripts under `evaluation/scripts/` and `evaluation/model_comparison/`.

#### Scenario: Fresh environment setup from evaluation root

- **WHEN** a developer creates a virtual environment and runs `pip install -r evaluation/requirements.txt` from the repository root
- **THEN** imports used by canonical scripts in `evaluation/scripts/01_model_evaluation/`, `evaluation/scripts/02_api_performance/`, and `evaluation/model_comparison/scripts/` succeed without additional manual `pip install` commands

#### Scenario: Documentation points to canonical file

- **WHEN** a developer reads `evaluation/README.md` or `evaluation/scripts/README.md` for setup instructions
- **THEN** both documents reference `evaluation/requirements.txt` as the primary install path

### Requirement: Dependency set covers canonical script imports

The canonical requirements file MUST include packages corresponding to third-party imports used by canonical evaluation scripts, including at minimum: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `scipy`, `requests`, `langdetect`, `kagglehub`, `nltk`, `textblob`, `locust`, `datasets`, `transformers`, `accelerate`, and `torch`.

#### Scenario: Model evaluation scripts import successfully

- **WHEN** dependencies are installed from `evaluation/requirements.txt`
- **THEN** running a representative model-evaluation script (e.g., `compare_metrics_vs_benchmark.py`) does not fail with `ModuleNotFoundError` for any listed package

#### Scenario: API performance scripts import successfully

- **WHEN** dependencies are installed from `evaluation/requirements.txt`
- **THEN** running a representative API performance script (e.g., `common.py` or `locust_test.py`) does not fail with `ModuleNotFoundError` for any listed package

#### Scenario: Model comparison scripts import successfully

- **WHEN** dependencies are installed from `evaluation/requirements.txt`
- **THEN** running a representative model-comparison script (e.g., `tfidf_logistic_classification_report.py`) does not fail with `ModuleNotFoundError` for any listed package

### Requirement: Hugging Face and datasets dependencies included by default

Packages used by subsets of canonical scripts—including `datasets`, `transformers`, `accelerate`, and `torch`—SHALL be listed in `evaluation/requirements.txt` and installed by the default `pip install -r evaluation/requirements.txt` command. They MUST NOT require a separate supplemental requirements file or undocumented extra install step.

#### Scenario: Hugging Face datasets validation scripts

- **WHEN** a developer runs `pip install -r evaluation/requirements.txt` and executes a script that imports `datasets` (e.g., `validate_with_airespucrs_pt.py`)
- **THEN** the script does not fail with `ModuleNotFoundError` for `datasets`

#### Scenario: Transformer model comparison notebooks

- **WHEN** a developer runs `pip install -r evaluation/requirements.txt` and executes model-comparison work that imports `transformers` or `torch`
- **THEN** those imports succeed without a second install command

### Requirement: No duplicate divergent requirement lists

The repository MUST NOT maintain two conflicting canonical dependency lists for evaluation scripts. The nested file `evaluation/model_comparison/scripts/requirements.txt` SHALL either be removed, replaced with a pointer to `evaluation/requirements.txt`, or reduced to a thin re-export that does not introduce divergent package sets.

#### Scenario: Model comparison README install path

- **WHEN** a developer follows install instructions in `evaluation/model_comparison/README.md`
- **THEN** the instructions reference `evaluation/requirements.txt`, not an independent unpinned package list that omits packages required elsewhere

### Requirement: Version pins follow documented baselines

Where the repository already documents specific package versions for reproducibility, those versions SHALL be preserved in the unified requirements file. Packages without documented pins MAY remain unpinned or use minimum compatible versions as decided in design.

#### Scenario: Model comparison accelerate pin preserved

- **WHEN** the unified requirements file is created
- **THEN** `accelerate==0.28.0` (or a documented successor pin) is retained in the unified file

#### Scenario: Methodology guide pins reflected

- **WHEN** `evaluation/05_guides/MODEL_EVALUATION_METHODOLOGY.md` lists pinned versions for core packages
- **THEN** the unified file either uses those pins or documents intentional unpinned choices in evaluation setup documentation

### Requirement: Active READMEs and guides reference canonical install

All active evaluation READMEs and methodology guides that describe Python setup SHALL reference `evaluation/requirements.txt` as the single install path. They MUST NOT instruct users to run ad-hoc `pip install <package>` lists or `pip install -r requirements.txt` without a path that resolves to the canonical file.

#### Scenario: Methodology guide setup section

- **WHEN** a developer follows the environment setup section in `evaluation/05_guides/MODEL_EVALUATION_METHODOLOGY.md` or `evaluation/05_guides/API_EVALUATION_METHODOLOGY.md`
- **THEN** the documented install command resolves to `evaluation/requirements.txt`

#### Scenario: Domain README prerequisites

- **WHEN** a developer reads prerequisites in `evaluation/api_load_testing/README.md`, `evaluation/scripts/03_api_e2e/README.md`, or `evaluation/scripts/02_api_performance/benchmarks/API_README.md`
- **THEN** inline per-package install lists are replaced by the canonical requirements file path

#### Scenario: Script error messages point to canonical install

- **WHEN** a validation script detects a missing dependency (e.g., `datasets` in `validate_with_airespucrs_pt.py`)
- **THEN** the error or warning message directs the user to `pip install -r evaluation/requirements.txt` rather than installing individual packages
