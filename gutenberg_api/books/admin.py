from django.contrib import admin
from .models import Book, Author, Language, Subject, Bookshelf, Format

# Register Book model with custom admin configuration
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Book model.
    
    Attributes:
        list_display (list): Fields to display in the admin list view
            - title: Book's title
            - gutenberg_id: Unique Project Gutenberg ID
            - download_count: Number of times the book has been downloaded
            
        search_fields (list): Fields that can be searched in admin
            - title: Search by book title
            - authors__name: Search by author name (related field)
            
        list_filter (list): Fields that can be used to filter the list
            - languages__code: Filter books by language code
    """
    list_display = ['title', 'gutenberg_id', 'download_count']
    search_fields = ['title', 'authors__name']
    list_filter = ['languages__code']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Author model.
    
    Attributes:
        list_display (list): Fields to display in the admin list view
            - name: Author's name
            - birth_year: Year of birth
            - death_year: Year of death
            
        search_fields (list): Fields that can be searched
            - name: Search by author's name
    """
    list_display = ['name', 'birth_year', 'death_year']
    search_fields = ['name']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Language model.
    
    Attributes:
        list_display (list): Fields to display in the admin list view
            - code: Language code (e.g., 'en' for English)
    """
    list_display = ['code']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Subject model.
    
    Attributes:
        list_display (list): Fields to display in the admin list view
            - name: Subject name/category
            
        search_fields (list): Fields that can be searched
            - name: Search by subject name
    """
    list_display = ['name']
    search_fields = ['name']

@admin.register(Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Bookshelf model.
    
    Attributes:
        list_display (list): Fields to display in the admin list view
            - name: Bookshelf name/category
            
        search_fields (list): Fields that can be searched
            - name: Search by bookshelf name
    """
    list_display = ['name']
    search_fields = ['name']

@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Format model.
    
    Attributes:
        list_display (list): Fields to display in the admin list view
            - book: Related book title
            - mime_type: Format type (e.g., 'text/plain')
            - url: Download URL for the format
            
        list_filter (list): Fields that can be used to filter the list
            - mime_type: Filter formats by type
    """
    list_display = ['book', 'mime_type', 'url']
    list_filter = ['mime_type']
