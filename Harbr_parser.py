import requests
import bs4
import fake_headers
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def page_parser(link):
    headers_list = fake_headers.Headers(browser='firefox', os='win').generate()
    main_html = requests.get(link, headers=headers_list).text
    main_soup = bs4.BeautifulSoup(main_html, 'lxml')
    articles_list = main_soup.find('div', class_='tm-articles-list').find_all('article', id=re.compile(r'\d+'))
    return articles_list


def data_filter(criteria: list, data: list):
    for word in criteria:
        if word in str(data[1]):
            print(f'{data[0]} || {data[1]} || {data[2]}')


def get_info(def_parser, criteria, site_name):
    for article in def_parser:
        articles_info = []
        title_h2 = article.find('h2', class_='tm-title tm-title_h2')
        title_text = title_h2.find('span').text
        article_date_title = article.find('span', class_='tm-article-datetime-published').find('time').get('title')
        article_date_formatted = re.search(r'\d{4}-\d{2}-\d{2}', article_date_title).group()
        article_href = f'{site_name}{title_h2.find("a").get("href")}'
        articles_info.append([article_date_formatted, title_text, article_href])
        data_filter(criteria, articles_info[-1])


if __name__ == '__main__':

    for p in range(1, 40):
        S_NAME = 'https://habr.com/'
        URL = f'{S_NAME}ru/all/page{p}/'
        get_info(page_parser(URL), KEYWORDS, S_NAME)
