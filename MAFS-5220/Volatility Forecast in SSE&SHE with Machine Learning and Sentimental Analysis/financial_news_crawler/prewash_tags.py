# coding=utf-8
import re
from bs4 import BeautifulSoup

# these code are from littlebai's blog
# here are the link:
# http://www.cnblogs.com/rails3/archive/2012/08/14/2636780.html


def remove_tags(htmlstr):
    # print(htmlstr)
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    # re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    re_script = re.compile(r'<script.+</script>', re.DOTALL)
    # re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    re_style = re.compile(r"<style.+</style>", re.DOTALL)
    re_p = re.compile('<P\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>].*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_p.sub('\r\n', s)  # 将<p>转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    blank_line = re.compile('\n+')  # 去掉多余的空行
    s = blank_line.sub('\n', s)
    return s


def choose_tags(soup):
    print('choose_tags')
    tags = soup.find_all('p', style=True)
    content = ''
    for tag in tags:
        content = remove_tags(repr(tag.get_text()))
        print(content+'\r\n')
    return content

