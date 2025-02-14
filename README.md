---

# 马丁策略回测工具

这是一个基于 **Backtrader** 框架的马丁策略回测工具，结合了 **MACD** 和 **RSI** 指标来进行模拟交易。该工具允许你指定初始本金、交易标的（如股票代码）以及回测的时间段，并提供最大亏损和最大盈利控制。回测结束后，工具会导出交易数据，并允许你将其转换为 TradingView 的 Pine Script 格式进行可视化。

## 功能特性

- **马丁策略**：根据 MACD 和 RSI 指标进行买入和卖出决策。
- **自定义初始本金**：可以在命令行中设置初始本金。
- **最大亏损和最大盈利控制**：回测过程中，设置最大亏损（10%）和最大盈利（500%）的控制条件。
- **回测结果导出**：回测结束后，导出 CSV 格式的交易数据，便于后续分析。
- **可视化支持**：可将导出的交易数据转换为 TradingView 的 Pine Script 格式进行图表展示。

## 安装依赖

首先，你需要安装所需的 Python 包：

```bash
pip install backtrader yfinance matplotlib
```

## 使用方法

### 1. 运行回测

在命令行中运行 `backtest.py` 脚本，按照提示输入相应的参数。

```bash
python backtest.py
```

运行时，系统会要求你依次输入：

- **股票代码**：例如输入 `AAPL` 或其他支持的股票代码。
- **回测起始日期**：格式为 `YYYY-MM-DD`，例如 `2021-01-01`。
- **回测结束日期**：格式为 `YYYY-MM-DD`，例如 `2021-12-31`。
- **初始本金**：例如输入 `10000`（回测开始时的账户余额）。

### 2. 查看回测结果

回测完成后，系统会输出账户余额，表示回测结束时的资金状况。交易数据会被导出为 `backtest_results.csv` 文件，包含每笔交易的详细信息，包括买入/卖出信号、交易价格和仓位大小。

### 3. 转换为 Pine Script 格式

回测数据会导出为 CSV 文件，格式如下：

```csv
date,signal,cash,price,size
2021-01-01 00:00:00,buy,10000,150,66.67
2021-02-01 00:00:00,sell,10500,160,65.62
2021-03-01 00:00:00,buy,10550,170,62.06
...
```

将 CSV 数据手动转换为 Pine Script 数组，并加载到 **TradingView** 中，以便在图表上展示买入/卖出信号。

#### Pine Script 示例

```pinescript
//@version=5
indicator("回测结果显示", overlay=true)

// 假设这些数据来自你的回测结果 CSV 文件（手动填充）
var float[] dates = array.new_float()
var float[] signals = array.new_float()
var float[] prices = array.new_float()
var float[] sizes = array.new_float()

// 手动填充数据
array.push(dates, timestamp("2021-01-01 00:00:00"))
array.push(signals, 1)  // 1表示买入
array.push(prices, 150)
array.push(sizes, 66.67)

array.push(dates, timestamp("2021-02-01 00:00:00"))
array.push(signals, -1)  // -1表示卖出
array.push(prices, 160)
array.push(sizes, 65.62)

array.push(dates, timestamp("2021-03-01 00:00:00"))
array.push(signals, 1)  // 1表示买入
array.push(prices, 170)
array.push(sizes, 62.06)

// 显示买卖信号
for i = 0 to array.size(dates) - 1
    date = array.get(dates, i)
    signal = array.get(signals, i)
    price = array.get(prices, i)

    if signal == 1
        label.new(bar_index, price, "Buy", style=label.style_label_up, color=color.green, textcolor=color.white)
    if signal == -1
        label.new(bar_index, price, "Sell", style=label.style_label_down, color=color.red, textcolor=color.white)
```

将回测导出的 CSV 数据手动填入 Pine Script 中，并在 TradingView 上查看交易信号。

## 参数说明

在回测过程中，你可以使用以下参数来调整策略行为：

- **rsi_period**：RSI 指标的周期（默认：14）
- **macd_short**：MACD 快速线的周期（默认：12）
- **macd_long**：MACD 慢速线的周期（默认：26）
- **macd_signal**：MACD 信号线的周期（默认：9）
- **rsi_overbought**：RSI 超买阈值（默认：70）
- **rsi_oversold**：RSI 超卖阈值（默认：30）
- **initial_cash**：回测时的初始本金（默认为 10000）
- **risk_per_trade**：每笔交易的风险比例（默认：0.1，即 10%）
- **max_loss**：最大亏损比例（默认：0.1，即 10%）
- **max_profit**：最大盈利比例（默认：5.0，即 500%）

### 示例：

```python
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
```

## 依赖项

- **Backtrader**：一个用于量化交易的 Python 库，支持策略回测、实盘交易等功能。
- **yfinance**：一个可以方便地获取历史股市数据的 Python 库。
- **matplotlib**：用于生成可视化图表，帮助分析回测结果。

## 贡献

欢迎提交问题报告或功能请求。若有任何问题或建议，请打开 [issues](https://github.com/yourusername/yourrepository/issues) 或提交 Pull Request。

## License

MIT License

---
