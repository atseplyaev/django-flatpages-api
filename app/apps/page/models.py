from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from polymorphic.models import PolymorphicModel


class Content(PolymorphicModel):
    """
    Родительская полиморфная модель контента

    Все новые типы контента должны наследоваться непосредственно от этой модели
    """

    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.PositiveSmallIntegerField("Порядок", default=0, db_index=True)

    title = models.CharField('Заголовок', max_length=64)
    views_count = models.PositiveIntegerField('Количество просмотров', default=0)

    class Meta(PolymorphicModel.Meta):
        verbose_name = "Блок контента"
        verbose_name_plural = "Блоки контента"
        ordering = ("order",)

    def __str__(self):
        return f"Блок контента: {self.title}"


class Video(Content):
    """ Модель видео-контента """

    video_link = models.URLField('Ссылка на видео файл')
    subtitle_link = models.URLField('Ссылка на субтитры к видео')

    class Meta(PolymorphicModel.Meta):
        verbose_name = 'Видео блок'
        verbose_name_plural = 'Видео блоки'
        ordering = ('order',)


class Audio(Content):
    """ Модель аудио-контента """

    audio_bitrate = models.PositiveIntegerField('Битрейт', default=320)

    class Meta(PolymorphicModel.Meta):
        verbose_name = 'Аудио блок'
        verbose_name_plural = 'Аудио блоки'
        ordering = ('order',)


class Text(Content):
    """ Модель аудио-контента """

    text_field = models.TextField('Текст')

    class Meta(PolymorphicModel.Meta):
        verbose_name = 'Текстовый блок'
        verbose_name_plural = 'Текстовые блоки'
        ordering = ('order',)


class Page(models.Model):
    """ Модель страницы """

    title = models.CharField('Заголовок страницы', max_length=64)
    created = models.DateTimeField('Создан', auto_now_add=True)
    content = GenericRelation('page.Content', verbose_name='Блоки контента')

    class Meta:
        verbose_name = 'Текстовый блок'
        verbose_name_plural = 'Текстовые блоки'
        ordering = ('-created',)

    def __str__(self):
        return self.title
