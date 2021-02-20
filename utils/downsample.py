# save to a different directory for easier creating of the necessary json files

from pydub import AudioSegment as am
import os

def resample_wav(input_filepath, output_filepath):
    sound = am.from_file(input_filepath, format='wav', frame_rate=48000)
    sound = sound.set_frame_rate(16000)
    sound.export(output_filepath, format='wav')

def process_wavs(directory, output_directory):
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    for f in os.listdir(directory):
        print(directory)
        print(f)
        resample_wav(directory + '/' + f, output_directory + '/' + f[:-4] + '_resampled.wav')

process_wavs('/home/ec2-user/valset/clean_train', '/home/ec2-user/valset/clean_train_resampled')
process_wavs('/home/ec2-user/valset/clean_test', '/home/ec2-user/valset/clean_test_resampled')
process_wavs('/home/ec2-user/valset/clean_dev', '/home/ec2-user/valset/clean_dev_resampled')
process_wavs('/home/ec2-user/valset/noisy_train', '/home/ec2-user/valset/noisy_train_resampled')
process_wavs('/home/ec2-user/valset/noisy_test', '/home/ec2-user/valset/noisy_test_resampled')
process_wavs('/home/ec2-user/valset/noisy_dev', '/home/ec2-user/valset/noisy_dev_resampled')
