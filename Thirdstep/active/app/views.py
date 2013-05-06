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
from django import http
import datetime,time

def admin_info(request):
    return render_to_response('admin_info.html',{'request':request})

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
                return HttpResponseRedirect('/base')    #注册成功跳转到主页
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
            return HttpResponseRedirect('/base')   #登录成功跳到home界面
        else:
            return HttpResponseRedirect('/base')  #登录失败跳到登录主页

    return render_to_response('base.html',{'request':request,'choices':choices,'actives':actives,'hot_actives':hot_actives,'cai_actives':cai_actives})


'''退出'''
def index_logout(request):
    logout(request)
    return HttpResponseRedirect('/base')       #退出跳到主页


#'''登录进去后的主页'''
#def home(request):
#    user = request.user
#    choices = Choice.objects.all()
#    actives = Active.objects.order_by('-id')
#    hot_actives = Active.objects.order_by('-join_num')[0:3]   #热门活动根据参加的人数的多少来获取，我这里只是在主页显示2个代表一下
#    cai_actives = Active.objects.order_by('-follow_num')[0:3] #猜你喜欢的活动根据关注的人数的多少来获取
#    return render_to_response('home.html',{'user':user,'choices':choices,'actives':actives,'hot_actives':hot_actives,'cai_actives':cai_actives})

'''热门活动'''
def hot_actives(request):
    hot_actives = Active.objects.order_by('-join_num')[0:10]
    return render_to_response('hot_actives.html',{'request':request,'hot_actives':hot_actives})

'''猜你喜欢活动'''
def cai_actives(request):
    cai_actives = Active.objects.order_by('-follow_num')[0:10]
    return render_to_response('cai_actives.html',{'request':request,'cai_actives':cai_actives})

'''用户页(默认关注的活动页)'''
def userpage(request):
    if request.user.is_authenticated():
    	user = request.user
    	follow_actives = user.get_profile().follow.all
    	return render_to_response('userpage.html',{'request':request,'user':user,'follow_actives':follow_actives})
    else:
    	return HttpResponseRedirect('/base')	


'''用户加入的活动页'''
def userpage_join(request):
    if request.user.is_authenticated():
    	user = request.user
    	join_actives = user.get_profile().join.all
    	return render_to_response('userpage_join.html',{'request':request,'user':user,'join_actives':join_actives})
    else:
        return HttpResponseRedirect('/base')

'''用户分享的活动页'''
def userpage_fenxiang(request):
    if request.user.is_authenticated():
    	user = request.user
    	fenxiang_actives = user.get_profile().zhuanfa.all
    	return render_to_response('userpage_fenxiang.html',{'request':request,'user':user,'fenxiang_actives':fenxiang_actives})
    else:
    	return HttpResponseRedirect('/base')

'''用户评论的活动页'''  ###此功能需要修改  重置数据库
def userpage_reply(request):
    user = request.user
    huifus = Huifu.objects.filter(user=user)
    
    return render_to_response('userpage_reply.html',{'request':request,'user':user,'huifus':huifus})

'''用户留念的活动页'''   ###此功能需要改进
def userpage_liunian(request):
    if request.user.is_authenticated():
    	join_actives = request.user.get_profile().join.all
    	return render_to_response('userpage_liunian.html',{'join_actives':join_actives,'request':request})
    else:
    	return HttpResponseRedirect('/base')

'''活动留念照片'''
def active_liunian(request,aid):
    active = Active.objects.get(id=aid)
    activemedias = active.activemedia_set.all()
    active_photos = active.activephoto_set.all()
    return render_to_response('active_liunian.html',{'active_photos':active_photos,'activemedias':activemedias,'request':request,'active':active})
def active_liunian1(request,aid):
    if request.method == 'POST':
        active = Active.objects.get(id=aid)
    	user = request.user
    	img = request.FILES.get('img')
    	ActivePhoto.objects.create(photofile=img,user=user,active=active)
    return http.HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))    
'''活动留念视频'''
def active_liunian2(request):
    if request.method == 'POST':
    	id = request.POST['aid']
        active = Active.objects.get(id=id)
        url = request.POST['url']
        user = request.user
        ActiveMedia(url=url,active=active).save()
    return http.HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))    
'''用户信息页'''
def user_info(request):
    user = request.user
    return render_to_response('user_info.html',{'request':request,'user':user})


'''去除修改用户信息相同问题'''
def validate1(name):
    users = User.objects.exclude(username=name)
    for user in users:
        if name == user.username:
            raise ValidationError(u'用户名已经存在')

'''规定修改用户信息组成'''
def validator1(name):
    pp = re.compile("\w+")
    pa = pp.match(name)
    if pa is None:
        raise ValidationError(u'只能是数字字母下划线')

'''规定修改用户信息字数'''
def activename1(name):
    users = User.objects.exclude(first_name=name)
    if len(name) > 6:
        raise ValidationError(u'昵称不能超过六个字')
    for user in users:
        if name == user.first_name:
            raise ValidationError(u'昵称已经存在')

