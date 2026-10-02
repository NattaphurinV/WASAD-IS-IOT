# Data Preprocessing

## Dataset

This project uses the WESAD (Wearable Stress and Affect Detection) dataset.

Subject S2 is used as the initial data source for pipeline validation and
cryptographic benchmarking. S2 is not intended to represent the entire WESAD
population.

## Signal Processing

| Signal | Source Rate | Target Rate |
|---|---:|---:|
| EDA | 4 Hz | 1 Hz |
| TEMP | 4 Hz | 1 Hz |

The processed signals are converted into a consistent 1 Hz representation
for the IoMT telemetry pipeline.

## Purpose

The preprocessing stage provides a reproducible physiological-data source
for the subsequent IoMT telemetry and security experiments.

The cryptographic benchmark is based on a fixed-size telemetry payload.
Therefore, subject selection does not constitute a comparison between
participants.

## Data Policy

The original WESAD dataset is not included in this repository.

Users must obtain the dataset separately and place it in the expected local
data directory according to the project setup instructions.
