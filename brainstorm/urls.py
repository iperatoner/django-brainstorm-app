from django.conf.urls.defaults import *
from brainstorm import views

urlpatterns = patterns('',
    url(
        r'^sort/(?P<orderby>.+)/$',
        views.list_all_ideas,
        name='bs_list_all_sorted'
    ),
    url(
        r'^idea/(?P<idea_id>[0-9]+)/$',
        views.show_idea,
        name='bs_show'
    ),
    url(
        r'^idea/(?P<idea_id>[0-9]+)/add-comment/$',
        views.add_comment,
        name='bs_add_comment'
    ),
    url(
        r'^idea/(?P<idea_id>[0-9]+)/like/$',
        views.like_idea,
        name='bs_like'
    ),
    url(
        r'^idea/(?P<idea_id>[0-9]+)/dislike/$',
        views.dislike_idea,
        name='bs_dislike'
    ),
    url(
        r'^create/$',
        views.create_idea,
        name='bs_create'
    ),
    url(
        r'^edit/(?P<idea_id>[0-9]+)/(?P<hash>[a-f0-9]{0,40})/$',
        views.edit_idea,
        name='bs_edit'
    ),
    url(r'^$', views.list_all_ideas, name='bs_list_all'),
)
