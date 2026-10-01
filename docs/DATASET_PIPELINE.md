# Dataset Pipeline — Paused

## Status

**Status: PAUSED**

The windowing and processed-dataset pipeline documented here was developed
during the initial exploration of the WESAD dataset.

It is **not part of the current primary research pipeline**.

The current research scope focuses on:

- IoMT telemetry payload construction
- Fixed-size binary payloads
- AES-GCM encryption
- Authentication and integrity protection
- Zero Trust security architecture
- Encryption performance evaluation

Machine learning tasks such as:

- signal windowing
- feature extraction
- stress classification
- model training
- model evaluation

are currently paused.

---

## 1. Purpose of the Previous Pipeline

The previous pipeline was created to understand the internal structure of
the WESAD dataset and verify that EDA and BVP signals could be extracted
reliably.

The experiment used subject S2 as a representative subject.

The pipeline was:

```text
WESAD S2
   |
   v
Load raw signals
   |
   v
Validate EDA / BVP
   |
   v
Segment labels
   |
   v
Create 60-second windows
   |
   v
Save processed windows

This pipeline was useful for understanding the dataset structure but is not
required for the current IoMT security experiments.

2. WESAD Dataset Findings

The following information remains useful as a reference for generating
realistic IoMT telemetry.

Wrist sampling rates
Signal	Sampling rate
EDA	4 Hz
BVP	64 Hz
Label	700 Hz

The original WESAD data is retained unchanged.

3. S2 Exploration Result

The S2 subject file was successfully loaded and inspected.

The previous experiment identified:

EDA shape   = (24316, 1)
BVP shape   = (389056, 1)
Label shape = (4255300,)

After validation:

EDA shape = (24316,)
BVP shape = (389056,)

No NaN or infinite values were detected in the tested S2 EDA and BVP
signals.

4. Previous Windowing Experiment

The previous experiment used:

Window length = 60 seconds
Step          = 30 seconds
Overlap       = 50%

For S2 this produced:

Total windows = 90

Label 1 = 37
Label 2 = 19
Label 3 = 11
Label 4 = 23

The resulting processed dataset contained:

EDA         = (90, 240)
BVP         = (90, 3840)
labels      = (90,)
start_time  = (90,)
end_time    = (90,)
subject_ids = (90,)

This experiment successfully verified the mechanics of signal extraction and
serialization.

5. Why This Pipeline Is Paused

The current research does not require classification of physiological
states.

The encryption system treats telemetry as application data rather than as
machine-learning features.

Therefore, the system does not need to determine whether a record represents:

Baseline
Stress
Amusement
Meditation

The security layer only needs a telemetry record that can be represented as
a fixed-size binary payload.

6. New Data Objective

The next data-generation stage will create 1,000 synthetic IoMT telemetry
records derived from realistic WESAD S2 signal values.

The records will be used as test inputs for:

IoMT Payload
     |
     v
Binary Serialization
     |
     v
AES-GCM Encryption
     |
     v
Performance Benchmark

The generated records are test data, not a machine-learning dataset.

7. Data Alignment

WESAD wrist signals have different native sampling rates.

For the IoMT prototype, telemetry will be represented at:

1 record / second

The current prototype will downsample the available signals to 1 Hz.

For EDA and Skin Temperature, one representative value will be selected
from each one-second interval according to the implementation documented
in docs/IOT_PAYLOAD.md.

BVP will not be converted into a medical-grade heart-rate measurement.

Instead, the prototype will use a documented mock heart-rate generator
because the research objective is encryption and system performance rather
than physiological inference.

8. Output

The generated IoMT records will be stored separately from the previous
windowed dataset.

Planned output:

data/
└── processed/
    └── iot/
        └── s2_dummy_1000.csv

The generated dataset must not be committed to Git.

9. Relationship to the Current Research

The previous WESAD processing work is retained as exploratory work.

It demonstrates that realistic physiological data can be obtained from
WESAD and transformed into telemetry-like records.

The current research pipeline starts from the telemetry representation:

WESAD-derived telemetry
        |
        v
12-byte binary payload
        |
        v
AES-GCM
        |
        v
Authenticated ciphertext
        |
        v
Zero Trust communication workflow
10. Future ML Work

Machine-learning experiments may be resumed in the future if required by
the research scope.

Until then, the following components remain inactive:

Windowing
Feature Extraction
Model Training
Model Evaluation

No further ML implementation should be performed unless the research scope
is explicitly changed.
