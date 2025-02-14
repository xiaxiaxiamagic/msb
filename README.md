---

# 马丁策略回测工具（MACD + RSI）

本项目实现了一个基于 **马丁交易策略** 的回测工具，结合了 **MACD** 和 **RSI** 指标进行模拟交易。该工具使用 **Backtrader** 库进行回测，支持使用 **Yahoo Finance** 数据进行不同股票代码的回测，并且支持定义回测的时间段。回测结果可以通过 **TradingView** 的 Pine Script 进行可视化展示。

## 功能特性

- **马丁策略**：该策略在每次亏损时加倍仓位，以期通过一次盈利弥补之前的损失。
- **MACD 和 RSI 指标**：通过 **MACD** 和 **RSI** 指标判断买入和卖出信号。
- **风险管理**：可以设置最大亏损和最大盈利限制，防止资金大幅亏损。
- **CSV 导出**：回测过程中的每一笔交易（买卖信号、价格、仓位大小等）都会记录并导出为 CSV 文件。
- **自定义参数**：通过命令行输入股票代码、回测起止日期、初始资金等，支持高度自定义的回测设置。
- **Pine Script 生成**：回测结果会自动转换为 Pine Script 格式，用于在 **TradingView** 上进行可视化展示。

## 安装依赖

在开始之前，请确保安装了以下依赖库：

- Python 3.x
- `backtrader` - 一款强大的回测库
- `yfinance` - 一个从 Yahoo Finance 获取股票历史数据的库
- `matplotlib` - 用于绘制回测数据图表的库

可以通过以下命令安装这些库：

```bash
pip install backtrader yfinance matplotlib
```

## 使用方法

### 步骤 1：克隆或下载项目

你可以通过 Git 克隆该项目到本地：

```bash
git clone https://github.com/your-username/martingale-backtest.git
```

或者直接下载 Python 脚本（`martingale_backtest.py` 和 `csv_to_pinescript.py`）。

### 步骤 2：运行回测脚本

1. 进入项目目录。

2. 运行回测脚本：

```bash
python martingale_backtest.py
```

3. 脚本会提示你输入以下参数：
   - **股票代码**：你想要回测的股票代码（例如：`AAPL`、`GOOG`）。
   - **回测开始日期**：回测的开始日期，格式为 `YYYY-MM-DD`（例如：`2020-01-01`）。
   - **回测结束日期**：回测的结束日期，格式为 `YYYY-MM-DD`（例如：`2021-01-01`）。
   - **初始本金**：回测时的初始资金（例如：`10000`）。

### 步骤 3：查看回测结果

回测完成后，脚本会输出最终的账户余额，表示回测结束时的资金情况。

- 同时，回测数据会被保存为 CSV 文件（`backtest_results.csv`），其中包含每一笔交易的详细信息，包括买入/卖出信号、价格和仓位大小。

  示例 `backtest_results.csv` 文件内容：

  ```csv
  date,signal,cash,price,size
  2021-01-01 00:00:00,buy,10000,150,66.67
  2021-02-01 00:00:00,sell,10500,160,65.62
  2021-03-01 00:00:00,buy,10550,170,62.06
  ```

### 步骤 4：将 CSV 转换为 Pine Script

回测结果会保存为 `backtest_results.csv` 文件，你可以使用 `csv_to_pinescript.py` 脚本将其转换为 TradingView 使用的 Pine Script 格式。

1. 运行脚本：

```bash
python csv_to_pinescript.py
```

2. 脚本会生成一个 `.pinescript` 文件，包含了基于 CSV 数据生成的 Pine Script 代码。

3. 打开 TradingView，进入 **Pine Editor**，将生成的 Pine Script 代码粘贴进去，点击 **Add to Chart** 来查看回测结果的可视化展示。

### 示例流程

1. **输入示例 1**：
   - 股票代码：`AAPL`
   - 开始日期：`2020-01-01`
   - 结束日期：`2021-01-01`
   - 初始本金：`10000`

2. **回测结果**：
   - 最终账户余额：`11500`
   - 生成 CSV 文件 `backtest_results.csv`，其中包含所有交易的详细信息。

### Pine Script 生成

回测完成后，你可以使用 `csv_to_pinescript.py` 脚本将 CSV 文件转为 Pine Script 格式，便于在 TradingView 中进行图表展示。

#### Pine Script 示例

生成的 Pine Script 代码示例如下：

```pinescript
//@version=5
indicator("Backtest Results", overlay=true)

// 手动填充的交易数据
var float[] dates = array.new_float()
var float[] signals = array.new_float()
var float[] prices = array.new_float()

array.push(dates, timestamp("2021-01-01 00:00:00"))
array.push(signals, 1)  // 1表示买入
array.push(prices, 150)

array.push(dates, timestamp("2021-02-01 00:00:00"))
array.push(signals, -1)  // -1表示卖出
array.push(prices, 160)

array.push(dates, timestamp("2021-03-01 00:00:00"))
array.push(signals, 1)  // 1表示买入
array.push(prices, 170)

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

将这段 Pine Script 代码粘贴到 TradingView 的 **Pine Editor** 中并点击 **Add to Chart**，你将看到回测过程中的每一笔交易的买入和卖出信号。

## 参数说明

在回测脚本中，你可以修改以下参数来调整策略行为：

- **rsi_period**：RSI 指标的周期（默认：14）
- **macd_short**：MACD 快速线的周期（默认：12）
- **macd_long**：MACD 慢速线的周期（默认：26）
- **macd_signal**：MACD 信号线的周期（默认：9）
- **rsi_overbought**：RSI 超买阈值（默认：70）
- **rsi_oversold**：RSI 超卖阈值（默认：30）
- **initial_cash**：回测时的初始本金（默认：10000）
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

## CSV 导出

回测结果会保存到 `backtest_results.csv` 文件，文件内容包括以下列：

```csv
date,signal,cash,price,size
2021-01-01 00:00:00,buy,10000,150,66.67
2021-02-01 00:00:00,sell,10500,160,65.62
2021-03-01 00:00:00,buy,10550,170,62.06
...
```

该文件可以用于进一步分析，或者将其转换为 Pine Script 在 TradingView 上进行可视化展示。

## 许可证

MIT 许可证

---
