
import json
import pandas as pd
from bs4 import BeautifulSoup
import csv
import re
import requests

def get_blog_url(soup):
    div_ = soup.find_all('div', attrs={'class': 'FL PR20'})
    url_list = ["https://www.moneycontrol.com/" + title.find('a')['href'] for title in div_]
    return url_list

def get_blog_content(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    all_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
    raw_article_str = all_scripts[2].get_text().replace('\r\n', ' ')
    parts = re.split(r"""("[^"]*"|'[^']*')""", raw_article_str)
    parts[::2] = map(lambda s: "".join(s.split()), parts[::2])
    article_str = "".join(parts)
    article_str = article_str[1:]
    article_str = article_str[:-1]
    article_dict = json.loads(article_str)
    all_tags = soup.find_all('div', attrs={'class': 'tags_first_line'})
    lst_all_tags = [i.get_text() for i in all_tags]
    tags = lst_all_tags[0].replace('TAGS:', '')
    tags = tags.replace('\n', '')
    tags = tags.split('#')
    tags = tags[1:]
    tags = ', '.join([str(elem).strip() for elem in tags])
    article_dict['tags'] = tags
    return article_dict

def get_page_no(url, sc_id, page_no, next, year):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    all_page_no = soup.find_all('div', attrs={'class': 'pages MR10 MT15'})
    page_list = [i.text for i in all_page_no[0].find_all('a')]
    if any(map(str.isdigit, page_list[-1])):
        return int(page_list[-1]), next
    else:
        next = next + 1
        page_no = int(page_list[-2])
        url = f"https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id={sc_id}&scat=&pageno={page_no}&next={next}&durationType=Y&Year={year}&duration=1&news_type="
        return get_page_no(url, sc_id, page_no, next, year)

def get_articles_for_page(url, company, year, page_no, next, df):
    url_list = []
    url = url + f"sc_id={company}&scat=&pageno={page_no}&next={next}&durationType=Y&Year={year}&duration=1&news_type="
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    url_list = get_blog_url(soup)

    for url in url_list:
        try:
            article_dict = get_blog_content(url)
            article_lst = [[company,
                            article_dict['datePublished'],
                            article_dict['author'],
                            article_dict['headline'],
                            article_dict['description'],
                            article_dict['articleBody'],
                            article_dict['tags'],
                            url]]

            df = df._append(pd.DataFrame(article_lst, columns=['company', 'datePublished', 'author', 'headline',
                                                               'description', 'articleBody', 'tags', 'url']),
                           ignore_index=True)

        except:
            article_lst = [[company, 'error', 'error', 'error', 'error', 'error', 'error', url]]
            df = df._append(pd.DataFrame(article_lst, columns=['company', 'datePublished', 'author', 'headline',
                                                               'description', 'articleBody', 'tags', 'url']),
                           ignore_index=True)
            continue

    return df

def save_company_data(url_="https://www.moneycontrol.com/stocks/company_info/stock_news.php?", sc_id=[], page_no=1, next=0, years=[]):
    for company in sc_id:
        df = pd.DataFrame(columns=['company', 'datePublished', 'author', 'headline', 'description', 'articleBody', 'tags', 'url'])

        for year in years:
            print('year: ', year)
            print('page_no: ', page_no)
            print('next: ', next)
            import pdb;pdb.set_trace()
            max_page_no, max_next = get_page_no(url_, company, page_no, next, year)
            max_next = max_next + 1

            for i in range(max_next):
                for j in range((i * 10) + 1, (i * 10) + 11):
                    if j <= max_page_no:
                        df = get_articles_for_page(url_, company, year, j, i, df)
                    else:
                        break

        df.to_csv(f'./content/{company}.csv')

save_company_data(sc_id=['RI'], years=[2021, 2020])