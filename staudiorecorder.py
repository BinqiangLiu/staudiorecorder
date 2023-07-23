#使用这个录音模块：https://github.com/theevann/streamlit-audiorecorder
import streamlit as st
from audiorecorder import audiorecorder
#import subprocess
import openai
import pyttsx3
#import sounddevice as sd
#import soundfile as sf
#import numpy as np
#from audio_recorder_streamlit import audio_recorder
#运行的时候有报错sh:1: ffmpeg not found
#import ffmpeg
#import av
#from pydub import AudioSegment

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are an intelligent professor."}]

st.title("Audio to Chat App")

# Audio input section语音输入部分
st.header("Step 1: Speak to the AI")
st.write("Click the Record Button below and speak to the AI.")

audio = audiorecorder("点击开始录音", "点击停止录音")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.tobytes())
    
    # To save audio to a file:
    audio_file = open("audio.mp3", "wb")
    audio_file.write(audio.tobytes())

# Transcribe the audio using OpenAI API将录音文件转文本
with open(audio_file, "rb") as file:
    transcript = openai.Audio.transcribe("whisper-1", file)
    text = transcript["text"]    
# Remove the temporary audio file
#    os.remove(audio_file)    

# Function to perform chat with OpenAI GPT-3
def chat_with_openai(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_text}],
    )
    return response["choices"][0]["message"]["content"]

# Function to convert text to speech using pyttsx3
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("voice", "english-us")
    engine.save_to_file(text, "response.mp3")
    engine.runAndWait()
    with open("response.mp3", "rb") as file:
        response_audio = file.read()
    os.remove("response.mp3")  # Remove the temporary audio file
    return response_audio

response = chat_with_openai(text)

# Display the chat history and play response audio
st.header("Chat History")
st.write("You: " + text)
st.write("AI: " + response)

# Audio output section
st.header("Step 2: Listen to the AI Response")
st.audio(text_to_speech(response), format="audio/mp3", start_time=0)

#if __name__ == "__main__":
#    main()