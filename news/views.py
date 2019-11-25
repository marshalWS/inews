from django.shortcuts import render,get_object_or_404
from news.models import news as NEWS
from news.models import news,writer,video,news_user
from django.conf import settings
import markdown
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.template.context_processors import csrf
from .forms import userForm
# Create your views here.
# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import random
from django.core.mail import send_mail
import base64
import misaka
from bs4 import BeautifulSoup
import os
from builtins import list as L
def generate_verification_code_v2():
    ''' 随机生成6位的验证码 '''
    code_list = []
    for i in range(2):
        random_num = random.randint(0, 9) # 随机生成0-9的数字
        # 利用random.randint()函数生成一个随机整数a，使得65<=a<=90
        # 对应从“A”到“Z”的ASCII码
        a = random.randint(65, 90)
        b = random.randint(97, 122)
        random_uppercase_letter = chr(a)
        random_lowercase_letter = chr(b)
        code_list.append(str(random_num))
        code_list.append(random_uppercase_letter)
        code_list.append(random_lowercase_letter)
    verification_code = ''.join(code_list)
    return verification_code


def index(request):
    news_list=NEWS.objects.order_by('-date')[:20]
    img_list=[]
    is_auth=0
    for news in news_list:
        md_render = misaka.Markdown(misaka.HtmlRenderer())
        html = md_render(news.text)
        soup = BeautifulSoup(html, features='html.parser')
        img=soup.find('img')
        if img != None:
            
            img_list.append(img.get('src'))
        else:
            img_list.append('')
    zipped = zip(news_list,img_list)
    zip_list=list(zipped)
    if request.user.is_authenticated:
        user=get_object_or_404(news_user,id=request.user.id)
        is_auth=1
        context={'news_list':zip_list,'user':user,'is_auth':is_auth}
       
    else:
        context={'news_list':zip_list,'img_list':img_list,'is_auth':is_auth}
    return render(request,"index.html" ,context)
    
def detail(request,news_id):
    
    News=news.objects.get(id=news_id)
    V=video.objects.filter(host=News)
    News.text = markdown.markdown(News.text.replace("\r\n", '  \n'),
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    
    
    context={'News':News,'V':V,'MEDIA_URL':settings.MEDIA_URL}   
    return render(request, "detail.html",context)
    
def write(request):
    
    name=request.GET.get("writer_name")
    name=name.replace(" ","")
    w=writer.objects.get(writer_name=name)
    news_list=news.objects.filter(writer=w)
    text=w.text
    context={"text":text,"news_list":news_list,"writer":w}
    return render(request,"writer.html",context)    

class sign_up(FormView):
    form_class=userForm
    template_name = 'base.html'
    success_url='../login'
    extra_context = {'type':'signup'}
    def post(self, request, *args, **kwargs):
        ctx ={}
        ctx.update(csrf(request))
        form=userForm(request.POST)
        if form.is_valid():
            e = request.POST['email']
            un = request.POST['username']
            pw = request.POST['password']
            code=request.POST['code']
            user=get_object_or_404(news_user,email=e)
            if code==user.verify_code:
                user.set_password(pw)
                user.nick_name=un
                user.is_active=True
                user.save()
                group = Group.objects.get(name='reader') 
                group.user_set.add(user)
            else: 
                print()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def sendemail(request):
    address=request.GET.get("email")
    code=generate_verification_code_v2()
    user = news_user.objects.create_user(email=address,password='wjx200022',verify_code=code)
    user.is_active=False
    res=send_mail('verify_code',code,'w13411965905@163.com',[address],fail_silently=False,)
    if res == 1:
            return render(request,'邮件发送成功')
    else:
            return render(request,'邮件发送失败')

def loadmore(request):
    type=request.GET.get('type')
    
    if type != None:
        List=NEWS.objects.filter(style=type).order_by('-date')
    else:
        List = NEWS.objects.order_by('-date')
    p=3
    limit =20
    img_list=[]
    for news in List:
        md_render = misaka.Markdown(misaka.HtmlRenderer())
        html = md_render(news.text)
        soup = BeautifulSoup(html, features='html.parser')
        img=soup.find('img')
        if img != None:
            
            img_list.append(img.get('src'))
        else:
            img_list.append('')
    zipped = zip(List,img_list)
    List=L(zipped)
    paginor = Paginator(List, limit)
    page = request.GET.get('page', p)
    item_info = paginor.page(page)
    news_list=item_info.object_list
    print(news_list)
    context = {'news_list': news_list,}
    template = 'load.html'
    return render(request, template, context)

def page_not_found(request,Exception):
    return render(request, '404.html', status=404)

@login_required
def pesonal(request,user_id):
    user=get_object_or_404(news_user,id=user_id)
    template='person.html'
    context={'user':user}
    return render(request,template,context)
        
def uploadimg(request):
  if request.method == 'POST':
    # 前端ajax请求，将图片对象、图片名称传递到了后台的views.py中；
    img = request.POST.get('imgData')
    type = request.POST.get('type')
    name= request.POST.get('imgname')
    # 再将列表合成一个字符串
    path = ''.join(name)
    print(img)
    i=img.split(',')
    img=i[1]
    url = settings.IMG_URL +path +'.jpg'
 
    img = base64.b64decode(img)
    # 将ajax传过来的图片写入到本地/static/images/....目录下。
    with open(url,'wb+') as f:
      
        f.write(img)
    user=get_object_or_404(news_user,id=request.user.id)
    # 以上步骤实现了图片的后台保存，还需要修改当前用户数据库中的头像路径。
    if type=='headimg':
        user.head_img = path
    else:
        user.bg_img=path
    user.save()
    template='blank.html'
    context={'content':'图片上传成功'}
    print("ok")
    return render(request,template,context)
# 500
def server_error(request):
    return render(request, '500.html', status=500)
def contact(request):
    template='contact.html'
    return render(request, template)

    