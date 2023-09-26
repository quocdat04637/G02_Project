from django import forms
from .models import Comment, Post, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Chỉ cho phép người dùng nhập nội dung bình luận


class PostForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ['title', 'content', 'image', 'status', 'category', 'tags',] # Chọn các trường dữ liệu bạn muốn cho phép người dùng chỉnh sửa