from pathlib import Path
import pickle


WESAD_ROOT = Path("data/raw/WESAD")


def load_subject(subject_id: str) -> dict:
    """
    Load a single WESAD subject.

    Parameters
    ----------
    subject_id : str
        Subject ID, e.g. "S2".

    Returns
    -------
    dict
        Raw subject data loaded from the WESAD pickle file.
    """
    subject_path = WESAD_ROOT / subject_id / f"{subject_id}.pkl"

    if not subject_path.exists():
        raise FileNotFoundError(
            f"WESAD subject file not found: {subject_path}"
        )

    with subject_path.open("rb") as f:
        data = pickle.load(f, encoding="latin1")

    if not isinstance(data, dict):
        raise TypeError(
            f"Expected WESAD subject data to be dict, got {type(data).__name__}"
        )

    return data


def get_subject_signals(subject_id: str) -> dict:
    """
    Load a subject and return the signals required for the POC.

    The POC currently uses wrist EDA and BVP together with the label signal.
    """
    data = load_subject(subject_id)

    try:
        wrist = data["signal"]["wrist"]
        label = data["label"]
    except KeyError as exc:
        raise KeyError(
            f"Missing expected WESAD key: {exc}"
        ) from exc

    required_signals = ("EDA", "BVP")

    for signal_name in required_signals:
        if signal_name not in wrist:
            raise KeyError(
                f"Missing wrist signal: {signal_name}"
            )

    return {
        "subject_id": subject_id,
        "eda": wrist["EDA"],
        "bvp": wrist["BVP"],
        "label": label,
    }
