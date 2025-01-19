# books/serializers.py

from rest_framework import serializers
from .models import Book, Author, Format, Language, Subject, Bookshelf

class FormatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Format model.
    
    Serializes format information including:
    - mime_type: The MIME type of the format (e.g., 'text/plain')
    - url: The download URL for the format
    """
    class Meta:
        model = Format
        fields = ['mime_type', 'url']

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    Serializes author information including:
    - name: The author's name
    - birth_year: Year of birth (optional)
    - death_year: Year of death (optional)
    """
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']

class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Language model.
    
    Serializes language information including:
    - code: The language code (e.g., 'en' for English)
    """
    class Meta:
        model = Language
        fields = ['code']

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.
    
    Serializes subject information including:
    - name: The subject/category name
    """
    class Meta:
        model = Subject
        fields = ['name']

class BookshelfSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bookshelf model.
    
    Serializes bookshelf information including:
    - name: The bookshelf category name
    """
    class Meta:
        model = Bookshelf
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Serializes complete book information including all related objects:
    - id: Internal database ID
    - gutenberg_id: Project Gutenberg ID
    - title: Book title
    - authors: List of authors (nested serialization)
    - languages: List of languages (nested serialization)
    - subjects: List of subjects (nested serialization)
    - bookshelves: List of bookshelves (nested serialization)
    - formats: List of available formats (nested serialization)
    - download_count: Number of downloads
    - media_type: Type of media
    
    Note:
    - All nested serializers are read-only
    - Uses nested serialization for related fields
    - Provides complete book information in a single response
    """
    # Nested serializers for related fields
    authors = AuthorSerializer(
        many=True, 
        read_only=True,
        help_text="List of authors associated with the book"
    )
    languages = LanguageSerializer(
        many=True, 
        read_only=True,
        help_text="List of languages the book is available in"
    )
    subjects = SubjectSerializer(
        many=True, 
        read_only=True,
        help_text="List of subjects/categories for the book"
    )
    bookshelves = BookshelfSerializer(
        many=True, 
        read_only=True,
        help_text="List of bookshelves the book belongs to"
    )
    formats = FormatSerializer(
        many=True, 
        read_only=True,
        help_text="List of available download formats"
    )

    class Meta:
        model = Book
        fields = [
            'id',              # Internal database ID
            'gutenberg_id',    # Project Gutenberg ID
            'title',           # Book title
            'authors',         # Nested authors data
            'languages',       # Nested languages data
            'subjects',        # Nested subjects data
            'bookshelves',     # Nested bookshelves data
            'formats',         # Nested formats data
            'download_count',  # Number of downloads
            'media_type'       # Type of media
        ]

    def to_representation(self, instance):
        """
        Custom representation method to handle any additional formatting.
        
        Args:
            instance: The Book instance being serialized
            
        Returns:
            dict: The formatted book data
        """
        # Get the default serialized data
        data = super().to_representation(instance)
        
        # You could add additional formatting here if needed
        # For example, sorting formats by mime_type:
        if data['formats']:
            data['formats'] = sorted(
                data['formats'], 
                key=lambda x: x['mime_type']
            )
            
        return data
