from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news

try:
    bayes = NaiveBayesClassifier.load("data/model.bin")
except FileNotFoundError:
    bayes = NaiveBayesClassifier(alpha=0.05)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    nid = request.query.id
    s = session()
    s.query(News).filter(News.id == nid).first().label = label
    # news.label = label
    # s.add(news)
    s.commit()

    # print(news.label)
    if name == "main":
        redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/newest", 1)
    for i in news:
        if not s.query(News).filter(News.title == i["title"]).first():
            s.add(
                News(
                    title=i["title"],
                    author=i["author"],
                    url=i["url"],
                    comments=i["comments"],
                    points=i["points"],
                )
            )
    s.commit()

    if name == "main":
        redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    train = s.query(News).filter(News.label != None).all()
    x = [i.title for i in train]
    y = [i.label for i in train]
    bayes.fit(x, y)
    news = s.query(News).filter(News.label == None).all()
    X = [i.title for i in news]
    y = bayes.predict(X)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return sorted(news, key=lambda x: x.label)


@route("/recommendations")
def recommendations():
    s = session()
    news = s.query(News).filter(News.label == None).all()
    X = [i.title for i in news]
    y = bayes.predict(X)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return template("news_template", rows=news)


if name == "main":
    run(host="localhost", port=1111, debug=False)
    bayes.save("data/model.bin")
