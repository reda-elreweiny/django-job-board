from django.contrib import admin
from .models import Company
from .models import Job
from .models import Application
from .models import Profile
from .models import ContactUs
from .models import Notification
from .models import Category,Post,Comment

# Register your models here.
class adminCompany(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
admin.site.register(Company,adminCompany)

class adminJob(admin.ModelAdmin):
    list_display = ['title','company']
    search_fields = ['title','company']
admin.site.register(Job,adminJob)

class adminApplication(admin.ModelAdmin):
    list_display = ['job','name','email']
    search_fields = ['job','name','email']
admin.site.register(Application)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','email']
admin.site.register(Profile,ProfileAdmin)

class msgAdmin(admin.ModelAdmin):
    list_display = ['name','email','message','created_at']
admin.site.register(ContactUs,msgAdmin)

class NotifyAdmin(admin.ModelAdmin):
    list_display = ['user','message','created_at']
admin.site.register(Notification,NotifyAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Category,CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created_at']
admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author','post','created_at']
admin.site.register(Comment,CommentAdmin)