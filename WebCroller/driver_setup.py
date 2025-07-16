# driver_setup.py

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

import undetected_chromedriver as uc

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )

    driver = uc.Chrome(options=options, use_subprocess=True)
    return driver
