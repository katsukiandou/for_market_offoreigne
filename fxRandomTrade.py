from fx import system_trade

class random_trade(system_trade):

    def profit_calculate(self):
        self.loss_position = 0
        now_position = self.now_position
        price = self.data.close.values
        profit_data = list()
        spread = self.spread

        for i in range(price.shape[0]):
            close = price[i]
            profit_data.append(self.profit)

            if now_position == 0:
                if self.loss_position == 1:
                    order_price = close
                    now_position = -1
                elif self.loss_position == -1:
                    order_price = close
                    now_position = 1
                else:
                    self.loss_position = np.random.randint(-1, 2)

            elif now_position == 1:

                if (close - order_price) >= 0.75:
                    self.profit += close - (order_price + spread)
                    now_position = 0
                elif (close - order_price) <= -0.25:
                    self.profit += close - (order_price + spread)
                    now_position = 0
                    self.loss_position = 1
                else:
                    pass
            elif now_position == -1:

                if order_price - (close + spread) >= 0.75:
                    self.profit += order_price - (close + spread)
                    now_position = 0
                elif order_price - (close + spread) <= -0.25:
                    self.profit += order_price - (close + spread)
                    self.loss_position = -1
                    now_position = 0
                else:
                    pass
        print("利益は{}円です".format(self.profit * 10000))

        return profit_data