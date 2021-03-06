from django import template

try:
    from settings import TEMPLATE_NAME
except ImportError:
    TEMPLATE_NAME = ''

register = template.Library()

@register.inclusion_tag(
    TEMPLATE_NAME + 'brainstorm/templatetags/show-idea-comments.html',
    takes_context=True
)
def show_idea_comments(context, idea):
    """This inclusion tag displays all comments
    related to the given idea."""
    
    context.update({
        'idea': idea,
        'comments': idea.comment_set.all()
    })
    
    return context

    
@register.inclusion_tag(
    TEMPLATE_NAME + 'brainstorm/templatetags/show-single-comment.html',
    takes_context=True
)
def show_single_comment(context, comment):
    """This inclusion tag displays a single comment."""
    
    context.update({
        'comment': comment
    })

    return context
