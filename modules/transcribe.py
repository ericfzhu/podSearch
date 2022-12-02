import whisper
import glob
import os
from pathlib import Path
import pandas as pd


def run(device: str, output_dir: str):
    model = whisper.load_model('medium', device=device)
    videos = glob.glob('videos/*')
    for video in videos:
        result = model.transcribe(video, verbose=True)
        audio_basename = os.path.basename(video)
        print(audio_basename)
        Path(os.path.join(output_dir, audio_basename)).mkdir(parents=True, exist_ok=True)

        pd.DataFrame(result['segments']).to_csv(os.path.join(output_dir, audio_basename, "segments.csv"))
        print(result['segments'])
        with open(os.path.join(output_dir, audio_basename, "text.txt"), 'w', encoding="utf-8") as f:
            f.write(result['text'])
