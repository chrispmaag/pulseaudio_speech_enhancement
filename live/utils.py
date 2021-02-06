from wiener import vocal_separation
from demucs import get_demucs

def get_pipe(args):
    """
    Load pretrained model and return inference pipeline.
    """

    if args.kind == "demucs":
        

