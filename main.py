import argparse
from pytubefix import YouTube
import os
from tqdm import tqdm


def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    live_progress = bytes_downloaded / total_size
    tqdm_instance.update(int(live_progress * total_size) - tqdm_instance.n)


# Setting up parser
parser = argparse.ArgumentParser(
    description="Example usage: python main.py --url 'https://www.youtube.com/watch?v=...' --output 'my_downloads' --resolution '1080p'")
parser.add_argument("--url", help="The YouTube video URL to download")
parser.add_argument(
    "--output", help="The folder path to store the downloaded video", default="downloads")
parser.add_argument("--resolution", help="Desired resolution")
args = parser.parse_args()

url = args.url
resolution = args.resolution
output = args.output

# If youtube.com is in the URL, then it could plausibly be a YouTube link.
if "youtube.com" in url:
    try:
        yt = YouTube(url, on_progress_callback=progress_function)
    except Exception:
        print("Could not find a Youtube video with that URL")
    else:
        # if the resolution is not specified, the stream will be the highest resolution
        if resolution == None:
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(res=resolution).first()

        tqdm_instance = tqdm(total=stream.filesize, unit="B",
                             unit_scale=True, desc=stream.title, ascii=True)
        # if the folder to download video exists, then download video there. If not, then make the folder and download
        if os.path.exists(output):
            try:
                stream.download(output)
            except Exception as e:
                print("An unexpected error occured during download: ", e)
        else:
            os.makedirs(output)
            try:
                stream.download(output)
            except Exception as e:
                print("An unexpected error occured during download: ", e)
        tqdm_instance.close()
else:
    print("Please at least provide a youtube.com url")
