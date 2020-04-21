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
# browser = webdriver.Chrome(APP_DRIVER, options=chrome_options)
browser = webdriver.Chrome(APP_DRIVER)

browser.implicitly_wait(5)

browser.get('http://prod.danawa.com/list/?cate=112758&15main_11_02')

# 제조사별 더 보기
# Explicitly wait

# 현재 엘리먼트가 모두 나타날때까지 기다린다.
WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dlMaker_simple"]/dd/div[2]/button[1]'))).click()

# apple 카테고리 선택
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectMaker_simple_priceCompare_A"]/li[13]/label'))).click()

# 현재까지의 소스를 가져온다.
# print(browser.page_source)

time.sleep(2)

soup = BeautifulSoup(browser.page_source, 'html.parser')

# print(soup.prettify())

product_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')
print(product_list)

for product in product_list:
    if not product.find('div', class_='ad_header'):
        print(product.select('p.prod_name > a')[0].text.strip())
        print(product.select('a.thumb_link > img')[0].get('data-original')) # attribute 가져오는 방법

    print()

# browser 종료
browser.quit()