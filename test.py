import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

# 马丁策略
class MartingaleStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('macd_short', 12),
        ('macd_long', 26),
        ('macd_signal', 9),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
        ('initial_cash', 10000),  # 初始资金
        ('risk_per_trade', 0.1),  # 每次交易的风险比例
        ('max_loss', 0.1),  # 最大亏损限制（10%）
        ('max_profit', 5.0),  # 最大利润限制（500%）
    )

    def __init__(self):
        # RSI和MACD指标
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.macd = bt.indicators.MACD(self.data.close, 
                                       fastperiod=self.params.macd_short,
                                       slowperiod=self.params.macd_long,
                                       signalperiod=self.params.macd_signal)
        self.candle_count = 0  # 用于记录已开仓的次数，控制马丁策略
        self.initial_balance = self.broker.get_cash()  # 初始余额
        self.max_balance = self.initial_balance * (1 + self.params.max_profit)  # 最大可接受的利润
        self.min_balance = self.initial_balance * (1 - self.params.max_loss)  # 最大可接受的亏损

    def next(self):
        # 获取当前的资金状况
        current_balance = self.broker.get_cash()

        # 如果达到最大亏损限制，停止交易
        if current_balance <= self.min_balance:
            print(f"最大亏损限制已触发，当前余额：{current_balance}")
            self.close()
            return

        # 如果达到最大盈利限制，停止交易
        if current_balance >= self.max_balance:
            print(f"最大盈利限制已触发，当前余额：{current_balance}")
            self.close()
            return

        # 交易信号：MACD金叉和RSI超卖
        if self.macd.macd > self.macd.signal and self.rsi < self.params.rsi_oversold:
            size = self.calculate_order_size()
            self.buy(size=size)
            self.candle_count += 1
            print(f"买入：{self.data.datetime.datetime()}, 当前仓位：{size}, 当前余额：{current_balance}")

        # 交易信号：MACD死叉和RSI超买
        elif self.macd.macd < self.macd.signal and self.rsi > self.params.rsi_overbought:
            size = self.calculate_order_size()
            self.sell(size=size)
            self.candle_count += 1
            print(f"卖出：{self.data.datetime.datetime()}, 当前仓位：{size}, 当前余额：{current_balance}")

    def calculate_order_size(self):
        """根据马丁策略计算每次交易的仓位"""
        available_cash = self.broker.get_cash()
        risk_amount = available_cash * self.params.risk_per_trade
        order_size = risk_amount / self.data.close[0]  # 假设每股价格就是当前的收盘价
        return order_size

# 主函数：执行回测
if __name__ == '__main__':
    stock_code = input("请输入股票代码: ").strip().upper()  # 输入股票代码
    
    # 下载数据
    data = bt.feeds.YahooFinanceData(dataname=stock_code, fromdate="2018-01-01", todate="2025-01-01")

    # 创建回测引擎
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(MartingaleStrategy)
    cerebro.broker.set_cash(10000)  # 初始资金
    cerebro.broker.set_commission(commission=0.001)  # 设置手续费

    # 执行回测
    print("开始回测...")
    cerebro.run()

    # 可视化结果
    cerebro.plot(style='candlestick')

    # 打印回测结束时的余额
    print(f"回测结束时的账户余额: {cerebro.broker.get_value():.2f}")
