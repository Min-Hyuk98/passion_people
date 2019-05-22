import requests
import json
import pandas as pd
import webbrowser
import random

#API 키 지정
apikey = "f7978bc0840def12cd41b5f8bcb17c39"

#날씨를 확인할 도시 지정
name = "Seoul,KR"

#API 지정
api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

#켈빈 온도를 섭씨 온도로 변환하는 함수
k2c = lambda k: k - 273.15

#서울의 날씨 추출
url = api.format(city=name, key=apikey)
r = requests.get(url)
data = json.loads(r.text)

weather = data["weather"][0]["description"]
avg_tmp = (k2c(data["main"]["temp_max"])+k2c(data["main"]["temp_min"]))/2

path = "C:/Users/Jang/passion_people_jupyter/"
top_csv = pd.read_csv(path+"41_cluster_df_top.csv",engine="python")
bottom_csv = pd.read_csv(path+"42_cluster_df_bottom.csv",engine="python")

#top avg cluster
if avg_tmp < -7.3:
    cluster_t = 9
elif avg_tmp < -1.3:
    cluster_t = 3
elif avg_tmp < 3.5:
    cluster_t = 7
elif avg_tmp < 8.8:
    cluster_t = 2
elif avg_tmp < 14.1:
    cluster_t = 5
elif avg_tmp < 17.8:
    cluster_t = 8
elif avg_tmp < 20.9:
    cluster_t =4
elif avg_tmp <24.8:
    cluster_t = 10
elif avg_tmp < 28.8:
    cluster_t = 1
else :
    cluster_t = 6

#bottom avg cluster
if avg_tmp < -8.0:
    cluster_b = 9
elif avg_tmp < -2.3:
    cluster_b = 0
elif avg_tmp < 2.6:
    cluster_b = 5
elif avg_tmp < 6.7:
    cluster_b = 2
elif avg_tmp < 11.2:
    cluster_b = 8
elif avg_tmp < 16.3:
    cluster_b = 4
elif avg_tmp < 20.9:
    cluster_b = 7
elif avg_tmp < 25.3:
    cluster_b = 1
elif avg_tmp < 28.8:
    cluster_b = 6
else :
    cluster_b = 3

text = input('캐주얼, 스트리트, 걸리시, 클래식, 유니크 중 스타일을 선택해주세요:')
# print(text)

def choose_style(text, cluster, df):
    tag_list = []
    for i, tag in enumerate((df['tags'])):
        tag = tag[1:-1]
        tag = tag.replace("'","")
        tag = tag.replace(",","")
        tag_list.append(tag.split())

    df.insert(loc=0, column='list', value=tag_list)
    url_list = []
    for i, tag in enumerate(tag_list):
        if text in tag:
            url_list.append("1")
        else:
            url_list.append("0")
    if "1" not in url_list:
        print("오늘은", text + "스타일이 없습니다. 다른 스타일로 추천해드리겠습니다")
        df["url_n"] = "1"
        return df
    else:
        df["url_n"] = url_list
        return df

def magic_top():
    top = str(random.choices(top_df3['url'].tolist()))[2:-2]
    return webbrowser.open(top)

def magic_bottom():
    bottom = str(random.choices(bottom_df3['url'].tolist()))[2:-2]
    return webbrowser.open(bottom)


top_df = top_csv[top_csv['cluster']==cluster_t]
bottom_df = bottom_csv[bottom_csv['cluster']==cluster_b]

top_df2 = choose_style(text, cluster_t, top_df)
bottom_df2 = choose_style(text, cluster_t, bottom_df)

top_df3 = top_df2[top_df2['url_n']=='1']
bottom_df3 = bottom_df2[bottom_df2['url_n']=='1']


# print("오늘의 날씨는 " + weather+"입니다")
print("오늘의 평균기온은 "+str(avg_tmp)+"입니다")
print("오늘의 추천상의는 ")
print(magic_top())
print("오늘의 추천하의는 ")
print(magic_bottom())
