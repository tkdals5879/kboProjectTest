from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
import os
from pathlib import Path

class TeamRankCrawler:

    url = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx"

    def crawling(self):
        # selenium 업데이트로 인해 이제 크롬드라이버가 필요없다!
        options = Options()

        options.add_argument("--headless")
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        table = driver.find_element(By.ID, "cphContents_cphContents_cphContents_udpRecord")
        thead = table.find_element(By.TAG_NAME, "thead") # 테이블 칼럼 부분
        header = thead.text.split() # df에 칼럼으로 쓸 부분 미리 빼놓음
        tbody = table.find_element(By.TAG_NAME, "tbody") # 경기 일정이 있는 부분
        rows = tbody.find_elements(By.TAG_NAME, "tr") # 각 라인 별 데이터 추출
        if len(rows) == 1:
            return '0'

        data = []
        for row in rows:  # 각 행 별로 반복문 돌며 데이터 추출
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 0:  # 데이터가 있는 행만 처리
                rank = columns[0].text.strip()  # 순위
                team = columns[1].text.strip()  # 팀명
                games = columns[2].text.strip()  # 경기
                wins = columns[3].text.strip()  # 승
                losses = columns[4].text.strip()  # 패
                draws = columns[5].text.strip()  # 무
                win_rate = columns[6].text.strip()  # 승률
                game_diff = columns[7].text.strip()  # 게임차
                last_10_games = columns[8].text.strip()  # 최근10경기
                streak = columns[9].text.strip()  # 연속
                home = columns[10].text.strip()  # 홈
                away = columns[11].text.strip()  # 방문

                # 각 행의 데이터를 딕셔너리로 저장
                data.append({
                    '순위': rank,
                    '팀명': team,
                    '경기': games,
                    '승': wins,
                    '패': losses,
                    '무': draws,
                    '승률': win_rate,
                    '게임차': game_diff,
                    '최근10경기': last_10_games,
                    '연속': streak,
                    '홈': home,
                    '방문': away
                })

        # 크롤링된 데이터를 pandas DataFrame으로 변환
        df = pd.DataFrame(data)

        df = pd.DataFrame(data, columns=header) # json으로 저장해주기 위해 데이터프레임 생성
        df = df.replace('','-')
        # 디렉토리 확인 및 생성
        # directory = './data/team_rank'
        # if not os.path.exists(directory):
        #     os.makedirs(directory)  # 디렉토리 생성

        # # 파일 저장
        # df.to_json(f'{directory}/team_rank.json', force_ascii=False, orient='records', indent=4)

        # # 크롬 드라이버 종료
        # driver.quit()
        BASE_DIR = Path(__file__).resolve().parent.parent
        SAVE_DIR = BASE_DIR / 'data' / 'team_rank'

        # 파일 저장
        file_path = SAVE_DIR / f'team_rank.json'
        df.to_json(file_path, force_ascii=False, orient='records', indent=4)
        driver.quit()

        return df  # DataFrame 반환

if __name__ == "__main__":
    crawler = TeamRankCrawler()
    df = crawler.crawling()
    # 크롤링된 데이터를 CSV로 저장 (원하는 경우)
    # df.to_csv("team_rank.csv", index=False)