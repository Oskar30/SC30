from rest_framework import serializers
from workshop import models

# class OrderSerializer(serializers.Serializer):


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'author', 'person', 'contact', 'title']
        read_only_fields = ['author',]