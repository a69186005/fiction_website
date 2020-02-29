from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
  nick_name = models.CharField(max_length=20, verbose_name='user name', unique=True, blank=True)

  class Meta:
    verbose_name = 'user name'
    verbose_name_plural = verbose_name
  
  def __str__(self):
    return self.username
  
class OriginalBooks(models.Model):
  unique_id = models.CharField(max_length=100, verbose_name='Book ID', unique=True, default='')
  book_name = models.CharField(max_length=100, verbose_name='Book Name', default='')
  book_author = models.CharField(max_length=30, verbose_name='Book Author', default='')
  book_category = models.CharField(max_length=120, verbose_name='Book Category', default='')
  book_tags = models.CharField(max_length=120, verbose_name='Book Tags', default='')
  book_abstract = models.TextField(verbose_name='Book Abstract', default='')
  total_words = models.IntegerField(verbose_name='Book Total Words')
  book_url = models.URLField(verbose_name='Books Url', max_length=255, default='')

  class Meta:
    verbose_name = 'Original Books'
    verbose_name_plural = verbose_name
  
  def __str__(self):
    return self.unique_id

class OriginalBooksContent(models.Model):
  book = models.ForeignKey(OriginalBooks, verbose_name='Book Information', on_delete=models.CASCADE)
  chapter_name = models.CharField(max_length=50, verbose_name='Chapter Name', default='')
  chapter_index = models.IntegerField(verbose_name='Chapter Index')
  chapter_content = models.TextField(verbose_name='Chapter Content', default='')
  words = models.IntegerField(verbose_name='Chapter words')
  chapter_url = models.URLField(verbose_name='Chapter Url', max_length=255, default='')

  class Meta:
    verbose_name = 'Original Books Content'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.chapter_name

class TranslationBooksEN(models.Model):
  book = models.ForeignKey(OriginalBooks, verbose_name='Book Information', on_delete=models.CASCADE)
  book_name = models.CharField(max_length=120, verbose_name='Book Name', default='')
  book_author = models.CharField(max_length=200, verbose_name='Book Author', default='')
  book_category = models.CharField(max_length=120, verbose_name='Book Category', default='')
  book_tags = models.CharField(max_length=120, verbose_name='Book Tags', default='')
  book_abstract = models.TextField(verbose_name='Book Abstract', default='')
  total_words_tran = models.IntegerField(verbose_name='Book Total Words')

  class Meta:
    verbose_name = 'Translation Books EN'
    verbose_name_plural = verbose_name
  
  def __str__(self):
    return self.book_name

class TanslationBookContentEN(models.Model):
  book = models.ForeignKey(TranslationBooksEN, verbose_name='Book Information', on_delete=models.CASCADE)
  chapter_name = models.CharField(max_length=150, verbose_name='Chapter Name', default='')
  chapter_index = models.IntegerField(verbose_name='Chapter Index')
  chapter_content = models.TextField(verbose_name='Chapter Content', blank=True)
  words = models.IntegerField(verbose_name='Chapter words')

  class Meta:
    verbose_name = 'Translation Book Content EN'
    verbose_name_plural = verbose_name
  
  def __str__(self):
    return self.chapter_name

class TranslationBooksVI(models.Model):
  book = models.ForeignKey(OriginalBooks, verbose_name='Book Information', on_delete=models.CASCADE)
  book_name = models.CharField(max_length=120, verbose_name='Book Name', default='')
  book_author = models.CharField(max_length=200, verbose_name='Book Author', default='')
  book_category = models.CharField(max_length=120, verbose_name='Book Category', default='')
  book_tags = models.CharField(max_length=120, verbose_name='Book Tags', default='')
  book_abstract = models.TextField(verbose_name='Book Abstract', default='')
  total_words_tran = models.IntegerField(verbose_name='Book Total Words')

  class Meta:
    verbose_name = 'Translation Books VI'
    verbose_name_plural = verbose_name
  
  def __str__(self):
    return self.book_name

class TanslationBookContentVI(models.Model):
  book = models.ForeignKey(TranslationBooksVI, verbose_name='Book Information', on_delete=models.CASCADE)
  chapter_name = models.CharField(max_length=150, verbose_name='Chapter Name', default='')
  chapter_index = models.IntegerField(verbose_name='Chapter Index')
  chapter_content = models.TextField(verbose_name='Chapter Content', blank=True)
  words = models.IntegerField(verbose_name='Chapter words')

  class Meta:
    verbose_name = 'Translation Book Content'
    verbose_name_plural = verbose_name
  
  def __str__(self):
    return self.chapter_name
