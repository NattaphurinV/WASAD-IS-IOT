from collections import Counter

from src.preprocessing.loader import get_subject_signals
from src.preprocessing.signals import preprocess_eda, preprocess_bvp
from src.preprocessing.labels import find_label_segments
from src.windowing.window import create_windows, extract_window_data


subject = get_subject_signals("S2")

eda = preprocess_eda(subject["eda"])
bvp = preprocess_bvp(subject["bvp"])

segments = find_label_segments(subject["label"])

windows = create_windows(
    subject_id=subject["subject_id"],
    segments=segments,
)

window_data = [
    extract_window_data(window, eda, bvp)
    for window in windows
]

print(f"Subject: {subject['subject_id']}")
print(f"Windows: {len(window_data)}")
print()

label_counts = Counter(
    item.label for item in window_data
)

print("Windows by label:")
for label in sorted(label_counts):
    print(f"  Label {label}: {label_counts[label]}")

print()
print("First 3 extracted windows:")

for i, item in enumerate(window_data[:3], start=1):
    print(
        f"{i:02d}. "
        f"label={item.label} "
        f"time={item.start_time:.2f}-{item.end_time:.2f}s "
        f"EDA shape={item.eda.shape} "
        f"BVP shape={item.bvp.shape}"
    )

print()
print("Signal lengths:")
print("  EDA:", sorted(set(len(item.eda) for item in window_data)))
print("  BVP:", sorted(set(len(item.bvp) for item in window_data)))
