from django.db import models
from mdeditor.fields import MDTextField
from django.conf import settings
from django.utils import timezone
from builtins import str
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.urls import reverse
# Create your models here.


class writer(models.Model):
    writer_name=models.CharField(max_length=50,primary_key=True,verbose_name="name")
    text=models.CharField(max_length=200)
    password=models.CharField(max_length=20)
    activate_choice=((0,'false'),(1,'true'))
    is_active=models.IntegerField(default=0,choices=activate_choice)
    def __str__(self):
        return self.writer_name
    def text(self):
        return self.text
class news_user(User):
    introduce=models.CharField(max_length=200)
    nick_name=models.CharField(max_length=20)
    verify_code=models.CharField(max_length=10)
    head_img = models.CharField(max_length=100)
    bg_img=models.CharField(max_length=100)
    def __str__(self):
        
        return self.nick_name

class news(models.Model):
    style_chioces=(('科技','tech'),('时政','political'),('经济','ecomony'),('军事','military'))
    style=models.CharField(max_length=6,choices=style_chioces)
    news_title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    text=MDTextField(max_length=5000)
    writer=models.ForeignKey(writer,on_delete=models.CASCADE)
    '''author = models.ForeignKey(
        news_user,
        on_delete=models.CASCADE,
        
    )'''
    def __str__(self):
        return self.news_title
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'news_id': self.id})
    
class video(models.Model):
    video_path=models.FileField(upload_to=settings.FILE_URL,verbose_name="视频")
    name=models.CharField(max_length=50,default=timezone.now)
    host=models.ForeignKey(news,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.video_path)

class img(models.Model):
    position=models.CharField(max_length=50)
    host=models.ForeignKey(news,on_delete=models.CASCADE)
    def __str__(self):
        return self.position


    