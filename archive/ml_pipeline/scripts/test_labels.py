from src.preprocessing.loader import get_subject_signals
from src.preprocessing.labels import find_label_segments


subject = get_subject_signals("S2")

segments = find_label_segments(subject["label"])

print(f"Subject: {subject['subject_id']}")
print(f"Target segments: {len(segments)}")
print()

for i, segment in enumerate(segments, start=1):
    print(
        f"{i:02d}. "
        f"label={segment.label} "
        f"start={segment.start_time:.2f}s "
        f"end={segment.end_time:.2f}s "
        f"duration={segment.duration:.2f}s"
    )

