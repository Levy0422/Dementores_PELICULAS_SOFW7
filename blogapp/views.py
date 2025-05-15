from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Blog, Review, Comment
from .forms import BlogForm  
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
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
class BlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = 'blogapp/blog_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'files': self.request.FILES})  # <--- Pasa los archivos correctamente
        return kwargs

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.save()
        messages.success(self.request, "¡Blog creado exitosamente!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})

# Vista para crear reseñas (reviews)
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']                # ← usa 'comment', no 'content'
    template_name = 'blogapp/review_form.html'

    def form_valid(self, form):
        # asignar autor y blog
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        # (ya NO intentes leer form.cleaned_data['content'])
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige de nuevo al detalle del blog
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