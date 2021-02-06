from wiener.pipeline import wiener_pipeline
import librosa

#wiener_pipeline('samples/valentini_noisy_testset_wav_p232_003.wav', 'output2.wav')

filepath = 'test.wav' 

y, sr = librosa.load(filepath, sr=16000)
print(y.shape)

