import streamlit as st
import time
import whisper
import os
from textblob import TextBlob





def generate_summary(text):
    sentences = text.split(".")
    summary = ". ".join(sentences[:3])
    return summary



def analyze_sentiment(text):
    analysis = TextBlob(text)

    if analysis.sentiment.polarity > 0:
        return "😊 Positive"

    elif analysis.sentiment.polarity < 0:
        return "😔 Negative"

    else:
        return "😐 Neutral"





os.environ["PATH"] += os.pathsep + r"D:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin"

st.set_page_config(
    page_title="VoiceOps Sentinel",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ VoiceOps Sentinel")
st.caption("AI-Powered Speech Analytics Platform")




st.write(
    "Real-Time Call Intelligence System"
)


st.header("📂 Upload Customer Call")
audio_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "flac"]
)

if audio_file is not None:

    st.subheader("🤖 AI Speech Recognition")

    

transcribe_btn = st.button("Generate Transcript")

if transcribe_btn:

    with st.spinner("Processing audio using AI..."):

        whisper_model = whisper.load_model("tiny")
        
        temp_audio = "temp_audio.mp3"

        result = whisper_model.transcribe(temp_audio)

    st.info("Whisper AI model loaded successfully!")


        

    with open(temp_audio, "wb") as f:
        f.write(audio_file.getbuffer())
    
    st.info("Transcribing audio...")

    result = whisper_model.transcribe(temp_audio)

    summary = generate_summary(result["text"])

    sentiment = analyze_sentiment(result["text"])

    with open("transcript.txt", "w") as f:
        f.write(result["text"])



    st.subheader("Transcript")

    st.text_area("Generated Transcript", result["text"], height=200)

    st.download_button("Download Transcript", result["text"], file_name="transcript.txt", mime="text/plain")

    
    st.subheader("AI Summary")
    st.write(summary)    
    st.divider()

    st.subheader("Sentiment Analysis")
    st.write(sentiment)
    st.divider()

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