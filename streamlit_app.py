import openai
import streamlit as st
from io import BytesIO
from pydub import AudioSegment
from youtube_dl import YoutubeDL
import validators

# Set OpenAI API key
openai.api_key = st.secrets["api_secrets"]

# Define app header
st.set_page_config(page_title="Hindi Audio to English Text", page_icon=":microphone:", layout="wide")

st.title("Hindi Audio to English Text")
st.markdown("""
    This app uses OpenAI to translate Hindi audio to English text. 
    Simply paste a YouTube link to a video with Hindi audio and the app will generate a transcript in English.
""")

# Display text input for YouTube link
yt_link = st.text_input("Enter a YouTube link:")

# Translate audio to text and display result
if yt_link and validators.url(yt_link):
    try:
        # Extract info about the YouTube video using youtube_dl
        ydl = YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
        info_dict = ydl.extract_info(yt_link, download=False)
        
        # Get the URL for the video with the highest resolution
        formats = info_dict.get('formats',None)
        formats.sort(key=lambda x:x.get('filesize',0),reverse=True)
        video_url = formats[0]['url']
        
        # Load audio data using PyDub
        audio = AudioSegment.from_file(video_url, format="webm")

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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please enter a valid YouTube link.")
