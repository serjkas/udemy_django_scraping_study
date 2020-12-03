import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def work(url, city=None, language=None):
    jobs_list = []
    errors = []
    domain_ua = 'https://www.work.ua'
    if url:
        # url = 'https://www.work.ua/jobs-python/'

        res = requests.get(url, headers=headers[randint(0, 2)])

        if res.status_code == 200:
            soup = BS(res.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                # for debug
                a = 1
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    descriptions = div.p.text
                    company = 'no name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                        jobs_list.append({'title': title.text, 'url': domain_ua + href,
                                          'description': descriptions, 'company': company,
                                          'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'code': res.status_code, 'title': 'div has not founded'})
        else:
            errors.append({'url': url, 'code': res.status_code, 'title': 'Page not found'})
    return jobs_list, errors


def rabota(url, city=None, language=None):
    jobs_list = []
    errors = []
    domain_ua = 'https://rabota.ua'
    if url:
        res = requests.get(url, headers=headers[randint(0, 2)])

        if res.status_code == 200:
            soup = BS(res.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs:
                table = soup.find('table', id='ctl00_content_vacancyList_gridList')
                if table:
                    tr_list = table.find_all('tr', attrs={'id': True})
                    # for debug
                    a = 1
                    for tr in tr_list:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('h2', attrs={'class': 'card-title'})

                            href = title.a['href']
                            descriptions = div.p.text
                            company = 'no name'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text
                                jobs_list.append({'title': title.text, 'url': domain_ua + href,
                                                  'description': descriptions, 'company': company,
                                                  'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'code': res.status_code, 'title': 'div has not founded'})
            else:
                errors.append({'url': url, 'code': res.status_code, 'title': 'Page empty'})

        else:
            errors.append({'url': url, 'code': res.status_code, 'title': 'Page not found'})
    return jobs_list, errors


def dou(url, city=None, language=None):
    jobs_list = []
    errors = []
    domain_ua = 'https://jobs.dou.ua'
    # url = 'https://www.work.ua/jobs-python/'
    # https://jobs.dou.ua/vacancies/?search=python
    if url:
        res = requests.get(url, headers=headers[randint(0, 2)])

        if res.status_code == 200:
            soup = BS(res.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                div_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                # for debug
                a = 1
                for li in div_list:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'sh-info'})
                    descriptions = cont.text
                    company = 'no name'
                    a = title.find('a', attrs={'class': 'company'})
                    if a:
                        company = a.text
                        jobs_list.append({'title': title.text, 'url': href,
                                          'description': descriptions, 'company': company,
                                          'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'code': res.status_code, 'title': 'div has not founded'})
        else:
            errors.append({'url': url, 'code': res.status_code, 'title': 'Page not found'})
    return jobs_list, errors


def djinni(url, city=None, language=None):
    jobs_list = []
    errors = []
    domain_ua = 'https://djinni.co'
    # url = 'https://www.work.ua/jobs-python/'
    # https://jobs.dou.ua/vacancies/?search=python
    # https://djinni.co/jobs/keyword-python/kyiv/
    if url:
        res = requests.get(url, headers=headers[randint(0, 2)])

        if res.status_code == 200:
            soup = BS(res.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                # for debug
                a = 1
                for li in li_list:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'list-jobs__description'})
                    descriptions = cont.text
                    company = 'no name'
                    comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                    if a:
                        company = comp.text
                        jobs_list.append({'title': title.text, 'url': domain_ua + href,
                                          'description': descriptions, 'company': company,
                                          'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'code': res.status_code, 'title': 'div has not founded'})
        else:
            errors.append({'url': url, 'code': res.status_code, 'title': 'Page not found'})
    return jobs_list, errors


if __name__ == '__main__':
    print("start parsing")
    url = 'https://djinni.co/jobs/keyword-python/kyiv/'
    jobs_list, errors = djinni(url)

    h = codecs.open('../work.txt', 'w', 'utf-8')
    h.write(str(jobs_list))
    h.close()
