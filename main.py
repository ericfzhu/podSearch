import argparse
import os

import torch.cuda

from transcribe_podcast import playlist, transcribe

# channel_id = "UCESLZhusAkFfsNsApnjF_Cg"
# data = playlist.get(channel_id)
# playlist.download(data)

# transcribe.run()


def cli():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("channel_id", nargs="+", type=str, help="Youtube channel(s) to transcribe")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu", help="Device to use for "
                                                                                                 "transcription")
    parser.add_argument("-v", "--verbose", type=bool, default=False, help="Print out progress and debug messages")
    parser.add_argument("-o", "--output_dir", type=str, default="output", help="Directory to store output transcripts")

    args = parser.parse_args().__dict__
    channel_id: str = args.pop("channel_id")
    device: str = args.pop("device")
    output_dir: str = args.pop("output_dir")

    os.makedirs(output_dir, exist_ok=True)

    # data = playlist.get(channel_id)
    # playlist.download(data)

    transcribe.run(device, output_dir)


if __name__ == '__main__':
    cli()
