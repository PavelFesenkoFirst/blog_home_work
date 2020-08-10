from django.contrib import admin

from .models import Rubrics, Posts, Comments


# Register your models here.

class PostInline(admin.TabularInline):
    model = Posts
    extra = 0


@admin.register(Rubrics)
class RubricsAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('id', 'rubric_name', 'in_active')


# @admin.register(Authors)
# class AuthorsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'second_name', 'email')


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author_id', 'rubrics_id', 'view_rubric', 'show_rubric',
                    'date_publication', 'upd_publication')


@admin.register(Comments)
class CommetnsAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_id', 'comment', 'date_creat')
