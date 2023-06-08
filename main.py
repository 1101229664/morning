from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
city_id = os.environ['CITY_ID']

def get_weather():
  url = "http://t.weather.itboy.net/api/weather/city/" + city_id
  res = requests.get(url).json()
  weather = res['data']['forecast'][0]
  return weather['type'], weather['high'],weather['low'],weather['notice']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_aaa():
  delta = today - datetime.strptime('2023-05-14', "%Y-%m-%d")
  int_deleta = int(delta.days%30)
  if int_deleta < 4:
    return f'预计今天是经期第{ int_deleta + 2 }天哦~不要吃凉的~'
  elif int_deleta == 29:
    return f'预计今天是经期第1天哦~不要吃凉的~'
  else:
    return f"预计经期{29 - int_deleta}天后开始哦~"
client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, highTemp, lowTemp, notice = get_weather()
data = {
    "city": {"value": city, "color":get_random_color()}, 
    "weather": {"value": wea}, 
    "highTemp": {"value": highTemp}, 
    "lowTemp": {"value": lowTemp}, 
    "notice" : {"value": notice},
    "aaa" : {"value": get_aaa()},
    "love_days": {"value": get_count()}, 
    "birthday_left": {"value": get_birthday()}, 
    "words": {"value": get_words(), 
    "color": get_random_color()}
    }
res = wm.send_template(user_id, template_id, data)
print(res,data)
