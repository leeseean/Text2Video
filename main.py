import os
import requests
import tkinter as tk
from tkinter import messagebox
from pydub import AudioSegment
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut, CrossFadeIn, CrossFadeOut
import my_unit

my_unit.load_dotenv_file()

# Pexels API Key
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
font_path = "C:/Windows/Fonts/simkai.ttf"  # Windows 系统示例
default_image_path = "default.jpg"

# 设置目标分辨率，这里可以修改为你想要的分辨率
target_width = 1280
target_height = 720

def get_image_from_pexels(query, index):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('photos'):
            photo_url = data['photos'][0]['src']['landscape']
            print(photo_url)
            image_path = f"{index}.jpg"
            with open(image_path, 'wb') as f:
                image_response = requests.get(photo_url)
                f.write(image_response.content)
            return image_path
    return default_image_path


def generate_video(sections, image_paths, durations, video_output):
    clips = []
    for section, image_path, duration in zip(sections, image_paths, durations):
        fade_duration = min(duration/4, 0.5)  # 限制最大淡入时间为0.5秒
        clip = ImageClip(image_path, duration=duration)
        clip = clip.resized(new_size=(target_width, target_height))
        # clip = clip.with_effects([FadeIn(fade_duration), FadeOut(fade_duration)])
        # 添加字幕（可选）
        clip_to_bottom_height = 150  # 字幕距离底部的高度
        # print(wrap_text(section))
        text_clip = TextClip(font=font_path, text=wrap_text(section),
                             text_align="center", horizontal_align="center", vertical_align="center", font_size=30,
                             color='white', 
                             bg_color=(0, 0, 0, 128),  # 这里使用 RGBA 元组，0.5 透明度对应的整数是 128（255 * 0.5）
                             transparent=True,  # 开启透明度支持
                             stroke_color='darkviolet',  # 描边颜色
                             stroke_width=2,  # 描边宽度，单位为像素
                             margin=(10, 10),
                             duration=duration)
        # text_clip = text_clip.with_position(("center", target_height - clip_to_bottom_height))
        text_clip = text_clip.with_position(("center", "center"))
        text_clip = text_clip.with_effects([CrossFadeIn(fade_duration), CrossFadeOut(fade_duration)])
        video_clip = CompositeVideoClip([clip, text_clip])
        clips.append(video_clip)
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(video_output, fps=30, codec='libx264', audio_codec='aac')

def merge_audio_video(video_path, audio_path, final_output):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final = video.with_audio(audio)
    final.write_videofile(final_output, codec='libx264', audio_codec='aac')

def split_into_captions(text):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return paragraphs

# 防止字幕溢出屏幕，换行展示
def wrap_text(text, max_length=30):
    # 使用列表推导式将文本分割成不超过 max_length 的块
    wrapped_lines = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    return '\n'.join(wrapped_lines)

def generate_video_from_gui():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("错误", "请输入需要转换为视频的文案。")
        return

    sections = split_into_captions(text)  
        
    audio_file = "audio.wav"
    video_file = "temp_video.mp4"
    final_output = "result.mp4"

    image_paths = []
    durations = []
    _sections = []
    _successed_audios = []
    # 为每部分获取图片并生成语音时长
    for index, section in enumerate(sections, start=1):
        duration = my_unit.text_to_audio_edgetts(section, f"{index}_audio.wav")
        # 只计算转语音成功的文本
        if duration != None:
            _successed_audios.append(f"{index}_audio.wav")
            _sections.append(section)
            durations.append(duration)
            keywords = my_unit.translateLang(section)
            image_path = get_image_from_pexels(keywords, index)
            image_paths.append(image_path)
        else:
            # 生成语音失败的不计入
            os.remove(f"{index}_audio.wav")
    # 生成视频
    generate_video(_sections, image_paths, durations, video_file)

    # 合并所有语音文件
    combined_audio = AudioSegment.empty()
    for _audio_file in _successed_audios:
            audio = AudioSegment.from_file(_audio_file)
            combined_audio += audio
            os.remove(_audio_file)
        
        
    combined_audio.export(audio_file, format="wav")

    # 合并音视频
    merge_audio_video(video_file, audio_file, final_output)
    
    result = messagebox.showinfo("完成", "视频生成完成！")
    if result == "ok":
        root.destroy()
         # 清理临时文件（可选）
        for image_path in image_paths:
            if image_path != default_image_path:
                os.remove(image_path)
        os.remove(audio_file)
        os.remove(video_file)

# 创建 GUI 窗口
root = tk.Tk()
root.title("文案转视频")

# 创建文本输入框
text_input = tk.Text(root, height=30, width=100)
text_input.pack(pady=10)

# 创建生成按钮
generate_button = tk.Button(root, text="生成视频", command=generate_video_from_gui)
generate_button.pack(pady=10)

# 运行主循环
root.mainloop()
    