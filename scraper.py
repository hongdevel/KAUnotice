import requests
from bs4 import BeautifulSoup
from enum import Enum
import re
import datetime
import os
from urllib.request import urlretrieve
from urllib.parse import urljoin
import cv2
from matplotlib import pyplot as plt
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

def menu_url():
    pages = target_html('https://kau.ac.kr/kaulife/foodmenu.php')

    now = datetime.datetime.now()

    date_re = re.compile(r"\[학생식당\] ((\d{1,2}년)(\d{1,2}월\d{1,2}일)~(\d{1,2}월\d{1,2}일))")

    base_url = 'https://kau.ac.kr'
    url = None

    for i in pages:
        date = date_re.search(i.text)

        if date:
            start_date = datetime.datetime.strptime(date.group(2)+date.group(3), "%y년%m월%d일")
            end_date = datetime.datetime.strptime(date.group(2)+date.group(4), "%y년%m월%d일")

            if start_date < now < end_date:
                url = i.select_one("td.tit > a").attrs["href"]
                url = urljoin(base_url, url)

    return url

def menu_img(url):
    base_url = 'https://kau.ac.kr'

    path_folder = "./foodmenu/"
    if not os.path.isdir(path_folder):
        os.mkdir("./foodmenu/")
     
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    
    try:
        img_url = soup.select_one("#sub_article > div.view > div.view_conts img").attrs["src"]
        urlretrieve(urljoin(base_url, img_url), path_folder + "foodmenu_img.png")
        return path_folder + "foodmenu_img.png"
    except AttributeError:
        return None
    
def menu_table(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    menu = soup.select("#sub_article > div.view > div.view_conts > table > tbody > tr > td")

    #test = menu[0].text.replace("\n", "").replace("\r", "")
    #for i in menu:
    #    print(i.text.replace("\n", "").replace("\r", ""))
    cnt = 1
    for i in menu:
        print(i.text.replace("\n", "").replace("\r", ""), end="")
        if cnt % 5 == 0:
            print("")
        cnt += 1

def menu_text(img_path):
    img = cv2.imread(img_path)

    weekday = datetime.datetime.now().weekday()
    weekday = 0

    img_cut = img[46 + (270 * weekday):273 + (270 * weekday), 38:212]

    img_zoom = cv2.resize(img_cut, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

    img_gray = cv2.cvtColor(img_zoom, cv2.COLOR_BGR2GRAY)

    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

    _, img_binary = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3,3), np.uint8)

    img_morph = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)

    plt.imshow(img)
    plt.show()

    config = ('-l kor --oem 3 --psm 6')
    output = pytesseract.image_to_string(img_morph, config=config)
    print(output)



if __name__ == "__main__":
    img_url = menu_url()

    img_path = menu_img(img_url)

    if img_path:
        menu_text(img_path)
    else:
        menu_table(img_url)