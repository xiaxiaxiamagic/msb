import yfinance as yf
import backtrader as bt
import datetime
import csv

# 创建一个马丁策略类
class MartingaleStrategy(bt.Strategy):
    # 定义策略的默认参数
    params = (
        ('rsi_period', 14),
        ('macd_short', 12),
        ('macd_long', 26),
        ('macd_signal', 9),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
        ('initial_cash', 10000),
        ('risk_per_trade', 0.1),
        ('max_loss', 0.1),
        ('max_profit', 5.0),
    )

    def __init__(self):
        # 初始化指标
        self.rsi = bt.indicators.RSI(self.data.close, period=self.p.rsi_period)
        self.macd = bt.indicators.MACD(self.data.close, 
                                       fastperiod=self.p.macd_short, 
                                       slowperiod=self.p.macd_long, 
                                       signalperiod=self.p.macd_signal)
        self.macd_hist = self.macd.histo
        self.trade_log = []

    def next(self):
        self.cash = self.broker.get_cash()  # 更新现金余额
        if self.rsi < self.p.rsi_oversold and self.macd_hist > 0:
            if self.position:
                return
            size = self.calculate_position_size()
            self.buy(size=size)
            self.trade_log.append((self.data.datetime.date(0), 'buy', self.data.close[0], size))
        
        elif self.rsi > self.p.rsi_overbought and self.macd_hist < 0:
            if not self.position:
                return
            self.sell(size=self.position.size)
            self.trade_log.append((self.data.datetime.date(0), 'sell', self.data.close[0], self.position.size))
    
    def calculate_position_size(self):
        risk_amount = self.cash * self.p.risk_per_trade
        size = risk_amount / self.data.close[0]
        return size

    def stop(self):
        # 计算回测最终结果
        print(f"Final Portfolio Value: {self.broker.get_value()}")
        # 保存交易记录到CSV文件
        self.save_trade_log_to_csv()

    def save_trade_log_to_csv(self):
        filename = 'backtest_results.csv'
        with open(filename, mode='a', newline='') as file:  # 改为追加模式
            writer = csv.writer(file)
            if file.tell() == 0:  # 如果文件为空，写入标题
                writer.writerow(['Date', 'Signal', 'Price', 'Size'])
            for log in self.trade_log:
                writer.writerow(log)
        print(f"Trade log saved to {filename}")

def run_backtest():
    # 获取用户输入的参数
    ticker = input("请输入股票代码（例如: AAPL）：")
    start_date = input("请输入回测开始日期（格式: YYYY-MM-DD）：")
    end_date = input("请输入回测结束日期（格式: YYYY-MM-DD）：")
    initial_cash = float(input("请输入初始资金（默认10000）：") or 10000)
    rsi_period = int(input("请输入RSI周期（默认14）：") or 14)
    macd_short = int(input("请输入MACD短期周期（默认12）：") or 12)
    macd_long = int(input("请输入MACD长期周期（默认26）：") or 26)
    macd_signal = int(input("请输入MACD信号线周期（默认9）：") or 9)
    rsi_oversold = int(input("请输入RSI超卖阈值（默认30）：") or 30)
    rsi_overbought = int(input("请输入RSI超买阈值（默认70）：") or 70)
    risk_per_trade = float(input("请输入每次交易风险比例（默认0.1）：") or 0.1)
    max_loss = float(input("请输入最大亏损比例（默认0.1）：") or 0.1)
    max_profit = float(input("请输入最大盈利比例（默认5.0）：") or 5.0)

    # 创建一个Cerebro实例
    cerebro = bt.Cerebro()

    # 设置初始资金
    cerebro.broker.set_cash(initial_cash)

    # 获取历史数据
    data = yf.download(ticker, start=start_date, end=end_date)

    # 检查数据是否成功获取
    if data.empty:
        print("未能成功获取数据，请检查股票代码和日期范围")
        return

    # 确保数据包含所有必要的列：Open, High, Low, Close, Volume, Adj Close
    if 'Adj Close' not in data.columns:
        data['Adj Close'] = data['Close']  # 如果没有 Adj Close 列，使用 Close 列作为 Adj Close

    data = data[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']]

    # 将数据传入Backtrader的PandasData
    data_feed = bt.feeds.PandasData(dataname=data)

    cerebro.adddata(data_feed)
    
    # 添加策略
    cerebro.addstrategy(MartingaleStrategy,
                        rsi_period=rsi_period,
                        macd_short=macd_short,
                        macd_long=macd_long,
                        macd_signal=macd_signal,
                        rsi_oversold=rsi_oversold,
                        rsi_overbought=rsi_overbought,
                        risk_per_trade=risk_per_trade,
                        max_loss=max_loss,
                        max_profit=max_profit)

    # 设置手续费
    cerebro.broker.setcommission(commission=0.001)

    # 启动回测
    cerebro.run()

def main():
    run_backtest()

if __name__ == '__main__':
    main()
