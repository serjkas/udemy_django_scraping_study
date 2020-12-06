import asyncio
import os, sys

from django.contrib.auth import get_user_model

from scraping.parsers_ua import *

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
# print(f'{proj} \n ')
import django

django.setup()

from django.db import DatabaseError
from scraping.models import Vacancy,  Error, Url

User = get_user_model()

parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (rabota, 'rabota'),
    (djinni, 'djinni')
)
jobs_list, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        # print(tmp)
        url_data = url_dict.get(pair)
        if url_data:
            tmp['url_data'] = url_dict.get(pair)
            urls.append(tmp)

    return urls


async def main(values):
    func, url, city, language = values
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs_list.extend(job)


settings = get_settings()
# print(q)
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
# for data in url_list:
#
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs_list += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs_list:
    # **job формируются\названы ключи в модели так же как и названные поля с парсинга
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save
# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs_list))
# h.close()
