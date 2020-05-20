import os
import config
from selenium import webdriver


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if '/Users/jinnify' in APP_ROOT:
    APP_DRIVER = os.path.join(APP_ROOT, config.APP_CONFIG['CHROME_DRIVER_TEST_PATH'])
else:
    APP_DRIVER = os.path.join(APP_ROOT, config.APP_CONFIG['CHROME_DRIVER_PATH'])

# web driver 설정
browser = webdriver.Chrome(APP_DRIVER)

# 브라우저 대기
browser.implicitly_wait(5) # 5초

# 속성 확인
print(dir(browser))

# 브라우저 사이즈
browser.set_window_size(920, 280) # browser.maximize_window(), browser.minimize_window()

# 페이지 이동
browser.get('https://www.daum.net')

# 페이지 내용
# print(browser.page_source)


############################################
# 선택자 접근 방법


# 검색창 input 선택
element = browser.find_element_by_css_selector('div.inner_search > input.tf_keyword')


# 검색창 입력 방법
element.send_keys('아이유')

# 버튼 선택
element.submit()

# 스크린샷 방법
# browser.save_screenshot('./iu.jpg')


# 브라우저 종료
browser.quit()