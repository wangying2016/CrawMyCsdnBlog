from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pprint


print('Please input CSDN user name:')
userName = input()
info = []

while True:
    # 1. Open my blog's first page.
    try:
        html = urlopen('http://blog.csdn.net/' + userName)
    except HTTPError as e:
        print('Open ' + 'http://blog.csdn.net/' + userName + ' failed.')
        break

    # 2. Traverse all the article's information at one page.
    bsObj = BeautifulSoup(html, 'html.parser')
    for article in bsObj.findAll('div', {'class': 'list_item article_item'}):
        newArticle = {}
        try:
            newArticle['title'] = article.find('div', {'class': 'article_title'}).get_text().strip().replace('\r\n', '')
            newArticle['view'] = article.find('span', {'class': 'link_view'})   \
                                        .get_text().replace('(', '').replace(')', '').strip()
            newArticle['comments'] = article.find('span', {'class': 'link_comments'})   \
                                            .get_text().replace('(', '').replace(')', '').strip()
            info.append(newArticle)
        except AttributeError as e:
            print('Tag not found')
            continue

    # 3. Move to next page.
    nextPage = bsObj.find('a', text='下一页')
    if nextPage is not None:
        userName = nextPage.attrs['href']
        print(userName)
    else:
        break

with open('record.md', 'w') as record:
    record.write('| 文章 | 阅读量 | 评论数 |\n')
    record.write('| --- | --- | --- |\n')
    for article in info:
        record.write('| ' + article['title'] + ' | ' + article['view'] + ' | ' + article['comments'] + ' |\n')

pprint.pprint(info)
