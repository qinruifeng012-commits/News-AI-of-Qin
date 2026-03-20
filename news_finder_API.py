# -*- coding: utf-8 -*-
"""
News Finder API - Multi-platform News/Video Finder

Supported Platforms:
- Bilibili (Hot Videos)
- Thepaper (News)
- Cailianpress (Finance News)
- Ifeng (News)
- Wallstreetcn (Finance)

Usage:
    api = NewsFinderAPI()
    news = api.get_all_news(rank=10)

NOTE: Replace RSS URLs below with valid feeds if the defaults don't work.
Check available feeds at: https://rsshub.app or use official RSS feeds.
"""

import feedparser
from typing import List, Dict
from datetime import datetime


class NewsFinderAPI:
    """News finder using RSS feeds"""

    def __init__(self):
        # =================== RSS CONFIGURATION ===================
        # Replace these URLs with working RSS feeds if needed
        # You can find more feeds at: https://rsshub.app
        self.feeds = {
            # Bilibili Hot Videos
            'bilibili': 'https://rsshub.app/bilibili/video/popular',

            # Official RSS feeds (recommended if available)
            'thepaper': 'https://www.thepaper.cn/rss/news.xml',
            'cailianpress': 'https://www.cls.cn/rss/telegraph.xml',
            'ifeng': 'https://news.ifeng.com/rss/index.xml',

            # Alternative feeds (via RSSHub)
            'wallstreet': 'https://rsshub.app/wallstreetcn',
        }
        # =======================================================

        # Request settings
        self.timeout = 10

    def _parse_rss(self, url: str, rank: int = 10) -> List[Dict]:
        """
        Parse RSS feed and return items

        Args:
            url: RSS feed URL
            rank: Number of items to return

        Returns:
            List of dictionaries with title, summary, url, time, author
        """
        try:
            # Parse RSS feed
            feed = feedparser.parse(url)

            if not feed.entries:
                return []

            items = []
            for entry in feed.entries[:rank]:
                # Extract basic info
                title = entry.get('title', '')
                link = entry.get('link', '')
                published = entry.get('published', '')
                author = entry.get('author', '')

                # Extract summary/description
                summary = ''
                if hasattr(entry, 'summary'):
                    summary = entry.summary[:150]
                elif hasattr(entry, 'description'):
                    summary = entry.description[:150]

                items.append({
                    'title': title,
                    'summary': summary,
                    'url': link,
                    'time': published,
                    'author': author
                })

            return items

        except Exception as e:
            print(f"Error parsing RSS ({url}): {e}")
            return []

    # ==================== Platform Methods ====================

    def get_bilibili(self, rank: int = 10) -> List[Dict]:
        """Get Bilibili hot videos"""
        return self._parse_rss(self.feeds['bilibili'], rank)

    def get_thepaper(self, rank: int = 10) -> List[Dict]:
        """Get Thepaper news"""
        return self._parse_rss(self.feeds['thepaper'], rank)

    def get_cailianpress(self, rank: int = 10) -> List[Dict]:
        """Get Cailianpress finance news"""
        return self._parse_rss(self.feeds['cailianpress'], rank)

    def get_ifeng(self, rank: int = 10) -> List[Dict]:
        """Get Ifeng news"""
        return self._parse_rss(self.feeds['ifeng'], rank)

    def get_wallstreet(self, rank: int = 10) -> List[Dict]:
        """Get Wallstreetcn finance news"""
        return self._parse_rss(self.feeds['wallstreet'], rank)

    # ==================== Utility Methods ====================

    def get_custom_rss(self, url: str, rank: int = 10) -> List[Dict]:
        """
        Get news from custom RSS feed

        Example:
            api.get_custom_rss('https://www.zhihu.com/rss', 5)
        """
        return self._parse_rss(url, rank)

    def get_all_news(self, rank: int = 10) -> Dict:
        """Get news from all configured platforms"""
        return {
            'bilibili': self.get_bilibili(rank),
            'thepaper': self.get_thepaper(rank),
            'cailianpress': self.get_cailianpress(rank),
            'ifeng': self.get_ifeng(rank),
            'wallstreet': self.get_wallstreet(rank),
            'query_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def add_feed(self, name: str, url: str):
        """Add custom RSS feed"""
        self.feeds[name] = url

    def remove_feed(self, name: str):
        """Remove RSS feed"""
        if name in self.feeds:
            del self.feeds[name]

    def list_feeds(self) -> Dict:
        """List all configured RSS feeds"""
        return self.feeds


# ==================== Usage Example ====================
if __name__ == "__main__":
    # Create API instance
    api = NewsFinderAPI()

    # Set rank (number of items per platform)
    RANK = 10

    print("=" * 50)
    print("News Finder API - Multi-platform News")
    print(f"Query Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # Show configured feeds
    print(f"\nConfigured RSS Feeds ({len(api.feeds)}):")
    for name, url in api.feeds.items():
        print(f"  - {name}: {url}")

    # Fetch and display news from each platform
    platforms = [
        ("Bilibili", api.get_bilibili),
        ("Thepaper", api.get_thepaper),
        ("Cailianpress", api.get_cailianpress),
        ("Ifeng", api.get_ifeng),
        ("Wallstreet", api.get_wallstreet),
    ]

    for name, method in platforms:
        print(f"\n{'=' * 50}")
        print(f"[{name} - Top {RANK}]")
        print('=' * 50)

        news = method(RANK)

        if news:
            for i, item in enumerate(news, 1):
                title = item['title'][:60] + '...' if len(item['title']) > 60 else item['title']
                print(f"{i}. {title}")
                if item['url']:
                    print(f"   URL: {item['url']}")
        else:
            print("  No items found (RSS feed may be unavailable)")

    # Summary
    all_news = api.get_all_news(RANK)
    total = sum(len(v) for v in all_news.values() if isinstance(v, list))
    print(f"\n{'=' * 50}")
    print(f"Summary: {total} items fetched from {len(platforms)} platforms")
    print(f"Query Time: {all_news['query_time']}")
    print('=' * 50)

    # Example: Add custom RSS feed
    # api.add_feed('custom', 'https://example.com/feed.xml')
    # print(f"\nCustom feed added: {api.get_custom_rss('https://example.com/feed.xml', 5)}")