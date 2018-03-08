#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.annotate(Count('post'))
    # 类似于all， annotate返回的依然是包含所有category的queryset，但添加了一列post__count值。

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(Count('post'))