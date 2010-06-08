from datetime import datetime
from django.db import models

import random
import time
import hashlib

PROMOTED = 1
DEMOTED = 2

class Idea(models.Model):
    """Model representing an idea."""
    
    short_description = models.CharField(max_length=128)
    long_description = models.TextField()
    
    promoted = models.IntegerField()
    demoted = models.IntegerField()
    
    author_name = models.CharField(max_length=128)
    author_email = models.EmailField(blank=True)
    author_website = models.CharField(blank=True, max_length=128)
    
    date_added = models.DateTimeField(default=datetime.now)
    
    edit_hash = models.CharField(max_length=40, 
        default=hashlib.sha1(
            str(random.getrandbits(100)) + str(time.time())
        ).hexdigest()
    )

    def __unicode__(self):
        return '%s' % self.short_description


class IdeaComment(models.Model):
    """Model representing a comment on one idea."""
    
    idea = models.ForeignKey(Idea, related_name='comment_set')
    
    author_name = models.CharField(max_length=128)
    author_email = models.EmailField(blank=True)
    author_website = models.CharField(blank=True, max_length=128)
    
    text = models.TextField()
    date_added = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return '%s writes: %s' % (self.author_name, self.text)
    
        
class Voter(models.Model):
    ip = models.CharField(max_length=16)
    idea = models.ForeignKey(Idea)
    
