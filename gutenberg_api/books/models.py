from django.db import models

class Author(models.Model):
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'books_author'

    def __str__(self):
        return self.name

class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)

    class Meta:
        db_table = 'books_language'

    def __str__(self):
        return self.code

class Subject(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = 'books_subject'

    def __str__(self):
        return self.name

class Bookshelf(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'books_bookshelf'

    def __str__(self):
        return self.name

class Book(models.Model):
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
        ordering = ['-download_count']

    def __str__(self):
        return self.title or f"Book {self.gutenberg_id}"

class Format(models.Model):
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(Book, related_name='formats', on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_format'

# Through Models
class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_authors'

class BookLanguage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_languages'

class BookSubject(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_subjects'

class BookBookshelf(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_bookshelves'
