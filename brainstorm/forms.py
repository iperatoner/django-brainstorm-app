from django import forms
from django.contrib.admin import widgets as adminwidgets

from brainstorm.models import Idea, IdeaComment

class IdeaForm(forms.ModelForm):
    """Form for creating/editing one idea."""
    
    short_description = forms.CharField(max_length=128)
    long_description = forms.CharField(max_length=1024, widget=forms.Textarea)
    
    class Meta(object):
        model = Idea
        fields = (
            'short_description', 'long_description', 
            'author_name', 'author_email', 'author_website'
        )


class IdeaCommentForm(forms.ModelForm):
    """Form for creating a comment."""
    
    text = forms.CharField(max_length=2048, widget=forms.Textarea)
    
    class Meta(object):
        model = IdeaComment
        fields = ('author_name', 'author_email', 'author_website', 'text',)
