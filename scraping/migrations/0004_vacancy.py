# Generated by Django 3.1.3 on 2020-11-25 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_auto_20201125_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('title', models.CharField(max_length=250, verbose_name='Название вакансии')),
                ('company', models.CharField(max_length=250, verbose_name='Компания')),
                ('description', models.TextField(max_length=250, verbose_name='Компания')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.city')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.language')),
            ],
        ),
    ]