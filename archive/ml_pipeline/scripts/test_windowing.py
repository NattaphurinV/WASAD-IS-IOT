from collections import Counter

from src.preprocessing.loader import get_subject_signals
from src.preprocessing.labels import find_label_segments
from src.windowing.window import create_windows


subject = get_subject_signals("S2")

segments = find_label_segments(subject["label"])

windows = create_windows(
    subject_id=subject["subject_id"],
    segments=segments,
)

print(f"Subject: {subject['subject_id']}")
print(f"Segments: {len(segments)}")
print(f"Windows: {len(windows)}")
print()

label_counts = Counter(window.label for window in windows)

print("Windows by label:")
for label in sorted(label_counts):
    print(f"  Label {label}: {label_counts[label]}")

print()
print("First 5 windows:")

for i, window in enumerate(windows[:5], start=1):
    print(
        f"{i:02d}. "
        f"label={window.label} "
        f"time={window.start_time:.2f}-{window.end_time:.2f}s "
        f"EDA={window.start_sample_eda}:{window.end_sample_eda} "
        f"BVP={window.start_sample_bvp}:{window.end_sample_bvp}"
    )
