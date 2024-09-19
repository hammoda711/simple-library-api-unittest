from rest_framework import serializers

from api.models import Author, Book

class AuthorSerializer(serializers.Serializer):
    class Meta:
        model = Author
        fields = ['id','name']


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields =  '__all__'
    