import sounddevice as sd
import numpy as np


def record(length: int, samplerate=48000, channels=2) -> np.array:
    """Records the default audio device input stream into a numpy array.

    TODO: Implement input device selection.

    Args:
        length (int): The duration of the recording in seconds.
        samplerate (int, optional): The number of samples to record per second. Defaults to 48000.
        channels (int, optional): The number of channels supported by the input device. Defaults to 2.

    Returns:
        np.array: A numpy array with shape (length*samplerate, channels).
    """
    recording = sd.rec(length*samplerate, samplerate=samplerate,
                       blocking=True, channels=channels)
    return recording


def play(data: np.array, samplerate=48000) -> None:
    """Plays the input data into the default output audio device.

    TODO: Implement output device selection.

    Args:
        data (np.array): A numpy array of dimensions (samplerate*length, channels).
        samplerate (int, optional): Sampling of the input data in Hertz. Defaults to 48000.
    """
    sd.play(data, samplerate)
    status = sd.wait()
 