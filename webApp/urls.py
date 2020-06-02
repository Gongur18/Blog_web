from django.urls import path
from .views import *

app_name = 'webApp'
urlpatterns = [
    # 首页
    path('', index, name="index"),
    # 用户登陆与注销
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    # 对用户的操作
    path('register/', register, name="register"),
    path('user/', user_index, name="user_index"),
    path('user/edit/', user_edit, name="user_edit"),
    path('user/delete/', user_delete, name="user_delete"),
    # 文章列表
    path('Books/p<int:page_index>/', Books, name="Books"),
    path('MyBooks/p<int:page_index>/', MyBooks, name="MyBooks"),
    # 对文章的操作
    path('MyBooks/new/', book_new, name="book_new"),
    path('Books/<int:book_id>/', book_index, name='book_index'),
    path('Books/<int:book_id>/edit/', book_edit, name='book_edit'),
    path('Books/<int:book_id>/delete/', book_delete, name='book_delete'),
    # 添加评论
    path('Books/<int:book_id>/comment/', comment_new, name="comment_new"),
]