"""setting the saving data file's path."""
# coding=utf-8

sqlite_path = '/home/stan_wp/newsVF/data/VF.sqlite'
error_path = '/home/stan_wp/newsVF/data/error.txt'
article_path = '/home/stan_wp/newsVF/data/article.txt'
number_path = '/home/stan_wp/newsVF/data/numberOfNews.txt'


def get_article_path():
    """"Return the test article path."""
    return article_path


def get_sqlite_path():
    """Return the Database path."""
    return sqlite_path


def get_error_path():
    """"Return the file's path,which contains the error url."""
    return error_path


def get_number_path():
    """"Return the file that saves the number of news for given company."""
    return number_path
