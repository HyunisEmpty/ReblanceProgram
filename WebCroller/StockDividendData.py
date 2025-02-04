# StockdData.txt 에서 티커, 주소를 받아와 딕셔너리에 저장

def InputChange(data):

    if data == "N/A":
        data = 999
    else:
        data = data.replace('%', '')

    return float(data)



stock_dividend_data_list = []
with open("StockDividendData.txt", 'r') as f:
    for line in f:
        # 티커, 배당 수익률, 배당 성장률 1Y, 배당 성장률 3Y, 배당 성장률 5Y, 배당 성향을 StockDividendData.txt에서 받아온다
        TICKER, dividend_yield, dividend_growth_1y, dividend_growth_3y, dividend_growth_5y, payout_ratio, progress_info = map(str, line.split())
        dividend_yield = InputChange(dividend_yield)
        dividend_growth_1y = InputChange(dividend_growth_1y)
        dividend_growth_3y = InputChange(dividend_growth_3y)
        dividend_growth_5y = InputChange(dividend_growth_5y)
        payout_ratio = InputChange(payout_ratio)
        stock_dividend_data_list.append([TICKER, dividend_yield, dividend_growth_1y, dividend_growth_3y, dividend_growth_5y, payout_ratio])
