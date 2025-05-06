
# 🎬 文字生成视频工具

- 一款为自媒体创作者设计的 **全自动视频生成工具**，输入文本即可输出高质量视频，大幅提升内容创作效率。
## 🎥 视频演示

[![YouTube 演示视频封面](https://img.youtube.com/vi/6ZHwECOm7fE/maxresdefault.jpg)](https://youtu.be/6ZHwECOm7fE?t=23 "点击观看演示视频")


---

## ✨ 功能亮点

| 功能模块       | 说明                                                                 |
|----------------|----------------------------------------------------------------------|
| 📝 **智能分段** | 自动将长文本拆分为视频分镜段落                                      |
| 🖼️ **精准配图** | 通过Pexels API获取无版权图片，或从本地库匹配                        |
| 🔊 **多音色配音** | 支持OpenAI TTS（拟真人声）和Edge TTS（免费合成音）                  |
| 🎥 **一键合成**  | 自动合成图片+音频+字幕，输出MP4/1080P视频                           |
| ⚡ **高效渲染**  | 基于MoviePy+FFmpeg的硬件加速渲染                                    |

---

## 🛠 技术栈

<div align="center">

| 技术组件               | 用途                             | 配置要求                          |
|------------------------|----------------------------------|----------------------------------|
| ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) | 核心逻辑        | ≥3.8                             |
| ![FFmpeg](https://img.shields.io/badge/FFmpeg-5.1%2B-red) | 视频编码        | 需[手动安装](https://ffmpeg.org) |
| ![MoviePy](https://img.shields.io/badge/MoviePy-1.0%2B-orange) | 视频剪辑      | `pip install moviepy`           |
| ![Edge TTS](https://img.shields.io/badge/Edge_TTS-浅蓝) | 免费语音合成    | `pip install edge-tts`          |
| ![百度开放平台](https://img.shields.io/badge/百度API-深红) | 语音/图片API   | 需[申请密钥](https://ai.baidu.com) |
| ![Pexels](https://img.shields.io/badge/Pexels_API-绿色) | 无版权图片      | 免费[申请密钥](https://www.pexels.com/api/) |
</div>

---

## 🚀 快速开始

### 1. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 验证FFmpeg安装
ffmpeg -version
```

### 2. 配置密钥
复制 `.env.example` 并重命名为 `.env.dev`、`.env.dev`，填写你的API密钥：
```env
PEXELS_API_KEY = "xxx"
baidu_appid = 'xxx'  # 百度开发者平台申请
baidu_secret_key = 'xxx'
```

### 3. 运行程序
```bash
python main.py
```
---

## 📁 项目结构
```
.
├── assets/                 # 存放演示视频/静态资源
├── src/
│   ├── text_processor.py   # 文本分段处理
│   ├── image_fetcher.py    # 图片获取（API+本地）
│   ├── audio_generator.py  # 语音合成
│   └── video_renderer.py   # 视频合成（MoviePy+FFmpeg）
├── .env.example            # 环境变量模板
└── requirements.txt        # 依赖列表
```

---

## 📜 开源协议
本项目采用 [MIT License](LICENSE)，可自由用于个人和商业用途。使用Pexels API、百度 API需遵守其[服务条款](https://www.pexels.com/api/terms/)。
