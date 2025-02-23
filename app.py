import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = "AIzaSyBeizaCGUg8Nbd64cx7TrM7acAoXgElE2Y"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to extract video ID from YouTube URL
def get_video_id(url):
    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

# Function to fetch transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except Exception as e:
        return f"Error: {e}"

# Function to summarize text using Gemini API
def summarize_text(text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize this in bullet points:\n{text}")
    return response.text if response else "Error generating summary"

# Streamlit App UI
st.title("🎬 YouTube Video Summarizer")

# Input field for YouTube URL
video_url = st.text_input("Enter YouTube Video URL")

if st.button("Summarize"):
    video_id = get_video_id(video_url)

    if not video_id:
        st.error("Invalid YouTube URL")
    else:
        st.info("Extracting transcript...")
        transcript = get_transcript(video_id)

        if "Error" in transcript:
            st.error(transcript)
        else:
            st.success("Transcript Extracted! Summarizing...")
            summary = summarize_text(transcript)
            st.subheader("📌 Bullet Point Summary")
            st.write(summary)
            
#streamlit run "D:\Mishal\API PROJECT\app.py"
