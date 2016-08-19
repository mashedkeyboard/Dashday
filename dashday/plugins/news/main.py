import os
import handlers
import feedparser
import pluginloader

def init():
    global newsFeed
    newsFeed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")

def print(p):
    global newsFeed
    p.set("RIGHT", "B", "B", 1.5, 1.5)
    p.text("News")
    p.set("LEFT", "A", "normal", 1, 1)
    for i, data in enumerate(newsFeed['items']):
        if i > 4:
            break
        else:
            p.set("LEFT", "A", "B", 1, 1)
            p.text(data['title'])
            p.set("LEFT", "A", "normal", 1, 1)
            p.text(data['summary'])