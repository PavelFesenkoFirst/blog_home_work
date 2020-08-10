from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.users.models import CustomUser

# Create your models here.


class Rubrics(models.Model):
    rubric_name = models.CharField(max_length=256, verbose_name='name rubric', )
    slug = models.SlugField(allow_unicode=True, default='', blank=True, )
    in_active = models.BooleanField(default=True, verbose_name='active rubric', )

    class Meta:
        verbose_name = 'rubrics'  # отображение названия модели в админке
        verbose_name_plural = 'rubric'  # во множественном числе
        ordering = ('rubric_name',)

    def __str__(self):
        return f"{self.rubric_name}"

    def get_absolute_url(self):
        return reverse('blog_home_work:rubric-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.rubric_name, allow_unicode=True)
        super().save(*args, **kwargs)

#
# class Authors(models.Model):
#     name = models.CharField(max_length=256, verbose_name='name author', )
#     second_name = models.CharField(max_length=256, verbose_name='surname author', )
#     email = models.EmailField(max_length=256, )
#
#
#     def get_absolute_url(self):
#         return reverse('blog_home_work:author-detail', kwargs={'pk': self.pk})
#
#     class Meta:
#         ordering = ('pk',)
#
#     def __str__(self):
#         return f"{self.name} {self.second_name}"
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#

class Posts(models.Model):
    title = models.CharField(max_length=256, verbose_name='title post', )
    content = models.TextField(verbose_name='content post', )
    image = models.ImageField(verbose_name='image', blank=True, null=True,)
    author_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='author',)
    rubrics_id = models.ForeignKey(Rubrics, on_delete=models.CASCADE, null=True, related_name='rubric',)
    view_rubric = models.IntegerField(verbose_name='quantity views', default=0, )
    show_rubric = models.BooleanField(verbose_name='display', default=True, )
    date_publication = models.DateTimeField(verbose_name='date crated', auto_now_add=True, )
    upd_publication = models.DateTimeField(verbose_name='date update', auto_now=True, )

    class Meta:
        ordering = ('pk',)


    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('blog_home_work:post-detail', kwargs={
            'slug_category': self.rubrics_id.slug,
            'pk': self.pk
        })

    def check_title(self):
        return self.title


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Comments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='author_post',)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post',)
    comment = models.TextField(verbose_name='comment post', )
    date_creat = models.DateTimeField(auto_now_add=True, verbose_name='date created', )

    class Meta:
        ordering = ('pk',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
