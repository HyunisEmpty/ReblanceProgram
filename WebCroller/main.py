import sys
import time
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QProgressBar
)
from PyQt6.QtCore import QThread, pyqtSignal
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import driver_setup
import StockData
import StockDividendData

XPATH_list = [
    '//*[@id="stock-overview"]/div/div[1]/div[3]/div/div/div[2]/div/div/div[4]/p[1]',
    '//*[@id="dividend-growth-history"]/section/table/tbody/tr[2]/td[3]/p',
    '//*[@id="dividend-growth-history"]/section/table/tbody/tr[2]/td[4]/p',
    '//*[@id="dividend-growth-history"]/section/table/tbody/tr[2]/td[5]/p',
    '//*[@id="stock-daily-snapshot"]/div[2]/div/div[1]/div[2]/div[2]'
]

class CrawlerThread(QThread):
    # 크롤링 결과를 문자열 형태로 메인 스레드에 보낼 시그널
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)  # 진행률 신호 (0~100 정수)
    finished_signal = pyqtSignal()

    def run(self):
        driver = driver_setup.get_driver()
        cnt = 1

        # 크롤링 결과 파일 초기화
        with open("TextDirectory/StockDividendData.txt", "w", encoding="utf-8") as f:
            pass

        for TICKER in StockData.stock_ticker_list:
            link = StockData.stock_link_dic[TICKER]
            progress_rate = round((cnt / len(StockData.stock_ticker_list)) * 100, 2)
            progress_int = int(progress_rate)  # QProgressBar는 int 값 필요

            # 진행률 GUI에 전달
            self.progress_signal.emit(progress_int)

            try:
                driver.get(link)

                if cnt == 1:
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, XPATH_list[0]))
                        )
                        self.log_signal.emit("[INFO] 첫 페이지 로딩 완료 확인")
                    except Exception as e:
                        self.log_signal.emit(f"[WARNING] 첫 페이지 로딩 대기 실패: {e}")

                time.sleep(random.uniform(0.5, 1))

                body = driver.find_element(By.TAG_NAME, "body")
                ActionChains(driver).move_to_element_with_offset(
                    body, random.randint(50, 200), random.randint(50, 200)
                ).perform()

                driver.execute_script(f"window.scrollBy(0, {random.randint(200, 400)})")
                time.sleep(random.uniform(0.5, 1))
                driver.execute_script(f"window.scrollBy(0, {random.randint(300, 600)})")
                time.sleep(random.uniform(0.5, 1))

                web_info_list = [0 for _ in range(5)]
                for i in range(5):
                    try:
                        element = driver.find_element(By.XPATH, XPATH_list[i])
                        web_info_list[i] = element.text.strip()
                    except Exception:
                        web_info_list[i] = "N/A"

                web_info_string = " ".join(map(str, web_info_list))

                # 로그 메시지 생성 및 시그널 송신
                log_line = f"{TICKER} {web_info_string} ({progress_rate}%)"
                self.log_signal.emit(log_line)

                # 결과 파일에 기록
                with open("TextDirectory/StockDividendData.txt", "a", encoding="utf-8") as f:
                    f.write(f"{TICKER} {web_info_string}\n")

            except Exception as e:
                self.log_signal.emit(f"[ERROR] {TICKER} 처리 중 오류 발생: {e}")

            cnt += 1

        driver.quit()
        self.finished_signal.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Dividend Crawler")

        # === 메인 레이아웃 (수평 분할) ===
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.body_layout = QHBoxLayout()  # 텍스트창 2개를 가로로 배치할 레이아웃
        self.main_layout.addLayout(self.body_layout)

        # === 왼쪽 레이아웃 ===
        self.left_layout = QVBoxLayout()
        self.start_button = QPushButton("크롤링 시작")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.left_layout.addWidget(self.start_button)
        self.left_layout.addWidget(self.log_text)

        # === 오른쪽 레이아웃 ===
        self.right_layout = QVBoxLayout()
        self.show_top10_button = QPushButton("상위 10개 주식 보기")
        self.top10_text = QTextEdit()
        self.top10_text.setReadOnly(True)

        self.right_layout.addWidget(self.show_top10_button)
        self.right_layout.addWidget(self.top10_text)

        # === 좌우 레이아웃을 body_layout에 추가 ===
        self.body_layout.addLayout(self.left_layout, stretch=2)   # 왼쪽이 넓게
        self.body_layout.addLayout(self.right_layout, stretch=1)  # 오른쪽이 좁게

        # === 진행률 바 ===
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.main_layout.addWidget(self.progress_bar)

        # === 버튼 클릭 이벤트 연결 ===
        self.start_button.clicked.connect(self.start_crawling)
        self.show_top10_button.clicked.connect(self.show_top10_stocks)

        self.crawler_thread = None

    def start_crawling(self):
        self.start_button.setEnabled(False)
        self.log_text.clear()
        self.progress_bar.setValue(0)

        self.crawler_thread = CrawlerThread()
        self.crawler_thread.log_signal.connect(self.append_log)
        self.crawler_thread.progress_signal.connect(self.update_progress)
        self.crawler_thread.finished_signal.connect(self.crawling_finished)
        self.crawler_thread.start()

    def append_log(self, message):
        self.log_text.append(message)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def crawling_finished(self):
        self.append_log("[INFO] 크롤링 완료")
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(100)

    def show_top10_stocks(self):
        self.top10_text.clear()
        self.top10_text.append("[INFO] 상위 10개 배당 성장주입니다.\n")

        top10 = StockDividendData.get_top10_stocks()

        for rank, stock in enumerate(top10, start=1):
            self.top10_text.append(
                f"{rank}. {stock.ticker} | 점수: {stock.total_score} | 순위표준편차: {round(stock.stdev_score, 2)}"
            )
            self.top10_text.append(
                f"    배당 수익률: {stock.dy}% | ({stock.rankings['dy']}위)\n"
                f"    배당증가율(1Y): {stock.dg_1y}% | ({stock.rankings['dg_1y']}위)\n"
                f"    배당증가율(3Y): {stock.dg_3y}% | ({stock.rankings['dg_3y']}위)\n"
                f"    배당증가율(5Y): {stock.dg_5y}% | ({stock.rankings['dg_5y']}위)\n"
                f"    배당성향: {stock.pr}% | ({stock.rankings['pr']}위)\n"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(700, 500)
    window.show()
    sys.exit(app.exec())
