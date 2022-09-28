import whisper
import glob
import os
from pathlib import Path
import pandas as pd

model = whisper.load_model('medium')
videos = glob.glob('videos/*')

for video in videos:
    result = model.transcribe(video)
    basename = os.path.basename(video)
    Path(f'output/{basename}').mkdir(parents=True, exist_ok=True)

    pd.DataFrame(result['segments']).to_csv(f'output/{basename}/segments.csv')
    with open(f'output/{basename}/text.txt', 'w') as f:
        f.write(result['text'])