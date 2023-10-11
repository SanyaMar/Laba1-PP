import requests
from bs4 import BeautifulSoup
from faker import UserAgent
import os

os.mkdir("Cat")
os.mkdir("Gog")

url = 'https://yandex.ru/images/search?from=tabbar&text=cat'

html = requests.get(url)
content = html.text

parse = BeautifulSoup(content,'html.parser')

img = parse.find_all('img')

def download_images(images):
    count = 0
    print(f"Total {len(images)} Image Found!")

    if len(images) != 0:
        for i, image in enumerate(images):

            try:
                image_link = image["data-srcset"]                
            except:
                try:
                    image_link = image["data-src"]
                except:
                    try:                        
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            image_link = image["src"]
                        except:
                            pass
            try:
                r = requests.get(image_link).content
                try:
                    r = str(r, 'utf-8')
                except UnicodeDecodeError:
                    with open(f"images{i+1}.jpg", "wb+") as f:
                        f.write(r)
                    count += 1
            except:
                pass    
            
download_images(img)            