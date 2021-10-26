#!/usr/bin/env python3
print("yes")
import os
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import InvalidSessionIdException

# This will go through the stories directory every 15 seconds, open the files inside stories/, then delete them afterwards
base_url = "http://web:5000/stories/"

chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--enable-javascript")

print("hello")


def setup_driver():
    global driver
    while True:
        try:
            driver.quit()
        except Exception as e:
            pass

        try:
            driver = webdriver.Remote(
                command_executor="http://driver:4444/wd/hub",
                desired_capabilities=DesiredCapabilities.CHROME,
                options=chrome_options,
            )

            # We must navigate to the site before setting the cookie
            driver.get(base_url)

            auth_cookie = "6b2a3d6dda4d0b27bbb82b8503339441"
            driver.add_cookie({"name": "auth", "value": auth_cookie})

            return
        except Exception as e:
            print("Waiting before re-attempting connection to driver due to error")
            print(e)
            time.sleep(15)


setup_driver()

while True:
    print("Checking files...")
    for story_file in os.listdir("stories"):
        print(story_file)
        story_id = story_file.replace(".html", "")
        story_url = base_url + story_id

        try:
            driver.get(story_url)
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass
        except Exception as e:
            print("Got exception when trying to view story ", story_file, e)
            setup_driver()
        else:
            time.sleep(3)
            os.unlink(os.path.join("stories", story_file))

    print("Sleeping...")
    time.sleep(15)
