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


def validate(name):
    users = User.objects.all()
    for user in users:
        if name == user.username:
            raise ValidationError(u'用户名已经存在')
def validator(name):
    pp = re.compile("\w+")
    pa = pp.match(name)
    if pa is None:
        raise ValidationError(u'只能是数字字母下划线')

def activename(name):
    users = User.objects.all()
    if len(name) > 6:
        raise ValidationError(u'昵称不能超过六个字')
    for user in users:
        if name == user.first_name:
            raise ValidationError(u'昵称已经存在')

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', validators=[validate,validator], error_messages={'required':'请输入用户名'})
    first_name = forms.CharField(label='昵称', validators=[activename], error_messages={'required':'请输入昵称'})
    password = forms.CharField(label='密码', widget=forms.PasswordInput, error_messages={'required':'请输入密码'})
    repassword = forms.CharField(label='确认密码', widget=forms.PasswordInput, error_messages={'required':'请确认密码'})
    email = forms.EmailField(label='邮箱', error_messages={'required':'请输入邮箱地址'})
    headimg = forms.FileField(label='头像', error_messages={'required':'请上传头像'})

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
                return HttpResponseRedirect('/login')
            else:
                return HttpResponseRedirect('/regist')
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf})



def index_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/home')
        else:
            return HttpResponseRedirect('/index')
    return render_to_response('index.html',{})

def index_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def home(request):
    user = request.user
    return render_to_response('home.html',{'user':user})