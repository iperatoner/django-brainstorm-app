from django import template

register = template.Library()

@register.inclusion_tag(
    'brainstorm/templatetags/idea-list-entry.html',
    takes_context=True
)
def idea_list_entry(context, idea):
    """This inclusion tag shows a single idea on the main idea list."""
    
    context.update({'idea': idea})
    
    return context


@register.inclusion_tag(
    'brainstorm/templatetags/show-idea.html',
    takes_context=True
)
def show_idea(context, idea):
    """This inclusion tag shows a single idea and all its data."""
    
    context.update({'idea': idea})

    return context
