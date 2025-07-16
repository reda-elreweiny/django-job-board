import os.path
from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=225)
    website = models.URLField(blank=True,null=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    location = models.CharField(max_length=225)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES= [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    email = models.EmailField()
    cv = models.FileField(upload_to='cvs/')
    applied_at = models.DateTimeField(auto_now_add=True,auto_now=False)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')


    def __unicode__(self):
        return f"{self.name} - {self.job}"
    def __str__(self):
        return f"{self.name} - {self.job}"


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='Static/avatars/',default='Static/avatars/default.png')
    def __str__(self):
        return self.user.username

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

# create notification panel
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    message = models.TextField()
    link = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username} - {self.message[:20]}"

# Create Blog Models
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def changePostImg(instance,name):
    ext = 'jpg'
    model = 'Post'
    filename = '{}{}.{}'.format(model,instance.id,ext)
    return os.path.join('Static/blog_images/',filename)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=changePostImg,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,related_name='posts',null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.post.title}"