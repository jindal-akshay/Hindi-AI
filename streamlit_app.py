import streamlit as st
import pytube
import os
from pydub import AudioSegment
import openai

openai.api_key = st.secrets["api_secrets"]
# Define app header
st.set_page_config(page_title="EZ hindi 2 english", page_icon=":microphone:", layout="wide")

st.title("EZ hindi 2 english")
st.markdown("""
    dont fuck it up. Enter your audio and get english translation. simple.
""")

# file uploader
uploaded_file = st.file_uploader("Upload an mp3 or wav file", type=["mp3", "wav"])

# YouTube video input
youtube_url = st.text_input("Enter the URL of a YouTube video")

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
    # close the file
    audio.close()
    os.remove("test.mp3")

if youtube_url:
    # Download YouTube video
    yt = pytube.YouTube(youtube_url)
    stream = yt.streams.get_highest_resolution()
    video_file = stream.download()

    # Convert video file to WAV format
    if video_file:
        audio_file = os.path.splitext(video_file)[0] + ".wav"
        AudioSegment.from_file(video_file).export(audio_file, format="wav")

        # Get the transcript
        with open(audio_file, "rb") as f:
            transcript = openai.Audio.translate("whisper-1", f, "This transcript is in Hindi.")
        st.header("Transcript:")
        st.markdown(transcript["text"])

        # Remove the temporary audio file
        os.remove(audio_file)
    else:
        st.error("Failed to download YouTube video")
