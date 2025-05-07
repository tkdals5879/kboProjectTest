from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PlayerDefenseCrawler:
    url = "https://www.koreabaseball.com/Record/Player/Defense/Basic.aspx"

    def crawling(self, max_page: 16):
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
                next_page_num = current_page + 1
                if next_page_num > max_page:
                    print("[INFO] 마지막 지정된 페이지 도달")
                    break

                try:
                    # 다음 페이지 그룹으로 넘어가는 경우 (ex. 5 → 6, 10 → 11)
                    if current_page % 5 == 0:
                        # "다음" 버튼 클릭
                        try:
                            next_btn = driver.find_element(By.ID, "cphContents_cphContents_cphContents_ucPager_btnNext")
                            driver.execute_script("arguments[0].click();", next_btn)
                            time.sleep(1)

                            # 다음 페이지 그룹의 btnNo1 클릭 (ex. 실제로는 6, 11, 16 등)
                            btn= driver.find_element(By.ID, "cphContents_cphContents_cphContents_ucPager_btnNo1")
                            driver.execute_script("arguments[0].click();", btn)
                            current_page += 1
                            time.sleep(1)
                        except Exception as e:
                            print(f"[ERROR] '다음' 버튼 클릭 실패: {e}")
                            break

                    else:
                        # 다음 페이지 버튼 클릭 (btnNoX)
                        next_page_num = current_page + 1
                        btn_index = next_page_num % 5
                        if btn_index == 0:
                            btn_index = 5  # 실제로는 btnNo5

                        btn = driver.find_element(By.ID, f"cphContents_cphContents_cphContents_ucPager_btnNo{btn_index}")
                        driver.execute_script("arguments[0].click();", btn)
                        current_page += 1
                        time.sleep(1)

                except Exception as e:
                    print(f"[ERROR] 페이지 이동 실패: {e}")
                    break

                

            # DataFrame 생성 및 저장
            df = pd.DataFrame(all_data, columns=headers)
            df = df.replace('', '-')

            directory = './app/defense'
            os.makedirs(directory, exist_ok=True)
            df.to_json(f'{directory}/5defense.json', force_ascii=False, orient='records', indent=4)

            return '1'
        finally:
            driver.quit()


# 실행
if __name__ == "__main__":
    crawler = PlayerDefenseCrawler()
    result = crawler.crawling(max_page=16)
    