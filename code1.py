import requests
import os
import time
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def creating_folder(name: str) -> None:
    if not os.path.isdir(name):
        os.mkdir(name)


def getting_links(request: str) -> None:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    time.sleep(2)
    url = f"https://yandex.ru/images/search?text={request}"
    driver.get(url=url)
    time.sleep(3)
    driver.find_element(
        By.CSS_SELECTOR, "div.serp-item__preview a.serp-item__link"
    ).click()
    with open(f"urls_{request}.txt", "w") as file:
        for _ in range(10):
            try:
                time.sleep(2)
                link = driver.find_element(
                    By.CLASS_NAME, "MMImage-Origin"
                ).get_attribute("src")
                file.write(link + "\n")
                driver.find_element(
                    By.CLASS_NAME, "MediaViewer_theme_fiji-ButtonNext"
                ).click()
            except:
                continue
    driver.close()
    driver.quit()


def download_images(images: str) -> None:
    count = 0

    creating_folder("dataset")
    creating_folder(os.path.join("dataset", images))

    with open(f"urls_{images}.txt", "r") as file:
        for line in file:
            try:
                url = line.strip()
                time.sleep(10)
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(
                        os.path.join("dataset", images, str(count).zfill(4)+".jpg"), "wb"
                    ) as image_file:
                        shutil.copyfileobj(response.raw, image_file)
                        
                        count += 1
                        
                else:
                    continue
            except:
                continue
    print(f"{count} Images downloaded successfully")


def main() -> None:
    if os.path.isdir("dataset"):
        shutil.rmtree("dataset")
    request = "dog"
    getting_links(request)
    time.sleep(5)
    download_images(request)
    request = "cat"
    getting_links(request)
    time.sleep(5)
    download_images(request)
    time.sleep(15)