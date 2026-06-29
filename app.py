import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="VoiceOps Sentinel",
    page_icon="🎙️",
    layout="wide"
)

# Title
st.title("🎙️ VoiceOps Sentinel")

st.write(
    "Real-Time Call Intelligence System"
)

# Upload Section
st.header("📂 Upload Customer Call")
audio_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "flac"]
)

if audio_file is not None:

    st.success("Audio uploaded successfully!")

    st.subheader("📋 Audio Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("File Name", audio_file.name)

    with col2:
        st.metric("File Type", audio_file.type)

    with col3:
        st.metric(
            "File Size",
            f"{round(audio_file.size/1024,2)} KB"
        )

    st.subheader("🎵 Audio Player")
    st.audio(audio_file)

    st.subheader("⚙️ Processing Status")

    progress = st.progress(0)

    for i in range(100):
        progress.progress(i+1)

    st.success("✅ Ready for Whisper Transcription")