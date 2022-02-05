from xml.dom.minidom import Document

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminStackedInline, AjaxSelectAdminTabularInline
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from django import forms
from django.contrib import admin
from django.forms import Textarea

from revije.models import *


@admin.register(Avtor)
class AvtorAdmin(admin.ModelAdmin):
    pass


class ClanekForm(forms.ModelForm):
    avtorji = AutoCompleteSelectMultipleField('avtorji', required=False, help_text=None)

    def __init__(self, *args, **kwargs):
        super(ClanekForm, self).__init__(*args, **kwargs)
        exclude_vsebina = Clanek.objects.all()
        if self.instance:
            exclude_vsebina = exclude_vsebina.exclude(pk=self.instance.pk)
        self.fields['vsebina'].queryset = ClanekVsebina.objects.exclude(id__in=exclude_vsebina.values('vsebina_id'))
        self.fields['vsebina'].widget.can_delete_related = False


class ClanekInline(AjaxSelectAdminStackedInline):
    model = Clanek
    extra = 1
    form = ClanekForm

    class Media:
        js = ['js/collapsed_stacked_inlines.js']


@admin.register(Revija)
class RevijaAdmin(admin.ModelAdmin):
    list_display = ['revija', 'datum_izdaje', 'stevilka', 'zakljuceno']
    inlines = [ClanekInline]
    list_filter = ['revija', 'zakljuceno']


@admin.register(Clanek)
class ClanekAdmin(AjaxSelectAdmin):
    form = ClanekForm
    list_display = ['revija', 'naslov', 'podnaslov', 'kategorija']


@admin.register(ClanekVsebina)
class ClanekVsebinaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 40, 'cols': 150})},
    }
