from django import template

#Registering the custom tags with the template library so Django recognizes it
#If new template tags are registered, the server must be closed and reopened for changes to take effect
register = template.Library()

@register.filter('can_see')
# Verifying the current user's current group memberships
def can_see(user, eval):
    evalID = eval.id
    eval_groups = eval.groups.through.objects.all().filter(evaluation_id=evalID)
    groups = user.groups.all().values_list('id', flat=True)
    for group in groups:
        filtered = eval_groups.filter(group_id=group)
        if filtered.exists():
            return True
    return False