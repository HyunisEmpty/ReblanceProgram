# StockdData.txt 에서 티커, 주소를 받아와 딕셔너리에 저장
stock_link_dic = dict()
stock_ticker_list = []      # 티커별 주소를 저장하는 딕셔너리
stock_rank_dic = dict()         # 티커별 점수를 저장하는 딕셔너리
with open("StockData.txt", 'r') as f:
    for line in f:
        TICKER, link = line.split()
        stock_ticker_list.append(TICKER)    # 티커 저장
        stock_link_dic[TICKER] = link       # 티커, 주소 저장
        stock_rank_dic[TICKER] = [["dividend_yield", "dividend_growth_1y", "dividend_growth_3y", "dividend_growth_5y", "payout_ratio"]]

