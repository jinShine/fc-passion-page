import os
import config
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def insta_fetch_feed():
    
    result_data = []
    insta_url_list = []
    image_url_list = []
    post_type_list = []
    post_id = 1

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    APP_DRIVER = os.path.join(APP_ROOT, config.APP_CONFIG['CHROME_DRIVER_PATH'])

    chrome_options = Options()
    chrome_options.add_argument('--headless') # 브라우저를 띄우지 않고 내부적으로 실행 가능

    # web driver 설정
    browser = webdriver.Chrome(APP_DRIVER, options=chrome_options)

    browser.get('https://www.instagram.com/fc_passion_jangan/?hl=ko')

    time.sleep(1)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    post_list = soup.select('#react-root > section > main > div > div > article > div > div')
    for post_row in post_list:
        for post in post_row.select('div > div'):

            a_tag = post.select('a')
            if not a_tag == []:
                insta_url_list.append('https://www.instagram.com' + a_tag[0].get('href'))

            type = post.select('a > div > span')
            if not type == []:
                post_type = type[0].get('aria-label')
                if post_type == '동영상':
                    post_type_list.append('동영상')
                else:
                    post_type_list.append('이미지')

            img_tag = post.select('div > div > a > div > div> img')
            if not img_tag == []:
                image_url_list.append(img_tag[0].get('src'))


    for insta_url, image_url, post_type in zip(remove_overlap(insta_url_list), remove_overlap(image_url_list), post_type_list):
        post_info = {
            'id': post_id,
            'image_url': image_url,
            'insta_url': insta_url,
            'post_type': post_type
        }
        post_id += 1
        result_data.append(post_info)

    browser.quit()

    return result_data


def remove_overlap(list):
    new_list = []
    for v in list:
        if v not in new_list:
            new_list.append(v)
    
    return new_list