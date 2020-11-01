from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
from secrets import username, password
import os
import time
import requests

# Instagram Web Scraper ( Logs into instagram and searches a specific tag, scrolls through the page to the bottom and then stores every single image found)
class InstaBot:
    def __init__(self, username, pw, tag_name):
        # Save your chromedriver somewhere where you won't forget.
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)

        # This is the website the webdriver will connect to.
        self.driver.get("https://instagram.com")

        # Maximise the window.
        self.driver.maximize_window()

        # You will need to send your username and password to the username and password input box.
        # This can be done using the .send_keys() method
        self.driver.find_element_by_xpath(
            "//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath(
            "//input[@name=\"password\"]").send_keys(pw)

        # Now you have to click the sign in button.
        # This can be done using the .click() method
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        # Sleep is being used so the website has time to load and the new elements to appear.
        sleep(4)

        # Click the not now buttons.
        self.driver.find_element_by_class_name('yWX7d').click()
        sleep(2)
        self.driver.find_element_by_class_name('HoLwm').click()
        sleep(2)

        # Send the tag name into the input box and click search.
        self.driver.find_element_by_class_name(
            'XTCLo').send_keys(tag_name)
        sleep(1)
        self.driver.find_element_by_class_name(
            'yCE8d').click()
        sleep(2)

        # Head over to the tagged section.
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/div[2]/a[3]").click()
        sleep(2)

        # --------------------------------------------------------- INFINTINE SCROLLING ---------------------------------------------------------
        # Wait to load page
        scroll_pause_time = 5

        # Get scroll height
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

        # Lets identify the images we want to download by class
        img_els = self.driver.find_elements_by_class_name("FFVAD")

        # --------------------------------------------------------- SAVE IMAGES FOUND AFTER INFINITE SCROLLING ---------------------------------------------------------

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(base_dir, "img")
        os.makedirs(image_dir, exist_ok=True)

        for el in img_els:
            url = el.get_attribute('src')
            base_url = urlparse(url).path
            filename = os.path.basename(base_url)
            filepath = os.path.join(image_dir, filename)
            if os.path.exists(filepath):
                continue
            with requests.get(url, stream=True) as r:
                try:
                    r.raise_for_status()
                except:
                    continue
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

        self.driver.close


my_bot = InstaBot(username, password, "juneshineco")
