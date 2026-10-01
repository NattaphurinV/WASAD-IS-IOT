import csv
from pathlib import Path

import numpy as np

from src.preprocessing.loader import load_subject


OUTPUT_PATH = Path("data/processed/iot/s2_dummy_1000.csv")

NUM_RECORDS = 1000
SOURCE_FS = 4
TARGET_FS = 1

# Synthetic Unix timestamp for reproducibility.
START_TIMESTAMP = 1_700_000_000

# Fixed seed so mock HR is reproducible.
RNG_SEED = 42

# Payload-related constants.
HR_MIN = 60
HR_MAX = 120

# WESAD wrist skin temperature is stored in degrees Celsius.
SKIN_TEMP_SCALE = 100


def downsample_mean(signal: np.ndarray, source_fs: int, target_fs: int):
    """Convert a signal to a lower sampling rate using block means."""
    if source_fs % target_fs != 0:
        raise ValueError(
            f"Sampling-rate conversion must be integer: "
            f"{source_fs} -> {target_fs}"
        )

    factor = source_fs // target_fs

    usable_length = (len(signal) // factor) * factor
    trimmed = signal[:usable_length]

    return trimmed.reshape(-1, factor).mean(axis=1)


def main():
    data = load_subject("S2")

    wrist = data["signal"]["wrist"]

    eda = np.asarray(wrist["EDA"]).squeeze()
    temp = np.asarray(wrist["TEMP"]).squeeze()

    if eda.ndim != 1 or temp.ndim != 1:
        raise ValueError("EDA and TEMP must be 1D arrays.")

    if len(eda) != len(temp):
        raise ValueError(
            f"EDA/TEMP length mismatch: {len(eda)} vs {len(temp)}"
        )

    eda_1hz = downsample_mean(
        eda,
        source_fs=SOURCE_FS,
        target_fs=TARGET_FS,
    )

    temp_1hz = downsample_mean(
        temp,
        source_fs=SOURCE_FS,
        target_fs=TARGET_FS,
    )

    if len(eda_1hz) < NUM_RECORDS:
        raise ValueError(
            f"Not enough data for {NUM_RECORDS} records. "
            f"Available: {len(eda_1hz)}"
        )

    eda_1hz = eda_1hz[:NUM_RECORDS]
    temp_1hz = temp_1hz[:NUM_RECORDS]

    rng = np.random.default_rng(RNG_SEED)

    heart_rate = rng.integers(
        HR_MIN,
        HR_MAX + 1,
        size=NUM_RECORDS,
        dtype=np.uint8,
    )

    timestamps = (
        START_TIMESTAMP + np.arange(NUM_RECORDS, dtype=np.uint32)
    )

    status_flags = np.ones(NUM_RECORDS, dtype=np.uint8)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "timestamp",
            "heart_rate",
            "skin_temp",
            "eda_value",
            "status_flag",
        ])

        for i in range(NUM_RECORDS):
            writer.writerow([
                int(timestamps[i]),
                int(heart_rate[i]),
                float(temp_1hz[i]),
                float(eda_1hz[i]),
                int(status_flags[i]),
            ])

    print("IoMT telemetry generation completed.")
    print(f"Source: WESAD S2")
    print(f"EDA source rate: {SOURCE_FS} Hz")
    print(f"TEMP source rate: {SOURCE_FS} Hz")
    print(f"Target rate: {TARGET_FS} Hz")
    print(f"Records: {NUM_RECORDS}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
