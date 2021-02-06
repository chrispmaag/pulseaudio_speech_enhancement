
class AudioStreamer:
    def __init__(self,
            sample_rate=16000,
            frame_length=256):
        self.sample_rate = sample_rate
        self.frame_length = frame_length

    def feed(self, signal):
        return signal
