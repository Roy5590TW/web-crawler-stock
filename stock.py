#引用模組
import csv
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import re

def stock():
  # 設定使用者代理標頭
  headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
  }

  # 構造股票資訊網址
  url = 'https://goodinfo.tw/tw/ShowSaleMonChart.asp?STOCK_ID=' + (
    stock_code_entry.get())

  # 發送 GET 請求獲取網頁內容
  resp = requests.get(url, headers=headers)
  resp.encoding = 'utf-8'
  raw_html = resp.text

  # 使用 BeautifulSoup 解析 HTML
  soup = BeautifulSoup(raw_html, "html.parser")

  # 將字串轉換為浮點數
  def parse_str_to_float(raw_value):
    return float(raw_value.replace(',', ''))

  performance_list = []

  # 解析每個月份的股票表現數據
  for index in range(5, 10):
    performance_dict = {}

    # 獲取月份
    performance_dict['月份'] = soup.select(
      f'#divDetail > table > tr:nth-child({index}) > td:nth-child(1) > nobr'
    )[0].text

    # 獲取開盤價
    performance_dict['開盤'] = parse_str_to_float(
      soup.select(
        f'#divDetail > table > tr:nth-child({index}) > td:nth-child(2) > nobr')
      [0].text)

    # 獲取收盤價
    performance_dict['收盤'] = parse_str_to_float(
      soup.select(
        f'#divDetail > table > tr:nth-child({index}) > td:nth-child(3) > nobr')
      [0].text)

    performance_list.append(performance_dict)

  # 尋找股票名稱
  nobr_elements = soup.find_all('nobr')
  stock_name = ""
  for element in nobr_elements:
    if element.text == '期貨標的':
      stock_name = re.sub(r'\d+|\s+', '', laste_one.text)
      break
    laste_one = element

  # 寫入 CSV 檔案
  output_headers = ['月份', '開盤', '收盤']
  with open(stock_code_entry.get() + '_' + stock_name + '_performance.csv',
            'w') as output_file:
    dict_writer = csv.DictWriter(output_file, output_headers)
    dict_writer.writeheader()
    dict_writer.writerows(performance_list)

  # 清空輸入框並顯示完成訊息
  stock_code_entry.delete(0, tk.END)


# 建立主視窗，建立 Tk 物件
window = tk.Tk()
window.title("網路爬蟲")

# 股票代號標籤
stock_code_label = tk.Label(window, text="股票代號:")
stock_code_label.pack()

# 股票代號輸入框
stock_code_entry = tk.Entry(window)
stock_code_entry.pack()

# 提交按鈕
stock_code_button = tk.Button(window, text="submit", command=stock)
stock_code_button.pack()

# 顯示結果的標籤
result_stock_code_label = tk.Label(window)
result_stock_code_label.pack()

window.mainloop()
