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
    pls enter your hindi audio below.
""")

# Display file uploader
audio_file = st.file_uploader("Upload an mp3 or wav file", type=["mp3", "wav"])

# Translate audio to text and display result
if audio_file is not None:
    # Convert file contents to bytes
    audio_bytes = BytesIO(audio_file.read()).getvalue()

    # Load audio file using PyDub
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format=audio_file.type)

    # Extract audio data as raw PCM
    raw_audio_data = audio.raw_data

    # Send audio to OpenAI to generate transcript
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Please translate the following Hindi audio to English:\n\n{raw_audio_data.decode('utf-8')}\n",
        temperature=0.8,
        max_tokens=2048,
        n = 1,
        stop=None,
        timeout=60,
        frequency_penalty=0,
        presence_penalty=0
    )
    transcript = response.choices[0].text.strip()

    st.header("Transcript:")
    st.text(transcript)
