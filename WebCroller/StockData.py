# StockData.py

"""
driver_setup.py

Selenium 웹 자동화를 위한 Chrome 드라이버를 생성하는 모듈입니다.
undetected_chromedriver(uc)를 사용하여 봇 감지 우회를 지원합니다.

함수:
    get_driver() -> selenium.webdriver.Chrome
        - Chrome 드라이버 인스턴스를 생성하여 반환합니다.
        - 다음과 같은 옵션을 적용합니다:
            • 창 최대화
            • 봇 감지 방지 설정 (AutomationControlled, infobars 등)
            • 사용자 에이전트 설정
            • 샌드박스 비활성화 및 리소스 사용 제한 해제

사용 예시:
    from driver_setup import get_driver
    driver = get_driver()
    driver.get("https://example.com")
"""

stock_link_dic = dict()
stock_ticker_list = []      # 티커별 주소를 저장하는 딕셔너리
stock_rank_dic = dict()         # 티커별 점수를 저장하는 딕셔너리
with open("TextDirectory/StockData.txt", 'r') as f:
    for line in f:
        TICKER, link = line.split()
        stock_ticker_list.append(TICKER)    # 티커 저장
        stock_link_dic[TICKER] = link       # 티커, 주소 저장
        stock_rank_dic[TICKER] = [["dividend_yield", "dividend_growth_1y", "dividend_growth_3y", "dividend_growth_5y", "payout_ratio"]]

