#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing, Yandex, Seznam...) about every URL in sitemap.xml.

Run after a deploy has gone live:  python3 _build/indexnow.py
"""
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'knoxvilleroofingquotes.com'
KEY = 'a2eeeb20ea5663746f8fbba66eb45ac5'

with open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8') as f:
    urls = re.findall(r'<loc>([^<]+)</loc>', f.read())

body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'})
with urllib.request.urlopen(req, timeout=30) as resp:
    print(f'IndexNow: submitted {len(urls)} URLs, HTTP {resp.status}')
