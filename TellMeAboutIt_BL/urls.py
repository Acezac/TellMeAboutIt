from django.conf.urls import patterns, url

from TellMeAboutIt_BL import views

urlpatterns = patterns('',
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='user_logout'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^complaints/$', views.index2, name='index2'),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^showComments/$', views.showComments, name='showComments'),
                       url(r'^comments/$', views.showComments, name='showComments'),
                       url(r'^PopuPcomments/$', views.PopuPcomments, name='PopuPcomments'),
                       url(r'^postComment/$', views.postComment, name='postComment'),
                       url(r'^rating/$', views.rating, name='rating'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^contactus/$', views.contactus, name='contactus'),
                       url(r'^recent/$', views.recent, name='recent'),
                       url(r'^popular/$', views.popular, name='popular'),
                       url(r'^mostCommenting/$', views.mostCommenting, name='mostCommenting'),

                       )


