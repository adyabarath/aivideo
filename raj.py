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
from moviepy.config import change_settings

# Specify the path to the ImageMagick binary
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\convert.exe"})
def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

def create_subtitle_clips(subtitles, videosize, fontsize=30, font='Arial', color='white', debug=False):
    subtitle_clips = []
    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time
        video_width, video_height = videosize
        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color='black', size=(video_width * 0.5, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height * 9 / 10
        text_position = (subtitle_x_position, subtitle_y_position)
        subtitle_clips.append(text_clip.set_position(text_position))
    return subtitle_clips

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
    video_clip = VideoFileClip(outputvideo_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    outputvideoaudio_path = 'output_video_with_audio.mp4'
    video_clip.write_videofile(outputvideoaudio_path, codec='libx264', audio_codec='aac')
    st.video(outputvideoaudio_path)
    video = VideoFileClip(outputvideoaudio_path)
    subtitles = pysrt.open(subtitle)
    begin, end = outputvideoaudio_path.split(".mp4")
    output_video_file = begin + "_subtitling.mp4"
    subtitle_clips = create_subtitle_clips(subtitles, video.size)
    final_video = CompositeVideoClip([video] + subtitle_clips)
    final_video.write_videofile(output_video_file)
    st.video(output_video_file)

generate_video_with_audio('img1.png','output.wav')
