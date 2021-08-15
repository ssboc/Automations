import requests
from bs4 import BeautifulSoup
import re
import pickle
import os
from linebot import LineBotApi
from linebot.models import TextMessage
from linebot.models import ImageSendMessage
import json
import matplotlib.pyplot as plt

#*スクレイピング
url = 'https://www.city.sapporo.jp/hokenjo/f1kansen/2019n-covhassei.html'
html = requests.get(url)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, 'html.parser')
number_list = soup.find('p', attrs={'align':'center'}).find('span').text
number = int(re.findall(r'\w+',number_list)[0].rstrip("人"))
date = soup.find('p', attrs={'id':'tmp_update'}).text.lstrip('更新日2021年：')


#*前のデータの読み込み
with open('numbers', 'rb') as f:
    numbers = pickle.load(f)
with open('dates', 'rb') as f:
    dates = pickle.load(f)

#*今回得たデータを前のデータに追加
numbers.append(number)
dates.append(date)

#*前回のデータファイルはもう使わないので削除
os.remove('numbers')
os.remove('dates')

#*新しいデータファイルとして保存
with open('numbers', 'wb') as f:
    pickle.dump(numbers, f)
with open('dates', 'wb') as f:
    pickle.dump(dates, f)

#*グラフの描写
plt.rcParams["font.family"] = "Meiryo"

fig = plt.figure()
plt.ylabel("感染者数(人)", size=16)
plt.plot(dates, numbers, color="hotpink", linewidth=3)
plt.grid()
plt.show()
fig.savefig("img.jpg")

#*MessagingAPIの設定
file = open('LINEinfo.json', 'r')
info = json.load(file)

CHANNEL_ACCESS_TOKEN = info['CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

contents = f'{date}の感染者数は{str(number)}人です。'
img_url = r"https://github.com/ssboc/Automations/blob/master/img.jpg?raw=true"


def main():
    USER_ID = info['USER_ID']
    messages = TextMessage(text=contents)
    img = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    line_bot_api.push_message(USER_ID, messages=messages)
    line_bot_api.push_message(USER_ID, messages=img)


if __name__ == '__main__':
    main()
