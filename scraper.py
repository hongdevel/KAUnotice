import requests
from bs4 import BeautifulSoup

def target_html(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    return soup.select("#sub_article > table > tbody > tr")

def detect_new_notice(notice):
    important_notice = 0

    for i in notice:
        if i.text[1] == '\n':
            important_notice += 1
        else:
            recent_notice_num = int(i.text[1:5])
            break
    
    return [important_notice, recent_notice_num]

def extract_title(notice):
    titles = []
    
    for i in notice:
        if i.text[1] == '\n':
            content = i.text[3:].replace('\n', '')
        else:
            content = i.text[7:].replace('\n', '')
        
        string = []
        for j in range(len(content)):
            if content[j:j+3] == '   ':
                break
            string.append(content[j])
        titles.append("".join(string))
    
    return titles