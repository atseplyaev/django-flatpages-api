from django.contrib import admin
from django.db.models import Max
from django.forms import HiddenInput, widgets

from polymorphic.admin import (
    PolymorphicInlineSupportMixin,
    GenericStackedPolymorphicInline,
)
from polymorphic.formsets.generic import (
    BaseGenericPolymorphicInlineFormSet,
    GenericPolymorphicFormSetChild,
)
from polymorphic.formsets.utils import add_media
from adminsortable2.admin import (
    _get_default_ordering,
    SortableInlineAdminMixin,
)
from .models import Page, Content, Text, Audio, Video


class PolymorphicOrderingInitFormSetMixin:
    """
    Миксин для инициализации дефолтных полей у админки inline полиморфных моделей
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_order_direction, self.default_order_field = _get_default_ordering(
            self.model, self
        )


class SortableGenericPolymorphicParentFormSet(
    PolymorphicOrderingInitFormSetMixin, BaseGenericPolymorphicInlineFormSet
):
    """
    FormSet для полиморфных моделей с возможностью сортировки.
    """

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        default_order_field = getattr(obj, self.default_order_field, None)
        if default_order_field is None or default_order_field >= 0:
            max_order = (
                self.queryset.aggregate(max_order=Max(self.default_order_field))['max_order'] or 0
            )
            setattr(obj, self.default_order_field, max_order + 1)
        if commit:
            obj.save()
        if commit and hasattr(form, 'save_m2m'):
            form.save_m2m()
        return obj


class SortableGenericPolymorphicFormSetChild(
    PolymorphicOrderingInitFormSetMixin, GenericPolymorphicFormSetChild
):
    """
    FormSet для дочерних полиморфных моделей с возможностью сортировки.
    """

    def get_form(self, **kwargs):
        self.form = super().get_form(**kwargs)
        if self.default_order_field not in self.form.base_fields:
            self.form.base_fields[self.default_order_field] = self.model._meta.get_field(
                self.default_order_field
            ).formfield()

        self.form.base_fields[self.default_order_field].is_hidden = True
        self.form.base_fields[self.default_order_field].required = False
        self.form.base_fields[self.default_order_field].widget = HiddenInput()
        return self.form


class SortableGenericPolymorphicChildInline(GenericStackedPolymorphicInline.Child):
    """
    GenericStackedPolymorphicInline.Child с возможностью сортировки
    """

    formset_child = SortableGenericPolymorphicFormSetChild


class ContentInline(SortableInlineAdminMixin, GenericStackedPolymorphicInline):
    template = 'block_stacked.html'
    formset = SortableGenericPolymorphicParentFormSet

    class AudioContentInline(SortableGenericPolymorphicChildInline):
        model = Audio

    class TextContentInline(SortableGenericPolymorphicChildInline):
        model = Text

    class VideoContentInline(SortableGenericPolymorphicChildInline):
        model = Video

    child_inlines = (AudioContentInline, TextContentInline, VideoContentInline)
    model = Content

    @property
    def media(self):
        share = super(GenericStackedPolymorphicInline, self).media
        sortable_media = super(SortableInlineAdminMixin, self).media
        add_media(
            sortable_media,
            widgets.Media(
                js=(
                    'admin/js/jquery.init.js',
                    'adminsortable2/js/inline-sortable.js',
                    'adminsortable2/js/inline-stacked.js',
                )
            ),
        )
        add_media(share, sortable_media)
        return share


@admin.register(Page)
class PageAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    search_fields = ('title',)
    inlines = (ContentInline,)
