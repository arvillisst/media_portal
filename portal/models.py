from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import unidecode
from django.utils.text import slugify as _slugify


def slugify(value):
    return _slugify(unidecode.unidecode(value))


class Category(models.Model):
    name = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField('Заголовок', max_length=255)
    raw_title = models.CharField('Сырой аголовок', max_length=255)
    link_new = models.URLField(blank=True, verbose_name='Оригинальный пост')
    slug = models.SlugField(max_length=255, unique_for_date='publish', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
    body = RichTextUploadingField(blank=True, default='', verbose_name='Текст статьи')
    raw_body = models.TextField(blank=True, verbose_name='Сырой текст')
    image = models.ImageField(verbose_name='Картинка', upload_to='images/', blank=True)
    publish = models.DateTimeField('Опубликован', default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = models.ManyToManyField('Tag', blank=True)
    objects = models.Manager()
    published = PublishedManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.title}'

    # def get_absolute_url(self):
    #     return reverse('post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Tag(models.Model):
    name = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}' 
