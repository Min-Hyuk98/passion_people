import requests
from bs4 import BeautifulSoup


#gender=f 또는 gender=m 를 url에 포함시킨다 --> 각각 따로 분석하려함
#sellitem = 1을 url에 포함시킨다 --> 현재 판매중인 옷을 입은 사진만 보여줌
#.area=001,002,004,007,003를 url에 포함시킨다 --> 서울지역만 보여줌
#.&age=10,20,30를 ,url에 포함시킨다 --> 10~30대까지만 보여줌

firstPage = 1
#마지막 페이지 번호는 .totalPagingNum에서 가져온다
lastPage = 1

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

    #마지막 페이지 번호를 구함
    lastPage = soup.find('span',class_='totalPagingNum').get_text()
    #print(lastPage) #lastPage는 str타입

    for i in range(firstPage, int(lastPage) + 1):
        r = requests.get('https://www.musinsa.com/index.php?m=street&_y=2018&gender=f&area=001,002,004,007,003&p=', str(i))
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.findAll('a', class_='creplyCnt'):
            if 'href' in link.attrs:
                uid = link.attrs['href']
                uid = uid[-17:-8]
#                 print(uid)

                new_url = "https://www.musinsa.com/index.php?m=street&" + uid
                r = s.post(new_url, data=data)
#                 print(r.text)

                beautifulSoup = BeautifulSoup(r.text, 'html.parser')
#                 print(beautifulSoup)
                raw_list = beautifulSoup.select('table > tbody > tr > td > span')

                info_list = []
                for i in raw_list:
                    info_list.append(i.get_text())

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

                print(info_list)

                date = info_list[1]
                style = info_list[5]
                views_like = info_list[6]
                print(date)
                print(style)
                print(views_like)
                print("/////////////////")
