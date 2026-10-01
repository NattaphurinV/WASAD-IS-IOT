from pathlib import Path

import numpy as np

from src.windowing.window import WindowData


def save_windows(
    windows: list[WindowData],
    output_path: str | Path,
) -> None:
    """
    Save windowed EDA/BVP data and metadata as a compressed NPZ file.
    """

    if not windows:
        raise ValueError("Cannot save an empty window dataset")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    eda = np.stack([window.eda for window in windows])
    bvp = np.stack([window.bvp for window in windows])

    labels = np.asarray(
        [window.label for window in windows],
        dtype=np.int64,
    )

    start_time = np.asarray(
        [window.start_time for window in windows],
        dtype=np.float64,
    )

    end_time = np.asarray(
        [window.end_time for window in windows],
        dtype=np.float64,
    )

    subject_ids = np.asarray(
        [window.subject_id for window in windows],
        dtype="<U16",
    )

    np.savez_compressed(
        output_path,
        eda=eda,
        bvp=bvp,
        labels=labels,
        start_time=start_time,
        end_time=end_time,
        subject_ids=subject_ids,
    )


def load_windows(
    input_path: str | Path,
) -> dict[str, np.ndarray]:
    """
    Load a processed window dataset from NPZ.
    """

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {input_path}"
        )

    with np.load(input_path, allow_pickle=False) as data:
        required_keys = {
            "eda",
            "bvp",
            "labels",
            "start_time",
            "end_time",
            "subject_ids",
        }

        missing = required_keys - set(data.files)

        if missing:
            raise ValueError(
                f"Missing keys in processed dataset: {sorted(missing)}"
            )

        return {
            key: data[key]
            for key in required_keys
        }
