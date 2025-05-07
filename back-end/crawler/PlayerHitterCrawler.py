from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PlayerHitterCrawler:
    url = "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx?sort=HRA_RT"

    def crawling(self, max_page: int):
        # 셀레니움 옵션 설정
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        try:
            all_data = []
            current_page = 1
            headers = []

            while current_page <= max_page:
                print(f"[INFO] {current_page} 페이지 크롤링 중...")

                # 테이블 로딩 대기
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "record_result"))
                )

                table = driver.find_element(By.CLASS_NAME, "record_result")

                # 첫 페이지에서만 헤더 추출
                if current_page == 1:
                    thead = table.find_element(By.TAG_NAME, "thead")
                    header_elements = thead.find_elements(By.TAG_NAME, "th")
                    headers = [elem.text.strip() for elem in header_elements]

                # 데이터 추출
                tbody = table.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    row_data = [col.text.strip() for col in cols]
                    all_data.append(row_data)

                # 다음 페이지 버튼 클릭
                current_page += 1
                try:
                    paging_div = driver.find_element(By.CLASS_NAME, "paging")
                    next_btn = paging_div.find_element(
                        By.XPATH, f".//a[contains(@id, 'btnNo{current_page}')]"
                    )
                    driver.execute_script("arguments[0].click();", next_btn)
                    time.sleep(1)  # 페이지 넘어가는 시간 대기
                except:
                    print("[INFO] 다음 페이지 없음 또는 에러 발생, 종료합니다.")
                    break

            # DataFrame 생성 및 저장
            df = pd.DataFrame(all_data, columns=headers)
            df = df.replace('', '-')

            directory = './app/hitter'
            os.makedirs(directory, exist_ok=True)
            df.to_json(f'{directory}/hitter.json', force_ascii=False, orient='records', indent=4)

            return '1'
        finally:
            driver.quit()


# 실행
if __name__ == "__main__":
    crawler = PlayerHitterCrawler()
    result = crawler.crawling(max_page=3)
    
        

