import librosa
from librosa import display
from librosa.core import audio
import matplotlib.pyplot as plt
import numpy as np
# from scipy.io import wavfile

# next need to pass in a path to my audio file
# def create_spectrogram(audio_path):


def create_spectrogram(request_id, audio_type='noisy'):
    # sr, y = wavfile.read(path_to_audio_clip)
    # Librosa will resample down to 16000 with this arg
    y, sr = librosa.load(
        f'./static/{request_id}-{audio_type}.wav', sr=16000, mono=True,  dtype=np.float32)
    # y, sr = librosa.load(librosa.ex('trumpet'))
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                                   y_axis='mel', sr=sr,
                                   fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    fig.savefig(f'./static/{request_id}-{audio_type}.png')

# Basic version that works on librosa's built in dataset
# def create_spectrogram(audio_type='noisy'):
#     y, sr = librosa.load(librosa.ex('trumpet'))
#     S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
#     fig, ax = plt.subplots()
#     S_dB = librosa.power_to_db(S, ref=np.max)
#     img = librosa.display.specshow(S_dB, x_axis='time',
#                                    y_axis='mel', sr=sr,
#                                    fmax=8000, ax=ax)
#     fig.colorbar(img, ax=ax, format='%+2.0f dB')
#     ax.set(title='Mel-frequency spectrogram')
#     fig.savefig(f'./static/{audio_type}_spectrogram.png')
