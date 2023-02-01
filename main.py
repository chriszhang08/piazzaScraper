# %%
import time
import requests
import selenium.common.exceptions
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# %% Launching automated Chrome Browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://piazza.com/")

# %%
driver.find_element(By.CSS_SELECTOR, "#login_button").click()
time.sleep(5)

# %%
driver.find_element(By.CSS_SELECTOR, "#email_field").send_keys("chrzhang@umich.edu")
driver.find_element(By.CSS_SELECTOR, "#password_field").send_keys("TTVAgentCaro1ina")
driver.find_element(By.CSS_SELECTOR, "#modal_login_button").click()

# %%
driver.get("https://piazza.com/class/l7548zpfvr8yj/post/1")

# %% iterate and scrape
post_id = 1
class_id = "l7548zpfvr8yj"
allPosts = open('allPosts.txt', 'w')


def scrape_content(post_id):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find("h1", {"id": "postViewSummaryId"})
    question_content = soup.find_all("div", {"class": "render-html-content overflow-hidden latex_process"})

    allPosts.write("\n------------------------@" + str(post_id) + "-------------------------\n")
    allPosts.write(header.text + "\n")
    for entry in question_content:
        for content in entry.contents:
            allPosts.write(str(content) + "\n")
        allPosts.write("\n-------------------------------------------------\n")


# %%
for id in range(2137, 4770):
    base_url = f"https://piazza.com/class/{class_id}/post/{id}"
    try:
        driver.get(base_url)
        scrape_content(id)
    except:
        print("not permitted")

allPosts.close()
