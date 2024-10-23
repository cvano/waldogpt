import streamlit as st
import yt_dlp
import whisper
import openai
import os

# Load Whisper model for transcription
model = whisper.load_model("base")

# Set your OpenAI API key
openai.api_key = "your key"

def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def transcribe_audio(audio_path):
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language="en", fp16=False)
    result = model.decode(mel, options)
    return result.text

def answer_question(question, context):
    prompt = f"Here is the video transcription:\n\n{context}\n\nQuestion: {question}\n"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while trying to get an answer."

# Streamlit App Configuration
st.set_page_config(page_title="WaldoGPT: Advanced YouTube Transcription & Q&A", layout="wide")

# Custom CSS for red and white themed advanced design
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    body {
        background-color: #F5F5F5;
        font-family: 'Poppins', sans-serif;
        color: #333;
    }
    .title {
        font-size: 52px;
        color: #D32F2F;
        text-align: center;
        margin-bottom: 40px;
        letter-spacing: 2px;
        font-weight: 600;
    }
    .subheader {
        font-size: 26px;
        color: #D32F2F;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton button {
        background-color: #D32F2F;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border: none;
        border-radius: 30px;
        font-family: 'Poppins', sans-serif;
        transition: transform 0.3s ease;
    }
    .stButton button:hover {
        background-color: #F44336;
        transform: scale(1.05);
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: #FFFFFF;
        color: #D32F2F;
        border: 2px solid #D32F2F;
        padding: 12px;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
    }
    .transcription-area {
        background-color: #FFFFFF;
        color: #333;
        border: 2px solid #D32F2F;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-family: 'Poppins', sans-serif;
        margin-bottom: 30px;
    }
    .chatbot-container {
        border: 2px solid #D32F2F; 
        border-radius: 12px; 
        background-color: #FFFFFF; 
        box-shadow: 0px 4px 8px rgba(0,0,0,.1); 
        display: flex; 
        flex-direction: column; 
        height: 500px; 
        padding: 15px;
    }
    .qa-display {
        flex-grow: 1; 
        overflow-y: auto; 
        padding: 10px; 
        margin-bottom: 10px; 
        border-bottom: 1px solid #eee;
    }
    .input-area {
        padding: 10px; 
        border-top: 1px solid #D32F2F; 
        background-color: #fff;
    }
    .chat-message {
        margin-bottom: 10px;
        padding: 8px;
        border-radius: 8px;
    }
    .question {
        background-color: #f8f8f8;
    }
    .answer {
        background-color: #fff5f5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and header
st.markdown("<h1 class='title'>🔍 WaldoGPT</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subheader'>Find hidden insights in your favorite YouTube videos!</h2>", unsafe_allow_html=True)

# Initialize session state
if 'qa_list' not in st.session_state:
    st.session_state.qa_list = []
if 'transcription' not in st.session_state:
    st.session_state.transcription = ""
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Sidebar for YouTube URL
st.sidebar.header("YouTube Video")
youtube_url = st.sidebar.text_input("YouTube URL", placeholder="Enter YouTube URL here")

if st.sidebar.button("Add Link"):
    if youtube_url:
        with st.spinner('Processing video...'):
            download_audio(youtube_url)
            transcription = transcribe_audio('audio.mp3')
            st.session_state.transcription = transcription
            st.session_state.youtube_link = youtube_url
    else:
        st.warning("Please enter a valid YouTube URL.")

# Sidebar for Transcription
if st.session_state.transcription:
    st.sidebar.text_area("Transcription:", st.session_state.transcription, height=200)

# Main content layout
if st.session_state.transcription:
    cols = st.columns([2, 1])
    
    # Video and chatbot column
    with cols[0]:
        st.video(st.session_state.youtube_link)
    
    # Chatbot column
    # Chatbot column
    # Chatbot column
    with cols[1]:
        st.markdown("<h4>Q&A:</h4>", unsafe_allow_html=True)

        # Use form to handle question input and submit
        with st.form(key='question_form', clear_on_submit=True):
            user_question = st.text_input("Ask a question:", placeholder="Type your question here...")
            submit_button = st.form_submit_button("Ask")

            if submit_button and user_question:
                # Get the answer immediately when the form is submitted
                answer = answer_question(user_question, st.session_state.transcription)

                # Append question and answer to the list in session state
                st.session_state.qa_list.append({
                    'question': user_question,
                    'answer': answer
                })
                
                # Rerun the app to immediately display the new Q&A
                st.session_state.user_input = ""

        # Display questions and answers in a fixed-size box with a scrollbar
        with st.container():
            for qa in st.session_state.qa_list:
                st.markdown(f"<div class='chat-message question'>{qa['question']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='chat-message answer'>{qa['answer']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
