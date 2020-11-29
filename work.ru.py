import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


domain_ru = 'https://hh.ru'


url_ru = 'https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python'

res = requests.get(url_ru, headers=headers)
jobs_list = []
errors = []


if res.status_code == 200:
    soup = BS(res.content, 'html.parser')
    # main_div = soup.find('div', id='vacancy-serp')
    #print(soup)
    main_div = soup.find('div', id='HH-React-Root')
    #print(main_div)
    if main_div:
        div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
        a = 1
        for div in div_list:
            title = div.find('a')
            href = title.a['href']
            descriptions = div.p.text
            company = 'no name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
                jobs_list.append({'title': title.text, 'url': domain_ru + href,
                                  'description': descriptions, 'company': company})
    else:
        errors.append({'url': url_ru, 'code': res.status_code, 'title': 'div has not founded'})

else:
    errors.append({'url': url_ru, 'code': res.status_code, 'title': 'Page not found'})

print(errors)
h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs_list))
h.close()
