#1.涨停：今日最高价格大于昨日收盘价格9.9%
#2.涨停时间段：选出5分钟K线
import tushare as ts
import pandas as pd
import time
import os
#print(ts.get_hist_data('000001',start='2018-07-13',end='2018-07-13')) #一次性获取全部日k线数据
# stock_info = ts.get_stock_basics('2018-07-13')
# print(stock_info.ix[[0]].index.values[0])
# name = stock_info['name']
# print(name)

# -*- coding:utf-8 -*-
# import pandas as pd
#
# d3 = pd.DataFrame({
#     'a': {'one': 4, 'two': 6, 'three': 6},
#     'b': {'one': 1, 'two': 2, 'three': 1},
#     'c': {'one': 1, 'two': 0, 'three': 6},
# })
# print(d3)
# print(d3.head(2))
# print(d3.tail(1))
# print(d3.index)
# print(d3.columns)
# print(d3.values)
# print(d3.T)
# print(d3.sort_values(by='c'))
# print(d3.a)
# print("d3[1:3]====")
# print(d3[1:3])
# print(d3.loc['one'])
# print(d3.loc[['one'], ['a', 'b']])
# print(d3.loc[['one', 'two'], ['a', 'b']])
# print(d3.iloc[1:2,1:2])
# print(d3.iloc[1:2])
# print(d3.iloc[[0, 2], [1]])


stockCodeList = []#股票代码
stockNameList = []#股票名称
limitUpDateT = []#T日涨停日期
limitUpTimeT = []#T日涨停时间段 4个时间段 0，1，2，3
limitUpVolume = []#T日涨停成交量和(T-1)20日平均成交量1.5  1.5-3  3
limitUpK60 = []#T日涨停与60日均线对比 -0.2 -0.2~-0.05 -0.05~0.1 0.1
limitUpPriceT = []#T日涨停价格
peT = []#T日市盈率
limitUpOpenT1 = []#T1开盘价格
peT1 = []#T1日市盈率
openT2 = []#T2开盘价
closeT2 = []#T2收盘价
yieldRateOpenOpenT2 = []#T2开盘-T1开盘，收益率
yieldRateCloseOpenT2 = []#T2收盘-T1开盘，收益率
peT2 = []
openT3 = []
closeT3 = []
yieldRateOpenOpenT3 = []
yieldRateCloseOpenT3 = []
peT3 = []
openT4 = []
closeT4 = []
yieldRateOpenOpenT4 = []
yieldRateCloseOpenT4 = []
peT4 = []
openT5 = []
closeT5 = []
yieldRateOpenOpenT5 = []
yieldRateCloseOpenT5 = []
peT5 = []
openT6 = []
closeT6 = []
yieldRateOpenOpenT6 = []
yieldRateCloseOpenT6 = []
peT6 = []


# aaa = ts.get_hist_data(code = '000001', start= "2018-07-16", end= "2018-07-16")
# print(aaa)


# stock_info = ts.get_stock_basics('2018-07-13')
# #print(stock_info)
#
# stockLen = len(stock_info)
# stockCodes = stock_info.index.tolist()
# stockCount = 1
#
# code = stockCodes[0]
# result = ts.get_hist_data(code=code, start="2018-07-13", end="2018-07-13")
#
# while stockCount < 10:
#     code = stockCodes[stockCount]
#     result = result.append(ts.get_hist_data(code=code, start="2018-07-13", end="2018-07-13"), ignore_index=True)
#     stockCount = stockCount + 1

basepath = '/Users/chenjian/Desktop/excel'


today = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400*1))
nextDay = time.strftime("%Y-%m-%d", time.localtime(time.time()))

cal_dates = ts.trade_cal()
status = cal_dates[cal_dates['calendarDate'] == today]['isOpen'].values[0]
if status == 0:
    print("==========非交易日=============")

#allFunds = ts.get_today_all()

stock_info = ts.get_stock_basics(today)

stockLen = len(stock_info)

stockCodes = stock_info.index.tolist()
stockCodeNames = stock_info['name'].tolist()

