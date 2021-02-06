import numpy as np
import soundfile as sf
import librosa

from utils.metrics import pesq_score, stoi_score

def wiener_metrics_pipeline(_X: np.array, sr=16000):
    """np array pipeline for denoising and recording results.

    Params:
        _X (np.array): array of multiple time series to denoise.
        sr (int): sample rate of time series.

    Returns:
        np array: PESQ and STOI results of each time series. [[pesq, stoi], [...]]
    """
    res = np.empty((len(_X), 2), dtype=float64)
    for i, x in enumerate(_X):
        y, _ = vocal_separation(x, sr)
        p = pesq_score(x, y, samplerate=sr)
        st= stoi_score(x, y, samplerate=sr)
        res[i] = [p, st]

    return res

def wiener_pipeline(filepath, outpath, sample_rate=16000):
    """File to file pipeline for vocal denoising.

    Parameters:
        filepath (str): Path to input file.
        outpath (str): Path and name of output file.
        sample_rate (int, optional): Target sample rate. Defaults to 16kHz.

    Returns:
        None
    """
    y, sr = librosa.load(filepath, sr=sample_rate)
    y, sr = vocal_separation(y, sr)
    sf.write(outpath, y, sr, 'PCM_16')

def vocal_separation(y, sr):
    """Vocal Separation

    This function is implements a simple vocal separation technique
    based on the "REPET-SIM" method of 'Rafii and Pardo, 2012'.

    Parameters:
        y (np.array): The audio time series.
        sr (int): Sample rate of 'y'.

    Retuns:
        np.array: The filtered foreground audio time series.
        int: The sample rate of the time series.

    Based on code by: Brian McFee
    License: ISC
    """
    
    # Compute the spectrogram magnitude and phase.

    S_full, phase = librosa.magphase(librosa.stft(y))

    # We'll compare frames using cosine similarity, and aggregate similar frames
    # by taking their (per-frequency) median value.
    #
    # To avoid being biased by local continuity, we constrain similar frames to be
    # separated by at least 2 seconds.
    #
    # This suppresses sparse/non-repetetitive deviations from the average spectrum,
    # and works well to discard vocal elements.

    S_filter = librosa.decompose.nn_filter(S_full,
                                           aggregate=np.median,
                                           metric='cosine',
                                           k=2)
                                           #width=int(librosa.time_to_frames(2, sr=sr)))

    # The output of the filter shouldn't be greater than the input
    # if we assume signals are additive.  Taking the pointwise minimium
    # with the input spectrum forces this.

    S_filter = np.minimum(S_full, S_filter)

    # The raw filter output can be used as a mask,
    # but it sounds better if we use soft-masking.
    # Non-local filtering is converted into a soft mask by Wiener filtering.
    
    margin_v = 10
    power = 2

    mask_v = librosa.util.softmask(S_full - S_filter,
                                   margin_v * S_filter,
                                   power=power)

    # Once we have the mask, multiply it with the input spectrum
    # to separate the components

    S_foreground = mask_v * S_full

    # Approximate magnitude spectrogram inversion using the “fast” Griffin-Lim algorithm.

    y = librosa.griffinlim(S_foreground)

    return y, sr

