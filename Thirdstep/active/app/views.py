#coding:utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms
from app.models import *
import re

'''去除注册帐号相同问题'''
def validate(name):
    users = User.objects.all()
    for user in users:
        if name == user.username:
            raise ValidationError(u'用户名已经存在')

'''规定注册帐号组成'''
def validator(name):
    pp = re.compile("\w+")
    pa = pp.match(name)
    if pa is None:
        raise ValidationError(u'只能是数字字母下划线')

'''规定注册帐号字数'''
def activename(name):
    users = User.objects.all()
    if len(name) > 6:
        raise ValidationError(u'昵称不能超过六个字')
    for user in users:
        if name == user.first_name:
            raise ValidationError(u'昵称已经存在')

'''注册表单'''
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', validators=[validate,validator], error_messages={'required':'请输入用户名'})
    first_name = forms.CharField(label='昵称', validators=[activename], error_messages={'required':'请输入昵称'})
    password = forms.CharField(label='密码', widget=forms.PasswordInput, error_messages={'required':'请输入密码'})
    repassword = forms.CharField(label='确认密码', widget=forms.PasswordInput, error_messages={'required':'请确认密码'})
    email = forms.EmailField(label='邮箱', error_messages={'required':'请输入邮箱地址'})
    headimg = forms.FileField(label='头像', error_messages={'required':'请上传头像'})


'''注册'''
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            repassword = uf.cleaned_data['repassword']
            email = uf.cleaned_data['email']
            headimg = uf.cleaned_data['headimg']
            first_name = uf.cleaned_data['first_name']
            if password == repassword:
                user = User.objects.create_user(username,email,password)
                user.first_name = first_name
                user.save()
                UserProfile.objects.create(headimg=headimg,user=user)
                return HttpResponseRedirect('/index')    #注册成功跳转到主页
            else:
                return HttpResponseRedirect('/regist')   #失败返回注册界面
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf})


'''登录（在公共主页上）'''
def index_login(request):
    choices = Choice.objects.all()
    actives = Active.objects.order_by('-id')
    hot_actives = Active.objects.order_by('-join_num')[0:3]   #热门活动根据参加的人数的多少来获取，我这里只是在主页显示2个代表一下
    cai_actives = Active.objects.order_by('-follow_num')[0:3] #猜你喜欢的活动根据关注的人数的多少来获取

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/home')   #登录成功跳到home界面
        else:
            return HttpResponseRedirect('/index')  #登录失败跳到登录主页

    return render_to_response('index.html',{'choices':choices,'actives':actives,'hot_actives':hot_actives,'cai_actives':cai_actives})


'''退出'''
def index_logout(request):
    logout(request)
    return HttpResponseRedirect('/index')       #退出跳到主页


'''登录进去后的主页'''
def home(request):
    user = request.user
    choices = Choice.objects.all()
    actives = Active.objects.order_by('-id')
    hot_actives = Active.objects.order_by('-join_num')[0:3]   #热门活动根据参加的人数的多少来获取，我这里只是在主页显示2个代表一下
    cai_actives = Active.objects.order_by('-follow_num')[0:3] #猜你喜欢的活动根据关注的人数的多少来获取
    return render_to_response('home.html',{'user':user,'choices':choices,'actives':actives,'hot_actives':hot_actives,'cai_actives':cai_actives})

'''热门活动'''
def hot_actives(request):
    hot_actives = Active.objects.order_by('-join_num')[0:10]
    return render_to_response('hot_actives.html',{'hot_actives':hot_actives})

'''猜你喜欢活动'''
def cai_actives(request):
    cai_actives = Active.objects.order_by('-follow_num')[0:10]
    return render_to_response('cai_actives.html',{'cai_actives':cai_actives})

'''用户页'''
def userpage(request):
    user = request.user
    return render_to_response('userpage.html',{'user':user})

'''用户信息页'''
def user_info(request):
    user = request.user
    return render_to_response('user_info.html',{'user':user})


class ChangeForm(forms.Form):
    username = forms.CharField(label='用户名', validators=[validate,validator], error_messages={'required':'请输入用户名'})
    first_name = forms.CharField(label='昵称', validators=[activename], error_messages={'required':'请输入昵称'})
    password = forms.CharField(label='密码', widget=forms.PasswordInput, error_messages={'required':'请输入密码'})
    email = forms.EmailField(label='邮箱', error_messages={'required':'请输入邮箱地址'})
    headimg = forms.FileField(label='头像', error_messages={'required':'请上传头像'})

'''ChangeInfo'''
def changeinfo(request):
    user = request.user
    if request.method == 'POST':
        cf = ChangeForm(request.POST,request.FILES)
        if cf.is_valid():
            username = cf.cleaned_data['username']
            password = cf.cleaned_data['password']
            email = cf.cleaned_data['email']
            headimg = cf.cleaned_data['headimg']
            first_name = cf.cleaned_data['first_name']
            user.username = username
            user.email = email
            user.first_name = first_name
            user.set_password(password)
            user.get_profile().headimg = headimg
            user.save()
            user.get_profile().save()
            return HttpResponseRedirect('/index')    #注册成功跳转到主页
    else:
        cf = ChangeForm(initial={'username':user.username,'first_name':user.first_name,'password':user.password,'email':user.email,'headimg':user.get_profile().headimg})
    return render_to_response('changeinfo.html',{'cf':cf,'user':user})