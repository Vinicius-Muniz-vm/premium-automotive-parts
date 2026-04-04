import urllib.request
import urllib.parse
import re

def search_yahoo(query):
    url = f"https://images.search.yahoo.com/search/images?p={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        m = re.search(r'<img[^>]+src=\'([^\']+)\'[^>]+class=\'process\'', html)
        if m: return m.group(1)
        # generic img
        m = re.search(r'src=\'(https://tse[^\']+)\'', html)
        if m: return m.group(1)
    except Exception as e: print(e)
    return ""

print("Vonixx V-Floc:", search_yahoo("Vonixx V-Floc 500ml"))
print("Dub Boyz Splash:", search_yahoo("Dub Boyz Splash Shampoo Neutro"))
