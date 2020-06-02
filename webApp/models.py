from django.db import models

# 用户账户信息
class User(models.Model):
    class Meta:
        db_table = 'users'
    
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name
    
    def getDict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'email': self.email
        }

# 博客正文
class Book(models.Model):
    class Meta:
        db_table = 'books'

    title = models.CharField(max_length=50)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):    
        return self.title
    
    @property
    def lessText(self):
        if len(self.text) > 50:
            return self.text[:50] + " ......"
        else:
            return self.text

# 博客评论
class Comment(models.Model):
    class Meta:
        db_table = 'comments'
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    belongs = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if len(self.text) > 50:
            return self.text[:50] + " ......"
        else:
            return self.text