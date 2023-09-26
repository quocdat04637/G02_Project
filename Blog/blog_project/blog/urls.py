from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),

    # Đường dẫn đến danh sách bài viết
    path('', views.post_list, name='post_list'),

    # Đường dẫn đến chi tiết bài viết với sử dụng số nguyên làm primary key (pk)
    path('post/<int:pk>', views.post_detail, name='post_detail'),

    # Đường dẫn để tạo bài viết mới
    path('post/new/', views.create_post, name='create_post'),

    # Đường dẫn để chỉnh sửa bài viết với sử dụng số nguyên làm primary key (pk)
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),

    # Đường dẫn để xoá bài viết với sử dụng số nguyên làm primary key (pk)
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    
    # Đường dẫn đến trang danh sách các thể loại (categories)
    path('categories/', views.category_list, name='category_list'),

    # Đường dẫn đến trang chi tiết thể loại với sử dụng slug của thể loại
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    # Đường dẫn đến trang danh sách các tags
    path('tags/', views.tag_list, name='tag_list'),

    # Đường dẫn đến trang chi tiết tag với sử dụng slug của tag
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),

    # Đường dẫn để tạo bình luận mới cho bài viết
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),

    # Đường dẫn đến trang danh sách các bình luận
    path('comments/', views.comment_list, name='comment_list'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('profile_view/', views.profile_view, name='profile_view'),

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('help/', views.help, name='help'),

    path('dashboard_view/', views.dashboard_view, name='dashboard_view'),

    path('all_posts/', views.all_posts, name='all_posts'),




]