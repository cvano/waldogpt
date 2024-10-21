import streamlit as st
import requests

st.title("Getting data from flask")

col1, col2 = st.columns(2)

with col1:
    video_url = 'https://www.youtube.com/watch?v=3Uj6Kct0_VI'
    st.video(video_url)

with col2:
    if st.button("Get Data"):
        response = requests.get("http://127.0.0.1:5000/api/data")
        if response.status_code == 200:
            data = response.json()
            st.write(f"Flask: {data['message']}")
        else:
            st.write("Error fetching data from Flask")

    st.html(
        """<div class="chat-container" <style> 
                <header class="chat-header">
                    <h1>WaldoGPT</h1>
                </header>
                <div class="chat-box" id="chat-box">
                </div>
                <div class="input-area">
                    <input type="text" id="user-input" placeholder="Type your message here..." />
                    <button id="send-button">Send</button>
                </div>
            </div>
            <script src="script.js"></script>"""
    )

    st.markdown(
        """
        <style>
        
        </style>
        """ #,
        #unsafe_allow_html=True
    )

