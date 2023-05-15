from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news

bayes = NaiveBayesClassifier(alpha=0.05)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    record_id = request.query.id
    s = session()
    record = s.query(News).filter(News.id == record_id).all()[0]
    record.label = label
    s.add(record)
    s.commit()

    if __name__ == "main":
        redirect("/news")


@route("/update")
def update_news():
    new_news = get_news("https://news.ycombinator.com/newest", n_pages=5)
    s = session()
    # print(new_news[:5])
    for record in new_news:
        if (
                s.query(News)
                        .filter(News.title == record["title"] and News.author == record["author"])
                        .first()
                is None
        ):
            data = News(
                title=record["title"],
                author=record["author"],
                url=record["url"],
                comments=record["comments"],
                points=record["points"],
                label=None,
            )
            s.add(data)
    s.commit()

    if __name__ == "main":
        redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    list_of_train = s.query(News).filter(News.label != None).all()
    x_train = []
    y_train = []
    for i in list_of_train:
        x_train.append(i.title)
        y_train.append(i.label)
    bayes.fit(x_train, y_train)
    news = s.query(News).filter(News.label == None).all()
    x = [i.title for i in news]
    y = bayes.predict(x)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return sorted(news, key=lambda i: i.label)


@route("/recommendations")
def recommendations():
    s = session()
    classified_news = s.query(News).filter(News.label == None).all()
    x = [i.title for i in classified_news]
    y = bayes.predict(x)
    for i in range(len(classified_news)):
        classified_news[i].label = y[i]
    s.commit()
    return template("news_recommendations", rows=classified_news)


if __name__ == "main":
    run(host="localhost", port=1111, debug=False)
