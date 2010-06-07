from django import template
from brainstorm.util import rating_pixel_values

try:
    from settings import TEMPLATE_NAME
except ImportError:
    TEMPLATE_NAME = ''

register = template.Library()

@register.inclusion_tag(
    TEMPLATE_NAME + 'brainstorm/templatetags/idea-list-entry.html',
    takes_context=True
)
def idea_list_entry(context, idea):
    """This inclusion tag shows a single idea on the main idea list."""
    
    promoted_pixels, demoted_pixels = rating_pixel_values(idea)
    
    context.update({
        'idea': idea,
        'promoted_pixels': promoted_pixels,
        'demoted_pixels': demoted_pixels
    })
    
    return context


@register.inclusion_tag(
    TEMPLATE_NAME + 'brainstorm/templatetags/show-idea.html',
    takes_context=True
)
def show_idea(context, idea):
    """This inclusion tag shows a single idea and all its data."""
    
    promoted_pixels, demoted_pixels = rating_pixel_values(idea)
    
    context.update({
        'idea': idea,
        'promoted_pixels': promoted_pixels,
        'demoted_pixels': demoted_pixels
    })
    

    return context
