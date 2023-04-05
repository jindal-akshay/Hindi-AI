import openai
import streamlit as st
from io import BytesIO

# Set OpenAI API key
openai.api_key = st.secrets["api_secrets"]

# Define Streamlit app title and description
st.set_page_config(page_title="Audio Translator", page_icon=":sound:", layout="wide")
st.title("Audio Translator")
st.write("This app allows you to upload an MP3 file and translate it into English text using OpenAI API.")

# Display a file uploader in Streamlit
audio_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

# Check if a file was uploaded
if audio_file:
    # Read the uploaded file
    audio_bytes = audio_file.read()
    
    # Convert the bytes to a file-like object
    audio_fileobj = BytesIO(audio_bytes)
    
    # Set the name attribute of the file object
    audio_fileobj.name = audio_file.name
    
    # Use OpenAI API to translate audio
    response = openai.Audio.create(
        model="whisper-1",
        audio=audio_fileobj,
        transcript_language="en"
    )
    
    # Extract the transcript text from the response
    transcript = response['text']
    
    # Display the transcript in Streamlit
    st.write("Transcript:")
    st.write(transcript)
    
    # Create a downloadable link to save the transcript as .txt file
    transcript_file = transcript.encode('utf-8')
    st.download_button('Download Transcript', data=transcript_file, file_name='transcript.txt', mime='text/plain')
