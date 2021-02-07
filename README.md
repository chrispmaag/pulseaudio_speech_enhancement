# Pulse Audio Real-Time Speech Enhancement
### Real-time speech enhancement for noisy calls. 

For your business partners, family members, or friends, background noise in conference calls can be distracting, unprofessional, and make understanding difficult. With working remotely becoming more common, it’s critical that people can work efficiently and productively from wherever they choose. 

What if we could remove the background noise, enabling workers to focus and understand exactly what their teammates are sharing or explaining? There would be fewer misunderstandings and mistakes, along with faster, more efficient communication. As a result, everyone gets time back in their schedules, and less mental fatigue from all-day video-conference meetings.

Our project aims to tackle this problem by focusing on using real-time speech enhancement to improve the quality of noisy virtual calls.

Data Sets:
- [Valentini](https://datashare.is.ed.ac.uk/handle/10283/2791)
- [Deep Noise Suppression (DNS)](https://github.com/microsoft/DNS-Challenge)

Metrics:
- [Perceptual Evaluation of Speech Quality (PESQ)](https://en.wikipedia.org/wiki/Perceptual_Evaluation_of_Speech_Quality)
- Short Term Objective Intelligibility (STOI)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```
pip install -r requirements.txt
```

## Usage

```
python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

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

Coming soon.

Noisy: Enhanced:

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

- Leo Tanenbaum-Diaz
- Chris Pontarolo-Maag - [@chrispmaag](https://twitter.com/chrispmaag) - chrispmaag@gmail.com
- Jorge Sierra - [@sierrajur](https://twitter.com/sierrajur) - jsierra.jur@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)
