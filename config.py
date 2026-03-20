import os
from dotenv import load_dotenv

load_dotenv()

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
GNEWS_API_URL = 'https://gnews.io/api/v4/top-headlines'

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
