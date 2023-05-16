import pandas as pd
import requests  # type: ignore
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


# Цель этой функции - извлечь новостные статьи из заданной веб-страницы и вернуть
# список словарей, содержащих информацию о каждой статье.
def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    tbl = parser.table.findAll("table")[1]
    news = tbl.findAll("tr")
    for i in range(len(news)):
        n = news[i]
        if i % 3 == 0:
            ninf = {
                "title": None,
                "url": None,
                "author": "None",
                "points": 0,
                "comments": 0,
            }
        if n.attrs:
            if n.attrs["class"][0] == "athing":
                title_link = n.find("a", class_="titlelink")
                if title_link:
                    link = title_link.get("href")
                    if "http" in link:
                        ninf["url"] = link
                    elif "item" in link:
                        ninf["url"] = "https://news.ycombinator.com/" + link
                site_link = n.find("span", class_="sitestr")
                if site_link:
                    site = site_link.string
                    # link = n.findAll("a")[-1].get("href")
                    ninf["url"] = f"{site}"
            title = n.find("span", class_="titleline")
            if title:
                ninf["title"] = title.a.text
        else:
            if n.find("a").attrs:
                if "class" in n.find("a").attrs and n.find("a").attrs["class"][0] == "hnuser":
                    ninf["author"] = n.find("a").string
                    points_string = n.find("span", class_="score").string
                    if points_string is not None:
                        ninf["points"] = int(points_string.split()[0])
                    com = str(n.findAll("a")[-1].string.split()[0])
                    if com.isdigit():
                        ninf["comments"] = int(com)
                    else:
                        ninf["comments"] = 0
                    if ninf.get("title") is not None and ninf.get("url") is not None:
                        if ninf and ninf not in news_list:
                            news_list.append(ninf)
                        ninf = {}
            else:
                break
        if ninf and ninf not in news_list:
            news_list.append(ninf)
    return news_list[:-1]


# функция используется для извлечения URL следующей страницы новостных
# статей с заданной веб-страницы.
def extract_next_page(parser):
    """Extract next page URL"""
    # Сначала функция выбирает второй элемент table на странице, используя метод findAll
    # Индекс [1] используется для выбора второго элемента таблицы, потому что
    # именно там можно найти ссылку "More", исходя из структуры HTML.
    tbl = parser.table.findAll("table")[1]
    # функция находит все теги якоря (`<a>`) внутри элемента table с классом morelink
    # с помощью метода findAll и присваивает их переменной link. Поскольку метод
    # findAll возвращает список, нас интересует только первый элемент этого списка,
    # поэтому мы используем индекс [0]. Затем осуществляется доступ к атрибуту
    # href первого тега a. Этот атрибут содержит относительный URL следующей
    # страницы новостных статей.
    link = tbl.findAll("a", {"class": "morelink"})[0]["href"]
    return "news" + str(link)


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        print("url", url)
        news.extend(news_list)
        n_pages -= 1
    print(news)
    print(len(news))
    return news


news = get_news("https://news.ycombinator.com", 9)
conn = create_engine("sqlite:///news.db")
df = pd.DataFrame(news)
df.to_sql("table_name", conn, if_exists="replace", index=False)
