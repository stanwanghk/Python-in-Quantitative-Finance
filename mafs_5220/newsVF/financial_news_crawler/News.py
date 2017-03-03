# coding: utf-8


# define the structure of the finanical news
class News(object):
    def __init__(self):
        self.success = True
        self.url = None
        self.title = None
        self.newsid = None
        self.author = None
        self.pubdate = None
        self.about = None
        self.content = None
        self.source = None
