from django.contrib import admin

from task.models import Category, Task


@admin.register(Category)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    exclude = ('id',)


@admin.register(Task)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created', 'due_date')
    exclude = ('id', 'created')
