import StockDividendData
import numpy as np

# 정렬 시킨 정보와 티커만 남기고 다른 요소들 제거
def RemakeList(dx_list, dx_index):

    for i in range(len(dx_list)):
        # dx_list[i] = [티커, 정렬의 기준이 되는 값]
        dx_list[i] = [dx_list[i][0], dx_list[i][dx_index]]

    return dx_list

score_dic = dict()
score_list = []

dividend_yield_list = sorted(StockDividendData.stock_dividend_data_list, key=lambda x: x[1], reverse=True)          # 배당 수익률 오름 차순 정렬
dividend_growth_1y_list = sorted(StockDividendData.stock_dividend_data_list, key=lambda x: x[2], reverse=True)      # 배당 성장률 1Y 오름 차순 정렬
dividend_growth_3y_list = sorted(StockDividendData.stock_dividend_data_list, key=lambda x: x[3], reverse=True)      # 배당 성장률 3Y 오름 차순 정렬
dividend_growth_5y_list = sorted(StockDividendData.stock_dividend_data_list, key=lambda x: x[4], reverse=True)      # 배당 성장률 5Y 오름 차순 정렬
payout_ratio_list = sorted(StockDividendData.stock_dividend_data_list, key=lambda x: x[5], reverse=False)           # 배당 성향 오름 차순 정렬

dividend_list = [dividend_yield_list, dividend_growth_1y_list, dividend_growth_3y_list, dividend_growth_5y_list, payout_ratio_list]
for i in range(len(dividend_list)):
     dividend_list[i] = RemakeList(dividend_list[i], i + 1)     # 정렬된 정보만 남기고 다른 정보 제거

# 항목별 1등 출력
# for i in range(len(dividend_yield_list)):
#     print(dividend_list[0][i], dividend_list[1][i], dividend_list[2][i], dividend_list[3][i], dividend_list[4][i])

# 각 순위 리스트에서 받아와 score_dic에 점수를 부여한다.
for i in range(len(dividend_list)):
    now_list = dividend_list[i]

    rank = 1
    for TICKER, val in now_list:
        if i == 0:  # 딕셔너리에 처음 티커가 들어가는 경우
            score_dic[TICKER] = [rank]
        else:
            score_dic[TICKER].append(rank)
        rank += 1

# 종합 점수 계산
for key in score_dic.keys():

    score_sum = sum(score_dic[key])
    score_std = float(round(np.std(score_dic[key])/2, 2))
    calibration_score = round(float(score_sum + score_std), 2)
    score_dic[key] = [score_sum, score_std, calibration_score]
    score_list.append([key, calibration_score])

score_list = sorted(score_list, key=lambda x: x[1], reverse=False)
cnt = 1
for info in score_list:
    print(cnt, info)
    cnt += 1



