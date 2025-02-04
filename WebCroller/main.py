from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import StockData    # StockData.py import

# 웹페이지에서 대상의 Xpath를 저장하는 리스트
XPATH_list = [
    '//*[@id="stock-overview"]/div/div[1]/div[3]/div/div/div[2]/div/div/div[4]/p[1]',
    '//*[@id="dividend-growth-history"]/section/table/tbody/tr[2]/td[3]/p',
    '//*[@id="dividend-growth-history"]/section/table/tbody/tr[2]/td[4]/p',
    '//*[@id="dividend-growth-history"]/section/table/tbody/tr[2]/td[5]/p',
    '//*[@id="stock-daily-snapshot"]/div[2]/div/div[1]/div[2]/div[2]'
]

# 진행률 저장
progress_rate = 0
cnt = 1

# with-as절을 통해 명령어가 끝나면 자체적으로 driver 객체를 소멸시켜 준다. 크롬 드라이버 객체 생성, Chrome 브라우저 실행
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:

    for TICKER in StockData.stock_ticker_list:
        link = StockData.stock_link_dic[TICKER]

        # 웹 크롤링 진행률
        progress_rate = round((cnt/len(StockData.stock_ticker_list)) * 100, 2)

        # Stock 주소
        driver.get(link)

        # 요청이 완벽하게 응답이 되면 다음을 실행하거나 10초를 기다린다. -> 10초까지를 기다리는데 렌더링이 끝나면 그때 종료
        driver.implicitly_wait(10)

        # 웹페이지에서 필요한 정보 크롤링
        dividend_yield = driver.find_element(By.XPATH, XPATH_list[0]).text
        dividend_growth_1y = driver.find_element(By.XPATH, XPATH_list[1]).text
        dividend_growth_3y = driver.find_element(By.XPATH, XPATH_list[2]).text
        dividend_growth_5y = driver.find_element(By.XPATH, XPATH_list[3]).text
        payout_ratio = driver.find_element(By.XPATH, XPATH_list[4]).text

        print(TICKER, dividend_yield, dividend_growth_1y, dividend_growth_3y, dividend_growth_5y, payout_ratio, str(progress_rate) + "%")
        cnt += 1

