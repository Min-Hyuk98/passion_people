import requests
from bs4 import BeautifulSoup


#gender=f �Ǵ� gender=m �� url�� ���Խ�Ų�� --> ���� ���� �м��Ϸ���
#sellitem = 1�� url�� ���Խ�Ų�� --> ���� �Ǹ����� ���� ���� ������ ������
#.area=001,002,004,007,003�� url�� ���Խ�Ų�� --> ���������� ������
#.&age=10,20,30�� ,url�� ���Խ�Ų�� --> 10~30������� ������

firstPage = 1 
#������ ������ ��ȣ�� .totalPagingNum���� �����´�
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
    
    #������ ������ ��ȣ�� ����
    lastPage = soup.find('span',class_='totalPagingNum').get_text()
    #print(lastPage) #lastPage�� strŸ��

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
                test = beautifulSoup.find('td').get_text()
                print(test)