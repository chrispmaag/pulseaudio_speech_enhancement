import argparse
import sys

import sounddevice as sd
import numpy as np

from wiener.pipeline import vocal_separation

def get_parser():
    parser = argparse.ArgumentParser(
        "PulseAudio",
        description="Live speech enhancement!\n"
                    "Created by:\n"
                    "    Chris Pontarolo-Maag\n"
                    "    Jorge Sierra\n"
                    "    Leo Tanenbaum-Diaz\n"
                    "\n"
                    "Uses the default mic (or interface specified by --in) and "
                    "writes the enhanced version to 'Soundflower (2ch)' "
                    "(or the interface specified by --out).",
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument(
        "-i", "--in", dest="in_",
        help="name or index of input interface.")
    parser.add_argument(
        "-o", "--out", dest="out_", default="Soundflower (2ch)",
        help="name or index of output interface.")
    parser.add_argument(
        "--sample_rate", type=int, default=16_000,
        help="Sample rate")
    parser.add_argument(
        "--dry", type=float, default=0.04,
        help="Dry/wet knob, between 0 and 1. 0=maximum noise removal "
             "but it might cause distortions. Default is 0.04")
    return parser


def parse_audio_device(device):
    if device is None:
        return device
    try:
        return int(device)
    except ValueError:
        return device


def query_devices(device, kind):
    try:
        caps = sd.query_devices(device, kind=kind)
    except ValueError:
        message = bold(f"Invalid {kind} audio interface {device}.\n")
        message += (
            "If you are on Mac OS X, try installing Soundflower "
            "(https://github.com/mattingalls/Soundflower).\n"
            "You can list available interfaces with `python3 -m sounddevice` on Linux and OS X, "
            "and `python.exe -m sounddevice` on Windows. You must have at least one loopback "
            "audio interface to use this.")
        print(message, file=sys.stderr)
        sys.exit(1)
    return caps


def main():
    args = get_parser().parse_args()

    device_in = parse_audio_device(args.in_)
    caps = query_devices(device_in, "input")
    channels_in = min(caps['max_input_channels'], 2)
    stream_in = sd.InputStream(
        device=device_in,
        samplerate=args.sample_rate,
        channels=channels_in)

    device_out = parse_audio_device(args.out_)
    caps = query_devices(device_out, "output")
    channels_out = min(caps['max_output_channels'], 2)
    stream_out = sd.OutputStream(
        device=device_out,
        samplerate=args.sample_rate,
        channels=channels_out)

    stream_in.start()
    stream_out.start()

    length = 256
    first = True
    while True:
        try:
            frame, overflow = stream_in.read(length)

            # do the thing:
            out = frame

            # compressor
            out = 0.99 * np.tanh(out)

            out = np.clip(out, -1, 1)
            underflow = stream_out.write(out)
        except KeyboardInterrupt:
            print("Stopping")
            break
    stream_out.stop()
    stream_in.stop()

if __name__ == "__main__":
    main()
