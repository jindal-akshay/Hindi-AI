import streamlit as st
from pydub import AudioSegment
from io import BytesIO
import base64
import mediainfo

st.set_page_config(page_title="Audio Player")

def main():
    st.title("Audio Player")

    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

    if audio_file is not None:
        try:
            audio_bytes = audio_file.read()
            audio = AudioSegment.from_file(BytesIO(audio_bytes), format=audio_file.type)
            st.audio(audio_bytes, format=audio_file.type)
            st.success("Audio file uploaded successfully!")
        except Exception as e:
            st.error("Error occurred while processing the audio file.")
            st.error(str(e))
            
        try:
            # Get metadata of the uploaded file
            metadata = mediainfo.analyze(audio_file)
            st.write("Metadata:")
            for key, value in metadata.to_data().items():
                st.write(f"{key}: {value}")
        except Exception as e:
            st.error("Error occurred while getting metadata of the audio file.")
            st.error(str(e))

if __name__ == "__main__":
    main()
