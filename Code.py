import requests
import os
import time
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def creating_folder(name):
    if not os.path.isdir(name):
         os.mkdir(name)

def getting_links(request)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    url = f"https://yandex.ru/images/search?text={request}"
    driver.get(url=url)
    driver.maximize_window()
    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR, 'div.serp-item__preview a.serp-item__link').click()
    with open(f"urls_{request}.txt", 'w') as file:
        for i in range(10):
            try:
                time.sleep(0.5)
                link = driver.find_element(By.CSS_SELECTOR, "a.Button2_view_action").get_attribute("href")
                file.write(link + '\n')
                driver.find_element(By.CSS_SELECTOR, "div.CircleButton:nth-child(4)").click()
            except:
                continue
    driver.close()
    driver.quit()




def download_images(images):
    count = 0

    creating_folder("dataset")
    creating_folder(f"dataset/{images}")

    with open(f"urls_{images}.txt", "r") as file:
        for line in file:
            try:
                url = line.strip()
                time.sleep(4)
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    count+=1
                    with open(f"dataset/{images}/{str(count).zfill(4)}.jpg", "wb") as image_file:
                        shutil.copyfileobj(response.raw, image_file)
                else:
                    continue
            except:
                continue
    print(f'{count} Images downloaded successfully')        


def main():
    if os.path.isdir("dataset"):
        shutil.rmtree("dataset")
    request = "cat"
    getting_links(request)
    download_images(request)
    request = "dog"
    getting_links(request)
    download_images(request)

if __name__ == "__main__":
    main()      