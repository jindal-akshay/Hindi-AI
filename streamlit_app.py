import streamlit as st
from pydub import AudioSegment
import openai
import os

# Set OpenAI API key
openai.api_key = st.secrets["api_secrets"]

# Set app header and page configuration
st.set_page_config(
    page_title="EZ Hindi 2 English",
    page_icon=":microphone:",
    layout="wide",
    page_bg_color='#f7f7f7',
    )

# Set app header and description
st.title("EZ Hindi 2 English")
st.markdown("""
    Don't mess it up. Upload an audio file in Hindi and get the English transcript. It's simple.
""")

# Create file uploader
uploaded_file = st.file_uploader("Upload an mp3 or wav file", type=["mp3", "wav"])

if uploaded_file:
    # Read the content of the uploaded file
    file_content = uploaded_file.read()

    # Save the uploaded file to disk
    with open("test.mp3", "wb") as f:
        audio_file = f.write(file_content)

    # Display the uploaded file name and play the audio file
    st.write("Filename:", uploaded_file.name)
    audio_format = uploaded_file.type.split('/')[1]
    st.audio(file_content, format=f'audio/{audio_format}')

    # Get the transcript
    audio = open("test.mp3", 'rb')
    transcript = openai.Audio.translate("whisper-1", audio, "This transcript is in Hindi.")
    st.header("Transcript:")
    st.markdown(transcript["text"])

    # Close the file and delete it from disk
    audio.close()
    os.remove("test.mp3")
