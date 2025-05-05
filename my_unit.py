import os
import requests
import random
from hashlib import md5
import asyncio
from edge_tts import Communicate
from gtts import gTTS
from pydub import AudioSegment
from dotenv import load_dotenv

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def load_dotenv_file():
    # 默认加载开发环境配置
    env_file = ".env.dev"  

    # 如果检测到生产环境变量，则切换为生产配置
    if os.getenv("ENV") == "prod":
        env_file = ".env.prod"
        
    # 加载对应的.env文件
    load_dotenv(env_file)

load_dotenv_file()

appid = os.getenv("baidu_appid")  # 从百度开发者平台获取
secret_key = os.getenv("baidu_secret_key")

def translateLang(text, from_code='zh', to_code='en'):
    # Build request
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + text + str(salt) + secret_key)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': text, 'from': from_code, 'to': to_code, 'salt': salt, 'sign': sign}
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    if r.json()["trans_result"] and len(r.json()["trans_result"]) > 0:
        result = r.json()["trans_result"][0]["dst"]
    else:
        result = "night"
    return result

def text_to_audio_edgetts(text, audio_output):
    # 定义与原函数类似的参数映射（可根据需求调整）
    params = {
        "voice": "zh-CN-XiaoxiaoNeural",  # 默认音色（原spk_emb类似功能）
        "rate": "+0%",  # 语速（原[speed_2]可映射为"+20%"）
        "volume": "medium"  # 音量（原参数可扩展）
    }
    
    # 解析原函数中的参数标记（如[speed_2]转换为SSML）
    # 示例：将[speed_2]替换为语速+20%（需根据原逻辑调整正则）
    # text = re.sub(r'\[speed_(\d+)\]', lambda m: f'<prosody rate="+{int(m.group(1))*10}%">', text)
    # text += '</prosody>'  # 闭合SSML标签（需根据实际标记数量调整）

    async def _tts_task():
        try:
            # 初始化edge-tts通信对象（传入处理后的文本和参数）
            tts = Communicate(
                text=text,
                voice=params["voice"],
                rate=params["rate"],
            )
            # 生成并保存音频
            await tts.save(audio_output)
            
            # 读取音频并计算时长（与原函数逻辑一致）
            audio = AudioSegment.from_file(audio_output)
            return len(audio) / 1000  # 返回秒数
        except Exception as e:
            print(f"文本转语音失败: {str(e)}")
            print(text)
            return None
    
    # 异步任务同步执行（保持原函数调用方式）
    return asyncio.run(_tts_task())

def text_to_audio_gtts(text, audio_output):
    try:
        tts = gTTS(text=text, lang='zh-CN', slow=False)
        # 保存为 MP3 文件
        tts.save(audio_output)
        # 读取音频并计算时长（与原函数逻辑一致）
        audio = AudioSegment.from_file(audio_output)
        return len(audio) / 1000  # 返回秒数
    except Exception as e:
            print(f"文本转语音失败: {str(e)}")
            return None