from django import template

register = template.Library() 

@register.filter(name='is_manager') 
def is_manager(user):
    return user.groups.filter(name="Manager").exists() 