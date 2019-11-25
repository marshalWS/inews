'''
Created on 2019年10月28日

@author: asus
'''
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import feeds
from django.contrib.auth import views as auth_views
app_name='news'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/',views.sign_up.as_view(),name='signUp'),
    path('login/',auth_views.LoginView.as_view(template_name='base.html',extra_context = {'type':'login'}),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='base.html',extra_context = {'type':'logout'}),name='logout'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='base.html',extra_context = {'type':'login'}),name='change_password'),
    path('<int:news_id>/',views.detail,name="detail"),
    path('writer/',views.write,name="writer"),
    path('loadmore/', views.loadmore, name='loadmore'),
    path('sendEmail/',views.sendemail,name='email'),
    path('rss/',feeds.LatestNewsFeed(),name='rss'),
    path('user/<int:user_id>',views.pesonal,name='user'),
    path('uploadimg/',views.uploadimg,name="upload"),
    path('contact/',views.contact,name="contact"),
    
    ]
