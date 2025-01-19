from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Book, Format
from .serializers import BookSerializer

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for the API.
    
    Attributes:
        page_size (int): Number of items per page (25)
        page_size_query_param (str): Query parameter to override page size
        max_page_size (int): Maximum allowed page size (100)
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookFilter(filters.FilterSet):
    """
    FilterSet for Book model providing various filter options.
    
    Filter Options:
        book_ids: Filter by Gutenberg ID numbers
        language: Filter by language codes
        mime_type: Filter by format types
        topic: Search in subjects and bookshelves
        author: Search by author name
        title: Search by book title
    """
    
    # Filter definitions with descriptions
    book_ids = filters.CharFilter(
        field_name='gutenberg_id',
        method='filter_book_ids',
        label='Book ID numbers (comma-separated)',
        help_text='e.g., 1,2,3'
    )
    
    language = filters.CharFilter(
        method='filter_language',
        label='Language (comma-separated)',
        help_text='e.g., en,fr'
    )
    
    mime_type = filters.CharFilter(
        field_name='formats__mime_type',
        label='Mime-type',
        help_text='e.g., text/plain, application/pdf'
    )
    
    topic = filters.CharFilter(
        method='filter_topic',
        label='Topic (searches subjects and bookshelves)',
        help_text='e.g., child, education'
    )
    
    author = filters.CharFilter(
        method='filter_author',
        label='Author (case-insensitive partial match)',
        help_text='e.g., Shakespeare'
    )
    
    title = filters.CharFilter(
        lookup_expr='icontains',
        label='Title (case-insensitive partial match)',
        help_text='e.g., Pride and Prejudice'
    )

    def filter_language(self, queryset, name, value):
        """
        Filter books by language code(s).
        
        Args:
            queryset: Initial queryset
            name: Field name (unused)
            value: Comma-separated language codes
            
        Returns:
            Filtered queryset
        """
        if value:
            languages = [lang.strip() for lang in value.split(',')]
            return queryset.filter(languages__code__in=languages)
        return queryset

    def filter_mime_type(self, queryset, name, value):
        """
        Filter books by MIME type(s).
        
        Args:
            queryset: Initial queryset
            name: Field name (unused)
            value: Comma-separated MIME types
            
        Returns:
            Filtered queryset
        """
        if value:
            mime_types = [mt.strip() for mt in value.split(',')]
            return queryset.filter(formats__mime_type__in=mime_types)
        return queryset

    def filter_topic(self, queryset, name, value):
        """
        Filter books by topic in subjects or bookshelves.
        
        Args:
            queryset: Initial queryset
            name: Field name (unused)
            value: Topic to search for
            
        Returns:
            Filtered queryset
        """
        if value:
            topics = [topic.strip() for topic in value.split(',')]
            q = Q()
            for topic in topics:
                q |= Q(subjects__name__icontains=topic) | Q(bookshelves__name__icontains=topic)
            return queryset.filter(q).distinct()
        return queryset

    def filter_author(self, queryset, name, value):
        """Filter books by author name (case-insensitive)."""
        if value:
            return queryset.filter(authors__name__icontains=value)
        return queryset

    def filter_book_ids(self, queryset, name, value):
        """Filter books by Gutenberg IDs."""
        if value:
            ids = [int(id.strip()) for id in value.split(',')]
            return queryset.filter(gutenberg_id__in=ids)
        return queryset

    class Meta:
        model = Book
        fields = ['language', 'mime_type', 'topic', 'author', 'title', 'book_ids']

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing books.
    
    Provides 'list' and 'retrieve' actions.
    Supports filtering, pagination, and ordering by download count.
    """
    queryset = Book.objects.all().order_by('-download_count')
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        """
        Get the queryset for the viewset.
        Optimizes database queries using prefetch_related.
        """
        return super().get_queryset().prefetch_related(
            'authors', 'languages', 'subjects', 'bookshelves', 'formats'
        )

def download_book(request, book_id, format_id):
    """
    Handle book download and increment download counter.
    
    Args:
        request: HTTP request
        book_id: ID of the book
        format_id: ID of the format
        
    Returns:
        Redirect to the actual download URL
    """
    # Get book and format or return 404
    book = get_object_or_404(Book, id=book_id)
    book_format = get_object_or_404(Format, id=format_id)
    
    # Increment download count atomically
    Book.objects.filter(id=book_id).update(download_count=F('download_count') + 1)
    
    # Redirect to download URL
    return HttpResponseRedirect(book_format.url)

def home(request):
    """
    Home page view showing book list with filters.
    
    Args:
        request: HTTP request containing filter parameters
        
    Returns:
        Rendered home page with filtered book list
    """
    # Get base queryset with optimized queries
    queryset = Book.objects.all().prefetch_related(
        'authors', 'languages', 'subjects', 'bookshelves', 'formats'
    )
    
    # Get filter parameters from request
    title = request.GET.get('title')
    author = request.GET.get('author')
    topic = request.GET.get('topic')
    language = request.GET.get('language')
    mime_type = request.GET.get('mime_type')
    book_ids = request.GET.get('book_ids')
    sort = request.GET.get('sort', '-download_count')
    
    # Apply filters if parameters are present
    if title:
        queryset = queryset.filter(title__icontains=title)
    if author:
        queryset = queryset.filter(authors__name__icontains=author)
    if topic:
        queryset = queryset.filter(
            Q(subjects__name__icontains=topic) | 
            Q(bookshelves__name__icontains=topic)
        ).distinct()
    if language:
        queryset = queryset.filter(languages__code=language)
    if mime_type:
        queryset = queryset.filter(formats__mime_type=mime_type)
    if book_ids:
        try:
            ids = [int(x.strip()) for x in book_ids.split(',')]
            queryset = queryset.filter(gutenberg_id__in=ids)
        except ValueError:
            pass
    
    # Apply sorting
    queryset = queryset.order_by(sort)
    
    # Set up pagination
    paginator = Paginator(queryset.distinct(), 25)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    # Get total count for display
    total_count = queryset.count()
    
    # Render template with context
    return render(request, 'books/home.html', {
        'books': books,
        'total_count': total_count,
        'filters': {
            'title': title,
            'author': author,
            'topic': topic,
            'language': language,
            'mime_type': mime_type,
            'book_ids': book_ids,
            'sort': sort,
        }
    })
