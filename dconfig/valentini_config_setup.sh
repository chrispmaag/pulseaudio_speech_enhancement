noisy_train=/home/ec2-user/valset/noisy_train_resampled
clean_train=/home/ec2-user/valset/clean_train_resampled
noisy_test=/home/ec2-user/valset/noisy_test_resampled
clean_test=/home/ec2-user/valset/clean_test_resampled
noisy_dev=/home/ec2-user/valset/noisy_dev_resampled
clean_dev=/home/ec2-user/valset/clean_dev_resampled

mkdir -p egs/val/tr
mkdir -p egs/val/cv
mkdir -p egs/val/tt

python -m denoiser.audio $noisy_train > egs/val/tr/noisy.json
python -m denoiser.audio $clean_train > egs/val/tr/clean.json

python -m denoiser.audio $noisy_test > egs/val/tt/noisy.json
python -m denoiser.audio $clean_test > egs/val/tt/clean.json

python -m denoiser.audio $noisy_dev > egs/val/cv/noisy.json
python -m denoiser.audio $clean_dev > egs/val/cv/clean.json
