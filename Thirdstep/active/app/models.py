#coding:utf8
from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    headimg = models.FileField(upload_to="./uploadfiles")  #用户头像
    latestlogintime = models.DateTimeField(default=datetime.datetime.now())    #最近一次登录时间

    follow = models.ManyToManyField('Active', related_name='milestone_follow') #用户关注的活动
    join = models.ManyToManyField('Active', related_name='milestone_join')     #用户参加的活动
    zhuanfa = models.ManyToManyField('Active', related_name='milestone_zhuanfa')#用户转发的活动
#    huifu = models.ManyToManyField('Active', related_name='milestone_huifu')#用户回复的活动


    	

class Active(models.Model):
    active_headimg = models.FileField(upload_to='./active_headimg')
    title = models.CharField(max_length=30, verbose_name=u'标题') #活动标题
    date  = models.DateTimeField(default=datetime.datetime.now(),verbose_name=u'时间')
    site = models.CharField(max_length=30, verbose_name=u'活动地点') #活动地点
    cost = models.CharField(max_length=30, verbose_name=u'活动费用') #活动费用
    content = models.TextField() #活动内容
    join_num = models.IntegerField(default=0) #活动参加人数
    follow_num = models.IntegerField(default=0)  #活动关注人数

    choice = models.ForeignKey('Choice')  #活动类别
    user_join = models.ManyToManyField(User,related_name='milestone_join',null=True,blank=True) #参加活动的用户
    user_follow = models.ManyToManyField(User,related_name='milestone_follow',null=True,blank=True) #关注活动的用户
    #active_photo = models.ForeignKey('ActivePhoto', null=True, blank=True)  #活动照片
    
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['-join_num']


class Choice(models.Model):
    choice = models.CharField(max_length=30)  #活动类别名

    def __unicode__(self):
        return self.choice


class Huifu(models.Model):
    active = models.ForeignKey(Active) #回复的活动
    reply = models.TextField()    #活动回复内容
    user = models.ForeignKey(User)  #回复的用户
    
    def __unicode__(self):
        return self.reply


class ActivePhoto(models.Model):
    photofile = models.FileField(upload_to="./Activephoto") #活动照片上传
    p_time = models.DateTimeField(auto_now_add=True)    #照片上传时间
    user = models.ForeignKey(User)   #上传照片的用户
    active = models.ForeignKey(Active)

   
    
class ActiveMedia(models.Model):
    url = models.URLField(blank=True, null=True) #视频的url
    m_time = models.DateTimeField(default=datetime.datetime.now())#视频上传时间
    active = models.ForeignKey(Active)
   

