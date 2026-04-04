import urllib.request
import urllib.parse
import re

def search_img(q):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        m = re.search(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        if m:
            return m.group(1)
        # fallback to DDG
        url2 = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
        req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
        html2 = urllib.request.urlopen(req2).read().decode('utf-8')
        m2 = re.search(r'src="(\/\/external-content\.duckduckgo\.com\/iu\/\?u=[^"]+)"', html2)
        if m2:
            return "https:" + m2.group(1).replace('&amp;', '&')
    except Exception as e:
        print(e)
    return ""

print("Test Lincoln Lava Auto:", search_img("Lincoln Lava Auto estetica automotiva"))
print("Test Dub Boyz Shampoo:", search_img("Dub Boyz Shampoo Neutro"))
