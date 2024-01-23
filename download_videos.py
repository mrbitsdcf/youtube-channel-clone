"""
Clone your Youtube Channel

Author: MrBiTs <mrbits@mrbits.com.br>
Date: 20 Auroran 2024
"""

import csv
import os
import logging
import ffmpeg
import requests
import sys
from pytube import YouTube
from pytube import Channel
from slugify import slugify


logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


def download_video(video_link, folder, maxres=None):
    """
    Download individual video, audio and thumbnail.
    Concatenate video and audio files and
    save it to folder, slugifying the name.
    Erase video and audio files.
    """

    if maxres is None:
        logging.info("Video Started")
        video_file = YouTube(video_link).streams.order_by(
            'resolution').desc().first().download()
        logging.info("Video Done")
    else:
        logging.info("Video Started")
        video_file = YouTube(video_link).streams.filter(
            res=maxres).order_by('resolution').desc().first().download()
        logging.info("Video Done")

    video_name = slugify(video_file.replace(".webm", "").split("/")[-1], allow_unicode=True)

    logging.info("Audio Started")
    audio_file = YouTube(video_link).streams.filter(only_audio=True).order_by(
        'abr').desc().first().download(filename_prefix="audio_")

    logging.info("Audio Done")

    logging.info("Thumbnail start")
    thumbnail_url = YouTube(video_link).thumbnail_url
    img_data = requests.get(thumbnail_url).content
    image_name = f"{video_name}.jpg"
    with open(f"{folder}/{image_name}", 'wb') as handler:
        handler.write(img_data)

    logging.info("Thumbnail done")

    source_audio = ffmpeg.input(audio_file)
    source_video = ffmpeg.input(video_file)

    logging.info("Concatenation Started")

    ffmpeg.concat(source_video, source_audio, v=1, a=1).output(f"{folder}/{video_name}.mp4").run()

    logging.info("Concatenation Done")

    if os.path.exists(audio_file):
        os.remove(audio_file)

    if os.path.exists(video_file):
        os.remove(video_file)

    return None


def download_channel(channel_link, folder, maxres=None):
    """
    Get a list with the URL of all videos in a given channel.
    Search the URL in a verification file.
    If found, the video is alread downloaded.
    If not, then call download_video function.
    With success, write video URL into the verification file.
    """

    pure_link = channel_link
    list_videos = Channel(pure_link).video_urls
    video_count = 0
    total_videos = len(list_videos)
    logging.info('%s Videos Found', total_videos)

    list_videos_downloaded = []

    with open('youtube_export_history.csv', 'r', encoding="utf-8", newline='') as csvfile:
        spamwriter = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in spamwriter:
            list_videos_downloaded.append(row[0])

    for video in list_videos:
        if video in list_videos_downloaded:
            video_count = video_count + 1
            logging.info('Video %s/%s already downloaded', video_count, total_videos)
        else:
            logging.info(video)
            video_count = video_count + 1
            logging.info('%s/%s Started', video_count, total_videos)
            download_video(video_link=video, maxres=maxres, folder=folder)

            with open('youtube_export_history.csv', 'a', encoding="utf-8", newline='') as csvfile:
                spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([video])

            logging.info('%s/%s Done', video_count, total_videos)


if __name__ == "__main__":
    try:
        channel_url = sys.argv[1]
    except IndexError:
        print("""Error trying to execute script.

Usage:
    python download_videos.py https://youtube.com/@ChannelName
        """)
        sys.exit(1)

    download_channel(
        channel_link=channel_url,
        folder="Videos",
        maxres=None
    )
