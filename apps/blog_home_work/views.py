from urllib import request

from django.db.models import Count, Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from apps.blog_home_work.forms import PostModelForm
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Comments, Posts, Rubrics #Authors
from datetime import datetime, timezone

from apps.users.models import CustomUser

# Create your views here.

class IndexTemplateView(TemplateView):
    template_name = 'contents/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_qs = Posts.objects.filter(show_rubric=True).order_by('-date_publication')[:5]
        context['post_list'] = post_qs
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.confirm == False:
                return redirect('users:confirm')
        return super().dispatch(request, *args, **kwargs)



# class RubricListView(ListView):
#     template_name = 'contents/rubric_list.html'
#     oder = request.GET.get('order', '-rubric_name')
#     search = request.GET.get('search', '')
#     queryset = Rubrics.objects.filter(
#         rubric_name__contains=search
#     ).order_by(oder)
#
#     def get_context_data(self, request, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['rubric_list'] = 'value'
#         return context


def rubric_list(request):
    context = {}
    user = request.user
    if user.confirm == True:
        # добавляем поиск
        oder = request.GET.get('order', '-rubric_name')
        search = request.GET.get('search', '')
        s_rubrics = Rubrics.objects.filter(
            rubric_name__contains=search
        ).order_by(oder)
        context['rubric_list'] = s_rubrics
        return render(request, 'contents/rubric_list.html', context)
    else:
        return redirect('users:confirm')


def rubric_detail(request, slug):
    context = {}
    rubrics = get_object_or_404(Rubrics, slug=slug)
    posts_qs = Posts.objects.filter(show_rubric=True)
    com = Comments.objects.all()
    post_qq = Posts.objects.all()
    context['rubric'] = rubrics
    context['post_in'] = posts_qs
    context['posts'] = post_qq
    context['com'] = com
    return render(request, 'contents/rubric.html', context)


class PostListView(ListView):
    template_name = 'contents/post_list.html'
    queryset = posts_qs = Posts.objects.filter(show_rubric=True)
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.confirm == False:
                return redirect('users:confirm')
        return super().dispatch(request, *args, **kwargs)

def post_detail(request, pk, slug_category):
    context = {}
    post = Posts.objects.filter(
        pk=pk, rubrics_id__slug=slug_category
    ).first()
    coment_qs = Comments.objects.filter(post_id=pk)
    time = datetime.now(timezone.utc) - post.date_publication

    #пост в простое без просмотров 1час
    if time.seconds > 3600:
        post.view_rubric += 1
        post.save()

    count_view = Posts.objects.get(pk=pk)
    context['cometns'] = coment_qs
    context['posts'] = post
    context['count_view'] = count_view
    return render(request, 'contents/post.html', context)


class AuthorTemplateList(TemplateView):
    template_name = 'contents/author_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_qs = CustomUser.objects.all()
        context['author_list'] = author_qs
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.confirm == False:
                return redirect('users:confirm')
        return super().dispatch(request, *args, **kwargs)


def author_detail(request, pk):
    context = {}
    user = request.user
    if user.confirm == True:
        author_qs = CustomUser.objects.filter(pk=pk)
        count_post = Posts.objects.filter(author_id=pk).aggregate(Count('pk'))['pk__count']
        count_comment = Comments.objects.filter(author=pk).aggregate(Count('pk'))['pk__count']
        last_pub = Posts.objects.filter(author_id=pk).last()
        post_qq = Posts.objects.filter(author_id=pk).aggregate(Sum('view_rubric'))['view_rubric__sum']
        context['comment_author'] = count_comment
        context['author_info'] = author_qs
        context['post_author'] = count_post
        context['total_post'] = post_qq
        context['last'] = last_pub
        return render(request, 'contents/author.html', context)
    else:
        return redirect('users:confirm')


"""попытаться сделать красивей код"""

def post_create(request):
    context = {}
    form = PostModelForm()
    us = request.user
    print(us.confirm)
    if us.confirm == True: #проверка на подтверждение
        if request.method == 'POST':
            form = PostModelForm(request.POST)
            if form.is_valid():
                post_obj = form.save(commit=False)
                post_title = request.POST.get('title')
                post = Posts.objects.filter(title=post_title).order_by('-date_publication') #проверяем есть ли совпадения по заголовкам
                if len(post) == 0:
                    posts_qs = Posts.objects.filter(show_rubric=True).aggregate(Count('pk'))['pk__count']
                    if posts_qs >= 15: #проверяем количество постов
                        Posts.objects.order_by('view_rubric').first().delete()
                        post_obj.author_id = request.user
                        post_obj.save()
                        return HttpResponseRedirect('/')
                    else:
                        post_obj.author_id = request.user
                        post_obj.save()
                        return HttpResponseRedirect('/')
                elif post.first().title == post_title: #если есть совпадения проверяем дату создания поста
                    check_time_range = datetime.now(timezone.utc) - post.first().date_publication
                    if check_time_range.days >= 1:
                        posts_qs = Posts.objects.filter(show_rubric=True).aggregate(Count('pk'))['pk__count']
                        if posts_qs >= 15:
                            Posts.objects.order_by('view_rubric').first().delete()
                            post_obj.author_id = request.user
                            post_obj.save()
                            return HttpResponseRedirect('/')
                        else:
                            post_obj.author_id = request.user
                            post_obj.save()
                            return HttpResponseRedirect('/')
                    else:
                        return HttpResponseRedirect('/')
                else:
                    post_obj.author_id = request.user
                    post_obj.save()
                    return HttpResponseRedirect('/')
        else:
            context['form'] = form
            return render(request, 'contents/post_create.html', context)
    else:
        return redirect('users:confirm')
