import requests
from config import GNEWS_API_URL

def gnews_fetcher(target_params, source_name="None"):
    print(f"不要着急啊，正在抓取 {source_name} 新闻了呢👀...")
    try:
        response = requests.get(GNEWS_API_URL, params=target_params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            print(f"✅ [{source_name}] 成功抓取到 {len(articles)} 条。")
            
            batch_text = ""
            for i, article in enumerate(articles):
                title = article.get("title")
                description = article.get("description")
                batch_text += f"[{source_name}新闻-{i+1}] 标题: {title} | 摘要: {description}\n"
            
            return batch_text
        else:
            print(f"❌ [{source_name}] API 请求失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"ERROR发生网络错误: {e}")
        return None
