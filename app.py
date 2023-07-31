#pip install -U openai-whisper
#pip install git+https://github.com/openai/whisper.git 
#https://github.com/openai/whisper

#使用这个录音模块：https://github.com/theevann/streamlit-audiorecorder
import streamlit as st
from audiorecorder import audiorecorder
import subprocess
import openai
#import pyttsx3
#import whisper 
import soundfile as sf
#import sounddevice as sd
#from scipy.io.wavfile import write
import numpy as np
#from audio_recorder_streamlit import audio_recorder
#运行的时候有报错sh:1: ffmpeg not found
import ffmpeg
#import av
#from pydub import AudioSegment
#import pyaudio
import wave
import sys
from langdetect import detect
from gtts import gTTS
#from pydub import AudioSegment

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are a helpful assistant."}]

system_message = ""
transcript = ""
ai_output_audio = ""
audio_input = ""

#display_output_text = st.checkbox("语音播放翻译结果")

#click_clear = st.button('清空输入框', key=3)

st.title("by Theevan - AI Audio Chat App")

# Audio input section语音输入部分
st.header("第一步：向AI语音提问")
st.write("点击下方按钮开始和停止语音输入")

audio = audiorecorder("点击开始录音", "点击停止录音")

if len(audio) > 0:
    # To play audio in frontend:
    st.write("你输入的语音")
    st.audio(audio.tobytes())    
    # To save audio to a file:/可以视为是临时文件，就是用于语音转文本用
#Open file "audiorecorded.mp3" in binary write mode
    audio_file = open("audiorecorded.webm", "wb")    
#    audio_file = open("audiorecorded.mp3", "wb")
    audio_file.write(audio.tobytes())
    audio_file.close()

    
   # Transcribe the audio using OpenAI API将录音文件转文本
#    stt_audio_file = open("audiorecorded.mp3", "rb")
    stt_audio_file = open("audiorecorded.webm", "rb")
#    model = whisper.load_model("base")
#    transcript = model.transcribe("audiorecorded.mp3")  
    transcript = openai.Audio.transcribe("whisper-1", stt_audio_file)
    text = transcript["text"]
# Remove the temporary audio file
#    os.remove("audiorecorded.mp3")    
    os.remove("audiorecorded.webm")   
#    os.remove(stt_audio_file)    

    # Print the transcript
    print("Transcript of your questions:",  transcript["text"])

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
    st.header("你和AI的问答文字记录")
    st.write("你的提问（语音转文字）: " + transcript["text"])
    st.write("AI回答（文字）: " + system_message)
    st.header("第二步：语音播放AI的回答")

language = detect(system_message)

st.write("检测到输出语言:", language)
print(language)

def text_to_speech(text):
    try:
        tts = gTTS(text, lang=language, slow=False)
        tts.save("translationresult.mp3")
        st.write("Success TTS成功将AI回答转换为语音")
        return "Success TTS成功将AI回答转换为语音"    
    except Exception as e:
        # Handle the error, e.g., print an error message or return a default text
        print(f"Translation error: {e}")
        st.write("TTS RESULT ERROR将AI回答转语音失败！")
        return "TTS RESULT ERROR将AI回答转语音失败！"
        st.stop()

if system_message is None:
    st.write("请先向AI提问！")    
    st.stop()
else: 
    st.write("你的提问（AI问答模型中的记录transcript）")
    st.write(transcript)
    st.write("AI回答")            
    ai_output_audio = text_to_speech(system_message)
    audio_file = open("translationresult.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio("translationresult.mp3")
    st.write(response)    
    st.write(system_message)    
