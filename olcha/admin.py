from django.contrib import admin

from .models import Category, Group, Product, Image, Comment


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('users_like',)



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('message',)
    list_filter = ('rating', 'created_at')