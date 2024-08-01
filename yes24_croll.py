from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import time

# Chrome 드라이버 경로
chrome_driver_path = 'C:/Users/406/Desktop/cr/chromedriver.exe'

# ChromeService 및 ChromeOptions 설정
service = ChromeService(executable_path=chrome_driver_path)
options = Options()
options.headless = False  # 브라우저를 숨기지 않고 실행할 경우 False, 숨기고 실행할 경우 True

driver = webdriver.Chrome(service=service, options=options)
driver.get('http://ticket.yes24.com/New/Genre/GenreList.aspx?genretype=1&genre=15456')
time.sleep(1)

# CSV 파일 설정
with open('data.csv', mode='w', newline='', encoding='utf-8') as data_file, \
     open('artist.csv', mode='w', newline='', encoding='utf-8') as artist_file:
    data_writer = csv.writer(data_file)
    # CSV 파일 헤더 작성
    data_writer.writerow(["URL", "상품 제목", "포스터 URL", "상세 포스터 URL", "공연장소", "공연기간", "캐스팅 리스트"])

    def scroll_into_view(driver, element):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(2)  # 스크롤 후 대기

    for x in range(2, 35):  # x가 2에서 34까지 증가
        for y in range(1, 6):  # y가 1에서 5까지 증가
            for _ in range(10):  # 페이지 다운을 10번 시도
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)  # 스크롤 후 대기

            try:
                path = f'/html/body/section/div[{x}]/a[{y}]'
                element = driver.find_element(By.XPATH, path)
                print(f"경로: {path}")
                time.sleep(1)
                element.click()
                time.sleep(3)

                # -----------------------------------------------
                current_url = driver.current_url
                print("URL:", current_url)

                # -----------------------------------------------
                titles = driver.find_elements(By.CLASS_NAME, "rn-big-title")
                for i in titles:
                    title = i.text
                    print("타이틀:", title)

                # -----------------------------------------------
                Thumbnail = driver.find_element(By.XPATH, '//div[@class="rn-03-left"]//img')
                Thumbnail_src = Thumbnail.get_attribute('src')
                print("썸네일:", Thumbnail_src)

                # -----------------------------------------------
                image_urls = []
                image_elements = driver.find_elements(By.XPATH, '//div[@class="rn08-txt"]//img')
                for element in image_elements:
                    img_src = element.get_attribute('src')
                    image_urls.append(img_src)
                    print(f"내용 이미지:", img_src)

                # -----------------------------------------------
                try:
                    location_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//th[text()="공연장소"]/following-sibling::td'))
                    )
                    location_text = location_element.text.strip()
                    print("공연장소:", location_text)
                except TimeoutException:
                    print("공연장소 정보를 찾을 수 없습니다.")
                    location_text = ""

                # -----------------------------------------------
                try:
                    date_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'ps-date'))
                    )
                    date_text = date_element.text.strip()
                    print("공연 날짜:", date_text)
                except TimeoutException:
                    print("공연 날짜 정보를 찾을 수 없습니다.")
                    date_text = ""

                # -----------------------------------------------
                try:
                    cast_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//th[text()="주연"]/following-sibling::td'))
                    )
                    cast_text = cast_element.text.strip()
                    print("주연:", cast_text)
                except TimeoutException:
                    print("주연 정보를 찾을 수 없습니다.")
                    cast_text = ""

                # -----------------------------------------------
                data_writer.writerow([current_url, title, Thumbnail_src, ", ".join(image_urls), location_text, date_text, cast_text])

                time.sleep(1)
                driver.back()  # 이전 페이지로 돌아가기
                time.sleep(2)

            except NoSuchElementException:
                print(f"요소를 찾을 수 없습니다: {path}")
                continue

driver.quit()
