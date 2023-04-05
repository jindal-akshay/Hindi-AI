import openai
import streamlit as st
from io import BytesIO
from pydub import AudioSegment
import youtube_dl

# Set OpenAI API key
openai.api_key = st.secrets["api_secrets"]

# Define app header
st.set_page_config(page_title="Hindi Audio to English Text", page_icon=":microphone:", layout="wide")

st.title("Hindi Audio to English Text")
st.markdown("""
    This app uses OpenAI to translate Hindi audio to English text. 
    Simply upload an mp3 file or provide a YouTube link and the app will generate a transcript in English.
""")

# Display file uploader and YouTube link input
audio_file = st.file_uploader("Upload an mp3 file", type=["mp3"])
yt_link = st.text_input("Enter a YouTube link")

# Translate audio to text and display result
if audio_file is not None:
    # Convert file contents to bytes
    audio_bytes = BytesIO(audio_file.read()).getvalue()

    # Load audio file using PyDub
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")

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

elif yt_link:
    # Download audio from YouTube link using youtube_dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(yt_link, download=True)
        if 'entries' in info_dict:
            # If playlist, use first video
            info_dict = info_dict['entries'][0]
        file_path = None
        if info_dict:
            # Check if the file is already downloaded
            file_path = ydl.prepare_filename(info_dict)
    if file_path is None:
        st.error("Could not download audio from the provided YouTube link.")
    else:
        # Load audio file using PyDub
        audio = AudioSegment.from_file(file_path, format="mp3")

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
            frequency_penalty=0
