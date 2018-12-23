from fx import system_trade

class system_trade_200sma(system_trade):

    def analyze_data(self):
        dataframe = self.data
        dataframe["sma200"] = dataframe.close / talib.SMA(dataframe.close, timeperiod=200) > 0
        dataframe.dropna()

    def check_tech(self):
        check_tech = []
        tech = self.data["sma200"].values
        return tech

    def profit_calculate(self):

        self.analyze_data()

        price = self.data.close.values
        techs = self.check_tech()
        now_position = self.now_position
        spread = self.spread
        profit_data = []

        for i in range(price.shape[0]):
            close = price[i]
            tech = techs[i]
            profit_data.append(self.profit)

            if now_position == 0:
                if tech == 1:
                    order_price = close
                    now_position = 1
                elif tech == 0:
                    order_price = close
                    now_position = -1
                else:
                    pass
            elif now_position == 1:
                if tech == 0:
                    self.profit += close - (order_price + spread)
                    now_position = 0
                elif (close - order_price) >= 1.0:
                    self.profit += close - (order_price + spread)
                    now_position = 0
                else:
                    pass
            elif now_position == -1:
                if tech == 1:
                    self.profit += order_price - (close + spread)
                    now_position = 0
                elif order_price - (close + spread) >= 1.0:
                    self.profit += order_price - (close + spread)
                    now_position = 0
                else:
                    pass
        print("取引回数は%d回でした" % self.trade_num)

        print("利益は{}でした".format(self.profit * 100000))

        return profit_data