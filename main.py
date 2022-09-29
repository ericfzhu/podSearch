import argparse


from transcribe_podcast import playlist, transcribe


channel_id = "UCESLZhusAkFfsNsApnjF_Cg"
# data = playlist.get(channel_id)
# playlist.download(data)

transcribe.run()


def cli():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("channel_id", nargs="+", type=str, help="Youtube channel(s) to transcribe")
    parser.add_argument("--verbose", type=str2bool, default=False, help="Print out progress and debug messages")


    args = parser.parse_args().__dict__
