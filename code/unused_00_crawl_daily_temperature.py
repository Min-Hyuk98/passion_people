import requests
from bs4 import BeautifulSoup

r = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&query=%EC%84%9C%EC%9A%B8%EB%82%A0%EC%94%A8')
html = r.text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# 오늘의 체감온도 가져오기
temperature = soup.find('span',class_='sensible').find('span').get_text()
print(temperature)
