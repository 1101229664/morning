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
    return f'今天是月经期第{ int_deleta + 2 }天哦~不要吃凉的~'
  elif int_deleta == 29:
    return f'今天是月经期第1天哦~不要吃凉的~'
  else:
    return f"月经期{29 - int_deleta}天后开始哦~"
# client = WeChatClient(app_id, app_secret)
# wm = WeChatMessage(client)
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
# res = wm.send_template(user_id, template_id, data)
print(res,data)


def getImg():
    res = requests.post('https://api.oioweb.cn/api/bing')
    imgUrl = res.json()['result'][0]
    return imgUrl['url']


def send_message(message):
    userid = 'FanXiGuo'  # userid
    agentid = '1000002' # 应用ID
    corpsecret = 'FKZWFTNuBWWM2N5C1bZVdH0H9_f8uPYR15RJdiDQAPk'  # Secret
    corpid = 'ww6c480527c618c53a' # 企业ID
    
    res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
    access_token = res.json()['access_token']
    
    json_dic = {
        "touser" : '@all',
        "msgtype" : "news",
        "agentid" : agentid,
        "news" : {
            "articles": [
                {
                    "title": "早上好~",
                    "description": message,
                    "picurl": getImg(),
                }
            ]
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800,
        "debug": 1
    }
    json_str = json.dumps(json_dic, separators=(',', ':'))
    res = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str)
    print(res.json())
    return res.json()['errmsg'] == 'ok'

mes = f"城市：{city}\n天气：{wea}\n最低气温: {lowTemp}\n最高气温: {highTemp}\n今日建议：{notice}\n预计：{menstruation()}\n今天是我们恋爱的第{get_count()}天\n距离小宝生日还有{get_birthday()}天\n寄言： {get_words()}"
print(mes)
send_message(mes)
