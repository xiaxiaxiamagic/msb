import yfinance as yf
import backtrader as bt
import datetime
import csv
import pandas as pd
import time
from alpha_vantage.timeseries import TimeSeries

# 替换为你自己的API密钥
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

# 获取Alpha Vantage数据
def fetch_data(ticker, start_date, end_date):
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    
    try:
        # 获取数据
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
        # 过滤数据范围
        data = data[(data.index >= start_date) & (data.index <= end_date)]
        if data.empty:
            print(f"未能成功获取数据: {ticker}")
            return None
        # 确保数据包含必要的列
        data['Adj Close'] = data['4. close']
        data = data[['1. open', '2. high', '3. low', '4. close', '5. volume', 'Adj Close']]
        return data
    except Exception as e:
        print(f"下载数据失败: {e}")
        return None

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

        # 修改MACD的参数名
        self.macd = bt.indicators.MACD(self.data.close,
                                       period_me1=self.p.macd_short,
                                       period_me2=self.p.macd_long,
                                       period_signal=self.p.macd_signal)
        self.macd_hist = self.macd.lines.macd - self.macd.lines.signal  # 计算MACD柱状图
        self.trade_log = []

    def next(self):
        # 打印调试信息，检查RSI和MACD的值
        print(f"Date: {self.data.datetime.date(0)}, RSI: {self.rsi[0]}, MACD: {self.macd.lines.macd[0]}, Signal: {self.macd.lines.signal[0]}")

        self.cash = self.broker.get_cash()  # 更新现金余额

        # 交易信号条件
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
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
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
    data = fetch_data(ticker, start_date, end_date)

    if data is None or data.empty:
        print("未能成功获取数据，请检查股票代码和日期范围")
        return

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
