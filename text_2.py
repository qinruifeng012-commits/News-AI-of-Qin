# love zyx #
import os
import asyncio
import datetime
import requests
import edge_tts
from zai import ZhipuAiClient
from dotenv import load_dotenv

# =========== 环境配置 ========== #

load_dotenv()
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

client = ZhipuAiClient(api_key=ZHIPU_API_KEY)

# ========== 用户画像 ========== #

USER_PREFS = """
这位用户是一位关注国际局势的高中生。
他的兴趣点极其明确：
- 必看：宏观经济政策、国际形势、政策公布、各国头条。
- 关注: 金融科技、科技行业(Apple, Nvidia, Tesla)、AI领域技术突破。
- 不关注：本地琐事、娱乐八卦、体育新闻。
回答可以尽量有意思，将一些难懂的理论知识做一些有趣比喻。
"""

# ========== 配置参数 ========== #

GNEWS_API_URL = 'https://gnews.io/api/v4/top-headlines'

print(f"初始化配置完成...")

params_us = {
    'country': 'us',
    'category': 'general',
    'lang': 'en',
    'max': 10,
    'apikey': GNEWS_API_KEY
}
params_cn = {
    'country': 'cn',
    'category': 'general',
    'lang': 'zh',
    'max': 10,
    'apikey': GNEWS_API_KEY
}

# ========== 核心函数：通用抓取器 ========== #

def gnews_fetcher(target_params, source_name="None"):
    print(f"不要着急啊，正在抓取 {source_name} 新闻了呢👀...")
    try:
        response = requests.get(GNEWS_API_URL, params=target_params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✅ [{source_name}] 成功抓取到 {len(articles)} 条。")
            
            batch_text = ""
            for i, article in enumerate(articles):
                title = article.get('title')
                description = article.get('description')
                batch_text += f"[{source_name}新闻-{i+1}] 标题: {title} | 摘要: {description}\n"
            
            return batch_text
        else:
            print(f"❌ [{source_name}] API 请求失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"ERROR发生网络错误: {e}")
        return None

# ========== AI 批处理 ========== #

def Zhipu_ai(all_news_text, news_count):
    print(" AI 正在阅读中外所有新闻，进行筛选、翻译和编排...")

    system_prompt = f"""
    你是一位王牌国际新闻栏目的主编。你的用户喜好是：{USER_PREFS}

    你的任务是：
    1. 【筛选】从给定的新闻（包含美国和中国源）中，**只挑选出最重要、最符合用户口味的 {news_count} 条**。请确保兼顾国际视野和国内热点。只要是不符合用户规定的内容都筛选掉。
    2. 【翻译与重写】将英文新闻翻译成中文，中文新闻保持原意。
    3. 【编排】不要机械地读，要用“另外”、“与此同时”、“把目光转向国内”等连接词串联。可以加入适当的幽默比喻，记住一定要适当不能失去新闻的专业性。
    4. 【优化】播报要有趣，进行适当的新闻拓展于解读。也可以加入适当的幽默比喻，记住一定要适当不能失去新闻的专业性。
    重要 **输出要求**：
    直接输出一段完整的、最少1400字中文播报文稿。
    文稿开头必须是：“早上好，我是播报员小Q，这是为您定制的全球早报。”
    文稿结尾必须是：“以上就是今天的早报，愿您拥有美好的一天。”
    不要输出 JSON，不要输出 Markdown，只输出纯文本，可以直接播报。
    """

    user_prompt = f"以下是今日全球原始新闻源汇总：\n\n{all_news_text}"

    try:
        response = client.chat.completions.create(
            model="glm-4.5-flash",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ],
            max_tokens=4095,
            temperature=0.2
        )
        
        final_script = response.choices[0].message.content
        return final_script
        

    except Exception as e:
        print(f"WARRING: AI 处理错误：{e}")
        return None

# ========== speech 功能 ========== #

async def speech_code(text, output_file="新闻早报.mp3"):
    print(f"正在生成语音 (字数: {len(text)})...")
    voice = "zh-CN-XiaoxiaoNeural" 
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"✅ 语音已生成：{output_file}")
    os.system(f"start {output_file}")

# ========== txt文件保存 ========== #

def save_to_txt(text):
    # 获取当前日期，格式如：2025-12-17
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"{today}_早报文稿.txt"
    
    try:
        # 使用 utf-8 编码写入，确保中文不乱码
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n\n\n\n==={today}===\n")
            f.write(text)
        print(f"文稿已成功保存至: {filename}")
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")

# ========== 主程序 ========== #

if __name__ == "__main__":
    global_or_not = input("是否开启全球搜索呢👀(回答请用Y或着N哦~)")
    if "y" in global_or_not.lower():
        global_value = True
        news_count = 10
    else:
        global_value = False
        news_count = 8

    full_news_content = ""

    if global_value:
        full_news_content += gnews_fetcher(params_us, source_name="美国")
    else:
        full_news_content += gnews_fetcher(params_cn, source_name="中国")

    full_news_content += "\n" + gnews_fetcher(params_cn, source_name="中国") 

    if len(full_news_content) > 23:
        
        final_script = Zhipu_ai(full_news_content, news_count)
        
        if final_script:
            print("\n--- AI 生成的最终文稿 ---") 
            print(final_script)
            print("---------------------------")
            save_to_txt(final_script)
            asyncio.run(speech_code(final_script))
        else:
            print("完了，AI 罢工了，未能生成文稿 (哭泣.....)。")
    else:
        print("哎呀，中外新闻都没抓到，要不检查一下网络或 Key。")