from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .models import Blog, Review, Comment
from .forms import BlogForm


# Vista para listar blogs
class BlogListView(ListView):
    model = Blog  # ← Solo el modelo Blog, sin mezclar con otra clase
    template_name = 'blogapp/blog_list.html'
    context_object_name = 'blogs'


# Vista para ver el detalle de un blog
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'
    context_object_name = 'blog'


# Vista para crear blogs (requiere login)
# Vista para crear blogs (requiere login)
class BlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = 'blogapp/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.save(author=self.request.user)
        self.object = form.save()
        messages.success(self.request, "¡Blog creado exitosamente!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})



# Vista para crear reseñas (reviews)
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        print("Contenido recibido:", form.cleaned_data['content'])
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


# Vista para registrar nuevos usuarios
class RegisterView(CreateView):
    template_name = 'blogapp/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blogapp:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "¡Registro exitoso! Por favor inicia sesión.")
        return response


from django.shortcuts import get_object_or_404, redirect
from .models import Blog, Review
from django.contrib.auth.decorators import login_required

@login_required
def add_review(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # Evitar reseñas duplicadas por el mismo usuario
    if Review.objects.filter(blog=blog, reviewer=request.user).exists():
        return redirect('blogapp:blog_detail', pk=pk)  # O un mensaje

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            blog=blog,
            reviewer=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('blogapp:blog_detail', pk=pk)