from django.contrib import admin
from . import models
from django.utils.html import mark_safe


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'category', 'title', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author', 'category')
    list_display_links = ('title',)
    list_per_page = 10
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def image_tag(self, obj): 
        return mark_safe('<img src="{}" width="70" height="50"/>'.format(obj.image.url))

    image_tag.short_description = 'Фото'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('email', 'author', 'post', 'text', 'created', )
    # list_filter = ('status', 'created', 'publish', 'author', 'category')
    # list_display_links = ('title',)
    # list_per_page = 10
    # search_fields = ('title', 'body')
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ('status', 'publish')

    # def image_tag(self, obj): 
    #     return mark_safe('<img src="{}" width="70" height="50"/>'.format(obj.image.url))

    # image_tag.short_description = 'Фото'



admin.site.register(models.Category)
admin.site.register(models.Tag)
# admin.site.register(models.Comment)
