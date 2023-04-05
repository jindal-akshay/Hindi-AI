import openai
import streamlit as st
from io import BytesIO

# Set OpenAI API key
openai.api_key = st.secrets["api_secrets"]

# Streamlit app header
st.set_page_config(page_title="Audio Translator", page_icon=":loud_sound:")

# Display app header
st.header("Audio Translator")
st.subheader("Translate MP3 audio to English")

# Display app description
st.write("This app allows you to upload an MP3 audio file and translates it to English using OpenAI's GPT-3 language model.")

# Display a file uploader in Streamlit
audio_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

# Check if a file was uploaded
if audio_file:
    # Read the uploaded file
    audio_bytes = audio_file.read()
    
    # Convert the bytes to a file-like object
    audio_fileobj = BytesIO(audio_bytes)
    
    # Use OpenAI API to translate audio
    response = openai.Audio.translate("whisper-1", audio_fileobj)
    
    # Extract the transcript text from the response
    transcript = response['text']
    
    # Display the transcript in Streamlit
    st.write("Transcript:")
    st.write(transcript)
