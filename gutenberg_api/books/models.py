from django.db import models

class Author(models.Model):
    """
    Model representing an author of a book.
    
    Attributes:
        birth_year (SmallIntegerField): The year the author was born (optional)
        death_year (SmallIntegerField): The year the author died (optional)
        name (CharField): The author's name, max length 128 characters
    """
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'books_author'

    def __str__(self):
        """String representation of the Author object."""
        return self.name

class Language(models.Model):
    """
    Model representing a language of a book.
    
    Attributes:
        code (CharField): The language code (e.g., 'en' for English), 
                         unique, max length 4 characters
    """
    code = models.CharField(max_length=4, unique=True)

    class Meta:
        db_table = 'books_language'

    def __str__(self):
        """String representation of the Language object."""
        return self.code

class Subject(models.Model):
    """
    Model representing a subject/category of a book.
    
    Attributes:
        name (CharField): The subject name, max length 256 characters
    """
    name = models.CharField(max_length=256)

    class Meta:
        db_table = 'books_subject'

    def __str__(self):
        """String representation of the Subject object."""
        return self.name

class Bookshelf(models.Model):
    """
    Model representing a bookshelf category.
    
    Attributes:
        name (CharField): The bookshelf name, unique, max length 64 characters
    """
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'books_bookshelf'

    def __str__(self):
        """String representation of the Bookshelf object."""
        return self.name

class Book(models.Model):
    """
    Model representing a book from Project Gutenberg.
    
    Attributes:
        gutenberg_id (IntegerField): Unique identifier from Project Gutenberg
        download_count (IntegerField): Number of times the book has been downloaded (optional)
        media_type (CharField): Type of media (e.g., 'Text'), max length 16 characters
        title (CharField): Book title, max length 1024 characters (optional)
        authors (ManyToManyField): Related Author objects through BookAuthor
        languages (ManyToManyField): Related Language objects through BookLanguage
        subjects (ManyToManyField): Related Subject objects through BookSubject
        bookshelves (ManyToManyField): Related Bookshelf objects through BookBookshelf
    """
    gutenberg_id = models.IntegerField(unique=True)
    download_count = models.IntegerField(null=True, blank=True)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024, null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name='books', through='BookAuthor')
    languages = models.ManyToManyField(Language, related_name='books', through='BookLanguage')
    subjects = models.ManyToManyField(Subject, related_name='books', through='BookSubject')
    bookshelves = models.ManyToManyField(Bookshelf, related_name='books', through='BookBookshelf')

    class Meta:
        db_table = 'books_book'
        ordering = ['-download_count']  # Order by download count in descending order

    def __str__(self):
        """String representation of the Book object."""
        return self.title or f"Book {self.gutenberg_id}"

class Format(models.Model):
    """
    Model representing a format of a book (e.g., PDF, TXT).
    
    Attributes:
        mime_type (CharField): MIME type of the format, max length 32 characters
        url (CharField): URL to download the book in this format, max length 256 characters
        book (ForeignKey): Related Book object
    """
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(Book, related_name='formats', on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_format'
    
    def __str__(self):
        """String representation of the Format object."""
        return f"{self.book.title} - {self.mime_type}"

# Through Models for Many-to-Many Relationships

class BookAuthor(models.Model):
    """
    Through model for Book-Author many-to-many relationship.
    
    Attributes:
        book (ForeignKey): Related Book object
        author (ForeignKey): Related Author object
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_authors'

class BookLanguage(models.Model):
    """
    Through model for Book-Language many-to-many relationship.
    
    Attributes:
        book (ForeignKey): Related Book object
        language (ForeignKey): Related Language object
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_languages'

class BookSubject(models.Model):
    """
    Through model for Book-Subject many-to-many relationship.
    
    Attributes:
        book (ForeignKey): Related Book object
        subject (ForeignKey): Related Subject object
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_subjects'

class BookBookshelf(models.Model):
    """
    Through model for Book-Bookshelf many-to-many relationship.
    
    Attributes:
        book (ForeignKey): Related Book object
        bookshelf (ForeignKey): Related Bookshelf object
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_bookshelves'
