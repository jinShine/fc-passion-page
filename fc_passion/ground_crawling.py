
import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# app = Flask(__name__)

# ground_url = 'https://m.iamground.kr/futsal/search'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(ground_url, headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')

# print(soup)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DRIVER = os.path.join(APP_ROOT, 'static/driver/chromedriver')

target_url = "http://m.iamground.kr/futsal/search"

driver = webdriver.Chrome(APP_DRIVER)
driver.get(target_url)

def remove_ad():
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "close-row"))
        )

        if element.is_displayed:
            ad_close_btn = driver.find_element_by_class_name('close-row')
            ad_close_btn.click()

    except:
        print('Time Out')

def auto_login():

    try:
        remove_ad()
        
        # 메뉴버튼(login 화면으로 이동)
        driver.implicitly_wait(2)
        menu_btn = driver.find_element_by_id('navMenu')
        menu_btn.click()

        # 카카오 로그인 클릭
        driver.implicitly_wait(2)
        kakao_btn = driver.find_element_by_id('kakao')
        kakao_btn.click()

        # Email 입력
        driver.find_element_by_id('id_email_2').send_keys('gktmdwls1346@naver.com')
        # PW 입력
        driver.find_element_by_id('id_password_3').send_keys('whis!346')

        # 로그인 클릭
        login_btn = driver.find_element_by_class_name('submit')
        login_btn.click()

        # 리다이렉트로 home화면 올때 광고가 있으면 제거
        remove_ad()

        return True

    except:
        return False


    def search():
        if auto_login():
                                        
                                        ㄷ          


auto_login()




# ri = GroundInfo('http://m.iamground.kr/futsal/search')
# ri.run()
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# APP_DRIVER = os.path.join(APP_ROOT, 'static/driver/chromedriver')


# driver = webdriver.Chrome(APP_DRIVER)
# driver.get("http://m.iamground.kr/futsal/search")

# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "close-row"))
#     )
#     if element.is_displayed:
#         ad_close_btn = driver.find_element_by_class_name('close-row')
#         ad_close_btn.click()
#     else:
#         print("오?")
# except:
#     print('Time Out')

# # 광고창이 뜨면 close
# # if element.is_displayed:
# #     ad_close_btn = driver.find_element_by_class_name('close-row')
# #     ad_close_btn.click()
# # else:
# #     print("오?")

# driver.implicitly_wait(2)
# menu_btn = driver.find_element_by_id('navMenu')
# menu_btn.click()

# driver.implicitly_wait(2)
# kakao_btn = driver.find_element_by_id('kakao')
# kakao_btn.click()

# email_input = driver.find_element_by_id('id_email_2').send_keys('gktmdwls1346@naver.com')
# pw_input = driver.find_element_by_id('id_password_3').send_keys('whis!346')

# login_btn = driver.find_element_by_class_name('submit')
# login_btn.click()

# try:
#     # ID가 myDynamicElement인 element가 로딩될 때 까지 10초 대기
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "close-row"))
#     )
    
# except:
# 	# 실패 시에는 에러메시지로 Time Out 출력
#     print('Time Out')
# finally:
#     # driver.quit()
#     print("Finally")

# # 광고창이 뜨면 close
# if element.is_displayed:
#     ad_close_btn = driver.find_element_by_class_name('close-row')
#     ad_close_btn.click()
# else:
#     print("오?")


# Ground()


# if __name__ == '__main__':
#    app.run('0.0.0.0',port=5019,debug=True)
# body > div.ad-container > div.close-row.covid19 > span


