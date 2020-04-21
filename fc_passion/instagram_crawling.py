import os
import config
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DRIVER = os.path.join(APP_ROOT, config.APP_CONFIG['CHROME_DRIVER_PATH'])

chrome_options = Options()
chrome_options.add_argument('--headless') # 브라우저를 띄우지 않고 내부적으로 실행 가능

# web driver 설정
browser = webdriver.Chrome(APP_DRIVER, options=chrome_options)
browser = webdriver.Chrome(APP_DRIVER)

browser.implicitly_wait(5)

browser.get('https://www.instagram.com/fc_passion_jangan/?hl=ko')

time.sleep(2)

soup = BeautifulSoup(browser.page_source, 'html.parser')

data = []
post_info = {}

post_list = soup.select('#react-root > section > main > div > div > article > div > div')

post_id = 0

for post_row in post_list:
    # post_info['insta_url'] = post_row.select('div > div')
    # for post in post_row.select('div > div'):
    #     if not post.select('a') == []:
    #         post_info['insta_url'] = 'https://www.instagram.com' + post.select('a')[0].get('href')
            
    for post in post_row.select('div > div'):
        if not post.select('a') == []:
            post_info['insta_url'] = 'https://www.instagram.com' + post.select('a')[0].get('href')
        
    for post in post_row.select('div > div > a > div > div'):
        if not post.select('img') == []:
            post_id += 1
            post_info['id'] = post_id
            post_info['image_url'] = post.select('img')[0].get('src')
            data.append(post_info)
        
    print()
    print()

print(data)

 


# browser.quit()