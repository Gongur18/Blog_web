from django.contrib import admin
from .models import User, Book, Comment
admin.site.site_header = "欢迎来到后台管理网站"
admin.site.site_title = "后台管理"
admin.site.index_title = "数据管理"

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'name', 'email']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'author', 'date_added']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'belongs', 'date_added']

admin.site.register(User, admin_class=UserAdmin)
admin.site.register(Book, admin_class=BookAdmin)
admin.site.register(Comment, admin_class=CommentAdmin)