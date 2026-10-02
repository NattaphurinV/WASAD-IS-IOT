# Reproducibility

## Environment

Record the following information when running experiments:

- Operating system
- CPU
- Python version
- cryptography package version
- Project commit/version

Example:

```bash
python --version
python -m pip show cryptography
git rev-parse HEAD
Virtual Environment

Create and activate a Python virtual environment:

python -m venv .venv
source .venv/bin/activate

Install project dependencies:

python -m pip install -r requirements.txt
Dataset

The WESAD dataset is not stored in Git because of its size and distribution
requirements.

Obtain the dataset separately and place it in the expected project data
directory.

Pipeline

The general experiment flow is:

WESAD
  ↓
Preprocessing
  ↓
IoMT telemetry generation
  ↓
AES-GCM benchmark
  ↓
Benchmark results
AES-GCM Benchmark

Run:

python -m scripts.benchmark_aes_gcm

The benchmark uses a fixed 12-byte plaintext payload and performs warm-up
iterations before collecting measurements.

Reproducibility Notes

Benchmark results may vary between machines and executions because of CPU
frequency scaling, operating-system scheduling, background processes,
Python runtime differences, and cryptography library versions.

Reported results should therefore include the environment and benchmark
configuration.
