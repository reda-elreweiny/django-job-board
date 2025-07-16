from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Application
from .Forms import ApplicationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .Forms import ApplicationStatusForm
from django.contrib.auth.forms import UserCreationForm
from .Forms import UserRegisterForm,CommentForm
from django.contrib.auth import logout
from .models import Profile
from django.contrib.auth.decorators import  login_required,user_passes_test
from .Forms import ProfileForm
from django.db.models import Q
from .models import Company
from .models import ContactUs
from .Forms import ContactForm,PostForm
from .models import Notification
from .models import Post
from django.utils.decorators import method_decorator


# Create your views here.

def index(request):
    return render(request, 'index.html')


def contactPage(request):
    return render(request, 'contact.html')


def service(request):
    return render(request, 'service.html')


def job_list(request):
    query = request.GET.get('q') # Search Word
    jobs = Job.objects.all().order_by('-posted_at')
    company_name = request.GET.get('company')
    companies = Company.objects.all()
    if company_name:
        jobs = jobs.filter(company__id = company_name)
    if query:
        jobs = jobs.filter(
            Q(title__icontains = query)|
            Q(description__icontains = query)|
            Q(location__icontains=query)
        )

    return render(request, 'Job Lists.html', {'jobs': jobs,'query':query,
                                              'companies':companies,
            'selected_company': str(company_name) if company_name else None})

@login_required
def apply_job(request, job_id=None):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            messages.success(request, 'Application Submitted Successfully!!')
            return HttpResponseRedirect('/thanks/')

    else:
        form = ApplicationForm()
    return render(request, 'Apply.html', {'form': form, 'job': job})


def thank_you(request):
    return render(request, 'thank_you.html')


@staff_member_required
# @staff To Allow Only Members To See This Page
def application_list(request):
    job_id = request.GET.get('job')
    jobs = Job.objects.all()
    applications = Application.objects.select_related('job').order_by('-applied_at')
    if job_id:
        applications = applications.filter(job_id=job_id)

    return render(request, 'application_list.html', {
        'applications': applications,
        'jobs': jobs,
        'selected_job_id': int(job_id) if job_id else None
    })


# Edit Job Status View
def edit_application_status(request,application_id):
    application = get_object_or_404(Application, id =application_id)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST,instance=application)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/applications/')
    else:
        form = ApplicationStatusForm(instance=application)

    return render(request,'edit_application_status.html',{'form':form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfully. You can now log in.')
            return HttpResponseRedirect('login/')
    else:
        form = UserCreationForm()

    return render(request, 'register.html',{'form':form})

def my_applications(request):
    applications = Application.objects.filter(user=request.user)
    return render(request,'my_applications.html',{'applications':applications})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'phone': '', 'email': request.user.email}
    )
    applications = Application.objects.filter(user=request.user).order_by('-applied_at')
    context = {
        'profile':profile,
        'applications': applications
    }

    return render(request,'profile.html',context)

@login_required
def edit_profile(request):
    profile , created =Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated Successfully!!")
            return redirect('/profile/')
    else:
        form =ProfileForm(instance=profile)
    return render(request,'edit_profile.html',{'form':form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message Sent Successfully. We Will Contact You Soon.')
            return redirect('/')
    else:
            form = ContactForm()

    return render(request, 'contact.html',{'form':form})

# Create Notification View
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'notifications/notifications_list.html',{'notifications':notifications})

@login_required
def read_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.link or 'notifications')

# Blog Views
def blog_post(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request,'blog/blogList.html',{'posts':posts})

def blog_detail(request,post_id):
    post = get_object_or_404(Post,id = post_id,is_published=True)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post= post
                comment.author= request.user
                comment.save()
        else:
            return redirect('/login/')
    else:
        form = CommentForm()

    return render(request,'blog/blog_detail.html',{'post':post,'comments':comments,'form':form})

# Create View For Admin To Add Posts

def staff_check(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(staff_check)
def admin_add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            return redirect('dashboard_posts')
    else:
        form = PostForm()

    return render(request,'blog/add_post.html',{'form':form})

# Create View For Admin To Display All Posts
@login_required
def dashboard_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request,'blog/dashboard_posts.html',{'posts':posts})

def edit_post(request,post_id):
    post = get_object_or_404(Post,id=post_id,author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard_posts')

    else:
        form = PostForm(instance=post)

    return render(request,'blog/edit_post.html',{'form':form})

def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id,author=request.user)
    post.delete()
    messages.success=(request,'Post Deleted !!!!')
    return redirect('dashboard_posts')
@login_required
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')