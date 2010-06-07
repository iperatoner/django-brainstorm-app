from django.shortcuts import get_object_or_404
from django.http import Http404

from brainstorm.models import Idea, Voter
from brainstorm.models import PROMOTED, DEMOTED

# the width of the rating bar
RATING_BAR_WIDTH = 70.0

def voted_idea(request, idea):
    """
    This function checks wether the current user has already voted the
    given idea and how he does that (cookies).
    """
    
    return False

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
    

def rating_pixel_values(idea):
    promoted_pixels = 0
    demoted_pixels = 0
    
    votes = idea.promoted + idea.demoted
    
    if votes > 0:
        votes = float(votes)
        
        percentage_promoted = (float(idea.promoted) / votes) * 100.0
        percentage_demoted = (float(idea.demoted) / votes) * 100.0
        
        print percentage_promoted, percentage_demoted
        promoted_pixels = round((RATING_BAR_WIDTH / 100.0) * percentage_promoted, 0)
        demoted_pixels = round((RATING_BAR_WIDTH / 100.0) * percentage_demoted, 0)
        
        if promoted_pixels + demoted_pixels > RATING_BAR_WIDTH:
            demoted_pixels -= 1
    
    return (promoted_pixels, demoted_pixels)
