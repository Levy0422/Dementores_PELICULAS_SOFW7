from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView,
    ReviewCreateView, CommentCreateView,
    CustomLoginView, CustomLogoutView, RegisterView
)

app_name = 'blogapp'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('add/', BlogCreateView.as_view(), name='add_blog'),
    path('login/', CustomLoginView.as_view(), name='login'),
      path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', 
         CommentCreateView.as_view(), name='add_comment'),
]