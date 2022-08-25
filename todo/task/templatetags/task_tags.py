from django import template

from task.models import *

register = template.Library()


@register.simple_tag()
def photo_tag(photo_pk):
    # todo: raises 500 if no image, use get_object_or_404 or filter()
    # also if these photos will be used always, you can add them in migrations
    context = SiteImages.objects.filter(pk=photo_pk)
    if context:
        return context
    return


@register.simple_tag()
def get_text_for_delete_forms(delete_number):
    # todo: its not the best practice, usually such situations handled from html/js
    return ["Ви впевнені, що хочете видалити цей запис?", "Ви впевнені, що хочете видалити всі виконані записи?"][
        delete_number]
