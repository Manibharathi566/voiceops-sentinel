import streamlit as st
import time
import whisper
import os
from textblob import TextBlob
import matplotlib.pyplot as plt





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

def word_frequency(text):
    words = text.lower().split()

    stop_words = {
        "the", "is", "a", "an", "and", "to", "of",
        "in", "for", "on", "with", "this", "that",
        "it", "are", "was"
    }

    frequency = {}

    for word in words:
        word = word.strip(".,!?()[]{}\"'")

        if word and word not in stop_words:
            frequency[word] = frequency.get(word, 0) + 1

    return dict(
        sorted(
            frequency.items(),
            key=lambda item: item[1],
            reverse=True
        )[:10]
    )




os.environ["PATH"] += os.pathsep + r"D:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin"

st.set_page_config(
    page_title="VoiceOps Sentinel",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ VoiceOps Sentinel")
st.caption("AI-Powered Speech Analytics Platform")

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "sentiment" not in st.session_state:
    st.session_state.sentiment = ""

if "word_stats" not in st.session_state:
    st.session_state.word_stats = {}




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

        file_extension = audio_file.name.split(".")[-1]
        temp_audio = f"temp_audio.{file_extension}"

        with open(temp_audio, "wb") as f:
            f.write(audio_file.getbuffer())

        whisper_model = whisper.load_model("tiny")
        result = whisper_model.transcribe(temp_audio)

    transcript = result["text"]

    summary = generate_summary(transcript)

    sentiment = analyze_sentiment(transcript)

    word_stats = word_frequency(transcript)

    # Save everything in Session State
    st.session_state.transcript = transcript
    st.session_state.summary = summary
    st.session_state.sentiment = sentiment
    st.session_state.word_stats = word_stats

    with open("transcript.txt", "w") as f:
        f.write(transcript)


if st.session_state.transcript != "":

    st.success("✅ Audio processed successfully!")

    st.subheader("Transcript")

    st.text_area(
        "Generated Transcript",
        st.session_state.transcript,
        height=200
    )

    st.download_button(
        "Download Transcript",
        st.session_state.transcript,
        file_name="transcript.txt",
        mime="text/plain"
    )

    st.divider()

    st.subheader("🔍 Search in Transcript")

    search_word = st.text_input("Enter a word to search")

    if search_word:

        if search_word.lower() in st.session_state.transcript.lower():
            st.success(f"'{search_word}' found in transcript.")
        else:
            st.error(f"'{search_word}' not found.")

    st.divider()

    st.subheader("AI Summary")
    st.write(st.session_state.summary)

    st.divider()

    st.subheader("Sentiment Analysis")
    st.write(st.session_state.sentiment)

    st.divider()

    st.subheader("📊 Top 10 Frequently Used Words")

    words = list(st.session_state.word_stats.keys())
    counts = list(st.session_state.word_stats.values())

    fig, ax = plt.subplots()

    ax.bar(words, counts)

    ax.set_xlabel("Words")
    ax.set_ylabel("Frequency")
    ax.set_title("Word Frequency")

    plt.xticks(rotation=45)

    st.pyplot(fig)

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
        progress.progress(i + 1)

    st.success("✅ Ready for Whisper Transcription")