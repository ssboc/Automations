import requests
from bs4 import BeautifulSoup
import re
from linebot import LineBotApi
from linebot.models import TextMessage
import json

url = 'https://www.city.sapporo.jp/hokenjo/f1kansen/2019n-covhassei.html'
html = requests.get(url)

html.encoding = 'utf-8'

soup = BeautifulSoup(html.text, 'html.parser')


number_list = soup.find('p', attrs={'align':'center'}).find('span').text

number = re.findall(r'\w+',number_list)[0]


file = open('info.json', 'r')
info = json.load(file)

CHANNEL_ACCESS_TOKEN = info['CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def main():
    USER_ID = info['USER_ID']
    messages = TextMessage(text=number)
    line_bot_api.push_message(USER_ID, messages=messages)

if __name__ == '__main__':
    main()
