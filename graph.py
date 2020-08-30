import librosa
import numpy as np

def get_mel_spectrogram(path):
    y, sr = librosa.load(path)

    mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=1024)
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

    return mel_spect


