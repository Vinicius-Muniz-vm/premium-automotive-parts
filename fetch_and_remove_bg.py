from duckduckgo_search import DDGS
from PIL import Image
import urllib.request
import io
import os

products = [
    # Lincoln
    {'id': 'lava-auto', 'q': 'Lava Auto Lincoln 500ml frasco estetica', 'img': 'lava-auto-lincoln.png'},
    {'id': 'lava-auto-cera', 'q': 'Lava Auto com Cera Lincoln 500ml frasco', 'img': 'lava-auto-cera-lincoln.png'},
    {'id': 'apc-lincoln', 'q': 'APC Lincoln 500ml frasco', 'img': 'apc-lincoln.png'},
    {'id': 'wheel-cleaner-lincoln', 'q': 'Wheel Cleaner Lincoln 500ml frasco', 'img': 'wheel-cleaner-lincoln.png'},
    {'id': 'iron-remover-lincoln', 'q': 'Iron Remover descontaminante ferroso Lincoln 500ml', 'img': 'iron-remover-lincoln.png'},
    {'id': 'cera-liquida-lincoln', 'q': 'Cera Liquida Lincoln 500ml frasco', 'img': 'cera-liquida-lincoln.png'},
    {'id': 'selante-lincoln', 'q': 'Selante Paint Sealer Lincoln frasco', 'img': 'selante-lincoln.png'},
    {'id': 'vitrificador-lincoln', 'q': 'Vitrificador Lincoln 50ml frasco', 'img': 'vitrificador-lincoln.png'},
    {'id': 'restaurador-lincoln', 'q': 'Restaurador Plastico Lincoln 500ml frasco', 'img': 'restaurador-lincoln.png'},
    {'id': 'leather-care-lincoln', 'q': 'Leather Care Lincoln banco couro 500ml frasco', 'img': 'leather-care-lincoln.png'},
    {'id': 'limpa-vidros-lincoln', 'q': 'Limpa Vidros Lincoln 500ml frasco', 'img': 'limpa-vidros-lincoln.png'},
    {'id': 'removedor-piche-lincoln', 'q': 'Removedor de Piche Lincoln 500ml frasco', 'img': 'removedor-piche-lincoln.png'},
    
    # Dub Boyz
    {'id': 'shampoo-wax-dub', 'q': 'Shampoo Wax Dub Boyz 500ml', 'img': 'shampoo-wax-dub.png'},
    {'id': 'all-cleaner-dub', 'q': 'All Cleaner apc Dub Boyz 500ml', 'img': 'all-cleaner-dub.png'},
    {'id': 'wheel-cleaner-dub', 'q': 'Wheel Cleaner limpador de rodas Dub Boyz 500ml', 'img': 'wheel-cleaner-dub.png'},
    {'id': 'iron-remover-dub', 'q': 'Iron Remover Dub Boyz 500ml', 'img': 'iron-remover-dub.png'},
    {'id': 'spray-wax-dub', 'q': 'Spray Wax cera liquida Dub Boyz 500ml', 'img': 'spray-wax-dub.png'},
    {'id': 'sealant-dub', 'q': 'Sealant selante Dub Boyz 500ml', 'img': 'sealant-dub.png'},
    {'id': 'coating-dub', 'q': 'Coating vitrificador Dub Boyz 50ml', 'img': 'coating-dub.png'},
    {'id': 'plastic-restorer-dub', 'q': 'Plastic Restorer plastico Dub Boyz 500ml', 'img': 'plastic-restorer-dub.png'},
    {'id': 'leather-dub', 'q': 'Leather hidratante couro Dub Boyz 500ml', 'img': 'leather-dub.png'},
    {'id': 'glass-dub', 'q': 'Glass limpador de vidro Dub Boyz 500ml', 'img': 'glass-dub.png'},
    {'id': 'tar-dub', 'q': 'Tar removedor de piche Dub Boyz 500ml', 'img': 'tar-dub.png'},

    # Car Collection
    {'id': 'cc-shampoo', 'q': 'Car Collection Shampoo 500ml produto', 'img': 'cc-shampoo.png'},
    {'id': 'cc-wash-wax', 'q': 'Car Collection Wash & Wax 500ml produto', 'img': 'cc-wash-wax.png'},
    {'id': 'cc-apc', 'q': 'Car Collection APC limpador multiuso 500ml produto', 'img': 'cc-apc.png'},
    {'id': 'cc-wheel', 'q': 'Car Collection limpador de rodas 500ml produto', 'img': 'cc-wheel.png'},
    {'id': 'cc-iron', 'q': 'Car Collection removedor ferroso 500ml produto', 'img': 'cc-iron.png'},
    {'id': 'cc-wax', 'q': 'Car Collection cera liquida 500ml produto', 'img': 'cc-wax.png'},
    {'id': 'cc-sealant', 'q': 'Car Collection selante 500ml', 'img': 'cc-sealant.png'},
    {'id': 'cc-coating', 'q': 'Car Collection vitrificador 50ml', 'img': 'cc-coating.png'},
    {'id': 'cc-plastic', 'q': 'Car Collection restaurador de plasticos 500ml', 'img': 'cc-plastic.png'},
    {'id': 'cc-leather', 'q': 'Car Collection hidratante couro 500ml produto', 'img': 'cc-leather.png'},
    {'id': 'cc-glass', 'q': 'Car Collection limpa vidros 500ml', 'img': 'cc-glass.png'},
    {'id': 'cc-tar', 'q': 'Car Collection removedor de piche 500ml', 'img': 'cc-tar.png'},

    # Vonixx (missing ones)
    {'id': 'v-floc-wash-wax', 'q': 'Vonixx V-Floc Wash & Wax 500ml', 'img': 'v-floc-wash-wax.png'},
    {'id': 'glass-cleaner', 'q': 'Vonixx Glass Cleaner 500ml', 'img': 'glass-cleaner.png'},
    {'id': 'hidra-couro', 'q': 'Vonixx Hidra Couro 500ml', 'img': 'hidra-couro.png'},
    {'id': 'tar-remover', 'q': 'Vonixx Tar Remover 500ml', 'img': 'tar-remover.png'},
]

def remove_white_bg(img_data):
    img = Image.open(io.BytesIO(img_data)).convert("RGBA")
    
    # Scale down if very large to save processing and space
    if img.width > 300:
        ratio = 300 / img.width
        img = img.resize((300, int(img.height * ratio)), Image.Resampling.LANCZOS)
        
    datas = img.getdata()
    newData = []
    # tollerant magic wand for white backgrounds
    for item in datas:
        # Check if the pixel is bright enough to be white background
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            newData.append((255, 255, 255, 0)) # make transparent
        else:
            newData.append(item)
            
    img.putdata(newData)
    
    # Check edges and crop automatically sometimes
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    return img

def main():
    ddgs = DDGS()
    base_dir = './assets/products/'
    os.makedirs(base_dir, exist_ok=True)
    
    for p in products:
        filename = base_dir + p['img']
        if os.path.exists(filename):
            print(f"Skipping {filename}")
            continue
            
        print(f"Searching for: {p['q']}")
        try:
            results = ddgs.images(p['q'], max_results=1)
            for res in results:
                url = res['image']
                print(f"Downloading from {url[:50]}...")
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(req, timeout=10).read()
                
                img_out = remove_white_bg(img_data)
                img_out.save(filename, "PNG")
                print(f"Saved {filename}")
                break
        except Exception as e:
            print(f"Error for {p['q']}: {e}")

if __name__ == "__main__":
    main()