stockCount = 0
#返回一个dataframe，后面append
# code = stockCodes[0]
# result = ts.get_hist_data(code=code, start=today, end=today)
result = pd.DataFrame()
start = 1
while stockCount < stockLen:
    code = stockCodes[stockCount]
    # code = '600158'
    print(code+"=========")
    codeName = stockCodeNames[stockCount]
    preTradeDay = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400 * start*2))
    while not cal_dates[cal_dates['calendarDate'] == preTradeDay]['isOpen'].values[0]:
        start = start + 2
        preTradeDay = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400 * start * 2))

    dataToday = ts.get_hist_data(code=code, start=today, end=today)
    dataPreToday = ts.get_hist_data(code=code, start=preTradeDay, end=preTradeDay)
    if dataToday is None or len(dataToday) == 0 or dataPreToday is None or len(dataPreToday) == 0:
        stockCount = stockCount + 1
        continue
    todayHigh = dataToday['high'].tolist()[0]
    preTodayHigh = dataPreToday['close'].tolist()[0]

    if preTodayHigh != 0 and todayHigh >= (1 + 0.099)*preTodayHigh:
        dataToday['code'] = code
        dataToday['codeName'] = codeName
        result = result.append(dataToday, ignore_index=True)
        break

    stockCount = stockCount + 1
    print("===========")
    print(stockCount)



#result = allFunds[(allFunds['high'] >= allFunds['settlement'] * 1.099) & (allFunds['settlement'] > 0)]
#选出当日涨停股票
#print(result.loc[:, ['code', 'name', 'open', 'high', 'low', 'settlement']])
print("result==========================================================")
print(len(result))

#选出当日涨停股票，取出当日5min的K线，计算涨停时间段
print("5min的K线数据=====================================================")
codeRow = result.iloc[:,13:14]
highRow = result.iloc[:, 1:2]
codeNameRow = result.iloc[:, 14:15]

size = len(codeRow)
count = 0

while count < size:
    highP = highRow.values.tolist()[count][0]
    codeInExcel = codeRow.values.tolist()[count][0]
    name = codeNameRow.values.tolist()[count][0]

    #首次大于等于high的时间段
    minK = ts.get_hist_data(codeInExcel, ktype='5', start=today, end=nextDay).loc[:, ['high']]
    highPList = minK.loc[minK['high'] >= highP]
    print(highPList)
    #获取正序第一个涨停的价格
    minR = highPList.sort_index(ascending=True)

    #数据装入
    limitUpTimeT.append(minR.iloc[0:1, 0:1].index[0])
    stockCodeList.append(codeInExcel)
    stockNameList.append(name)
    limitUpDateT.append(today)
    limitUpPriceT.append(minR.iloc[0:1, 0:1].values[0][0])

    count = count + 1

#生成涨停当日excel
df = pd.DataFrame({'股票代码': stockCodeList,
                   '股票名称': stockNameList,
                   'T涨停日期': limitUpDateT,
                   'T涨停时间段': limitUpTimeT,
                   'T涨停价格': limitUpPriceT,
                   'T1开盘价格': [0],
                   'T2开盘价格': [0],
                   'T2收盘价格': [0],
                   'T2收益率（收-开）': [0],
                   'T2收益率（开-开）': [0],
                   'T3开盘价格': [0],
                   'T3收盘价格': [0],
                   'T3收益率（收-开）': [0],
                   'T3收益率（开-开）': [0],
                   'T4开盘价格': [0],
                   'T4收盘价格': [0],
                   'T4收益率（收-开）': [0],
                   'T4收益率（开-开）': [0],
                   'T5开盘价格': [0],
                   'T5收盘价格': [0],
                   'T5收益率（收-开）': [0],
                   'T5收益率（开-开）': [0],
                   'T6开盘价格': [0],
                   'T6收盘价格': [0],
                   'T6收益率（收-开）': [0],
                   'T6收益率（开-开）': [0],
                   })
cols=['股票代码', '股票名称', 'T涨停日期', 'T涨停时间段', 'T涨停价格','T1开盘价格','T2开盘价格',
      'T2收盘价格', 'T2收益率（收-开）', 'T2收益率（开-开）', 'T3开盘价格',
      'T3收盘价格', 'T3收益率（收-开）', 'T3收益率（开-开）', 'T4开盘价格',
      'T4收盘价格', 'T4收益率（收-开）', 'T4收益率（开-开）', 'T5开盘价格',
      'T5收盘价格', 'T5收益率（收-开）', 'T5收益率（开-开）', 'T6开盘价格',
      'T6收盘价格', 'T6收益率（收-开）', 'T6收益率（开-开）']
df=df.ix[:, cols]
df.to_excel( basepath + "/" + today + ".xlsx" , sheet_name="sheet1")

