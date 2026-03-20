from zai import ZhipuAiClient
from config import ZHIPU_API_KEY

client = ZhipuAiClient(api_key=ZHIPU_API_KEY)

USER_PREFS = """
这位用户是一位关注国际局势的高中生。
他的兴趣点极其明确：
- 必看：宏观经济政策、国际形势、政策公布、各国头条。
- 关注: 金融科技、科技行业(Apple, Nvidia, Tesla)、AI领域技术突破。
- 不关注：本地琐事、娱乐八卦、体育新闻。
回答可以尽量有意思，将一些难懂的理论知识做一些有趣比喻。
"""

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
            model="glm-4.7-flash",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ],
            max_tokens=4095,
            temperature=0.1
        )
        
        final_script = response.choices[0].message.content
        return final_script
        

    except Exception as e:
        print(f"WARRING: AI 处理错误：{e}")
        return None
