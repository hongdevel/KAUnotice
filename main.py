from scraper import *

html = target_html('https://kau.ac.kr/kaulife/notice.php')

print(detect_new_notice(html))

titles = extract_title(html)

for i in titles:
    print(i)