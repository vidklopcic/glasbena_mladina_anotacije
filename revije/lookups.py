from ajax_select import register, LookupChannel
from .models import Avtor


@register('avtorji')
class AvtorjiLookup(LookupChannel):
    model = Avtor

    def get_query(self, q, request):
        return self.model.objects.filter(ime_in_priimek__icontains=q)

    def format_item_display(self, item):
        return f'<span class="avtor">{item.ime_in_priimek}</span>'
