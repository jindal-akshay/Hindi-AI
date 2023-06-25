import streamlit as st
from pydub import AudioSegment
import openai
import os

openai.api_key = st.secrets["api_secrets"]
# Define app header
st.set_page_config(page_title="EZ hindi 2 english", page_icon=":microphone:", layout="wide")

# Translation function
def translate_text(text, source_lang, target_lang):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Translate the following text from {source_lang} to {target_lang}: {text}",
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None
    )

    translation = response.choices[0].text.strip()
    return translation

# App title and description
st.title("EZ hindi 2 english")
st.markdown("""
    Don't mess it up. Enter your audio and get the English translation. Simple.
""")

# File uploader
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
    transcript_text = transcript["text"]
    
    # Translate the transcript from Hindi to English
    translated_text = translate_text(transcript_text, "hi", "en")
    
    st.header("Transcript:")
    st.markdown(transcript_text)
    
    st.header("Translated Text:")
    st.markdown(translated_text)
    
    # Close the file
    audio.close()
    os.remove("test.mp3")
