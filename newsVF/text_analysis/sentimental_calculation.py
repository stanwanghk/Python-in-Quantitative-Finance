"""Calculate the sentimental value for given text"""
import jieba
import settings


def get_sentimental_value(text, wordsbase):
    paragraphs = text.split('\r\n')
    text_value = 0.0
    for paragraph in paragraphs:
        paragrah_value = 0.0
        
    return text_value


fname = "test.txt"
f = open(fname).read()
print(sentimental_value(f))
