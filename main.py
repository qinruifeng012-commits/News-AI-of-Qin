#love zyx#
import asyncio
from Gnews_fetcher import gnews_fetcher
from ai_processor import Zhipu_ai
from speech_synthesizer import speech_code
from utils import save_to_txt
from config import params_us, params_cn

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
        us_news = gnews_fetcher(params_us, source_name="美国")
        if us_news:
            full_news_content += us_news
    
    cn_news = gnews_fetcher(params_cn, source_name="中国")
    if cn_news:
        if full_news_content:
            full_news_content += "\n" + cn_news
        else:
            full_news_content += cn_news

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
