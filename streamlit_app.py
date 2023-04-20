import streamlit as st
from pydub import AudioSegment
import openai
import os
import requests
from io import BytesIO
import urllib.request
import youtube_dl


openai.api_key = st.secrets["api_secrets"]
# Define app header
st.set_page_config(page_title="EZ hindi 2 english", page_icon=":microphone:", layout="wide")

st.title("EZ hindi 2 english")
st.markdown("""
    dont fuck it up. Enter your audio and get english translation. simple.
""")

# file uploader
option = st.selectbox("Select a source", ["Upload an mp3 or wav file", "Enter a YouTube link"])
if option == "Upload an mp3 or wav file":
    uploaded_file = st.file_uploader("Upload an mp3 or wav file", type=["mp3", "wav"])

    if uploaded_file:
        # Read the content of the uploaded file
        file_content = uploaded_file.read()

        with open("test.mp3", "wb") as f:
            audio_file = f.write(file_content)

        st.write("Filename:", uploaded_file.name)
        audio_format = uploaded_file.type.split('/')[1]  # Get the file format, either 'mp3' or 'wav'
        audio = open("test.mp3", 'rb')
        # Play the uploaded audio file
        st.audio(file_content, format=f'audio/{audio_format}')

        # Get the transcript
        transcript = openai.Audio.translate("whisper-1", audio, "This transcript is in Hindi.")
        st.header("Transcript:")
        st.markdown(transcript["text"])
        print(transcript)
        # close the file
        audio.close()
        os.remove("test.mp3")

elif option == "Enter a YouTube link":
    yt_link = st.text_input("Enter a YouTube link")
    if yt_link:
        with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
            info_dict = ydl.extract_info(yt_link, download=False)
            video_title = info_dict.get('title', None)
            video_url = info_dict.get("url", None)
            audio_url = info_dict["formats"][-1]["url"]
            st.write("Video Title:", video_title)
            # Download audio file
            with requests.get(audio_url) as r:
                audio_file = r.content
            st.audio(audio_file, format="audio/mp3")

            # Get the transcript
            audio = BytesIO(urllib.request.urlopen(audio_url).read())
            transcript = openai.Audio.translate("whisper-1", audio, "This transcript is in Hindi.")
            st.header("Transcript:")
            st.markdown(transcript["text"])
            print(transcript)
