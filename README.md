# WESAD-IS

Proof-of-Concept for stress-related state classification using the WESAD dataset.

## 1. Requirements

- Python 3.10+
- Git
- WESAD dataset

## 2. Setup

Clone the repository:

    git clone <repository-url>
    cd wesad-is

Create virtual environment:

    python3 -m venv .venv

Activate virtual environment:

    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

## 3. Dataset

This project uses the WESAD dataset.

The raw WESAD dataset is NOT included in this repository because of its size
and dataset distribution restrictions.

Download/acquire WESAD separately and place it under:

    data/raw/WESAD/

For example:

    data/raw/WESAD/S2/S2.pkl

## 4. Verify Dataset

Run:

    python scripts/check_wesad.py

## 5. Run POC

Preprocessing:

    python scripts/preprocess.py

Windowing:

    python scripts/create_windows.py

Feature extraction:

    python scripts/extract_features.py

Training:

    python scripts/train.py

Evaluation:

    python scripts/evaluate.py

## 6. Current POC

Current experiment:

- Dataset: WESAD
- Subject: S2
- Signals: Wrist EDA + Wrist BVP
- Target classes:
  - 1 = Baseline
  - 2 = Stress
  - 3 = Amusement
  - 4 = Meditation
- Window: 60 seconds
- Overlap: 50%
- Step: 30 seconds
- Windows crossing label boundaries are excluded

These parameters are experimental and may change during development.

## 7. Documentation

Data inspection and validation:

    docs/WESAD_DATA_INSPECTION.md