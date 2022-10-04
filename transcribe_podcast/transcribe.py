import whisper
import glob
import os
from pathlib import Path
import pandas as pd


def run(device: str, output_dir: str):
    model = whisper.load_model('medium', device=device)
    videos = glob.glob('videos/*')
    for video in videos:
        result = model.transcribe(video)
        audio_basename = os.path.basename(video)
        Path(os.path.join(output_dir, audio_basename)).mkdir(parents=True, exist_ok=True)

        pd.DataFrame(result['segments']).to_csv(os.path.join(output_dir, audio_basename, "segments.csv"))

        with open(os.path.join(output_dir, audio_basename, "text.txt"), 'w', encoding="utf-8") as f:
            f.write(result['text'])
