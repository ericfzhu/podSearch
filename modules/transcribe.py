import logging
import os

import pandas as pd
import whisper

import utils


def run(device: str):
    # Load the Whisper model
    model = whisper.load_model('medium', device=device)

    # Iterate through all podcast directories
    directories = next(os.walk('data/.'))[1]
    for directory in directories:
        # Load podcast metadata and filter by not transcribed episodes
        metadata = pd.read_csv(f'data/{directory}/metadata.csv')
        to_process = metadata[~metadata['transcribed']]

        for i, episode in to_process.iterrows():
            try:
                # Try to transcribe the episode audio file and write the transcript to a file
                file_name = utils.slugify(episode.title)
                audio_path = f'data/{directory}/audio/{file_name}.mp3'
                result = model.transcribe(audio_path, verbose=False)
                pd.DataFrame(result.segments).to_csv(f'data/{directory}/transcriptions/{file_name}.csv', index=False)
                with open(f'data/{directory}/transcriptions/{file_name}.txt', 'w') as f:
                    f.write(result.text)

                # Update the original metadata file once the episode is transcribed
                metadata.loc[i, 'transcribed'] = True

            except:
                logging.warning(f'Unable to process transcription for episode: {episode.title}')

        # Save the updated metadata file
        metadata.to_csv(f'data/{directory}/metadata.csv', index=False)