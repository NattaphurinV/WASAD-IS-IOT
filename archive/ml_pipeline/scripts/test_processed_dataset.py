from pathlib import Path

import numpy as np

from src.preprocessing.loader import get_subject_signals
from src.preprocessing.signals import preprocess_eda, preprocess_bvp
from src.preprocessing.labels import find_label_segments
from src.windowing.window import create_windows, extract_window_data
from src.windowing.dataset import save_windows, load_windows


SUBJECT_ID = "S2"
OUTPUT_PATH = Path("data/processed/S2/windows.npz")


subject = get_subject_signals(SUBJECT_ID)

eda = preprocess_eda(subject["eda"])
bvp = preprocess_bvp(subject["bvp"])

segments = find_label_segments(subject["label"])

windows = create_windows(
    subject_id=SUBJECT_ID,
    segments=segments,
)

window_data = [
    extract_window_data(window, eda, bvp)
    for window in windows
]

save_windows(window_data, OUTPUT_PATH)

loaded = load_windows(OUTPUT_PATH)

print(f"Subject: {SUBJECT_ID}")
print(f"Saved to: {OUTPUT_PATH}")
print()

for key, value in loaded.items():
    print(f"{key:12s} shape={value.shape} dtype={value.dtype}")

print()

assert loaded["eda"].shape == (90, 240)
assert loaded["bvp"].shape == (90, 3840)
assert loaded["labels"].shape == (90,)
assert loaded["start_time"].shape == (90,)
assert loaded["end_time"].shape == (90,)
assert loaded["subject_ids"].shape == (90,)

assert np.array_equal(
    loaded["eda"],
    np.stack([item.eda for item in window_data]),
)

assert np.array_equal(
    loaded["bvp"],
    np.stack([item.bvp for item in window_data]),
)

assert np.array_equal(
    loaded["labels"],
    np.asarray([item.label for item in window_data]),
)

assert np.allclose(
    loaded["end_time"] - loaded["start_time"],
    60.0,
)
assert np.all(
    loaded["subject_ids"] == SUBJECT_ID
)

print("All processed dataset checks passed.")
