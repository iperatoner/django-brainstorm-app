from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

from brainstorm.models import Idea, IdeaComment
from brainstorm.forms import IdeaForm, IdeaCommentForm
from brainstorm.util import voted_idea, set_voted

# Ordering possibilities
IDEA_ORDER_BY = {
    'latest' : 'date_added',
    'oldest' : '-date_added',
    'az' : 'subject__name',
    'za' : '-subject__name'
}
DEFAULT_ORDER_BY = 'latest'

def list_all_ideas(request, orderby='latest'):
    """This view lists all available ideas in a specific order."""
    
    # Choose the correct ordering type
    if orderby not in IDEA_ORDER_BY:
        model_orderby = IDEA_ORDER_BY[DEFAULT_ORDER_BY]
    else:
        model_orderby = IDEA_ORDER_BY[orderby]
        
    ideas = Idea.objects.all().order_by(model_orderby)
        
    data = {
        'ideas' : ideas,
        'orderby' : orderby
    }
    
    return render_to_response(
        'brainstorm/idea-list.html',
        data,
        context_instance = RequestContext(request),
    )
    

def show_idea(request,idea_id, form=False):
    """This view shows a single idea and all its comments."""
    
    idea = get_object_or_404(Idea, id=idea_id)
    
    # Create a comment form if it's not given (via the `add_comment` view)
    if not form:
        form = IdeaCommentForm()
        
    data = {
        'idea': idea,
        'form': form
    }

    return render_to_response(
        'brainstorm/show.html',
        data,
        context_instance = RequestContext(request),
    )


def create_idea(request):
    """
    This view displays a form for creating a idea resp. 
    creates a idea using the form data.
    """
    
    form = IdeaForm(request.POST or None)

    if form.is_valid():
        idea = form.save(commit=False)
        idea.promoted = 0
        idea.demoted = 0
        idea.save()
        
        return HttpResponseRedirect(reverse('bs_show', args=[idea.id]))

    data = {
        'form': form,
        'new' : True,
        'idea': None
    }

    return render_to_response(
        'brainstorm/edit.html',
        data,
        context_instance = RequestContext(request),
    )


def edit_idea(request, idea_id, edit_hash):
    """
    This view displays a form to edit an idea resp.
    saves an idea using the form data.
    """
    
    idea = get_object_or_404(Idea, id=idea_id)
    
    if idea.edit_hash != edit_hash:
        return Http404
    
    if not request.POST:
        form = IdeaForm(instance=idea)
    else:
        form = IdeaForm(request.POST)
        
        if form.is_valid():
            idea.short_description = form.cleaned_data['short_description']
            idea.long_description = form.cleaned_data['long_description']
            
            idea.author_name = form.cleaned_data['author_name']
            idea.author_email = form.cleaned_data['author_email']
            idea.author_website = form.cleaned_data['author_website']
            
            idea.save()
            
            request.user.message_set.create(message="Your homework was saved.")
            
            return HttpResponseRedirect(reverse('bs_show', args=[idea.id]))

    data = {
        'form': form,
        'new': False,
        'idea': idea
    }

    return render_to_response(
        'brainstorm/edit.html',
        data,
        context_instance = RequestContext(request),
    )


def like_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    
    if not voted_idea(request, idea):
        idea.promoted += 1
        idea.save()
        set_voted(request, idea)
    
    return HttpResponseRedirect(reverse('bs_show', args=[idea.id]))


def dislike_idea(request, idea_id):    
    idea = get_object_or_404(Idea, id=idea_id)
    
    if not voted_idea(request, idea):
        idea.demoted += 1
        idea.save()
        set_voted(request, idea)
    
    return HttpResponseRedirect(reverse('bs_show', args=[idea.id]))
    

def add_comment(request, idea_id):
    """This view creates a comment on the given idea."""
    
    idea = get_object_or_404(Idea, id=idea_id)
    
    form = IdeaCommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.idea = idea
        comment.save()
        
        return HttpResponseRedirect(
            reverse('bs_show', args=[idea_id]) + '#comments'
        )
    
    return show_idea(request, idea_id, form)
