import urllib.request
import urllib.parse
import re

def scrape_vonixx(query):
    url = f"https://vonixx.com.br/?s={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        m = re.search(r'<img[^>]+src="([^"]+wp-content/uploads/[^"]+)"', html)
        if m: return m.group(1)
    except Exception as e: print("Vonixx err", e)
    return ""

def scrape_dubboyz(query):
    url = f"https://www.dubboyz.com.br/buscar?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        m = re.search(r'<img[^>]+src="([^"]+images/produtos/[^"]+)"', html)
        if m: return m.group(1)
    except Exception as e: print("Dub err", e)
    return ""

print("Vonixx V-Floc Wash & Wax:", scrape_vonixx("V-Floc Wash"))
print("Dub Boyz Splash:", scrape_dubboyz("Shampoo"))
