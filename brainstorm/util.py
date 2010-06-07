from django.shortcuts import get_object_or_404
from django.http import Http404

from brainstorm.models import Idea, Voter
from brainstorm.models import PROMOTED, DEMOTED

def voted_idea(request, idea):
    """
    This function checks wether the current user has already voted the
    given idea and how he does that (cookies).
    """

    if 'cream_brainstorm' in request.session:
        cream_brainstorm = request.session['cream_brainstorm'].split('#')
        
        if str(idea.id) in cream_brainstorm:
            return True
        else:
            return False
    else:
        try:
            Voter.objects.get(ip=request.META['REMOTE_ADDR'], idea=idea)
        except Voter.DoesNotExist:
            return False
        else:
            return True
            

def set_voted(request, idea):
    if 'cream_brainstorm' not in request.session:
        request.session['cream_brainstorm'] = ''
        
    request.session['cream_brainstorm'] += '#' + str(idea.id)
    voter = Voter(ip=request.META['REMOTE_ADDR'], idea=idea)
    voter.save()
