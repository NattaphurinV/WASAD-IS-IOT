import numpy as np


def to_1d(signal, name: str) -> np.ndarray:
    """
    Convert a signal to a 1D NumPy array.

    WESAD wrist signals are commonly stored as shape (N, 1).
    """
    array = np.asarray(signal).squeeze()

    if array.ndim != 1:
        raise ValueError(
            f"{name} must be 1D after squeezing, got shape {array.shape}"
        )

    return array


def validate_signal(signal, name: str) -> np.ndarray:
    """
    Normalize signal shape and validate basic numerical quality.

    No filtering, resampling, or normalization is performed.
    """
    array = to_1d(signal, name)

    if array.size == 0:
        raise ValueError(f"{name} is empty")

    if not np.issubdtype(array.dtype, np.number):
        raise TypeError(
            f"{name} must contain numeric values, got {array.dtype}"
        )

    nan_count = np.isnan(array).sum()

    if nan_count > 0:
        raise ValueError(
            f"{name} contains {nan_count} NaN values"
        )

    inf_count = np.isinf(array).sum()

    if inf_count > 0:
        raise ValueError(
            f"{name} contains {inf_count} infinite values"
        )

    return array


def preprocess_eda(eda) -> np.ndarray:
    """
    Prepare wrist EDA for downstream processing.

    Current POC:
    - convert to 1D
    - validate numerical values
    - keep native 4 Hz sampling rate
    - no filtering
    - no normalization
    """
    return validate_signal(eda, "EDA")


def preprocess_bvp(bvp) -> np.ndarray:
    """
    Prepare wrist BVP for downstream processing.

    Current POC:
    - convert to 1D
    - validate numerical values
    - keep native 64 Hz sampling rate
    - no filtering
    - no normalization
    """
    return validate_signal(bvp, "BVP")
