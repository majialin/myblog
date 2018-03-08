#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm, Textarea
from django.db import models
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'text': Textarea(attrs={'class': 'form-control', 'rows': 4})
        }