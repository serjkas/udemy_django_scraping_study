from django.db import models
from django.utils.text import slugify


from scraping.utils import from_cyrillic_to_eng


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
            # self.slug = from_cyrillic_to_eng(str(self.name))
            self.slug = slugify(self.name)
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

    def __str__(self):
        return self.title