import requests
from bs4 import BeautifulSoup
import re
from linebot import LineBotApi
from linebot.models import TextMessage
import json

#*スクレイピング
url = 'https://www.city.sapporo.jp/hokenjo/f1kansen/2019n-covhassei.html'
html = requests.get(url)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, 'html.parser')
number_list = soup.find('p', attrs={'align':'center'}).find('span').text
number = int(re.findall(r'\w+',number_list)[0].rstrip("人"))
date = soup.find('p', attrs={'id':'tmp_update'}).text.lstrip('更新日2021年：')


#*MessagingAPIの設定
file = open('LINEinfo.json', 'r')
info = json.load(file)

CHANNEL_ACCESS_TOKEN = info['CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

contents = f'{date}の感染者数は{str(number)}人です。'


def main():
    USER_ID = info['USER_ID']
    messages = TextMessage(text=contents)
    line_bot_api.push_message(USER_ID, messages=messages)
    


if __name__ == '__main__':
    main()