'''修改用户信息表单'''
class ChangeForm(forms.Form):
    username = forms.CharField(label='用户名', validators=[validate1,validator1], error_messages={'required':'请输入用户名'})
    first_name = forms.CharField(label='昵称', validators=[activename1], error_messages={'required':'请输入昵称'})
    password = forms.CharField(label='密码', widget=forms.PasswordInput, error_messages={'required':'请输入密码'})
    email = forms.EmailField(label='邮箱', error_messages={'required':'请输入邮箱地址'})
    headimg = forms.FileField(label='头像', error_messages={'required':'请上传头像'})

'''修改用户信息'''
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
            return HttpResponseRedirect('/base')    #注册成功跳转到主页
    else:
        cf = ChangeForm(initial={'username':user.username,'first_name':user.first_name,'password':user.password,'email':user.email,'headimg':user.get_profile().headimg})
    return render_to_response('changeinfo.html',{'request':request,'cf':cf,'user':user})


'''活动详情'''
def active_info(request,aid):
    user = request.user
    active = Active.objects.get(id=aid)
    
    #if request.method == 'POST':
    #	reply = request.POST['reply']
    #    Huifu.objects.create(reply=reply,user=user,active=active)
    return render_to_response('active_info.html',{'request':request,'active':active,'user':user})


'''活动搜索功能'''
def active_search(request):
    hot_actives = Active.objects.order_by('-join_num')[0:3]   #热门活动根据参加的人数的多少来获取，我这里只是在主页显示2个代表一下
    cai_actives = Active.objects.order_by('-follow_num')[0:3] #猜你喜欢的活动根据关注的人数的多少来获取
    if request.method == 'POST':
        active_name = request.POST['active_name']
        actives = Active.objects.all().filter(title__icontains=active_name)
    return render_to_response('active_search.html',{'hot_actives':hot_actives,'cai_actives':cai_actives,'request':request,'actives':actives})

'''按主页活动分类搜索'''
def index_choice_search(request,cid,time=None):
    today = datetime.date.today()
    print today
    tomorrow = today + datetime.timedelta(days=1)
    houtian = today + datetime.timedelta(days=2)
    week = today + datetime.timedelta(days=7)
    choice = Choice.objects.get(id=cid)
    choices = Choice.objects.all()
    if time:
        if time == week:
            today = today.strftime("%Y-%m-%d")
            actives = choice.active_set.filter(date_gta=today) and choice.active_set.filter(date_lte=time)
            
    	else:
            pass
             #date_joined__monthx=datetime.datetime.now().month, date_joined__day=datetime.datetime.now().day 
            #actives = choice.active_set.filter(date_gta=time) and choice.active_set.filter(date_lte=time1)
            
    else:
	actives = choice.active_set.all()
    return render_to_response('index_choice_search.html',{'request':request,'actives':actives,'choices':choices,'cid':cid,'today':today,'tomorrow':tomorrow,'houtian':houtian,'week':week})

'''活动回复'''
def active_reply(request):
    if request.method == 'POST':
        user = request.user
    	reply = request.POST['reply']
        id = request.POST['active_id']
        active = Active.objects.get(id=id)
        huifu = Huifu.objects.create(reply=reply,user=user,active=active) 
 
        #Reply.objects.create(reply=reply,user=user,active=active)此处需要重置表
    	return http.HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))    

'''参加活动'''
def join_active(request):
    if request.method == 'POST':
    	id = request.POST['id']
        user = request.user
        active = Active.objects.get(id=id)
        user.get_profile().join.add(active)
        active.user_join.add(user)
        active.join_num += 1
        active.save() 
    	return http.HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

'''取消参加活动'''
def deljoin_active(request):
    if request.method == 'POST':
    	id = request.POST['id']
        user = request.user
        active = Active.objects.get(id=id)
        user.get_profile().join.remove(active) 
        active.user_join.remove(user)
        active.join_num -= 1
        active.save() 
    	return http.HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        

'''关注活动'''
from django import http
def follow_active(request):
    if request.method == 'POST':
    	id = request.POST['id']
        user = request.user
        active = Active.objects.get(id=id)
        user.get_profile().follow.add(active)
        active.user_follow.add(user)
        active.follow_num += 1
        active.save() 
    	return http.HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

'''取消关注活动'''
def delfollow_active(request):
    if request.method == 'POST':
    	id = request.POST['id']
        user = request.user
        active = Active.objects.get(id=id)
        user.get_profile().follow.remove(active) 
	active.user_follow.remove(user)
        active.follow_num -= 1
        active.save() 
    	return http.HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


'''活动参加的用户列表'''
def join_user(request,jid):
    active = Active.objects.get(id=jid)
    users = active.user_join.all
    return render_to_response('join_user.html',{'request':request,'active':active,'users':users})



'''活动关注的用户列表'''
def follow_user(request,fid):
    active = Active.objects.get(id=fid)
    users = active.user_follow.all()
    return render_to_response('follow_user.html',{'request':request,'active':active,'users':users})
