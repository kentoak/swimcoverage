from urllib import request
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import requests
import csv
from pprint import pprint
import sys
#sys.path.append('/home/pi/.local/lib/python3.9/site-packages')
sys.path.append('/usr/local/lib/python3.9/site-packages')
import tweepy
import random
import time
#https://miyashinblog.com/news_colab/
CONSUMER_KEY=""
CONSUMER_SECRET=""
ACCESS_TOKEN=""
ACCESS_TOKEN_SECRET=""

def get_shortenURL(longUrl):
    url = 'https://api-ssl.bitly.com/v3/shorten'
    access_tokens = ['','']
    if random.random() >= 0.5:
        access_token = access_tokens[0]
    else:
        access_token = access_tokens[1]
    access_token = access_tokens[1]#とりまこっち制限ないので...
    query = {
        'access_token': access_token,
        'longurl':longUrl
    }
    pprint(requests.get(url,params=query).json()['data'])
    if "data" in requests.get(url,params=query).json():
        if "url" in requests.get(url,params=query).json()['data']:
            r = requests.get(url,params=query).json()['data']['url']
            return r


def post(str):
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    t = tweepy.API(auth)
    #str1 = str.replace('\\n',"\\n\\")
    t.update_status(status=str)

#url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
#url="https://news.google.com/rss/search?q=swimming&hl=en-US&gl=US&ceid=US:en"
#2019/8/30以前2019/7/29以降の記事→https://news.google.com/rss/search?q=after:2019/7/29+before:2019/8/30&hl=ja&gl=JP&ceid=JP:ja
#https://news.google.com/rss/search?q=swimming&hl=en-US&gl=US&ceid=US:en

keywords = ["池江 璃花子", "競泳", "世界水泳 競泳", "競泳 日本代表", "瀬戸大也", "萩野公介", "今井月 競泳 水泳 スイマー", "中村克 競泳 水泳 スイマー", "水沼尚輝 競泳 水泳 スイマー", "成田実生 競泳 水泳 スイマー", "松本信歩 競泳 水泳 スイマー", "松本悠里 競泳 水泳 スイマー", "谷川亜華葉 競泳 水泳 スイマー", "本多灯 競泳 水泳 スイマー", "入江陵介 競泳 水泳 スイマー", "松元克央 競泳 水泳 スイマー", "渡辺一平 競泳 水泳 スイマー", "白井璃緒 競泳 水泳 スイマー", "五十嵐千尋 競泳 水泳 スイマー", "日本雄也 競泳 水泳 スイマー", "ピーティ ピーティー 競泳 水泳 スイマー", "レデッキー 競泳 水泳 スイマー", "ミラーク ミラク 競泳 水泳 スイマー", "ドレセル ドレッセル 競泳 水泳 スイマー", "マッキントッシュ 競泳 水泳 スイマー", "個人メドレー 競泳 水泳 スイマー", "平泳ぎ 競泳 水泳 スイマー", "背泳ぎ 競泳 水泳 スイマー", "バタフライ 競泳 水泳 スイマー", "自由形 競泳 水泳 スイマー", "萩野公介 競泳 水泳 スイマー", "パリ五輪 競泳 水泳 スイマー", "東京五輪 競泳 水泳 スイマー", "ショーストロム ショーストレム 競泳 水泳 スイマー", "オレクシアク 競泳 水泳 スイマー", "世界記録 世界新記録 世界新 競泳 水泳 スイマー", "日本記録 日本新記録 日本新 競泳 水泳 スイマー", "松田丈志 競泳 水泳 スイマー", "平井伯昌 競泳 水泳 スイマー", "鈴木大地 競泳 水泳 スイマー", "本多灯 競泳 水泳 スイマー", "北島康介 競泳 水泳 スイマー", "本多灯 競泳 水泳 スイマー", "梅原孝之 競泳 水泳 スイマー", "大橋悠依 競泳 水泳 スイマー", "日本水連 競泳 水泳 スイマー", "北京五輪 競泳 水泳 スイマー", "フェルプス 競泳 水泳 スイマー", "ロクテ 競泳 水泳 スイマー", "イアン・ソープ 競泳 水泳 スイマー", "中村礼子 競泳 水泳 スイマー", "金藤理絵 競泳 水泳 スイマー"]# 検索キーワードを入れてください
number_searches = 10 # 記事の上位検索数
url = 'https://news.google.com/search'

for keyword in keywords:
    print("\n★「"+str(keyword)+"」"+"の最新ニュースを検索★")
    params = {'hl':'ja', 'gl':'JP', 'ceid':'JP:ja', 'q':keyword}
    #response = request.urlopen(url)
    res = requests.get(url, params=params)
    #soup = BeautifulSoup(response,"xml")
    #response.close()
    soup = BeautifulSoup(res.content, "html.parser")
    #articles = soup.find_all("item")
    articles = soup.select(".xrnccd")
    for i,item in enumerate(articles):
        if i > number_searches:
            break
        #title = item.find("title").getText()
        #item=item.encode('cp932').decode('shift_jis')
        title=item.select_one("h3 a").text
        link=urllib.parse.urljoin(url,item.select_one("h3 a")["href"])
        print(title,"\n",link)
        with open('./swimcoverageResult.csv',mode="a",encoding='utf-8') as f:
            # 前回スクレイピングした結果と比較する
            try:
                df = pd.read_csv('./swimcoverageResult.csv', header=None)
            except:
                df = pd.DataFrame(["log取得開始"])
            flag = 0
            for index, row in df.iterrows():
                if (str(row[0]) == str(title)):
                    flag = 1
                    print("過去の記事と一致しました")
                    break
            #Bitlyを使うとき
            if flag == 0:
                # ニュースのタイトル、リンクをファイルに書き込む
                writer = csv.writer(f)
                if len(title)>=140-22:
                    print("bitlyします！")
                    # newlink=get_shortenURL(link)
                    # if newlink:
                    #     writer.writerows([[title,newlink]])
                    # else:
                    #     writer.writerows([[title,link]])
                else:
                    writer.writerows([[title,link]])
                print(title+"\n"+link)
                #post(title+link)
                #f.write('\r\n')
