import requests
from bs4 import BeautifulSoup

import re             # 정규표현식 (For문의 반복 시퀀스 증가를 이용한 순위가 아닌 실제 사이트에 표현된 순위 추출을 위해)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['scc-w4']

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


for i  in range(1, 5 ,1) :
    data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&pg={}'.format(i), headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    chart = soup.select('#body-content > div.newest-list > div.music-list-wrap > table > tbody > tr')

    for song in chart :
        rank = re.findall('^[0-9]+',song.select('td.number')[0].text)[0]
        title = song.select('td > input')[0]['title']
        artist = song.select('a.artist')[0].text
        info = {'rank': rank, 'title': title, 'artist' : artist}
        db.geniemusic.insert_one(info)
        print(info)
