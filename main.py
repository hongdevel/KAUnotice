import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://kau.ac.kr/kaulife/notice.php',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

notice = soup.select("#sub_article > table > tbody > tr")

for i in notice:
    print((i.text.replace('\n', '')))