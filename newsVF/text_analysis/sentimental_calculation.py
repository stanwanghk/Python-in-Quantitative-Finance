"""Calculate the sentimental value for given text"""
import jieba
# import wordbase
import settings

def HowNet_value(seg):
    seg_value = 0.0
    
    
    return seg_value


def sentimental_value(text):
    paragraphs = text.split('\r\n')
    text_value = 0.0
    for paragraph in paragraphs:
        sentences = paragraph.split('。')
        for sentence in sentences:
            segs = jieba.lcut(sentence,cut_all=False)
            for seg in segs:
                text_value += HowNet_value()
    return text_value


fname = "test.txt"
f = open(fname).read()
print(sentimental_value(f))