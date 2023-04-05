import openai
import streamlit as st
from io import BytesIO
from pydub import AudioSegment

# Set OpenAI API key
openai.api_key = st.secrets["api_secrets"]

# Define app header
st.set_page_config(page_title="Hindi Audio to English Text", page_icon=":microphone:", layout="wide")

st.title("Hindi Audio to English Text")
st.markdown("""
    This app uses OpenAI to translate Hindi audio to English text. 
    Simply upload an mp3 file and the app will generate a transcript in English.
""")

# Display file uploader
audio_file = st.file_uploader("Upload an mp3 file", type=["mp3"])

# Translate audio to text and display result
if audio_file is not None:
    # Convert file contents to bytes
    audio_bytes = BytesIO(audio_file.read()).getvalue()

    # Convert audio file to AudioSegment object
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")

    # Translate audio to text
    response = openai.Audio.create(model="whisper-1", media=audio.raw_data, sample_rate=audio.frame_rate, language="hi")
    transcript = response['text']

    st.header("Transcript:")
    st.text(transcript)
