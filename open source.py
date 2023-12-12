#get_temp.py
import requests
from bs4 import BeautifulSoup
class Get_Temp:
    def __init__(self):
        self.today = dict()
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}"
        날씨 = "서울날씨"
        url = url.format(날씨)
        html = requests.get(url)
        self.soup= BeautifulSoup(html.text,"html.parser")

    def get_temp(self):
        now_temperate = self.soup.select_one(".temperature_text > strong ").text
        self.today[now_temperate[:5]]=now_temperate[5:]

    def get_dust(self):
        dust = self.soup.select(".item_today > a > span")
        title = self.soup.select(".item_today > a > strong")
        for i in range(3):
            self.today[title[i].text]=dust[i].text

    def get_rain_wind(self):
        rain_wind = self.soup.select_one(".summary_list")
        rain_wind_t = rain_wind.select(".term")
        rain_wind_d = rain_wind.select(".desc")
        for i in range(3):
            # Check if the term is '강수확률' or '바람'
            term = rain_wind_t[i].text
            if rain_wind_t[i].text[:2]=="바람":
                self.today[rain_wind_t[i].text[:2]]=rain_wind_d[i].text
            else:
                self.today[rain_wind_t[i].text]=rain_wind_d[i].text

    def get_max_min(self):
        min_max = self.soup.select_one(".temperature_inner").text
        self.today["최저최고"] = min_max


    def start(self):
        self.get_temp()
        self.get_rain_wind()
        self.get_dust()
        self.get_max_min()
        return self.today

start = Get_Temp()
result = start.start()
print(result)
#naver_crawling.py
import requests
from bs4 import BeautifulSoup

today = dict()
url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}"
날씨 = "서울날씨"
url = url.format(날씨)
html = requests.get(url)
soup= BeautifulSoup(html.text,"html.parser")
now_temperate = soup.select_one(".temperature_text > strong ").text
today[now_temperate[:5]]=now_temperate[5:]
dust = soup.select(".item_today > a > span")
title = soup.select(".item_today > a > strong")

for i in range(3):
    today[title[i].text]=dust[i].text
rain_wind = soup.select_one(".summary_list")
rain_wind_t = rain_wind.select(".term")
rain_wind_d = rain_wind.select(".desc")
for i in range(3):
    today[rain_wind_t[i].text]=rain_wind_d[i].text
temp = soup.select_one(".temperature_inner").text
print(temp)
print(today)
#send_sms.py
from twilio.rest import Client
import get_temp
from dotenv import load_dotenv
import os
load_dotenv(verbose=True)
account_sid = 'ACf56ba573054612e428a81e61857a0bba'
auth_token  = '97d3e3fe9446e3ff41b8e5fce972c4b8'
client = Client(account_sid,auth_token)
temp_data = get_temp.Get_Temp().start()
print(temp_data)
current_temperature = temp_data.get('현재 온도', 'N/A')
min_max_temperature = temp_data.get('최저최고', 'N/A')
fine_dust = temp_data.get('미세먼지', 'N/A')
ultrafine_dust = temp_data.get('초미세먼지', 'N/A')
humidity = temp_data.get('습도', 'N/A')

json_to_string = " 현재 온도 : {}\n\n{}\n\n \n\n 미세먼지 : {} \n\n 초미세먼지 : {}\n\n 습도 : {} ".format(
    current_temperature, min_max_temperature, fine_dust, ultrafine_dust, humidity
)


message = client.messages.create(
    to="+8201021259308", 
    from_="+12029329002",
    body=json_to_string)

print(message.sid)