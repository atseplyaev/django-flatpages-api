from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Content, Video, Text, Audio, Page


class ContentSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор блока контента

    От него должны наследоваться остальные блоки контента.
    """

    class Meta:
        model = Content
        fields = ('id', 'title', 'views_count')


class VideoSerializer(serializers.ModelSerializer):
    """ Сериализатор видео-контента """

    class Meta:
        model = Video
        fields = (*ContentSerializer.Meta.fields, 'video_link', 'subtitle_link')


class TextSerializer(serializers.ModelSerializer):
    """ Сериализатор текстового-контента """

    class Meta:
        model = Text
        fields = (*ContentSerializer.Meta.fields, 'text_field')


class AudioSerializer(serializers.ModelSerializer):
    """ Сериализатор аудио-контента """

    class Meta:
        model = Audio
        fields = (*ContentSerializer.Meta.fields, 'audio_bitrate')


class ContentPolymorphicSerializer(PolymorphicSerializer):
    """
    Полиморфный сериализатор блока контента и его наследников
    """

    model_serializer_mapping = {
        Content: ContentSerializer,
        Video: VideoSerializer,
        Audio: AudioSerializer,
        Text: TextSerializer,
    }


class BasePageSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор модели страницы
    От него должны наследоваться остальные сериализаторы страниц.
    """

    class Meta:
        model = Page
        fields = ('id', 'title')


class PageListSerializer(BasePageSerializer, serializers.HyperlinkedModelSerializer):
    """
    Сериализатор модели страницы.
    Используется для сериализации списка страниц
    """

    class Meta(BasePageSerializer.Meta):
        fields = (*BasePageSerializer.Meta.fields, 'url')


class PageRetrieveSerializer(BasePageSerializer):
    """
    Сериализатор модели страницы.
    Используется для сериализации расширенной информации о странице
    """

    content = ContentPolymorphicSerializer(many=True)

    class Meta(BasePageSerializer.Meta):
        fields = (*BasePageSerializer.Meta.fields, 'content')
