import streamlit as st
from pydub import AudioSegment
from io import BytesIO
import base64
import mediainfo
import whisper

st.set_page_config(page_title="Audio Player")

st.title("Whisper App")

#upload audio file with streamlit
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

model = whisper.load_model("base")
st.text("whisper model loaded")


if st.sidebar.button("transcribe audio"):
	if audio_file is not None:
		st.sidebar.success("Transcribing audio")
		transcription = model.transcribe(audio_file.name)
		st.sidebar.success("Transcription complete")
		st.markdown(transcription["text"])
	else:
		st.sidebar.error("Please upload file")

st.sidebar.header("play audio file")
st.sidebar.audio(audio_file)