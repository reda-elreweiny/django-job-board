"""
URL configuration for JobBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import namedtuple

from django.contrib import admin
from django.urls import path

from Jobs import views as jobView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', jobView.index),
    path('contact/', jobView.contact, name='contact'),
    path('service/', jobView.service),
    path('jobs/', jobView.job_list, name='jobs'),
    path('apply/<job_id>', jobView.apply_job, name='apply'),
    path('thanks/', jobView.thank_you, name='thanks'),
    path('applications/', jobView.application_list,name='applications'),
    path('applications/<int:application_id>/edit/', jobView.edit_application_status, name='edit_application_status'),
    path('register/', jobView.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('my_applications/', jobView.my_applications, name='my_applications'),
    path('logout/', jobView.logout_user, name='logout'),
    path('profile/', jobView.profile_view, name='profile'),
    path('profile/edit/', jobView.edit_profile, name='edit_profile'),
    path('profile/change_password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/change_password.html',
        success_url='/profile/'
    ), name='change_password'),
    path('notifications/', jobView.notifications_view, name='notifications'),
    path('notification/<int:pk>/read/', jobView.read_notification, name='read_notification'),
    path('blog/',jobView.blog_post,name='blog_post'),
    path('blogDetails/<int:post_id>', jobView.blog_detail, name='blog_details'),
    path('blog/add', jobView.admin_add_post, name='add_post'),
    path('dashboard/posts', jobView.dashboard_posts, name='dashboard_posts'),
    path('dashboard/edit/<int:post_id>', jobView.edit_post, name='edit_post'),
    path('dashboard/delete/<int:post_id>', jobView.delete_post, name='delete_post'),
    path('dashboard/', jobView.admin_dashboard, name='admin_dashboard'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
