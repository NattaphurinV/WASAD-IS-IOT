from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LabelSegment:
    """
    A continuous time segment belonging to one label.
    """

    label: int
    start_sample: int
    end_sample: int
    start_time: float
    end_time: float

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time


def find_label_segments(
    labels,
    sampling_rate: float = 700.0,
    target_labels: tuple[int, ...] = (1, 2, 3, 4),
) -> list[LabelSegment]:
    """
    Convert a high-frequency label signal into continuous target-label segments.

    Parameters
    ----------
    labels:
        Label signal from WESAD.
    sampling_rate:
        Native WESAD label sampling rate in Hz.
    target_labels:
        Labels to keep for the POC.

    Returns
    -------
    list[LabelSegment]
        Continuous segments for the requested labels.

    Notes
    -----
    Segment boundaries are represented using sample indices [start, end),
    where `end` is exclusive.
    """
    labels = np.asarray(labels).squeeze()

    if labels.ndim != 1:
        raise ValueError(
            f"Labels must be 1D after squeezing, got shape {labels.shape}"
        )

    if labels.size == 0:
        raise ValueError("Labels are empty")

    if sampling_rate <= 0:
        raise ValueError("sampling_rate must be greater than zero")

    if not target_labels:
        raise ValueError("target_labels must not be empty")

    target_labels = set(target_labels)

    # Find indices where the label changes.
    change_points = np.flatnonzero(labels[1:] != labels[:-1]) + 1

    starts = np.concatenate(([0], change_points))
    ends = np.concatenate((change_points, [len(labels)]))

    segments = []

    for start, end in zip(starts, ends):
        label = int(labels[start])

        if label not in target_labels:
            continue

        segments.append(
            LabelSegment(
                label=label,
                start_sample=int(start),
                end_sample=int(end),
                start_time=float(start / sampling_rate),
                end_time=float(end / sampling_rate),
            )
        )

    return segments
