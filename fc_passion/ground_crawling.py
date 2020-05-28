import os
import time
import config
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class ReservationGround:

    def __init__(self):
        self.ground_dates = []
        self.reservation_results = []

    def setup(self):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        if '/Users/jinnify' in APP_ROOT:
            APP_DRIVER = os.path.join(APP_ROOT, config.APP_CONFIG['CHROME_DRIVER_TEST_PATH'])
        else:
            APP_DRIVER = os.path.join(APP_ROOT, config.APP_CONFIG['CHROME_DRIVER_PATH'])

        target_url = "http://m.iamground.kr/futsal/search"

        chrome_options = Options()
        chrome_options.add_argument('--headless') # 브라우저를 띄우지 않고 내부적으로 실행 가능
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")

        # web driver 설정
        self.driver = webdriver.Chrome(APP_DRIVER, options=chrome_options)
        # self.driver.set_window_size(300, 920)
        self.driver.get(target_url)

    def remove_ad(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]'))).click()

        except:
            print('Time Out')

    def auto_login(self):
        try:
            self.setup()

            self.remove_ad()

            # 메뉴버튼(login 화면으로 이동)
            self.driver.implicitly_wait(2)
            menu_btn = self.driver.find_element_by_id('navMenu')
            menu_btn.click()

            # 카카오 로그인 클릭
            self.driver.implicitly_wait(2)
            kakao_btn = self.driver.find_element_by_id('kakao')
            kakao_btn.click()

            # Email 입력
            self.driver.find_element_by_id('id_email_2').send_keys(config.APP_CONFIG['K_ID'])
            # PW 입력
            self.driver.find_element_by_id('id_password_3').send_keys(config.APP_CONFIG['K_PW'])

            # 로그인 클릭
            login_btn = self.driver.find_element_by_class_name('submit')
            login_btn.click()

            # 리다이렉트로 home화면 올때 광고가 있으면 제거
            self.remove_ad()

            return True
        except:
            return False

    
    def ground_search(self, success, input_text):
        if success:
            print('성공')
            # 검색 버튼
            
            search_btn = self.driver.find_element_by_id('filterDirect')
            search_btn.click()
            
            # 검색어에 Input
            self.driver.find_element_by_id('iSearch').send_keys(input_text)

            # 검색 구장 선택
            time.sleep(1)
            ground_list = self.driver.find_element_by_css_selector('#ui-id-1').find_elements_by_tag_name('li')
            ground_list[0].click()

            # 예약 리스트 보기
            timetables = self.driver.find_element_by_css_selector(
                    "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
                ).find_elements_by_tag_name('option')

            self.ground_dates.clear()
            for time_content in timetables:
                self.ground_dates.append(time_content.text)

            return {
                "result": "success",
                "data" : self.ground_dates
            }

        else:
            return {
                "result": "failure",
                "msg": "데이터 가져오기 실패! 관리자에게 문의 바랍니다."
            }
    
    def select_date_info(self, selected_date):
        self.reservation_results.clear()

        timetables = self.driver.find_element_by_css_selector(
                    "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
                ).find_elements_by_tag_name('option')

        for time_content in timetables:
            if selected_date == time_content.text:
                time_content.click() # 선택
                schedules = self.driver.find_element_by_class_name('schedule-view').find_elements_by_class_name('time-container')
                for sch in schedules:
                    if sch.get_attribute('resvgroup'):
                        self.reservation_results.append(sch.get_attribute('offset') + ',' + '예약 가능')
                    else:
                        self.reservation_results.append(sch.get_attribute('offset') + ',' + '예약 불가')

        print({selected_date:self.reservation_results})

        return {
            "result": "success",
            "data": self.reservation_results
        }

    def reserve_selected_date(self, selected_date):
        
        try:
            schedules = self.driver.find_element_by_class_name('schedule-view').find_elements_by_class_name('time-container')
            for sch in schedules:
                if sch.find_element_by_class_name('badge-number').get_attribute('offset') == selected_date:
                    sch.click()
            
            time.sleep(1)
            self.driver.find_element_by_id('goToPayment').click();

            # 전체 약관에 모두 동의합니다.
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[8]/label'))).click()


            # 예약 신청 하기
            self.driver.find_element_by_id('resvSubmit').click();
            
            # alert창 확인 버튼
            self.driver.switch_to_alert().accept()

            time.sleep(1)
            self.driver.find_element_by_id('resvClose').click();
            self.driver.quit()
            print("예약 성공!!!!!!")

            return True
        except:
            self.driver.quit()
            return False

        # finally:
        #     # self.driver.quit()

    # 토요일 21시(금요일 00시에 예약해야됨)
    def auto_saturday_reserve(self):
        if self.auto_login():
            print('성공')
            # 검색 버튼
            
            search_btn = self.driver.find_element_by_id('filterDirect')
            search_btn.click()
            
            # 검색어에 Input
            self.driver.find_element_by_id('iSearch').send_keys("토모스포츠클럽")

            # 검색 구장 선택
            time.sleep(1)
            ground_list = self.driver.find_element_by_css_selector('#ui-id-1').find_elements_by_tag_name('li')
            ground_list[0].click()

            # 예약 리스트 보기
            timetables = self.driver.find_element_by_css_selector(
                    "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
                ).find_elements_by_tag_name('option')

            self.ground_dates.clear()
            for time_content in timetables:
                self.ground_dates.append(time_content.text)

            # 마지막 값 날짜 선택
            last_date = self.ground_dates[-1]

            self.reservation_results.clear()

            timetables = self.driver.find_element_by_css_selector(
                        "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
                    ).find_elements_by_tag_name('option')

            # 날짜 선택
            for time_content in timetables:
                if last_date == time_content.text:
                    time_content.click() # 선택


            # 시간 선택 - 21시
            self.reserve_selected_date("2100")
            
    # 금요일 23시(목요일 00시에 예약해야됨)
    def auto_friday_reserve(self):
        if self.auto_login():
            print('성공')
            # 검색 버튼
            
            search_btn = self.driver.find_element_by_id('filterDirect')
            search_btn.click()
            
            # 검색어에 Input
            self.driver.find_element_by_id('iSearch').send_keys("토모스포츠클럽")

            # 검색 구장 선택
            time.sleep(1)
            ground_list = self.driver.find_element_by_css_selector('#ui-id-1').find_elements_by_tag_name('li')
            ground_list[0].click()

            # 예약 리스트 보기
            timetables = self.driver.find_element_by_css_selector(
                    "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
                ).find_elements_by_tag_name('option')

            self.ground_dates.clear()
            for time_content in timetables:
                self.ground_dates.append(time_content.text)

            # 마지막 값 날짜 선택
            last_date = self.ground_dates[-1]

            self.reservation_results.clear()

            timetables = self.driver.find_element_by_css_selector(
                        "#cardContainer > div.container.col-md-6.cardHolder.col-double-6 > div.timetable-container.schedule_list.table-786.search-bottom > div.timetable-content.resv-cal > select"
                    ).find_elements_by_tag_name('option')

            # 날짜 선택
            for time_content in timetables:
                if last_date == time_content.text:
                    time_content.click() # 선택


            # 시간 선택 - 23시
            self.reserve_selected_date("2300")



            

