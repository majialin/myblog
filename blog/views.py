from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Q

# Create your views here.
'''
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html',{'post_list': post_list})
# 使用ListView类视图重写
'''

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def paginate_queryset(self, queryset, page_size):
        paginator, page, object_list, is_paginated = super().paginate_queryset(queryset, page_size)
        # 用来显示类似 1 ... 3, 4 ,5 ,6 ,7 ,8, 9, 10, 11 ... 114 这样的分页
        # 对应 left ... middle ... right ，使用page的属性来保存
        page.left, page.right = 1, paginator.num_pages
        page.middle = [x for x in range(page.number-4, page.number+5) if x in range(1, paginator.num_pages+1)]
        if page.middle[0] == 1:
            page.left = False
        if page.middle[-1] == paginator.num_pages:
            page.right = False
        return (paginator, page, object_list, is_paginated)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'current': 'article'})
        return context

def detail(request, uri):
    from django.utils.encoding import uri_to_iri
    post = get_object_or_404(Post, uri=uri_to_iri(uri))
    post.increase_views() # 阅读量+1
    comment_form = CommentForm()
    context = {'post': post,
               'form': comment_form}
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # commit=False 使表单不保存到数据库
            # 因为是带Forreign Key的， 稍后添加外键再保存
            comment.post = post
            comment.save()
        else:
            # 如果数据不合法
            # 返回带form数据的detail页面
            context['form'] = form

    context['comment_list'] = post.comment_set.all()
    return render(request, 'blog/detail.html',context)


class PostDetailView(DetailView):
    model = Post
    template_name =  'blog/detail.html'
    context_object_name =  'post'

    def get_object(self):
        post = super(PostDetailView, self).get_object()
        post.increase_views()
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        # self.object 即对应的post, 在get_object之后被赋值。
        context.update({
            'form':form,
            'comment_list': comment_list,
            'current': 'article'
        })
        return context

'''
def archives(request, year, month):
    post_list = Post.objects.filter( created_time__year=year,
                                     created_time__month=month
                                     ).order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})
'''

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/archives.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year, month = self.kwargs['year'], self.kwargs['month']
        if year and month:
            return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)
        else:
            return super(ArchivesView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(ArchivesView, self).get_context_data(**kwargs)
        context.update({'current': 'archives'})
        return context


'''
def category(request, cate):
    post_list = Post.objects.filter(category__name=cate).order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})
'''

class CategoryView(IndexView):
    def get_queryset(self):
        cate = self.kwargs.get('cate')
        return super(CategoryView, self).get_queryset().filter(category__name=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return super(TagView, self).get_queryset().filter(tag__name=tag)

class SearchView(IndexView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        return super().get_queryset().filter(Q(title__icontains=q)|Q(body__icontains=q))



