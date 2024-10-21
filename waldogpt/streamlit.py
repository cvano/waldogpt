import streamlit as st
import yt_dlp
import whisper
from transformers import pipeline
import os

# Load Whisper model for transcription
model = whisper.load_model("base")

# Load a QA pipeline (using Hugging Face's GPT-Neo)
qa_pipeline = pipeline("question-answering", model="EleutherAI/gpt-neo-125M")

def download_audio(youtube_url):
    # Specify ffmpeg location in WSL
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.mp3',
        'noplaylist': True,
        'ffmpeg_location': '/usr/bin/',  # Path to ffmpeg in WSL
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def transcribe_audio(audio_path):
    # Load audio and transcribe
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    
    # Transcribe using Whisper
    options = whisper.DecodingOptions(language="en", fp16=False)
    result = model.decode(mel, options)
    return result.text

def answer_question(question, context):
    return qa_pipeline(question=question, context=context)['answer']

# Streamlit App
st.set_page_config(page_title="YouTube Transcription & Q&A", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        color: #FF0000; /* Red color */
        text-align: center;
    }
    .subheader {
        font-size: 24px;
        color: #555;
        text-align: center;
    }
    .markdown-text {
        font-size: 18px;
        color: #333;
    }
    .info {
        font-size: 16px;
        color: #007BFF;
    }
    body {
        background-color: #FFFFFF; /* White background */
    }
    .stButton button {
        background-color: #FF0000; /* Red button */
        color: white; /* White text */
    }
    .stTextInput>div>input {
        border: 2px solid #FF0000; /* Red border for text input */
    }
    .stTextArea>div>textarea {
        border: 2px solid #FF0000; /* Red border for text area */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='title'>🎥 WaldoGPT</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subheader'>Get insights from your favorite YouTube videos!</h2>", unsafe_allow_html=True)

# Tabs for organization
tab1, tab2 = st.tabs(["Transcribe Video", "Ask Questions"])

with tab1:
    st.markdown("### Enter the YouTube URL below:")
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=example")

    if youtube_url:
        if st.button("Transcribe"):
            with st.spinner('Downloading and transcribing...'):
                download_audio(youtube_url)
                transcription = transcribe_audio('audio.mp3')
                st.success("✅ Transcription completed!")
                st.markdown("### Transcription:")
                st.text_area("Transcription Output:", transcription, height=300)

                # Save transcription in session state for chatbot
                st.session_state.transcription = transcription

with tab2:
    if 'transcription' in st.session_state:
        st.markdown("### Ask a question about the video:")
        question = st.text_input("Your Question", placeholder="What is this video about?")
        if question:
            answer = answer_question(question, st.session_state.transcription)
            st.markdown("### Answer:")
            st.write(answer)
    else:
        st.warning("Please transcribe a video first to ask questions.")

# Additional tips or instructions
st.markdown("---")
st.info("### Tips for Better Results:")
st.markdown("""  
1. Ensure the YouTube URL is valid and publicly accessible.  
2. Ask specific questions for more accurate answers.  
3. If the transcription is lengthy, consider summarizing it.  
""")
