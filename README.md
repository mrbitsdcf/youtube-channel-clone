Youtube Channel Clone
===


# About the project

Project to backup and clone a Youtube channel by downloading all videos in highest resolution available and keep them as a backup.


# Requirements

The first thing we are going to need is to install the two libraries that we will use throughout this project.

The first one is called pytube and is available with pip. It’s a simple interface that allows us to retrieve information from Youtube videos feeds and download those videos. It supports thumbnail download, supports caption track downloading as .srt files and many more features. For the purpose of this exercise, we will only focus on how to download videos. Due to a new channel name format with @, we need to use a patched version, already configured in requirements.txt.

The second library we are going to need is called FFmpeg and is also available with pip. If you are familiar with the eponym command-line tool, it is a simple interface between the actual tool and the Python language.

Once you have installed these two Python libraries, you also need to download the actual FFmpeg tool. Just head on to their [downloads](https://www.ffmpeg.org/download.html) page and pick the software appropriate for your operating system.


# Instructions

I recommend to create a python virtual environment to execute the steps bellow.

1. Clone the repository and access the folder

```
git clone URL
cd youtube-channel-clone
```

2. Create a Python virtualenv

```
python -m venv venv
```

3. Install libraries

```
pip install -R requirements.txt
```

4. Get the Channel URL and run dowload_videos.py

```
python download_videos.py "https://youtube.com/@channelname"
```

5. Wait until finish

6. TODO: Automatically upload videos to a new channel, by using google-api-python-client.
