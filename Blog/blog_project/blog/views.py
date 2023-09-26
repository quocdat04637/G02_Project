from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category, Tag, User
from .forms import CommentForm, PostForm, RegistrationForm, LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm  # Tùy chỉnh form để cập nhật thông tin User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from datetime import datetime

# Create your views here.
def home(request):
    # Lấy tất cả bài đăng từ cơ sở dữ liệu
    posts = Post.objects.all()

    # Truyền danh sách bài đăng vào template
    context = {
        'posts': posts,
    }

    # Sử dụng template để render trang chủ và trả về HttpResponse
    return render(request, 'blog/home.html', context)


def post_list(request):
    # Logic để lấy danh sách bài viết từ CSDL và hiển thị lên trang web
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'post': posts})

def post_detail(request, pk):
    # Logic để hiển thị chi tiết bài viết và bình luận
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        # Xử lý bình luận mới nêú có
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


# Sử dụng form PostForm trong view để tạo bài viết mới hoặc chỉnh sửa bài viết
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = datetime.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

def delete_post(request, pk):
    # Lấy bài viết cần xoá từ CSDL hoặc trả về lỗi 404 nếu không tồn tại
    post = get_object_or_404(Post, pk=pk)

    # Kiểm tra quyền truy cập: chỉ người tạo bài viết mới được xoá
    if request.user == post.author:
        if request.method == 'POST':
            # Xoá bài viết nếu người dùng xác nhận xoá
            post.delete()
            return redirect('post_list')
        else:
            # Hiển thị trang xác nhận xoá bài viết
            return render(request, 'blog/post_confirm_delete.html', {'post': post})
    else:
        # Trả về lỗi 403 nếu không có quyền xoá
        return render(request, 'blog/post_delete_permission_denied.html')
    
def edit_post(request, pk):
    # Lấy bài viết cần chỉnh sửa từ CSDL hoặc trả về lỗi 404 nếu không tồn tại
    post = get_object_or_404(Post, pk=pk)

    # Kiểm tra quyền truy cập: chỉ người tạo bài viết mới được chỉnh sửa
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.updated_at = datetime.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        # Trả về lỗi 403 nếu không có quyền chỉnh sửa
        return render(request, 'blog/post_edit_permission_denied.html')
    
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Lấy danh sách bài viết thuộc thể loại này
    posts = category.post_set.all()
    return render(request, 'blog/category_detail.html', {'posts': posts})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Lấy danh sách bài viết liên quan đến tag này
    posts = tag.post_set.all()
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'posts': posts})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'comment_form': comment_form})


def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'blog/comment_list.html', {'comments': comments})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Đăng ký thành công!')
            return redirect('home')
    else:
        form = RegistrationForm()
    # Set a variable to indicate successful registration
    context = {'registration_successful': True, 'form': form}
    return render(request, 'blog/register.html', context)
            

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('home')
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
        else:
            messages.error(request, 'Tên đăng nhập và mật khẩu không hợp lệ.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')  
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)  
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'Đăng nhập thành công!')
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Email hoặc mật khẩu không đúng.')
#         else:
#             messages.error(request, 'Email và mật khẩu không hợp lệ.')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'blog/login.html', {'form': form})



@login_required
def profile_view(request):
    user = request.user  # Lấy thông tin người dùng hiện tại

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.password = make_password(new_password)  # Mã hóa mật khẩu mới
                update_session_auth_hash(request, user)  # Cập nhật session auth hash
            form.save()
            messages.success(request, 'Thông tin đã được cập nhật thành công.')
            return redirect('login')

    else:
        form = UserProfileForm(instance=user)

    return render(request, 'blog/profile.html', {'form': form})


def help(request):
    return render(request, 'blog/help.html')


def dashboard_view(request):
    return render(request, 'blog/dashboard.html')

def view_time(request):
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")  # Format as a string
    return render(request, 'blog/base.html', {'current_time': current_time_str})


def all_posts(request):
    render(request, 'blog/all_posts.html')