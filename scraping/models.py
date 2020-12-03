import jsonfield as jsonfield
from django.db import models
from django.utils.text import slugify

from scraping.utils import from_cyrillic_to_eng


def default_urls():
    return {"work": '',
            'rabota': '',
            'dou': '',
            'djinni': ''}


class City(models.Model):
    name = models.CharField(verbose_name='Название города',
                            max_length=50,
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Название городов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
            # self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(verbose_name='Название языка',
                            max_length=50,
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название ЯП'
        verbose_name_plural = 'Названия языков'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
            # self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(verbose_name='URL', unique=True)
    title = models.CharField(verbose_name='Название вакансии', max_length=250)
    company = models.CharField(verbose_name='Компания', max_length=250)
    description = models.TextField(verbose_name='Описание', max_length=250)
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    # data = models.JSONField()
    data = jsonfield.JSONField()
    # {'url': url, 'code': res.status_code, 'title': 'div has not founded'}


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        # уникальные поля
        unique_together = ("city", 'language')
