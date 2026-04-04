import os
import time
import urllib.request
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

products = [
    # Vonixx
    {'id': 'vfloc', 'q': 'Vonixx V-Floc', 'img': 'v-floc.png'},
    {'id': 'blend', 'q': 'Vonixx Blend Cera', 'img': 'blend.png'},
    {'id': 'shiny', 'q': 'Vonixx Shiny renovador de pneus 500ml', 'img': 'shiny.png'},
    
    # Lincoln
    {'id': 'hsf', 'q': 'Lincoln HSF polidor', 'img': 'hsf.png'},
    {'id': 'hof', 'q': 'Lincoln HOF polidor', 'img': 'hof.png'},
    {'id': 'crystal-clear', 'q': 'Lincoln Crystal Clear limpa vidros', 'img': 'crystal-clear-lincoln.png'},
    
    # Dub Boyz
    {'id': 'reboot', 'q': 'Dub Boyz Reboot descontaminante', 'img': 'reboot-dub.png'},
    {'id': 'd-ret', 'q': 'Dub Boyz D Ret', 'img': 'd-ret-dub.png'},
    
    # Car Collection
    {'id': 'finishs-pro', 'q': 'Car Collection Finishs Pro', 'img': 'finishs-pro.png'},
    {'id': 'pro-wash', 'q': 'Car Collection Pro Wash', 'img': 'pro-wash-cc.png'},
    {'id': 'pro-cleanse', 'q': 'Car Collection Pro Cleanse', 'img': 'pro-cleanse.png'},
]

def remove_white_bg(img_data):
    img = Image.open(io.BytesIO(img_data)).convert("RGBA")
    
    if img.width > 300:
        ratio = 300 / img.width
        img = img.resize((300, int(img.height * ratio)), Image.Resampling.LANCZOS)
        
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

def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    base_dir = './assets/products/'
    os.makedirs(base_dir, exist_ok=True)
    
    for p in products:
        filename = os.path.join(base_dir, p['img'])
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print(f"Already exists: {filename}")
            continue
            
        print(f"Searching: {p['q']}")
        try:
            driver.get(f"https://www.bing.com/images/search?q={urllib.parse.quote(p['q'])}")
            time.sleep(1)
            
            # Find the first image using Bing's selector
            img_element = driver.find_element(By.CSS_SELECTOR, "img.mimg")
            src = img_element.get_attribute("src") or img_element.get_attribute("data-src")
            
            if src and src.startswith("http"):
                req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(req, timeout=10).read()
                
                img_out = remove_white_bg(img_data)
                img_out.save(filename, "PNG")
                print(f"Saved {filename}")
            else:
                print(f"No valid src found for {p['q']}")
        except Exception as e:
            print(f"Error for {p['q']}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
