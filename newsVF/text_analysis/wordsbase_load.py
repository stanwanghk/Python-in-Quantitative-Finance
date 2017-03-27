"""Load the words base to sentiment analysis."""
import settings


def get_mix_wordsbase(set_name):
    file = settings.get_sentiment_files(set_name)
    if set_name is 'modifiers':
        f = open(file, encoding='GBK')
    else:
        f= open(file,encoding='utf-8')
    if set_name is not 'modifiers':
        set_wordsbase = set()
        start = 0
        for line in f:
            if start < 2:
                start += 1
            else:
                line = line.strip()
                set_wordsbase.add(line)
    else:
        set_wordsbase = {}
        index = 0
        start = 0
        # set_level = set()
        for raw in f:
            if start < 2:
                start += 1
            else:               
                if str(index+1) in raw:
                    if index > 0:
                        set_wordsbase[level] = set_level
                    index += 1
                    level = 'level{}'.format(index)
                    set_level = set()
                else:
                    raw = raw.strip()
                    if raw is not "":
                        set_level.add(raw.strip())
        set_wordsbase['level6'] = set_level
    return set_wordsbase


def get_wordsbase():
    """Return the given wordsbase as a dict."""
    sets = ['positive','negative','privative','modifiers']
    wordsbase ={}
    for set_name in sets:
        wordsbase[set_name] = get_mix_wordsbase(set_name)
    return wordsbase
