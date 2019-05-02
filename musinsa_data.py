import requests
from bs4 import BeautifulSoup


#gender=f 또는 gender=m 를 url에 포함시킨다 --> 각각 따로 분석하려함
#sellitem = 1을 url에 포함시킨다 --> 현재 판매중인 옷을 입은 사진만 보여줌
#.area=001,002,004,007,003를 url에 포함시킨다 --> 서울지역만 보여줌
#.&age=10,20,30를 ,url에 포함시킨다 --> 10~30대까지만 보여줌

#마지막 페이지 번호는 .totalPagingNum에서 가져온다
firstPage = 1
lastPage = 1

# 로그인 세션 만들어서, 이 안에서 코드 실행
with requests.session() as s:
    url = "https://store.musinsa.com/app/api/login/make_login"
    data = {
        "referer" : "https://www.musinsa.com/index.php",
        "id" : "wkdalsgur85",
        "pw" : "cnj140535",
    }
    response = s.post(url, data=data)
    response.raise_for_status
#     print(response.text)

    r = requests.get('https://www.musinsa.com/index.php?m=street&_y=2018&gender=f&area=001,002,004,007,003')
    html = r.text
#     print(html)
    soup = BeautifulSoup(html, 'html.parser')

# 마지막 페이지 번호를 구함
    lastPage = soup.find('span',class_='totalPagingNum').get_text()
#     print(lastPage) #lastPage는 str타입

# 바깥 페이지에서 모든 페이지에 하나하나 접근함(성별, 지역, 연령, 시기는 밑의 url에 포함)
    for i in range(firstPage, int(lastPage) + 1):
        r = requests.get('https://www.musinsa.com/index.php?m=street&_y=2018&gender=f&area=001,002,004,007,003&p=', str(i))
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
# 각 아이템에 접근함
        for link in soup.findAll('a', class_='creplyCnt'):
            if 'href' in link.attrs:
                uid = link.attrs['href']
                uid = uid[-17:-8]
#                 print(uid)

# 각 아이템의 링크에 들어감
                new_url = "https://www.musinsa.com/index.php?m=street&" + uid
                r = s.post(new_url, data=data)
#                 print(r.text)
                beautifulSoup = BeautifulSoup(r.text, 'html.parser')
#                 print(beautifulSoup)

# 아이템의 정보
                raw_list = beautifulSoup.select('table > tbody > tr > td > span')

                info_list = []
                for i in raw_list:
                    info_list.append(i.get_text())
# 예외 없애줌
                if '2018 F/W 헤라 서울패션위크' in info_list:
                    info_list.pop(3)
                elif '2018 서머 뮤직 페스티벌' in info_list:
                    info_list.pop(3)
                elif "2018 MUSINSA MD'S PICK" in info_list:
                    info_list.pop(3)
                elif '2018 F/W 하우스 오브 반스' in info_list:
                    info_list.pop(3)
                elif '2018 신학기 스타일 가이드 북' in info_list:
                    info_list.pop(3)
                elif '2018 스웨트 페스티벌' in info_list:
                    info_list.pop(3)
                elif '2018 S/S 일본 트렌드 리포트' in info_list:
                    info_list.pop(3)
                elif '2018 F/W 버쉬카 도쿄 리포트' in info_list:
                    info_list.pop(3)
                elif '2018 아우터 페스티벌' in info_list:
                    info_list.pop(3)
                elif '2019 S/S 헤라 서울패션위크' in info_list:
                    info_list.pop(3)
                elif '2018 서머 뮤직 페스티벌' in info_list:
                    info_list.pop(3)

#                 print(info_list)

                date = info_list[1]
                style = info_list[5]
                views_like = info_list[6]
#                 print(date)
#                 print(style)
#                 print(views_like)
#                 print("/////////////////")



# # 이미지 링크
#                 photos = []
#                 raw_photos = beautifulSoup.select('ul > li > div.itemImg > a > img')
#                 for i in raw_photos:
#                     photos.append(i.get("src"))
#                 print(photos)

# # 이미지 설명
#                 explanations = []
#                 raw_explanations = beautifulSoup.select('ul > li > div.itemImg > div > ul > li > a > span')[:1]
#                 for i in raw_explanations:
#                     explanations.append(i.get_text())
#                 print(explanations)





# 이미지 및 설명 이중리스트로 만듦
                photos = [[],[],[]]
                explanations = []
                raw_photos = beautifulSoup.select('ul > li > div.itemImg > a > img')
                raw_explanations = beautifulSoup.select('ul > li > div.itemImg > div > ul > li > a > span')
                for i in raw_explanations:
                    explanations.append(i.get_text())
                num = 0
                for i in raw_photos:
                    photos[num].append(i.get("src"))
                    for j in explanations:
                        if "색" in j or "블랙" in j or "베이지" in j or "체크" in j or "아이보리" in j or "스트라이프" in j or "브라운" in j or "레드" in j or "오렌지" in j:
                            photos[num].append(j)
                            explanations.remove(j)
                            break
                        else:
                            photos[num].append(j)
                            explanations.remove(j)
                    num += 1
#                 print(photos)


                print(date)
                print(style)
                print(views_like)
                for i in photos:
                    for j in i:
                        print(j)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
     
