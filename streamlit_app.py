import streamlit as st
from pydub import AudioSegment
import openai
import os

openai.api_key = st.secrets["api_secrets"]
# Define app header
st.set_page_config(page_title="EZ hindi 2 english", page_icon=":microphone:", layout="wide")

st.title("Hindi Audio to English Text")
st.markdown("""
    dont fuck it up. Enter your audio and get english text. simple.
""")

# file uploader
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
