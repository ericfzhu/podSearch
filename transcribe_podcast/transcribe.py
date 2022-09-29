import whisper
import glob
import os
from pathlib import Path
import pandas as pd

model = whisper.load_model('medium')
videos = glob.glob('videos/*')


def run():
    for video in videos:
        result = model.transcribe(video)
        audio_basename = os.path.basename(video)
        Path(f'output/{audio_basename}').mkdir(parents=True, exist_ok=True)

        pd.DataFrame(result['segments']).to_csv(f'output/{audio_basename}/segments.csv')

        with open(f'output/{audio_basename}/text.txt', 'w', encoding="utf-8") as f:
            f.write(result['text'])
