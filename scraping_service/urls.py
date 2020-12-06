from django.contrib import admin
from django.urls import path, include
from scraping.views import home_view, list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', list_view, name='list'),
    # 1 подлкючаем юрл, а второе пространство имен
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('', home_view, name='home'),




]
