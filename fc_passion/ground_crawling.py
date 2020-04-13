import os
import time
import config
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DRIVER = os.path.join(APP_ROOT, config.APP_CONFIG['CHROME_DRIVER_PATH'])

target_url = "http://m.iamground.kr/futsal/search"

driver = webdriver.Chrome(APP_DRIVER)
driver.get(target_url)

ground_dates = []
results = []

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
        driver.find_element_by_id('id_email_2').send_keys(config.APP_CONFIG['K_ID'])
        # PW 입력
        driver.find_element_by_id('id_password_3').send_keys(config.APP_CONFIG['K_PW'])

        # 로그인 클릭
        login_btn = driver.find_element_by_class_name('submit')
        login_btn.click()

        # 리다이렉트로 home화면 올때 광고가 있으면 제거
        remove_ad()

        return True
    except:
        return False


def ground_search(success, input_text):
    if success:
        print('성공')
        # 검색 버튼
        search_btn = driver.find_element_by_id('filterDirect')
        search_btn.click()
        
        # 검색어에 Input
        driver.find_element_by_id('iSearch').send_keys(input_text)

        # 검색 구장 선택
        time.sleep(0.5)
        ground_list = driver.find_element_by_css_selector('#ui-id-1').find_elements_by_tag_name('li')
        ground_list[0].click()

        # 예약 리스트 보기
        timetables = driver.find_element_by_css_selector(
                "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
            ).find_elements_by_tag_name('option')

        ground_dates.clear()
        for time_content in timetables:
            # schedule_dic = { 
            #     time_content.text : time_content.get_attribute('value')
            # }
            ground_dates.append(time_content.text)
        print(ground_dates)

        
        # 해당 날짜 선택 
        select_date_info(ground_dates[10])
        
    else:
        print('실패')

def select_date_info(selected_date):
    timetables = driver.find_element_by_css_selector(
                "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
            ).find_elements_by_tag_name('option')

    for time_content in timetables:
        if selected_date == time_content.text:
            time_content.click() # 선택
            schedules = driver.find_element_by_class_name('schedule-view').find_elements_by_class_name('time-container')
            for sch in schedules:
                if sch.get_attribute('resvgroup'):
                    results.append(sch.get_attribute('offset') + ',' + '예약 가능')
                else:
                    results.append(sch.get_attribute('offset') + ',' + '예약 불가')

            print({selected_date:results})
    
    

# auto_login()
ground_search(auto_login(), "토모스포츠클럽")
