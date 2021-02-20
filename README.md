# Pulse Audio Real-Time Speech Enhancement
### Real-Time Speech Enhancement for a Better Workflow

![deployed_result_1](https://github.com/chrispmaag/pulseaudio_speech_enhancement/blob/main/images/deployed_result_1.jpg)

Check out our deployed project at [http://pulseaudio.duckdns.org](http://pulseaudio.duckdns.org)!

For your business partners, family members, or friends, background noise in conference calls can be distracting, unprofessional, and make understanding difficult. With working remotely becoming more common, it’s critical that people can work efficiently and productively from wherever they choose.

What if we could remove the background noise, enabling workers to focus and understand exactly what their teammates are sharing or explaining? There would be fewer misunderstandings and mistakes, along with faster, more efficient communication. As a result, everyone gets time back in their schedules, and less mental fatigue from all-day video-conference meetings.

Our project aims to tackle this problem by focusing on using real-time speech enhancement to improve the quality of noisy virtual calls.

## The Team

- Leo Tanenbaum-Diaz [LinkedIn](https://linkedin.com/in/leot-d)
- Chris Pontarolo-Maag - [LinkedIn](https://linkedin.com/in/chrispmaag) 
- Jorge Sierra - [LinkedIn](https://www.linkedin.com/in/jorgeandressierrajurado) 

---

Data Sets:
- [Valentini](https://datashare.is.ed.ac.uk/handle/10283/2791)
- [Deep Noise Suppression (DNS)](https://github.com/microsoft/DNS-Challenge)

Metrics:
- [Perceptual Evaluation of Speech Quality (PESQ)](https://en.wikipedia.org/wiki/Perceptual_Evaluation_of_Speech_Quality)
- Short Term Objective Intelligibility (STOI)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependecies.

```
pip install -r requirements.txt
```

## Usage

```
cd development
python -m denoiser.enhance --file_location="PATH_TO_WAV"
```
The enhanced audio clip will be saved in `denoiser/static`.

## Results

![target_results_denoiser](https://github.com/chrispmaag/pulseaudio_speech_enhancement/blob/main/images/target_results_denoiser.jpg)

Results on the Valentini dataset.

| Model         | PESQ | STOI (%) |
|:-------------:| ----:| ----:    |
| Wiener*       | 2.22 | 93       |
| SEGAN**       | 2.19 | 93.12    |
| SASEGAN**     | 2.36 | 03.32    |
| Wave U-Net*   | 2.40 | -        |
| DEMUCS        | 2.96 | 94.21    |

\* Results from Table 1 of Denoiser paper <br />
** Results from Table 1 of SASEGAN paper

### Samples from the Valentini test set

(Github Markdown doesn't support embeding audio, so this will have to do.)

Here we have a few side-by-side spectrogram comparisons of the results of our model. You can see that in general our model tends to perform much like a traditional gate would. In sections devoid of speech, the model effectively removes extraneous sounds. However, it also seems to be overcompensating in the higher frequency ranges during sections of speech.

Compare the 'clean' and 'enhanced' spectrograms for each example and you'll see noticably more activity in the upper regions of speech segments (corresponding to higher frequency sounds).

In audio clips, these differences manifest as a form of digital white noise and sharpness in the higher registers.

![good result 1](https://github.com/chrispmaag/pulseaudio_speech_enhancement/blob/main/images/p232_005_spectrogram_comparison.png)
![good result 2](https://github.com/chrispmaag/pulseaudio_speech_enhancement/blob/main/images/p232_125_spectrogram_comparison.png)
![good result 3](https://github.com/chrispmaag/pulseaudio_speech_enhancement/blob/main/images/p232_142_spectrogram_comparison.png)
![bad result 1](https://github.com/chrispmaag/pulseaudio_speech_enhancement/blob/main/images/p257_022_spectrogram_comparison.png)
![bad result 2](https://github.com/chrispmaag/pulseaudio_speech_enhancement/blob/main/images/p257_430_spectrogram_comparison.png)

Something else to keep an eye on is the sharpness of the spectrogram images. The "grainy" quality of the spectrogram images are indicative of broad-spectrum noise across the signal. Think: cars idling or a consistent breeze.

Looking at the final two examples in particular, you can see a clear contrast in the sharpness of the 'clean' clip as compared with the 'enchanced' indicating that the model was unable to fully eliminate broad-spectrum noise.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
[MIT](https://choosealicense.com/licenses/mit/)
