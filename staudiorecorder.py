#pip install -U openai-whisper
#pip install git+https://github.com/openai/whisper.git 
#https://github.com/openai/whisper

#使用这个录音模块：https://github.com/theevann/streamlit-audiorecorder
import streamlit as st
from audiorecorder import audiorecorder
import subprocess
import openai
import pyttsx3
#import whisper 
#import sounddevice as sd
import soundfile as sf
import numpy as np
#from audio_recorder_streamlit import audio_recorder
#运行的时候有报错sh:1: ffmpeg not found
import ffmpeg
import av
from pydub import AudioSegment
import Pyaudio

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
    
    # To save audio to a file:/可以视为是临时文件，就是用于语音转文本用
#Open file "audio.mp3" in binary write mode
    audio_file = open("audiorecorded.mp3", "wb")
    audio_file.write(audio.tobytes())
    audio_file.close()

# Use soundfile, pydub, or wave to handle audio file I/O

   # Transcribe the audio using OpenAI API将录音文件转文本

    stt_audio_file = open("audiorecorded.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", stt_audio_file)
#    text = transcript["text"]
# Remove the temporary audio file
    os.remove("audiorecorded.mp3")    

    # Print the transcript
    print("Transcript:",  transcript["text"])


#   ChatGPT API
#   append user's inut to conversation
    conversation.append({"role": "user", "content": transcript["text"]})
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation
    )    
    print(response)

#   system_message is the response from ChatGPT API
    system_message = response["choices"][0]["message"]["content"]

#   append ChatGPT response (assistant role) back to conversation
    conversation.append({"role": "assistant", "content": system_message})

# Display the chat history
    st.header("Chat History")
    st.write("You: " + transcript["text"])
    st.write("AI: " + system_message)

# Function to convert text to speech using pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
#    engine.setProperty("voice", "english-us")
    engine.save_to_file(text, "response.mp3")
    engine.runAndWait()
# response audio output section
    st.header("Step 2: Listen to the AI Response")
    st.audio("response.mp3", format="audio/mp3", start_time=0)
#    os.remove("response.mp3")  # Remove the temporary audio file

#response = chat_with_openai(transcript["text"])

#if __name__ == "__main__":
#    main()
