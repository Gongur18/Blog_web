from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Book, Comment

from rest_framework import viewsets
from .serializers import UserSerializer, BookSerializer

def index(request):
    return HttpResponseRedirect(reverse(viewname='webApp:Books', args=('1',)))

def login(request):
    # 已经登录的用户不再进入登陆页面
    if request.session.get('user_id'):
        return redirect('/')
    # 具体登录过程
    if request.method != 'POST':
        return render(request, "login.html")
    try:
        user = User.objects.get(username=request.POST['username'])
        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['password'], encoding="utf-8"))
        if user.password == m.hexdigest():
            request.session['name'] = user.name
            request.session['user_id'] = user.id
            return redirect('/')
        else:
            context = {'info': '密码错误，请重新输入'}
            return render(request, 'login.html', context)
    except:
        context = {'info': '该用户不存在'}
        return render(request, 'login.html', context)

def logout(request):
    """注销登陆"""
    del request.session['name']
    del request.session['user_id']
    return redirect('/')

def register(request):
    # 已经登录的用户不再进入注册页面
    if request.session.get('user_id'):
        return redirect('/')
    # 具体注册过程
    if request.method != 'POST':
        return render(request, "register.html")
    try:
        # 判断账号有无重名
        ob = User.objects.all()
        for old in ob:
            if old.username == request.POST['username']:
                context={"info":"账户名已存在"}
                return render(request, "register.html", context)
        # 判断密码是否一致
        if request.POST['password'] != request.POST['repassword']:
            context={"info":"两次输入密码不一致"}
            return render(request, "register.html", context)

        new = User()
        new.username = request.POST['username']
        new.email = request.POST['email']
        new.name = request.POST['name']
        #对密码进行MD5加密
        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['password'],encoding="utf8"))
        new.password = m.hexdigest()
        #保存
        new.save()
        request.session['name'] = new.name
        request.session['user_id'] = new.id
        return redirect('/')
    except Exception as err:
        print(err)
        context = {"info":"账户错误"}  
        return render(request, "register.html", context)

def user_index(request):
    # 控制只有已经登录的账户能访问自己个人中心
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(id=user_id)
    context = {'user': user}
    return render(request, "user_index.html", context)

def user_edit(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    if request.method != 'POST':
        context = {'user': User.objects.get(id=user_id)}
        return render(request, "user_edit.html", context)
    try:
        user = User.objects.get(id=user_id)
        user.email = request.POST['email']
        user.name = request.POST['name']
        if request.POST['password']:
            # 判断密码是否一致
            if request.POST['password'] != request.POST['repassword']:
                context={"info":"两次输入密码不一致"}
                return render(request, "register.html", context)
            else:
                #对密码进行MD5加密
                import hashlib
                m = hashlib.md5()
                m.update(bytes(request.POST['password'],encoding="utf8"))
                user.password = m.hexdigest()
        user.save()
        return HttpResponseRedirect(reverse(viewname='webApp:user_index'))
    except Exception as err:
        return HttpResponseRedirect(reverse(viewname='webApp:user_index'))

def user_delete(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(id=user_id)
    books = Book.objects.filter(author=user)
    # 删除该用户的所有文章
    for book in books:
        # 递归删除文章下的所有评论
        comments = Comment.objects.filter(belongs=book)
        for comment in comments:
            comment.delete()
        book.delete()
    comments = Comment.objects.filter(author=user)
    # 删除该用户的所有评论
    for comment in comments:
        comment.delete()
    user.delete()
    del request.session['name']
    del request.session['user_id']
    return redirect('/')

def Books(request, page_index=1):
    if request.method != 'POST':
        bookList = Book.objects.all().order_by('-date_added')
    else:
        bookList = Book.objects.filter(title__contains=request.POST['search']).order_by('-date_added')
    # 执行分页处理
    page_index = int(page_index)
    page = Paginator(bookList, 5)
    max_pages = page.num_pages
    page_list = page.page_range
    if page_index > max_pages:
        page_index = max_pages
    if page_index < 1:
        page_index = 1
    # 当前页数据
    currentList = page.page(page_index)
    context = {
        "bookList": currentList,
        "page_list":page_list,
        "page_index": page_index,
        "max_pages":max_pages,
    }
    return render(request, "books.html", context)

def MyBooks(request, page_index=1):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    bookList = Book.objects.filter(author_id=user_id).order_by('-date_added')
    # 执行分页处理
    page_index = int(page_index)
    page = Paginator(bookList, 5)
    max_pages = page.num_pages
    page_list = page.page_range
    if page_index > max_pages:
        page_index = max_pages
    if page_index < 1:
        page_index = 1
    # 当前页数据
    currentList = page.page(page_index)
    context = {
        "bookList": currentList,
        "page_list":page_list,
        "page_index": page_index,
        "max_pages":max_pages,
    }
    return render(request, "books.html", context)

# 某博客详情页
def book_index(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        comments = Comment.objects.filter(belongs=book).order_by('-date_added')
        context = {
            "book": book,
            "comments": comments
        }
        return render(request, "book_index.html", context)
    except:
        return HttpResponse("该博客可能丢失或者被删除了")

# 新建博客
def book_new(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    if request.method != 'POST':
        return render(request, "book_new.html")
    else:
        new = Book()
        new.title = request.POST['title']
        new.text = request.POST['text']
        new.author = User.objects.get(id=user_id)
        new.save()
        return HttpResponseRedirect(reverse(viewname='webApp:MyBooks', args=(1,)))

# 编辑博客
def book_edit(request, book_id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    context = {'book':book}
    if request.method != 'POST':
        return render(request, "book_edit.html", context)
    else:
        old = Book.objects.get(id=book_id)
        old.title = request.POST['title']
        old.text = request.POST['text']
        old.save()
        return HttpResponseRedirect(reverse(viewname='webApp:MyBooks', args=(1,)))

# 删除博客
def book_delete(request, book_id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    comments = Comment.objects.filter(belongs=book)
    for comment in comments:
        comment.delete()
    book.delete()
    return HttpResponseRedirect(reverse(viewname='webApp:MyBooks', args=(1,)))        


# 编写新评论
def comment_new(request, book_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    if request.method != 'POST':
        return HttpResponseRedirect(reverse(viewname='webApp:book_index', args=(book_id,)))
    else:
        comment = Comment()
        comment.author = User.objects.get(id=user_id)
        comment.belongs = book
        comment.text = request.POST['text']
        comment.save()
        return HttpResponseRedirect(reverse(viewname='webApp:book_index', args=(book_id,)))

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer