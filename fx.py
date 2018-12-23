import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class system_trade():

    def __init__(self):
        self.profit = 0
        self.position = 0
        self.now_position = 0
        self.order_num = 100 ^ 3
        self.spread = 0.01
        self.trade_num = 0

    def reset_profit(self):
        self.profit = 0

    def set_data(self, data):
        self.data = pd.read_csv(data)

    def anaryze_data(self):
        dataframe = self.data
        pl_dm = talib.MINUS_DM(dataframe.high, dataframe.low, timeperiod=7)
        mi_dm = talib.PLUS_DM(dataframe.high, dataframe.low, timeperiod=7)
        dataframe["dmi_sig"] = (pl_dm - mi_dm) >= 0

        macd, macdsignal, macdhist = talib.MACD(dataframe.close, fastperiod=9, slowperiod=26, signalperiod=9)
        dataframe["macd"] = (macd - macdsignal) >= 0

        sma5 = talib.SMA(dataframe.close, timeperiod=45)
        sma15 = talib.SMA(dataframe.close, timeperiod=75)
        dataframe["sma_sig"] = (dataframe.close - sma15) >= 0

        dataframe.dropna()

    def check_tech(self):
        check_tech = []
        tech = self.data[["dmi_sig", "sma_sig", "macd"]].values
        for i in range(len(tech)):
            check_tech.append(tech[i].sum())
        return check_tech

    def profit_calculate(self):
        price = self.data.close.values
        techs = self.check_tech()
        now_position = self.now_position
        spread = self.spread
        profit_data = []

        for i in range(price.shape[0]):
            close = price[i]  # 現在の値段
            tech = techs[i]  # 現在のテクニカル指標
            profit_data.append(self.profit)

            # ポジションがない時
            if now_position == 0:
                # 買い注文
                if tech == 3:
                    order_price = close
                    now_position = 1
                    self.trade_num += 1
                # 売り注文
                elif tech == 0:
                    order_price = close
                    now_position = -1
                    self.trade_num += 1
                # 見送り~
                else:
                    pass

            # 買いポジションの時
            elif now_position == 1:  # 買い
                # シグナル転換
                if tech == 0:
                    self.profit += close - (order_price + spread)
                    now_position = 0
                # 損切り
                elif (close - order_price) <= -0.25:
                    self.profit += close - (order_price + spread)
                    now_position = 0

                # 利確
                elif (close - order_price) >= 0.5:
                    self.profit += close - (order_price + spread)
                    now_position = 0
                # 見送り
                else:
                    pass

            # 売りポジションの時
            elif now_position == -1:
                # シグナル転換
                if tech == 3:
                    self.profit += order_price - (close + spread)
                    now_position = 0
                # 損切り
                elif order_price - (close + spread) <= -0.25:
                    self.profit += order_price - (close + spread)
                    now_position = 0
                # 利確
                elif order_price - (close + spread) >= 0.5:
                    self.profit += order_price - (close + spread)
                    now_position = 0
                # 見送り
                else:
                    pass

        print("取引回数は%d回でした" % self.trade_num)
        print("利益は{}でした".format(self.profit * 10000))

        return profit_data