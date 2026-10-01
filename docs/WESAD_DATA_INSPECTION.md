# WESAD Data Inspection & Initial Validation

## Purpose

This document records the commands and procedures used to inspect and validate the WESAD dataset during the initial proof-of-concept (POC) stage.

The current inspection uses:

```text
data/raw/WESAD/S2/S2.pkl

The purpose of this stage is to:

understand the dataset structure
verify signal sampling rates and recording duration
inspect label distribution and temporal boundaries
perform basic raw-signal quality checks
define the initial preprocessing and windowing configuration

No processed dataset is created during this inspection stage.

1. Load the WESAD S2 file

Command:

python -c "import pickle; f=open('data/raw/WESAD/S2/S2.pkl','rb'); d=pickle.load(f,encoding='latin1'); print(d.keys()); f.close()"
Technique

Use Python pickle to load the original WESAD .pkl file.

pickle.load(f, encoding="latin1")

The latin1 encoding is used for compatibility with the original WESAD pickle file.

2. Inspect the dataset structure

The main structure is:

S2.pkl
├── signal
│   ├── chest
│   └── wrist
│       ├── EDA
│       ├── BVP
│       ├── TEMP
│       ├── ACC
│       └── other wrist signals
│
└── label

Useful inspection command:

python -c "import pickle; f=open('data/raw/WESAD/S2/S2.pkl','rb'); d=pickle.load(f,encoding='latin1'); print(d.keys()); print(d['signal'].keys()); print(d['signal']['wrist'].keys()); f.close()"

For the current POC, the primary signals are:

Wrist EDA → 4 Hz
Wrist BVP → 64 Hz
Label     → 700 Hz

The original sampling rates are retained during preprocessing. Signals are not resampled to a common sampling rate at this stage.

3. Check recording duration

Command:

python -c "import pickle; f=open('data/raw/WESAD/S2/S2.pkl','rb'); d=pickle.load(f, encoding='latin1'); y=d['label']; print('Label duration:', len(y)/700, 'sec'); print('EDA duration:', len(d['signal']['wrist']['EDA'])/4, 'sec'); print('BVP duration:', len(d['signal']['wrist']['BVP'])/64, 'sec'); f.close()"

Result:

Label duration: 6079.0 sec
EDA duration: 6079.0 sec
BVP duration: 6079.0 sec

Therefore:

S2 duration = 6079 seconds
            ≈ 101.32 minutes
            ≈ 1 hour 41 minutes 19 seconds

The label, EDA, and BVP recordings cover the same overall time span.

4. Inspect label distribution

Command:

python -c "import pickle,numpy as np; f=open('data/raw/WESAD/S2/S2.pkl','rb'); d=pickle.load(f,encoding='latin1'); y=d['label']; u,c=np.unique(y,return_counts=True); print(dict(zip(u,c))); print(); print('Label duration:'); [print('Label',int(k),':',int(v), 'samples =',round(v/700,2),'sec') for k,v in zip(u,c)]; f.close()"

Result:

Label 0 : 2142701 samples = 3061.0 sec
Label 1 : 800800 samples = 1144.0 sec
Label 2 : 430500 samples = 615.0 sec
Label 3 : 253400 samples = 362.0 sec
Label 4 : 537599 samples = 768.0 sec
Label 6 : 45500 samples = 65.0 sec
Label 7 : 44800 samples = 64.0 sec

Labels present in S2:

0, 1, 2, 3, 4, 6, 7

For the current four-class POC, the target classes are:

1 = Baseline
2 = Stress
3 = Amusement
4 = Meditation

The following labels are excluded:

0, 6, 7
5. Inspect label segments and temporal boundaries

A label distribution shows how many samples belong to each class, but it does not show where each class occurs in the recording.

Temporary inspection script:

cat > /tmp/check_segments.py <<'PY'
import pickle
import numpy as np

with open("data/raw/WESAD/S2/S2.pkl", "rb") as f:
    d = pickle.load(f, encoding="latin1")

y = d["label"]

change = np.where(y[1:] != y[:-1])[0] + 1

start = 0

print("Label segments:")
print("-" * 60)

for i, end in enumerate(np.append(change, len(y)), 1):
    label = int(y[start])
    start_sec = start / 700
    end_sec = end / 700
    duration = end_sec - start_sec

    print(
        f"{i:02d}: "
        f"label={label} | "
        f"{start_sec:8.2f}s -> {end_sec:8.2f}s | "
        f"duration={duration:7.2f}s"
    )

    start = end
PY

python /tmp/check_segments.py

Result:

01: label=0 |     0.00s ->  306.55s | duration=306.55s
02: label=1 |   306.55s -> 1450.55s | duration=1144.00s
03: label=0 |  1450.55s -> 2273.55s | duration=823.00s
04: label=2 | 2273.55s -> 2888.55s | duration=615.00s
05: label=0 | 2888.55s -> 3160.55s | duration=272.00s
06: label=6 | 3160.55s -> 3225.55s | duration=65.00s
07: label=0 | 3225.55s -> 4097.55s | duration=872.00s
08: label=4 | 4097.55s -> 4488.55s | duration=391.00s
09: label=0 | 4488.55s -> 4763.55s | duration=275.00s
10: label=3 | 4763.55s -> 5125.55s | duration=362.00s
11: label=0 | 5125.55s -> 5269.55s | duration=144.00s
12: label=7 | 5269.55s -> 5333.55s | duration=64.00s
13: label=0 | 5333.55s -> 5496.55s | duration=163.00s
14: label=4 | 5496.55s -> 5873.55s | duration=377.00s
15: label=0 | 5873.55s -> 6079.00s | duration=205.45s
Important observation

Label 4 appears in two separate temporal segments:

4097.55–4488.55 s = 391 s
5496.55–5873.55 s = 377 s

Total:

391 + 377 = 768 s

This matches the label distribution.

This is important for windowing because windows must not cross label boundaries.

6. Check raw EDA and BVP quality

Command:

python -c "import pickle,numpy as np; f=open('data/raw/WESAD/S2/S2.pkl','rb'); d=pickle.load(f,encoding='latin1'); eda=np.asarray(d['signal']['wrist']['EDA']).squeeze(); bvp=np.asarray(d['signal']['wrist']['BVP']).squeeze(); print('EDA:', eda.shape, 'NaN=',np.isnan(eda).sum(), 'min=',eda.min(), 'max=',eda.max(), 'mean=',eda.mean(), 'std=',eda.std()); print('BVP:', bvp.shape, 'NaN=',np.isnan(bvp).sum(), 'min=',bvp.min(), 'max=',bvp.max(), 'mean=',bvp.mean(), 'std=',bvp.std()); f.close()"

Result:

EDA: (24316,) NaN= 0 min= 0.045113 max= 1.717419 mean= 0.39174332912485604 std= 0.3292287628310672

BVP: (389056,) NaN= 0 min= -873.67 max= 988.08 mean= -0.00042682801447604924 std= 75.87123615470419
Interpretation

EDA:

Samples = 24,316
Sampling rate = 4 Hz
NaN = 0

BVP:

Samples = 389,056
Sampling rate = 64 Hz
NaN = 0

No missing values were detected in either signal.

The positive and negative BVP values are expected for a waveform signal and do not by themselves indicate corrupted data.

7. Current data definition for the POC

Dataset:

WESAD

Subject:

S2

File:

data/raw/WESAD/S2/S2.pkl

Duration:

6079 seconds

Primary signals:

Wrist EDA → 4 Hz
Wrist BVP → 64 Hz

Label:

700 Hz

Target classes:

1 = Baseline
2 = Stress
3 = Amusement
4 = Meditation

Excluded labels:

0, 6, 7
8. Data inspection status

Completed:

[x] Dataset documentation / README reviewed
[x] S2 file identified
[x] S2.pkl loaded successfully
[x] Main structure inspected
[x] Wrist signals identified
[x] Sampling rates verified
[x] Recording duration verified
[x] Label distribution inspected
[x] Label timeline inspected
[x] Raw EDA checked
[x] Raw BVP checked
[x] NaN check completed
Status

Data structure and initial raw-data validation are complete.

The project can now move to:

Preprocessing
    ↓
Windowing
    ↓
Feature extraction
    ↓
Model training
    ↓
Evaluation
9. Initial preprocessing specification

The initial preprocessing stage will preserve the native sampling rates of the selected signals:

EDA → 4 Hz
BVP → 64 Hz

The preprocessing stage will focus on:

Loading the original WESAD .pkl files.
Selecting wrist EDA and wrist BVP.
Validating signal dimensions and sampling rates.
Checking for invalid or missing values.
Applying signal-specific cleaning/filtering only where justified.
Keeping EDA and BVP on their native sampling rates.
Representing labels as temporal segments rather than resampling the label signal to the signal sampling rates.
Keeping raw data unchanged.
No global normalization

Global normalization will not be applied to the complete dataset before train/test splitting.

If normalization is required for a model, normalization statistics must be calculated from the training data only and then applied to validation/test data.

This prevents information from the evaluation subjects from leaking into the training process.

10. Initial windowing specification

The initial windowing experiment is:

Signals:
    Wrist EDA + Wrist BVP

Classes:
    1, 2, 3, 4

Window size:
    60 seconds

Overlap:
    50%

Step:
    30 seconds
Window boundary rule

Windows must not cross label boundaries.

For example, a window that begins inside label 1 and ends inside label 0 is invalid and must not be created.

Windows are generated independently within each valid target-label segment.

Example:

Label 1 segment:
306.55s ─────────────────────────────── 1450.55s

Possible windows:
306.55 → 366.55
336.55 → 396.55
366.55 → 426.55
...

The final incomplete window within a segment is discarded if fewer than 60 seconds remain.

This is an initial POC configuration and may be changed after inspecting the resulting window counts and class distribution.

11. Preprocessing and windowing design principles

The preprocessing pipeline should follow these principles:

Raw data preservation

The original WESAD files under:

data/raw/WESAD/

must remain unchanged.

Reproducibility

Preprocessing and windowing should be implemented as reusable Python modules rather than ad-hoc one-line commands.

Subject identity preservation

Every processed sample/window must retain its subject identifier.

For example:

subject = S2

This is required for subject-independent train/test splitting later.

Avoid data leakage

Subject-level separation must be respected during model evaluation.

Information from a subject used for evaluation must not be used to fit preprocessing parameters, feature scaling parameters, or the model.

12. Reproducibility note

The inspection commands in this document are intentionally kept simple and executable from the project root.

All raw-data inspection is performed directly against:

data/raw/WESAD/S2/S2.pkl

No processed dataset is created during this inspection stage.

The next stage should use dedicated preprocessing and windowing modules instead of continuing to use ad-hoc inspection commands.

13. Next experimental stage

The next implementation stage is:

Raw WESAD
    ↓
Load subject
    ↓
Validate / preprocess EDA
    ↓
Validate / preprocess BVP
    ↓
Convert label signal into temporal segments
    ↓
Window target-label segments
    ↓
Save processed/windowed data
    ↓
Feature extraction

The first implementation should be tested on S2 before processing all subjects.
