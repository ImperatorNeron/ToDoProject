from django import template

from task.models import *

register = template.Library()


@register.simple_tag()
def photo_tag(photo_pk):
    context = SiteImages.objects.get(pk=photo_pk)
    return context


@register.simple_tag()
def get_text_for_delete_forms(delete_number):
    return ["Ви впевнені, що хочете видалити цей запис?", "Ви впевнені, що хочете видалити всі виконані записи?"][
        delete_number]
