"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path,re_path

from .views import (
    IndexTemplateView, AuthorTemplateList, post_create,
    rubric_detail, rubric_list, PostListView, post_detail, author_detail
                    )
app_name = 'blog_home_work'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('rubric/', rubric_list, name='rubric-list'),
    path('rubric/<slug>/', rubric_detail, name='rubric-detail'),
    #path('rubric/<slug>/', rubric_show, name='rubric-show')
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/<slug_category>/<pk>', post_detail, name='post-detail'),
    path('author', AuthorTemplateList.as_view(), name='author-list'),
    path('author/<pk>', author_detail, name='author-detail'),
    path('post_create/', post_create, name='post-create'),
]
