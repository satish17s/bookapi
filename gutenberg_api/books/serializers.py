# books/serializers.py

from rest_framework import serializers
from .models import Book, Author, Format, Language, Subject, Bookshelf

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type', 'url']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    bookshelves = BookshelfSerializer(many=True, read_only=True)
    formats = FormatSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 
            'gutenberg_id',
            'title', 
            'authors', 
            'languages', 
            'subjects', 
            'bookshelves', 
            'formats',
            'download_count',
            'media_type'
        ]
