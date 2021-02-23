import librosa
from librosa import display
from librosa.core import audio
import matplotlib.pyplot as plt
import numpy as np

def create_spectrogram(request_id, audio_type='noisy'):
    # Librosa will resample down to 16000 with this arg
    y, sr = librosa.load(
        f'./static/{request_id}-{audio_type}.wav', sr=16000, mono=True,  dtype=np.float32)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                                   y_axis='mel', sr=sr,
                                   fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    fig.savefig(f'./static/{request_id}-{audio_type}.png')