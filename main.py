import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://kau.ac.kr/kaulife/notice.php',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

notice = soup.select("#sub_article > table > tbody > tr")

important_notice = 0
recent_notice_num = 0
for i in notice:
    if i.text[1] == '\n':
        important_notice += 1
        content = i.text[3:].replace('\n', '')
    else:
        if recent_notice_num == 0:
            recent_notice_num = int(i.text[1:5])
        content = i.text[7:].replace('\n', '')
    string = []
    for j in range(len(content)):
        if content[j:j+3] == '   ':
            break
        string.append(content[j])
    print("".join(string))
print(important_notice, recent_notice_num)