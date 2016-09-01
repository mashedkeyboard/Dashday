import os
import handlers
import feedparser
import pluginloader

def init():
    global newsFeed
    newsFeed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")

def print(p):
    global newsFeed
    p.set("RIGHT", "B", "B", 2, 2)
    p.text("News")
    p.text("\n")
    for i, data in enumerate(newsFeed['items']):
        if i > 2:
            break
        else:
            p.set(text_type="U")
            p.text(data['title'] + "\n")
            p.set(text_type="normal")
            p.text(data['summary'] + "\n")
