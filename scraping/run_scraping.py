import codecs

from scraping.parsers_ua import *

jobs_list, errors = [], []

parsers = (
    (work, 'https://www.work.ua/jobs-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?search=python'),
    (rabota, 'https://rabota.ua/zapros/python/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0'),
    (djinni, 'https://djinni.co/jobs/keyword-python/')
)

for func, url in parsers:
    j, e = func(url)
    jobs_list += j
    errors += e

h = codecs.open('../work.txt', 'w', 'utf-8')
h.write(str(jobs_list))
h.close()
