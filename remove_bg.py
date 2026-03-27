import urllib.request, os

os.makedirs("assets/products", exist_ok=True)

products = {
    "v-floc": "https://www.vonixx.com.br/wp-content/uploads/2023/07/v-floc-240ml_final.webp",
    "sintra-fast": "https://www.vonixx.com.br/wp-content/uploads/2023/07/sintra-fast.png",
    "revox": "https://www.vonixx.com.br/wp-content/uploads/2023/07/revox-sem-fundo-1.png",
    "blend": "https://www.vonixx.com.br/wp-content/uploads/2023/07/blend-paste-100ml.png",
    "intense": "https://www.vonixx.com.br/wp-content/uploads/2025/03/intense-240ml_final.webp",
    "v-lub": "https://www.vonixx.com.br/wp-content/uploads/2023/07/v-lub-2.png",
    "delet": "https://www.vonixx.com.br/wp-content/uploads/2023/07/delet-500ml-2.png",
    "izer": "https://www.vonixx.com.br/wp-content/uploads/2023/06/izer-novo-gatilho-copiar-scaled.webp",
    "v-plastic": "https://www.vonixx.com.br/wp-content/uploads/2023/07/v-plastic-20-ml-1-1-1.png",
    "native": "https://www.vonixx.com.br/wp-content/uploads/2023/06/native-100g-editada-nova-lata-copiar-1.png",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.vonixx.com.br/"
}

for name, url in products.items():
    ext = url.split(".")[-1]
    out_path = f"assets/products/{name}.{ext}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(out_path, "wb") as f:
            f.write(resp.read())
        print(f"OK: {name} -> {out_path}")
    except Exception as e:
        print(f"FAIL: {name} - {e}")

print("Done!")
