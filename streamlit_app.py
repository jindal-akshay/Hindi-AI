import streamlit as st
import pafy
import yt_dlp

st.title("YouTube Video Downloader")

yt_link = st.text_input("Enter the YouTube video link:")
if yt_link:
    with st.spinner("Loading video info..."):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(yt_link, download=False)
            video = pafy.new(info_dict['webpage_url'])
        except yt_dlp.utils.DownloadError:
            st.error("The video is either private or has been removed from YouTube. Please try another video.")
            st.stop()

        st.write("Title:", video.title)
        st.write("Duration:", video.duration)
        st.write("Rating:", video.rating)
        st.write("Author:", video.author)
        st.write("Views:", video.viewcount)

    download_option = st.selectbox("Select download option:", video.streams)
    if st.button("Download"):
        with st.spinner("Downloading..."):
            download_option.download()
        st.success("Video downloaded successfully!")
