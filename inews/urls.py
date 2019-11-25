"""inews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls import *
from django.conf import settings
import django.views
import django.contrib.auth.urls
from django.contrib.sitemaps.views import sitemap as s
from news import views
from django.contrib.sitemaps import GenericSitemap
from news.models import news
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as v
from django.views import static as ds
info_dict = {
    'queryset': news.objects.all(),
    'date_field': 'date',
}

sitemap={'news': GenericSitemap(info_dict, priority=0.6,changefreq = 'daily')}
urlpatterns = [
    path('', include('news.urls')),
    path('admin/', admin.site.urls),
    path('mdeditor/', include('mdeditor.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml/', s, {'sitemaps': sitemap},name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap-<int:section>\.xml', v.sitemap, {'sitemaps': sitemap},name='django.contrib.sitemaps.views.sitemap'),
]
if settings.DEBUG: 
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^media/(?P<path>.*)$', 
           django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),   
            url(r'^static/(?P<path>.*)$',
          django.views.static.serve,{'document_root':settings.STATIC_ROOT})]
    
handler404 = views.page_not_found
handler500 = views.server_error