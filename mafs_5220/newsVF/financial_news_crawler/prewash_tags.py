# coding=utf-8
import re

# these code follows from littlebai's blog
# here are the link:
# http://www.cnblogs.com/rails3/archive/2012/08/14/2636780.html


def remove_adv(s):
    advs = set()
    advs.add('牛人大赛】快来腾讯证券官号（qqzixuangu）参赛啦！点击“话费天天送”，话费、苹果电脑大派送，更有三重奖等你拿！')
    advs.add('更多精彩内容欢迎搜索关注微信公众号：腾讯财经（financeapp）。')
    advs.add('最牛操盘手策略曝光投顾大师赛：大跌依旧抓涨停跟叶智华解套')
    for adv in advs:
        re_adv = re.compile(adv)
        s = re_adv.sub('', s)
    return s


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
    re_strong = re.compile('</?strong>')
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_p.sub('\r\n', s)  # 将<p>转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    s = re_strong.sub('', s)
    blank_line = re.compile('\n+')  # 去掉多余的空行
    s = blank_line.sub('\n', s)
    return s

# data = """<span class=\"a_source\" bosszone=\"jgname\"><a target=\"_blank\" href=\"http://www.ccstock.cn/\">证券日报</a></span>"""
# print(remove_tags(data))
