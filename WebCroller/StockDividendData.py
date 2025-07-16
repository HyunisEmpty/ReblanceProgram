import statistics


class Stock:

    def __init__(self, ticker, dy, dg_1y, dg_3y, dg_5y, pr):
        # 해당 주식 티커
        self.ticker = ticker

        # 배당 관련 정보들
        self.dy = dy
        self.dg_1y = dg_1y
        self.dg_3y = dg_3y
        self.dg_5y = dg_5y
        self.pr = pr

        # 각 항목별 순위 저장
        self.rankings = {
            'dy': 0, 'dg_1y': 0, 'dg_3y': 0, 'dg_5y': 0, 'pr': 0
        }

        self.stdev_score = 0.0
        self.total_score = 0.0

    def get_value(self, key: str) -> int:
        return getattr(self, key)

    def set_ranking(self, key: str, rank: int) -> None:
        self.rankings[key] = rank

    def compute_score(self) -> None:
        scores = list(self.rankings.values())
        self.stdev_score = statistics.stdev(scores) / 2
        self.total_score = round(sum(scores) + self.stdev_score, 2)


# 배당 수익률과 성장률의 N/A값을 적절한 값으로 변환하는 함수
def na_change(data: str) -> float:
    return float(0) if data == "N/A" else float(data.replace('%', ''))


# 배당 성향의 N/A값을 적절한 값으로 변환하는 함수
def na_change2(data: str) -> float:
    return float(999) if data == "N/A" else float(data.replace('%', ''))


def assign_ranking(stocks: list[Stock], key: str, reverse: bool) -> None:
    # 키를 기준으로 stock객체를 flag에 따라서 정렬
    sorted_stocks = sorted(stocks, key=lambda s: s.get_value(key), reverse=reverse)

    # 주식별 순위 설정
    for rank, stock in enumerate(sorted_stocks, start=1):
        stock.set_ranking(key, rank)


# 상위 10개 주식 반환
def get_top10_stocks() -> list:
    stock_list = []

    # 파일에 저장된 모든 주식 정보 Stock 객체로 변환
    with open("TextDirectory/StockDividendData.txt", 'r') as f:
        for line in f:
            # 각 라인 별 데이터 분활
            datas = list(map(str, line.split()))
            ticker = datas[0]
            dy, dg_1y, dg_3y, dg_5y = map(na_change, datas[1:5])
            pr = na_change2(datas[5])

            stock = Stock(ticker, dy, dg_1y, dg_3y, dg_5y, pr)
            stock_list.append(stock)

    # 순위 계산
    assign_ranking(stock_list, 'dy', reverse=True)
    assign_ranking(stock_list, 'dg_1y', reverse=True)
    assign_ranking(stock_list, 'dg_3y', reverse=True)
    assign_ranking(stock_list, 'dg_5y', reverse=True)
    assign_ranking(stock_list, 'pr', reverse=False)

    for stock in stock_list:
        stock.compute_score()

    sorted_by_score = sorted(stock_list, key=lambda s: s.total_score)

    # 출력 예시
    for rank, stock in enumerate(sorted_by_score[:10], start=1):
        print(f"{rank}. {stock.ticker} | Score: {stock.total_score} | Stdev: {stock.stdev_score}")
        print(f"  dy: {stock.dy}, dg_1y: {stock.dg_1y}, dg_3y: {stock.dg_3y}, dg_5y: {stock.dg_5y}, pr: {stock.pr}")
        print(f"  Rank: {stock.rankings}\n")

    return sorted_by_score[:10]

get_top10_stocks()

