from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView,
    ReviewCreateView, CommentCreateView,
    CustomLoginView, CustomLogoutView, RegisterView
)

app_name = 'blogapp'

urlpatterns = [
    # Blogs
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),  # Cambiado a 'blog/add/' para mejor estructura
    
    # Autenticación
    path('accounts/login/', CustomLoginView.as_view(), name='login'),  # Mejor práctica para URLs de login
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    
    # Reviews y Comments
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', 
         CommentCreateView.as_view(), name='add_comment'),
]