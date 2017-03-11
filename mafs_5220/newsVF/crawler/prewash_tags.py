# coding=utf-8
import re
import settings

# these code follows from littlebai's blog
# here are the link:
# http://www.cnblogs.com/rails3/archive/2012/08/14/2636780.html


def remove_adv(s):
    # print(s)
    fname = settings.get_adv_path()
    f = open(fname).read()
    advs = f.split('\n')
    for adv in advs:
        # print(adv)
        re_adv = re.compile(adv)
        s = re_adv.sub('', s)
    # print(s)
    return s


def remove_tags(htmlstr):
    # print(htmlstr)
    re_cdata = re.compile('//<!\[CDATA\[[^>]*?//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile(r'<script.*?</script>', re.DOTALL)
    re_style = re.compile(r'<style.*?</style>', re.DOTALL)
    re_comment = re.compile('<!--/?.*?-->', re.DOTALL)  # HTML注释
    re_h = re.compile('</?\w+[^>]*?>')  # HTML标签
    re_p = re.compile('</p>')  # 处理换行
    re_strong = re.compile('</?strong>')

    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_comment.sub('', s)  # 去掉HTML注释

    s = re_p.sub('\n', s)  # 将</p>转换为换行
    s = re_strong.sub('', s)  # remove <strong>

    s = re_h.sub('', s)  # 去掉HTML 标签
    
    s = remove_adv(s)
    re_head = re.compile('^[\n]*')
    blank_line = re.compile('\n{2,}')  # 去掉多余的空行
    s = re_head.sub('', s)
    s = blank_line.sub('\n', s)  # remove the adv
    # print(s)
    return s


# data = 
# print(remove_tags(data))
