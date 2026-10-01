# WESAD Preprocessing

## Purpose

This document describes the preprocessing pipeline implemented for the WESAD stress-detection project.

The preprocessing pipeline is designed to:

- preserve the original WESAD raw dataset
- validate and prepare wrist EDA and BVP signals
- convert the high-frequency label signal into continuous temporal segments
- prepare the data for fixed-length windowing
- avoid data leakage in later machine-learning stages

The current implementation is validated using subject S2 before being applied to all subjects.

---

## 1. Raw Data

The original WESAD dataset is stored under:

```text
data/raw/WESAD/

Raw data must not be modified during preprocessing.

The raw WESAD dataset is excluded from Git through .gitignore.

2. Project Pipeline

The current preprocessing pipeline is:

Raw WESAD
    |
    v
Load subject
    |
    v
Validate EDA / BVP
    |
    v
Convert label signal into temporal segments
    |
    v
Windowing
    |
    v
Feature extraction
    |
    v
Model training / evaluation

Only the stages up to label segmentation have currently been implemented.

3. Subject Loader

Implementation:

src/preprocessing/loader.py

The loader reads one WESAD subject from:

data/raw/WESAD/<subject_id>/<subject_id>.pkl

For example:

data/raw/WESAD/S2/S2.pkl

The loader provides the following signals for the current proof of concept:

subject_id
EDA
BVP
label

The current POC uses wrist EDA and wrist BVP.

4. Signal Validation

Implementation:

src/preprocessing/signals.py

The current signal preprocessing performs only basic validation and shape normalization.

4.1 Shape normalization

WESAD wrist signals are loaded as column vectors:

EDA: (N, 1)
BVP: (N, 1)

They are converted to one-dimensional arrays:

EDA: (N,)
BVP: (N,)

No samples are removed during this operation.

4.2 Validation

The preprocessing checks that:

the signal is not empty
the signal contains numeric values
there are no NaN values
there are no infinite values
4.3 Operations intentionally not performed yet

The current implementation does not perform:

resampling
filtering
normalization
standardization
interpolation

These operations will only be introduced when their necessity and parameters have been established.

5. Native Sampling Rates

The current POC preserves the native sampling rates of the WESAD signals.

Signal	Sampling rate
Wrist EDA	4 Hz
Wrist BVP	64 Hz
Label	700 Hz

EDA and BVP are therefore not resampled to a common sampling rate at this stage.

The label signal is handled separately as a temporal annotation rather than as a continuous physiological signal.

6. Label Segmentation

Implementation:

src/preprocessing/labels.py

The WESAD label signal is sampled at 700 Hz.

Instead of resampling the label signal to EDA or BVP frequency, the preprocessing detects points where the label changes and converts the label sequence into continuous temporal segments.

Each segment contains:

label
start_sample
end_sample
start_time
end_time
duration

Segment intervals use the convention:

[start_sample, end_sample)

where end_sample is exclusive.

7. Target Labels

For the current proof of concept, the target classes are:

Label	Meaning
1	Baseline
2	Stress
3	Amusement
4	Meditation

The following labels are excluded from the POC:

0
6
7

Excluded labels are not used for target windows.

8. S2 Label Segments

The current implementation was validated using WESAD subject S2.

The target-label segments are:

Segment	Label	Start (s)	End (s)	Duration (s)
1	1	306.55	1450.55	1144
2	2	2273.55	2888.55	615
3	4	4097.55	4488.55	391
4	3	4763.55	5125.55	362
5	4	5496.55	5873.55	377

Label 4 appears in two separate temporal segments. They must remain separate during windowing.

9. Windowing Plan

Windowing is the next preprocessing stage.

The planned configuration is:

Window length : 60 seconds
Overlap       : 50%
Step          : 30 seconds

Windows must be generated independently inside each continuous target-label segment.

A window must never cross:

a label boundary
an excluded-label region
two separate segments with the same label

For example, the two meditation segments of label 4 remain separate even though they have the same class label.

Incomplete windows shorter than 60 seconds will be discarded.

10. Data Leakage Prevention

Subject identity must be preserved for every generated window.

The subject ID will later be used for subject-level train/validation/test splitting.

The project should not perform random window-level splitting because windows originating from the same subject may contain highly correlated physiological patterns.

Scaling or normalization, if required later, must be fitted using the training subjects only and then applied to validation/test subjects.

11. Reproducibility Principles

The preprocessing pipeline should follow these principles:

Keep data/raw/WESAD/ unchanged.
Implement preprocessing as reusable Python modules.
Avoid ad-hoc preprocessing commands for the final pipeline.
Preserve subject IDs.
Preserve label boundaries.
Keep native signal sampling rates unless a later method explicitly requires resampling.
Avoid fitting preprocessing parameters on the complete dataset.
Validate each preprocessing stage on S2 before processing all subjects.
12. Current Implementation Status
Stage	Status
Dataset inspection	Done
Subject loader	Done
EDA validation	Done
BVP validation	Done
Label segmentation	Done
Windowing	Next
Feature extraction	Not started
Model training	Not started
Evaluation	Not started
13. Validation Commands

The current modules can be tested with:

python -m scripts.test_loader

and:

python -m scripts.test_signals

and:

python -m scripts.test_labels

These tests currently use subject S2.

14. Next Step

The next implementation stage is fixed-length windowing.

The windowing module will generate 60-second windows with 50% overlap while enforcing label-segment boundaries.

The implementation will first be validated on S2 before being applied to the remaining subjects.
