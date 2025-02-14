import csv

def generate_pine_script(csv_file, output_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # 开始构建 Pine Script
        pinescript_code = """//@version=5
indicator("Backtest Results", overlay=true)

// 手动填充的交易数据
var float[] dates = array.new_float()
var float[] signals = array.new_float()
var float[] prices = array.new_float()

"""

        # 读取 CSV 文件并将数据转换为 Pine Script 格式
        for row in reader:
            date = row['date']
            signal = 1 if row['signal'] == 'buy' else -1
            price = row['price']

            pinescript_code += f'array.push(dates, timestamp("{date}"))\n'
            pinescript_code += f'array.push(signals, {signal})\n'
            pinescript_code += f'array.push(prices, {price})\n'

        # 生成买入和卖出信号标签的代码
        pinescript_code += """
for i = 0 to array.size(dates) - 1
    date = array.get(dates, i)
    signal = array.get(signals, i)
    price = array.get(prices, i)

    if signal == 1
        label.new(bar_index, price, "Buy", style=label.style_label_up, color=color.green, textcolor=color.white, size=size.small)
    if signal == -1
        label.new(bar_index, price, "Sell", style=label.style_label_down, color=color.red, textcolor=color.white, size=size.small)
"""

        # 将 Pine Script 保存到文件
        with open(output_file, 'w') as outfile:
            outfile.write(pinescript_code)

        print(f"Pine Script has been generated and saved to {output_file}.")

# 使用示例
csv_file = 'backtest_results.csv'  # 输入你的 CSV 文件路径
output_file = 'generated_pinescript.pinescript'  # 输出的 Pine Script 文件名

generate_pine_script(csv_file, output_file)