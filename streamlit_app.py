import streamlit as st
import pafy
import yt_dlp

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    from __future__ import unicode_literals
    import youtube_dl
    ydl_opts = {
         'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['link'])

use this:
from pytube import YouTube
import os

yt = YouTube('link')

video = yt.streams.filter(only_audio=True).first()

out_file = video.download(output_path=".")

base, ext = os.path.splitext(out_file)
new_file = base + '.mp3'
os.rename(out_file, new_file)
