from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

# Vista para listar blogs
class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
    context_object_name = 'blogs'

# Vista para detalle de blog
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'
    context_object_name = 'blog'

# Vista para crear blogs (requiere login)
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blogapp/blog_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})

# Vista para crear reseñas
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'
    
    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})

# Vista para crear comentarios
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'
    
    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})

# Vista personalizada para login
class CustomLoginView(LoginView):
    template_name = 'blogapp/login.html'
    
    def get_success_url(self):
        return reverse_lazy('blogapp:blog_list')

# Vista personalizada para logout
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('blogapp:login')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
# Vista para registro de usuarios
class RegisterView(CreateView):
    template_name = 'blogapp/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blogapp:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "¡Registro exitoso! Por favor inicia sesión.")
        return response