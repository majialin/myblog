#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^post/(?P<uri>[0-9a-zA-Z%_-]+)', views.detail, name='detail'), 弃用
    url(r'^post/(?P<uri>.+)', views.detail, name='detail'),
    url(r'^archives/(?:(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2}))?$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<cate>\w+)', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<cate>\w+)', views.TagView.as_view(), name='tag'),
    url(r'^search$', views.SearchView.as_view(), name='search'),
]
