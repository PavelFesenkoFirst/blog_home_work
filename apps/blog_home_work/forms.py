from django import forms

from apps.blog_home_work.models import Posts

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea({'cols': 120, 'rows': 3}))
    class Meta:
        model = Posts
        fields = ('title', 'content', 'image', 'rubrics_id')


