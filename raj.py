import streamlit as st
import google.generativeai as genai
from pathlib import Path
import assemblyai as aai
from PIL import Image
from moviepy.editor import *
from moviepy.config import change_settings
import pysrt
from gtts import gTTS
import os
from mutagen import File
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import numpy as np
import re

def generate_video_with_audio(image_path, audio_path):
    aai.settings.api_key = "e1313b421dec4789bddac187ad824975"
    transcript = aai.Transcriber().transcribe(audio_path)
    subtitles = transcript.export_subtitles_srt()
    subtitle = "subtitles.srt"
    with open(subtitle, "w") as f:
        f.write(subtitles)
    audio = File(audio_path)
    duration_seconds=audio.info.length
    print("Duration of the audio:", duration_seconds, "seconds")
    image = Image.open(image_path)
    image_np = np.array(image)
    image_clip = ImageClip(image_np)
    video = image_clip.set_duration(duration_seconds).set_fps(24)
    outputvideo_path = 'output_video.mp4'
    video.write_videofile(outputvideo_path, codec='libx264', fps=24)
    st.video(outputvideo_path)

generate_video_with_audio('img1.png','output.wav')