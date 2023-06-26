import streamlit as st
import yt_dlp
import ffmpeg
from pydub import AudioSegment
import openai
import os

openai.api_key = st.secrets["api_secrets"]
# Define app header
st.set_page_config(page_title="EZ hindi 2 english", page_icon=":microphone:", layout="wide")

st.title("EZ hindi 2 english")
st.markdown("""
    dont fuck it up. Enter your audio and get english translation. simple.
""")

def download_mp3_from_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# file uploader
uploaded_file = st.file_uploader("Upload an mp3 or wav file", type=["mp3", "wav"])
youtube_link = st.text_input("Enter a YouTube link")

if uploaded_file:
    # Read the content of the uploaded file
    file_content = uploaded_file.read()

    with open("test.mp3", "wb") as f:
        audio_file = f.write(file_content)
    
    st.write("Filename:", uploaded_file.name)
    audio_format = uploaded_file.type.split('/')[1]  # Get the file format, either 'mp3' or 'wav'
    audio_path = "test.mp3"
    
elif youtube_link:
    download_mp3_from_youtube(youtube_link)
    st.write("Downloading audio from YouTube...")
    audio_format = "mp3"
    audio_path = f"{youtube_link.split('=')[1]}.mp3"

    st.write("YouTube Link:", youtube_link)
    st.audio(youtube_link, format='audio/mp3')

if uploaded_file or youtube_link:
    audio = open(audio_path, 'rb')
    # Get the transcript
    transcript = openai.Audio.translate("whisper-1", audio, "This transcript is in Hindi.")
    st.header("Transcript:")
    st.markdown(transcript["text"])
    print(transcript)
    # close the file
    audio.close()
    os.remove(audio_path)
