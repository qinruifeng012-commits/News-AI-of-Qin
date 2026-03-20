import os
import asyncio
import edge_tts

async def speech_code(text, output_file="新闻早报.mp3"):
    print(f"正在生成语音 (字数: {len(text)})...")
    voice = "zh-CN-XiaoxiaoNeural" 
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"✅ 语音已生成：{output_file}")
    os.system(f"start {output_file}")
