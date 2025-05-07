from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
import os
import re
from pathlib import Path

class GameCalCrawler:

    url = "https://www.koreabaseball.com/Schedule/Schedule.aspx"

    def crawling(self, month):
        # selenium 업데이트로 인해 이제 크롬드라이버가 필요없다!
        options = Options()

        options.add_argument("--headless")
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        select = Select(driver.find_element(By.ID, "ddlMonth"))
        select.select_by_value(month)
        table = driver.find_element(By.CLASS_NAME, "tbl-type06")
        thead = table.find_element(By.TAG_NAME, "thead") # 테이블 칼럼 부분
        header = thead.text.split() # df에 칼럼으로 쓸 부분 미리 빼놓음
        header.append("score")
        tbody = table.find_element(By.TAG_NAME, "tbody") # 경기 일정이 있는 부분
        rows = tbody.find_elements(By.TAG_NAME, "tr") # 각 라인 별 데이터 추출
        if len(rows) == 1:
            return '0'

        lines = []
        # for value in rows: # 라인 별로 반복문 돌며 데이터 추출
        #     body = value.find_elements(By.TAG_NAME, "td")
        #     schedule_list = []
        #     for b in body:
        #         schedule_list.append(b.text) # 칼럼 별 데이터들 라인 별로 리스트에 저장
        #     lines.append(schedule_list) # 각 라인 별 데이터를 한번 더 리스트에 저장

        for value in rows:
            body = value.find_elements(By.TAG_NAME, "td")
            schedule_dict = {}

            for idx, b in enumerate(body):
                col_name = header[idx] if idx < len(header) else f"col_{idx}"
                text = b.text.strip()

                if col_name == "경기":
                    text = text.replace(" ", "")
                    if "vs" in text:
                        parts = text.split("vs")
                        if len(parts) == 2:
                            away_text = parts[0]
                            home_text = parts[1]

                            # 예: "롯데2vs12LG" → home: 롯데2, away: 12LG
                            away_match = re.match(r"([가-힣]+)(\d+)$", away_text)
                            home_match = re.match(r"(\d+)([가-힣]+)$", home_text)

                            if  away_match and home_match:
                                away_team, away_score = away_match.groups()
                                home_score, home_team = home_match.groups()

                                schedule_dict["경기"] = f"{away_team} vs {home_team}"
                                schedule_dict["score"] = {
                                    "away": int(away_score),
                                    "home": int(home_score)
                                }
                            else:
                                schedule_dict["경기"] = text
                                schedule_dict["score"] = {"away": None, "home": None}
                        else:
                            schedule_dict["경기"] = text
                            schedule_dict["score"] = {"away": None, "home": None}
                    else:
                        schedule_dict["경기"] = text
                        schedule_dict["score"] = {"away": None, "home": None}
                else:
                    schedule_dict[col_name] = text

            lines.append(schedule_dict)


        # 날짜 데이터가 없는 라인을 위해 데이터 핸들링
        data = []
        game_day = None

        for line in lines:
            if line.get("날짜", "").endswith(")"):
                game_day = line["날짜"]
                data.append(line)
            else:
                line["날짜"] = game_day
                data.append(line)

        df = pd.DataFrame(data, columns=header) # json으로 저장해주기 위해 데이터프레임 생성
        df = df.replace('','-')
        # 디렉토리 확인 및 생성
        # directory = './data/game_schedule'
        # if not os.path.exists(directory):
        #     os.makedirs(directory)  # 디렉토리 생성
        BASE_DIR = Path(__file__).resolve().parent.parent
        SAVE_DIR = BASE_DIR / 'data' / 'game_schedule'

        # 파일 저장
        file_path = SAVE_DIR / f'games_{month}.json'
        df.to_json(file_path, force_ascii=False, orient='records', indent=4)
        driver.quit()

        return '1'

if __name__ == "__main__":
    crawler = GameCalCrawler()
    df = crawler.crawling('04')
    # print(df)