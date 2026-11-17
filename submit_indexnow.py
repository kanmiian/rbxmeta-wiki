import json
import re
import urllib.request

KEY = "d9fff1aa6c384251b984519c49ed6831"
HOST = "rbxmeta.wiki"
KEY_URL = f"https://{HOST}/{KEY}.txt"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"

sm = urllib.request.urlopen(urllib.request.Request(SITEMAP_URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read().decode("utf-8")
urls = re.findall(r"<loc>(.*?)</loc>", sm)

payload = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": KEY_URL,
    "urlList": urls,
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.indexnow.org/IndexNow",
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"},
    method="POST",
)
resp = urllib.request.urlopen(req, timeout=20)
print(f"Submitted {len(urls)} URLs to IndexNow -> HTTP {resp.status}")
