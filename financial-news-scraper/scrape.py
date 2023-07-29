import requests
import bs4
import re
import json
import pandas as pandas
import csv
# request = requests.get("https://www.moneycontrol.com/company-article/relianceindustries/news/RI")
# soup=bs4.BeautifulSoup(request.text,"html.parser")
# para=soup.select('p')
# anchor=soup.find_all('a',attrs={'class':"arial11_summ"})
# for i in anchor:
#     print("Title",i['title'])

url="https://www.moneycontrol.com/news/business/earnings/ril-q1-preview-net-profit-seen-at-rs-16995-crore-10995281.html"

# request=requests.get(url)
# soup=bs4.BeautifulSoup(request.text,"html.parser")

# all_script=soup.find_all('script',attrs={"type":"application/ld+json"})
# raw_article_str=all_script[2].get_text().replace('\r\n',' ')
# parts=re.split(r"""("[^"]*"|'[^']*')""",raw_article_str)
# parts[::2]=map(lambda s:"".join(s.split()),parts[::2])
# article_str="".join(parts)
# article_str=article_str[1:]
# article_str=article_str[:-1]
# article_dict=json.loads(article_str)


# all_tags=soup.find_all('div',{'class':"tags_first_line"})
# list_all_tags=[]
# for i in all_tags:
#     list_all_tags.append(i.get_text())
# clean_tags=list_all_tags[0].replace("Tags:","")
# clean_tags=clean_tags.replace("\n","")
# splitted=clean_tags.split('#')
# splitted=splitted[1:]
# final=','.join([ele.strip() for ele in splitted])
# print(final)
# article_dict['tags']=final
# print(article_dict)

def get_page_no(url,sc_id,page_no,next,year):
    request=requests.get(url)
    soup=bs4.BeautifulSoup(request.text,'html.parser')
    all_page_no=soup.find_all('div',attrs={'class':"pages MR10 MT15"})
    page_list=[i.text for i in all_page_no[0].find_all('a')]
    print(page_list)
    if not any(map(str.isdigit,page_list[-1])):
        next=next+1
        page_no=int(page_list[-2])
        url = "https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id="+sc_id+"&scat=&pageno="+str(page_no)+"&next="+str(next)+"&durationType=Y&Year="+str(year)+"&duration=1&news_type="
        print('going to page',next)
        return get_page_no(url, sc_id, page_no, next, year)        

        # Checks if the last elemetn is next or is a digit if it's a digit then it implies a last page. stop there
    else:
        return int(page_list[-1]),next        
        


sc_id = "RI"
page_no = 1
next = 0
year = 2017
url = "https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id="+sc_id+"&scat=&pageno="+str(page_no)+"&next="+str(next)+"&durationType=Y&Year="+str(year)+"&duration=1&news_type="
page_no, next = get_page_no(url, sc_id, page_no, next, year)
print(page_no, next)