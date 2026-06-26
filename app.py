import streamlit as st


st.set_page_config(
    page_title="VoiceOps Sentinel",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ VoiceOps Sentinel")


st.write("Welcome to the Real-Time Call Intelligence System.")


st.header("Upload Customer Call")


audio_file = st.file_uploader(
    "Choose an audio file",
    type=["mp3", "wav", "flac"]
)


if audio_file is not None:
    st.success("Audio uploaded successfully!")
    st.audio(audio_file)