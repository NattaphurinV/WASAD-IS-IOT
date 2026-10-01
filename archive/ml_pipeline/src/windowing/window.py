from dataclasses import dataclass

import numpy as np

from src.preprocessing.labels import LabelSegment


@dataclass(frozen=True)
class Window:
    """
    A fixed-length window within a single label segment.
    """

    subject_id: str
    label: int
    start_time: float
    end_time: float
    start_sample_eda: int
    end_sample_eda: int
    start_sample_bvp: int
    end_sample_bvp: int


@dataclass(frozen=True)
class WindowData:
    """
    Actual signal data belonging to one window.
    """

    subject_id: str
    label: int
    start_time: float
    end_time: float
    eda: np.ndarray
    bvp: np.ndarray


def create_windows(
    subject_id: str,
    segments: list[LabelSegment],
    eda_sampling_rate: float = 4.0,
    bvp_sampling_rate: float = 64.0,
    window_seconds: float = 60.0,
    step_seconds: float = 30.0,
) -> list[Window]:
    """
    Create fixed-length windows inside each label segment.

    Windows never cross label-segment boundaries.
    Incomplete windows at the end of a segment are discarded.
    """

    if eda_sampling_rate <= 0:
        raise ValueError("eda_sampling_rate must be greater than zero")

    if bvp_sampling_rate <= 0:
        raise ValueError("bvp_sampling_rate must be greater than zero")

    if window_seconds <= 0:
        raise ValueError("window_seconds must be greater than zero")

    if step_seconds <= 0:
        raise ValueError("step_seconds must be greater than zero")

    windows = []

    for segment in segments:
        start_time = segment.start_time
        segment_end = segment.end_time

        while start_time + window_seconds <= segment_end:
            end_time = start_time + window_seconds

            windows.append(
                Window(
                    subject_id=subject_id,
                    label=segment.label,
                    start_time=start_time,
                    end_time=end_time,
                    start_sample_eda=round(
                        start_time * eda_sampling_rate
                    ),
                    end_sample_eda=round(
                        end_time * eda_sampling_rate
                    ),
                    start_sample_bvp=round(
                        start_time * bvp_sampling_rate
                    ),
                    end_sample_bvp=round(
                        end_time * bvp_sampling_rate
                    ),
                )
            )

            start_time += step_seconds

    return windows


def extract_window_data(
    window: Window,
    eda: np.ndarray,
    bvp: np.ndarray,
) -> WindowData:
    """
    Extract actual EDA and BVP samples for a window.
    """

    eda = np.asarray(eda).squeeze()
    bvp = np.asarray(bvp).squeeze()

    if eda.ndim != 1:
        raise ValueError(
            f"EDA must be 1D, got shape {eda.shape}"
        )

    if bvp.ndim != 1:
        raise ValueError(
            f"BVP must be 1D, got shape {bvp.shape}"
        )

    eda_window = eda[
        window.start_sample_eda:window.end_sample_eda
    ]

    bvp_window = bvp[
        window.start_sample_bvp:window.end_sample_bvp
    ]

    expected_eda_samples = (
        window.end_sample_eda - window.start_sample_eda
    )

    expected_bvp_samples = (
        window.end_sample_bvp - window.start_sample_bvp
    )

    if len(eda_window) != expected_eda_samples:
        raise ValueError(
            "Unexpected EDA window length: "
            f"expected {expected_eda_samples}, "
            f"got {len(eda_window)}"
        )

    if len(bvp_window) != expected_bvp_samples:
        raise ValueError(
            "Unexpected BVP window length: "
            f"expected {expected_bvp_samples}, "
            f"got {len(bvp_window)}"
        )

    return WindowData(
        subject_id=window.subject_id,
        label=window.label,
        start_time=window.start_time,
        end_time=window.end_time,
        eda=eda_window,
        bvp=bvp_window,
    )
