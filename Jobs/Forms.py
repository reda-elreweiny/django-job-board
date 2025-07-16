from django import forms
from .models import Application
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import ContactUs,Comment,Post


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'email', 'cv']

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields= ['status']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username','password1','password2']

    def save(self, commit=True):
        user = super().save(commit)
        profile = Profile.objects.create(
            user=user,
            email=self.cleaned_data['email'],
            phone = self.cleaned_data['phone']
        )
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email','phone','avatar']
        widgets={
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone' : forms.TextInput(attrs={'class':'form-control'})
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name','email','message']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Your Name'}),
            'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Your Email'}),
            'message' : forms.Textarea(attrs={'class':'form-control','placeholder':'Your Message'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['content']
        widgets = {
            'content' : forms.Textarea(attrs={'rows':3,'class':'form-control','placeholder':'Write Your Comment.....'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['title', 'content', 'image', 'category', 'is_published']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'content' : forms.Textarea(attrs={'class':'form-control','rows':5,'placeholder':'Enter Content Of Post ...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(),
        }