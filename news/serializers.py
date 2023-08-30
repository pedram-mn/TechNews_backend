from rest_framework import serializers
from .models import News, Reference


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['link', 'author', 'date']


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    references = ReferenceSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            'title',
            'content',
            'tags',
            'references'
        ]
