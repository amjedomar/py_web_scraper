import os
import string
import requests
from bs4 import BeautifulSoup


# utils
def escape_title(title):
    escaped = ''

    for char in title:
        if char == ' ':
            escaped += '_'
        elif char not in string.punctuation:
            escaped += char

    return escaped


# web scrapping
pages_num = int(input())
target_type = input()

website_url = 'https://www.nature.com'


for page_num in range(1, pages_num + 1):
    page_url = f'/nature/articles?sort=PubDate&year=2020&page={page_num}'
    page_res = requests.get(website_url + page_url)
    page = BeautifulSoup(page_res.content, 'html.parser')
    articles = page.find_all('article')

    page_dirname = f'Page_{page_num}'

    if os.access(page_dirname, os.F_OK) is False:
        os.mkdir(page_dirname)

    for article in articles:
        article_type = article.find('span', {'data-test': 'article.type'}).text.strip()

        if article_type == target_type:
            article_anchor_el = article.find('a', {'data-track-action': 'view article'})

            article_title = article_anchor_el.text
            article_filename = escape_title(article_title) + '.txt'
            article_filepath = os.path.join(os.getcwd(), page_dirname, article_filename)

            article_link = article_anchor_el.get('href')
            article_res = requests.get(website_url + article_link)
            article_page = BeautifulSoup(article_res.content, 'html.parser')
            article_body = article_page.find('div', {'class': 'c-article-body'})
            article_content = article_body.text.strip()

            article_file = open(article_filepath, 'w', encoding='utf-8')
            article_file.write(article_content)
            article_file.close()

print("articles have been saved!")
