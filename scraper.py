import requests
from bs4 import BeautifulSoup
from enum import Enum

class NoticeUrls(Enum):
    일반 = 'https://kau.ac.kr/kaulife/notice.php'
    학사 = 'https://kau.ac.kr/kaulife/acdnoti.php'
    장학및대출 = 'https://kau.ac.kr/kaulife/scholnoti.php'
    행사 = 'https://kau.ac.kr/kaulife/event.php'
    모집및채용 = 'https://kau.ac.kr/kaulife/recruitment.php'
    입찰 = 'https://kau.ac.kr/kaulife/bid.php'
    전염병관리 = 'https://kau.ac.kr/kaulife/covidnoti.php'
    IT = 'https://kau.ac.kr/kaulife/itnoti.php'
    산학및연구 = 'https://kau.ac.kr/kaulife/iunoti.php'
    교내식단표 = 'https://kau.ac.kr/kaulife/foodmenu.php'

def target_html(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    return soup.select("#sub_article > table > tbody > tr")

def get_new_notice_num(notice):
    important_notice = 0
    notice_num = 0
    important_notice_date = ''

    for i in notice:
        if i.text[1] == '\n':
            important_notice += 1
        else:
            notice_num = int(i.text[1:5])
            break
    
    if notice_num == 0:
        for i in range(-1, -len(notice[0].text), -1):
            if notice[0].text[i] == "-":
                important_notice_date = notice[0].text[i - 7:i + 3]
                break
    
    return [important_notice, notice_num, important_notice_date]

def extract_title(notice):
    titles = []
    
    for i in notice:
        if i.text[1] == '\n':
            content = "📢  :  " + i.text[3:].replace('\n', '')
        else:
            content = i.text[1:5] + ' : ' + i.text[7:].replace('\n', '')
        
        string = []
        for j in range(len(content)):
            if content[j:j+3] == '   ':
                break
            string.append(content[j])
        titles.append("".join(string))
    
    return titles