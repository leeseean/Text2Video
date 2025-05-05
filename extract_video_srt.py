import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr

# 1. 提取音频
def extract_audio(video_path, audio_path="audio.wav"):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

# 2. 分割音频
def split_audio(audio_path, chunk_dir="chunks"):
    os.makedirs(chunk_dir, exist_ok=True)
    audio = AudioSegment.from_wav(audio_path)
    chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-40, keep_silence=200)
    time_intervals = []
    current_start = 0
    
    for i, chunk in enumerate(chunks):
        chunk.export(f"{chunk_dir}/chunk{i}.wav", format="wav")
        duration = len(chunk)
        time_intervals.append( (current_start, current_start + duration) )
        current_start += duration
    
    return time_intervals

# 3. 语音识别
def audio_to_text(chunk_dir="chunks"):
    recognizer = sr.Recognizer()
    text_list = []
    
    for chunk_file in sorted(os.listdir(chunk_dir)):
        audio_path = os.path.join(chunk_dir, chunk_file)
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="zh-CN")
                text_list.append(text)
            except Exception as e:
                print(f"识别失败: {e}")
    
    return text_list

# 4. 生成SRT字幕
def save_as_srt(text_list, time_intervals, output_path="subtitle.srt"):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, (text, (start, end)) in enumerate(zip(text_list, time_intervals)):
            start_time = f"{start//3600000:02}:{(start//60000)%60:02}:{(start//1000)%60:02},{start%1000:03}"
            end_time = f"{end//3600000:02}:{(end//60000)%60:02}:{(end//1000)%60:02},{end%1000:03}"
            f.write(f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n")

# 主流程
video_path = "video.mp4"
audio_path = extract_audio(video_path)
time_intervals = split_audio(audio_path)
text_list = audio_to_text()
save_as_srt(text_list, time_intervals)