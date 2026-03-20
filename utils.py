import datetime

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
