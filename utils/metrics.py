import numpy as np
from pesq import pesq, PesqError


def pesq_score(y_true: np.array, y_pred: np.array, samplerate=16000, mode='wb') -> float:
    """Computes the Perceptual evaluation of speech quality metric between `y_true` and `y_pred`.

    Args:
        y_true (np.array): The original audio signal with shape (samplerate*length).
        y_pred (np.array): The predicted audio signal with shape (samplerate*length).
        rate (int, optional): Either 8000 or 16000. Defaults to 16000.
        mode (str, optional): Either 'wb' or 'nb'. 'wb' is only available for 16000Hz. Defaults to 'wb'.

    Returns:
        float: The pesq score between `y_true` and `y_pred`.
    """
    return pesq(ref=y_true, deg=y_pred, rate=samplerate, mode=mode, on_error=PesqError.RETURN_VALUES)
