import requests
from bs4 import BeautifulSoup
import urllib.parse
from PIL import Image
import io
import base64
import os

products = [
    # Lincoln
    {'id': 'lava-auto', 'q': 'Lava Auto Lincoln 500ml', 'img': 'lava-auto-lincoln.png'},
    {'id': 'lava-auto-cera', 'q': 'Lava Auto com Cera Lincoln', 'img': 'lava-auto-cera-lincoln.png'},
    {'id': 'apc-lincoln', 'q': 'APC Lincoln 500ml', 'img': 'apc-lincoln.png'},
    {'id': 'wheel-cleaner-lincoln', 'q': 'Wheel Cleaner Lincoln 500ml', 'img': 'wheel-cleaner-lincoln.png'},
    {'id': 'iron-remover-lincoln', 'q': 'Iron Remover descontaminante Lincoln 500ml', 'img': 'iron-remover-lincoln.png'},
    {'id': 'cera-liquida-lincoln', 'q': 'Cera Liquida Lincoln', 'img': 'cera-liquida-lincoln.png'},
    {'id': 'selante-lincoln', 'q': 'Selante Paint Sealer Lincoln', 'img': 'selante-lincoln.png'},
    {'id': 'vitrificador-lincoln', 'q': 'Vitrificador Lincoln', 'img': 'vitrificador-lincoln.png'},
    {'id': 'restaurador-lincoln', 'q': 'Restaurador Plastico Lincoln', 'img': 'restaurador-lincoln.png'},
    {'id': 'leather-care-lincoln', 'q': 'Leather Care Lincoln 500ml', 'img': 'leather-care-lincoln.png'},
    {'id': 'limpa-vidros-lincoln', 'q': 'Limpa Vidros Lincoln 500ml', 'img': 'limpa-vidros-lincoln.png'},
    {'id': 'removedor-piche-lincoln', 'q': 'Removedor de Piche Lincoln 500ml', 'img': 'removedor-piche-lincoln.png'},
    
    # Dub Boyz
    {'id': 'shampoo-wax-dub', 'q': 'Shampoo Wax Dub Boyz 500ml', 'img': 'shampoo-wax-dub.png'},
    {'id': 'all-cleaner-dub', 'q': 'All Cleaner apc Dub Boyz 500ml', 'img': 'all-cleaner-dub.png'},
    {'id': 'wheel-cleaner-dub', 'q': 'Wheel Cleaner Dub Boyz 500ml', 'img': 'wheel-cleaner-dub.png'},
    {'id': 'iron-remover-dub', 'q': 'Iron Remover Dub Boyz 500ml', 'img': 'iron-remover-dub.png'},
    {'id': 'spray-wax-dub', 'q': 'Spray Wax Dub Boyz 500ml', 'img': 'spray-wax-dub.png'},
    {'id': 'sealant-dub', 'q': 'Sealant Dub Boyz 500ml', 'img': 'sealant-dub.png'},
    {'id': 'coating-dub', 'q': 'Coating Dub Boyz 50ml', 'img': 'coating-dub.png'},
    {'id': 'plastic-restorer-dub', 'q': 'Plastic Restorer Dub Boyz', 'img': 'plastic-restorer-dub.png'},
    {'id': 'leather-dub', 'q': 'Leather hidratante Dub Boyz', 'img': 'leather-dub.png'},
    {'id': 'glass-dub', 'q': 'Glass limpador de vidro Dub Boyz 500ml', 'img': 'glass-dub.png'},
    {'id': 'tar-dub', 'q': 'Tar removedor Dub Boyz 500ml', 'img': 'tar-dub.png'},

    # Car Collection
    {'id': 'cc-shampoo', 'q': 'Car Collection Shampoo 500ml', 'img': 'cc-shampoo.png'},
    {'id': 'cc-wash-wax', 'q': 'Car Collection Wash & Wax 500ml', 'img': 'cc-wash-wax.png'},
    {'id': 'cc-apc', 'q': 'Car Collection APC', 'img': 'cc-apc.png'},
    {'id': 'cc-wheel', 'q': 'Car Collection limpador de rodas', 'img': 'cc-wheel.png'},
    {'id': 'cc-iron', 'q': 'Car Collection iron 500ml', 'img': 'cc-iron.png'},
    {'id': 'cc-wax', 'q': 'Car Collection cera liquida 500ml', 'img': 'cc-wax.png'},
    {'id': 'cc-sealant', 'q': 'Car Collection selante 500ml', 'img': 'cc-sealant.png'},
    {'id': 'cc-coating', 'q': 'Car Collection vitrificador 50ml', 'img': 'cc-coating.png'},
    {'id': 'cc-plastic', 'q': 'Car Collection restaurador de plasticos', 'img': 'cc-plastic.png'},
    {'id': 'cc-leather', 'q': 'Car Collection leather 500ml', 'img': 'cc-leather.png'},
    {'id': 'cc-glass', 'q': 'Car Collection glass 500ml', 'img': 'cc-glass.png'},
    {'id': 'cc-tar', 'q': 'Car Collection removedor de piche', 'img': 'cc-tar.png'},

    # Vonixx (missing)
    {'id': 'v-floc-wash-wax', 'q': 'Vonixx V-Floc Wash & Wax 500ml', 'img': 'v-floc-wash-wax.png'},
    {'id': 'glass-cleaner', 'q': 'Vonixx Glass Cleaner 500ml', 'img': 'glass-cleaner.png'},
    {'id': 'hidra-couro', 'q': 'Vonixx Hidra Couro 500ml', 'img': 'hidra-couro.png'},
    {'id': 'tar-remover', 'q': 'Vonixx Tar Remover 500ml', 'img': 'tar-remover.png'},
]

def remove_white_bg(img_data):
    img = Image.open(io.BytesIO(img_data)).convert("RGBA")
    
    # Scale down if too large, we just need thumbnails for cards
    if img.width > 400:
        ratio = 400 / img.width
        img = img.resize((400, int(img.height * ratio)), Image.Resampling.LANCZOS)
        
    datas = img.getdata()
    newData = []
    for item in datas:
        # Check if the pixel is bright enough to be white background
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            newData.append((255, 255, 255, 0)) # make transparent
        else:
            newData.append(item)
            
    img.putdata(newData)
    
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    return img

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

base_dir = './assets/products/'
os.makedirs(base_dir, exist_ok=True)

import json
for p in products:
    filename = os.path.join(base_dir, p['img'])
    
    # Let's override skip if we actually need the real image instead of placeholder
    # Because my generated placeholders were saved in a file with "placeholder" in the name,
    # but the ones running here will be e.g. "lava-auto-lincoln.png".
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        continue

    print(f"Searching: {p['q']}")
    url = f"https://www.google.com/search?q={urllib.parse.quote(p['q'])}&tbm=isch"
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find images in HTML
        imgs = soup.find_all("img")
        img_data = None
        
        for img in imgs:
            src = img.get("src") or img.get("data-src")
            if src:
                if src.startswith("data:image"):
                    # it's a base64 thumbnail
                    b64_str = src.split(",", 1)[1]
                    img_data = base64.b64decode(b64_str)
                    break
                elif src.startswith("http") and "gstatic" in src:
                    # External thumbnail
                    img_data = requests.get(src).content
                    break
                    
        if img_data:
            img_out = remove_white_bg(img_data)
            img_out.save(filename, "PNG")
            print(f"Saved {p['img']}")
        else:
            print("No image found.")
    except Exception as e:
        print(e)