#读已存在的excel,增加数据
preDayCount = 6
execlDay = []
start = 1
dayIndex = 1
while start <= preDayCount:
    preDay = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400*dayIndex))
    status = cal_dates[cal_dates['calendarDate'] == preDay]['isOpen'].values[0]
    dayIndex = dayIndex + 1
    if status == 1:
        execlDay.append(preDay)
        start = start + 1

for index, day in enumerate(execlDay):
    path = basepath + "/" + day + ".xlsx"
    if os.path.exists(path):
        frame = pd.read_excel(path, sheetname="sheet1")
        codeList = frame['股票代码'].tolist()
        openTPrice = frame['T1开盘价格']
        for codeInExcel in codeList:
            selectRow = result[result['code'] == str(codeInExcel)]
            if selectRow is None or len(selectRow) == 0:
                continue
            if index == 0:
                limitUpOpenT1.append(selectRow['open'].tolist()[0])
            if index == 1:
                openT2.append(selectRow['open'].tolist()[0])  # T2开盘价
                closeT2.append(selectRow['close'].tolist()[0])  # T2收盘价
                yieldRateOpenOpenT2.append((selectRow['open'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2开盘-T1开盘，收益率
                yieldRateCloseOpenT2.append((selectRow['close'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2收盘-T1开盘，收益率
            if index == 2:
                openT3.append(selectRow['open'].tolist()[0])  # T2开盘价
                closeT3.append(selectRow['close'].tolist()[0])  # T2收盘价
                yieldRateOpenOpenT3.append((selectRow['open'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2开盘-T1开盘，收益率
                yieldRateCloseOpenT3.append((selectRow['close'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2收盘-T1开盘，收益率
            if index == 3:
                openT4.append(selectRow['open'].tolist()[0])  # T2开盘价
                closeT4.append(selectRow['close'].tolist()[0])  # T2收盘价
                yieldRateOpenOpenT4.append((selectRow['open'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2开盘-T1开盘，收益率
                yieldRateCloseOpenT4.append((selectRow['close'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2收盘-T1开盘，收益率
            if index == 4:
                openT5.append(selectRow['open'].tolist()[0])  # T2开盘价
                closeT5.append(selectRow['close'].tolist()[0])  # T2收盘价
                yieldRateOpenOpenT5.append((selectRow['open'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2开盘-T1开盘，收益率
                yieldRateCloseOpenT5.append((selectRow['close'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2收盘-T1开盘，收益率
            if index == 5:
                openT6.append(selectRow['open'].tolist()[0])  # T2开盘价
                closeT6.append(selectRow['close'].tolist()[0])  # T2收盘价
                yieldRateOpenOpenT6.append((selectRow['open'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2开盘-T1开盘，收益率
                yieldRateCloseOpenT6.append((selectRow['close'].tolist()[0] - openTPrice)/selectRow['open'].tolist()[0])  # T2收盘-T1开盘，收益率

        if index == 0 and len(limitUpOpenT1) != 0:
            frame['T1开盘价格'] = limitUpOpenT1
        if index == 1 and len(openT2) != 0:
            frame['T2开盘价格'] = openT2
            frame['T2收盘价格'] = closeT2
            frame['T2收益率（收-开）'] = yieldRateCloseOpenT2
            frame['T2收益率（开-开）'] = yieldRateOpenOpenT2
        if index == 2:
            frame['T3开盘价格'] = openT3
            frame['T3收盘价格'] = closeT3
            frame['T3收益率（收-开）'] = yieldRateCloseOpenT3
            frame['T3收益率（开-开）'] = yieldRateOpenOpenT3
        if index == 3:
            frame['T4开盘价格'] = openT4
            frame['T4收盘价格'] = closeT4
            frame['T4收益率（收-开）'] = yieldRateCloseOpenT4
            frame['T4收益率（开-开）'] = yieldRateOpenOpenT4
        if index == 4:
            frame['T5开盘价格'] = openT5
            frame['T5收盘价格'] = closeT5
            frame['T5收益率（收-开）'] = yieldRateCloseOpenT5
            frame['T5收益率（开-开）'] = yieldRateOpenOpenT5
        if index == 5:
            frame['T6开盘价格'] = openT6
            frame['T6收盘价格'] = closeT6
            frame['T6收益率（收-开）'] = yieldRateCloseOpenT6
            frame['T6收益率（开-开）'] = yieldRateOpenOpenT6

        frame.to_excel(path, sheet_name="sheet1")