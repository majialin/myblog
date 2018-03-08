from django.db import models
from django.contrib.auth.models import User

from markdown import Markdown
from markdown.extensions.toc import TocExtension
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.encoding import iri_to_uri


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)

    views = models.PositiveIntegerField(default=0)
    body_md = models.TextField(editable=False, blank=True) # 保存markdown处理后的文本，即带html格式
    body_toc = models.TextField(editable=False, blank=True) # markdown处理后的目录
    excerpt = models.CharField(max_length=200, editable=False, blank=True)
    uri = models.CharField(max_length=600, editable=False, blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:detail', kwargs={'uri': self.uri})
    def increase_views(self):
        self.views = self.views + 1
        self.save(update_fields=['views'])
    def save(self, *args, **kwargs):
        md = Markdown(extensions=['markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  TocExtension(slugify=slugify)])
        self.body_md = md.convert(self.body)
        self.body_toc = md.toc
        self.excerpt = strip_tags(self.body_md)[:54]
        self.uri = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)

    def __str__(self):
        return self.text[:20]