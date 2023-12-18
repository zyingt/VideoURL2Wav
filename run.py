import os
import pandas as pd
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
from pytube import YouTube
from moviepy.editor import AudioFileClip
from bilibili2wav import bilibili2wav

# Constants
INPUT_CSV = 'singfake.csv'
OUTPUT_PATH = "/Users/hehaorui/Documents/GitHub/processSingfake/download"

def download_ytb_as_wav(youtube_url, output_path, index):
    """
    Download audio from a YouTube URL and save as WAV file.
    """
    try:
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        audio_file = video.download()
        audio_clip = AudioFileClip(audio_file)
        audio_clip.write_audiofile(f"{output_path}/{str(index)}.wav", codec='pcm_s16le', logger=None)
        os.remove(audio_file)
    except Exception as e:
        print(f"Error downloading from YouTube URL {youtube_url}: {e}")

def download_bilibili_as_wav(url, output_path, index):
    """
    Download audio from a Bilibili URL and save as WAV file.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    p_value = query_params.get('p', [None])[0]
    try:
        bilibili2wav(url, output_path, index, page=p_value)
    except Exception as e:
        print(f"Error downloading from Bilibili URL {url}: {e}")

def main():
    df = pd.read_csv(INPUT_CSV)
    for i in tqdm(range(len(df))):
        url = df["Url"].iloc[i]
        if str(i)+'.wav' in os.listdir(OUTPUT_PATH):
            continue
        if 'bilibili' in url:
            download_bilibili_as_wav(url, OUTPUT_PATH, i)
        elif 'youtube' in url:
            download_ytb_as_wav(url, OUTPUT_PATH, i)

if __name__ == "__main__":
    main()
