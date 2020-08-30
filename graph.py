import numpy as np
import librosa
import librosa.display
import os

def get_mel_spectrogram(path):
    y, sr = librosa.load(path)

    mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=1024)
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

    return mel_spect

def get_mel_spectrogram_for_each_genre():
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    mel_spectograms = []

    for genre in genres:
        path = os.listdir(f'genres/{genre}')[0]
        path = f'genres/{genre}/{path}'
        mel_spect = get_mel_spectrogram(path=path)
        mel_spectograms.append(mel_spect)

    return mel_spectograms


if __name__ == '__main__':
    l = get_mel_spectrogram_for_each_genre()
    for s in l:
        librosa.display.specshow(s, y_axis='mel', fmax=8000, x_axis='time')
