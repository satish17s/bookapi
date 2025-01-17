from django.shortcuts import render
from django.core.paginator import Paginator  # Add this import
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Book
from .serializers import BookSerializer

class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookFilter(filters.FilterSet):
    language = filters.CharFilter(method='filter_language')
    mime_type = filters.CharFilter(field_name='formats__mime_type')
    topic = filters.CharFilter(method='filter_topic')
    author = filters.CharFilter(method='filter_author')
    title = filters.CharFilter(lookup_expr='icontains')
    book_ids = filters.CharFilter(method='filter_book_ids')

    def filter_language(self, queryset, name, value):
        if value:
            languages = [lang.strip() for lang in value.split(',')]
            return queryset.filter(languages__code__in=languages)
        return queryset

    def filter_mime_type(self, queryset, name, value):
        if value:
            mime_types = [mt.strip() for mt in value.split(',')]
            return queryset.filter(formats__mime_type__in=mime_types)
        return queryset

    def filter_topic(self, queryset, name, value):
        if value:
            topics = [topic.strip() for topic in value.split(',')]
            q = Q()
            for topic in topics:
                q |= Q(subjects__name__icontains=topic) | Q(bookshelves__name__icontains=topic)
            return queryset.filter(q).distinct()
        return queryset

    def filter_author(self, queryset, name, value):
        if value:
            return queryset.filter(authors__name__icontains=value)
        return queryset

    def filter_book_ids(self, queryset, name, value):
        if value:
            ids = [int(id.strip()) for id in value.split(',')]
            return queryset.filter(gutenberg_id__in=ids)
        return queryset

    class Meta:
        model = Book
        fields = ['language', 'mime_type', 'topic', 'author', 'title', 'book_ids']

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all().order_by('-download_count')
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'authors', 'languages', 'subjects', 'bookshelves', 'formats'
        )


def home(request):
    queryset = Book.objects.all()
    
    # Apply filters
    title = request.GET.get('title')
    author = request.GET.get('author')
    topic = request.GET.get('topic')
    language = request.GET.get('language')
    mime_type = request.GET.get('mime_type')
    book_ids = request.GET.get('book_ids')
    sort = request.GET.get('sort', '-download_count')
    
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
    
    # Pagination
    paginator = Paginator(queryset.distinct(), 25)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    return render(request, 'books/home.html', {'books': books})

