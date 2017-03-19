"""Load the error information, and execute the crawler again for the error."""
import settings
import data_load as dl
# import crawler.tencent_news_crawler as tnc


error_company = []
number_url = 0

fname = settings.get_error_path()
ferror = open(fname, 'a')
ferror.write('correct error' + '\r\n')
ferror.close()

ferror = open(fname).read()
errors = ferror.split('\n')

for error in errors:
    if 'correct error' in error:
        break
    if 'http' in error:
        # tnc.get_qq_news(error[:8], error[9:])
        number_url += 1
    else:
        error_company.append(error[20:])

print(number_url)
dl.news_load(error_company)
