import streamlit as st
import pafy

# Title of the web app
st.title("YouTube Video Downloader")

# Get YouTube link from user input
yt_link = st.text_input("Enter the YouTube video link:")

# If user has provided a link
if yt_link:
    try:
        # Create a Pafy object
        video = pafy.new(yt_link)

        # Display video details
        st.write(f"Title: {video.title}")
        st.write(f"Author: {video.author}")
        st.write(f"Duration: {video.duration}")

        # Get best available resolution
        streams = video.streams
        resolutions = [stream.resolution for stream in streams if stream.resolution]
        selected_resolution = st.selectbox("Select resolution:", resolutions)
        stream = video.getbest(preftype="mp4", ftypestrict=True, resolution=selected_resolution)

        # Download video
        st.write("Downloading...")
        filename = stream.download()
        st.write("Download complete!")
    except (OSError, IOError):
        st.error("The video is either private or has been removed from YouTube. Please try another video.")
