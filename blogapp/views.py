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
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required


@staff_member_required
def admin_dashboard(request):
    total_blogs = Blog.objects.count()
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    # Datos para gráfico: número de reseñas por blog
    blog_review_data = (
        Blog.objects.annotate(review_count=Count('reviews'))
        .values('title', 'review_count')
    )

    context = {
        'total_blogs': total_blogs,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 2),
        'blog_review_data': list(blog_review_data),
    }

    return render(request, 'admin_dashboard.html', context)



# Vista para listar blogs
class BlogListView(ListView):
    model = Blog  # ← Solo el modelo Blog, sin mezclar con otra clase
    template_name = 'blogapp/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 4 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Blogs mejor calificados (solo los que tienen reseñas)
        top_rated = Blog.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            num_reviews=Count('reviews')
        ).filter(num_reviews__gte=1).order_by('-avg_rating')[:5]

        context['top_rated_blogs'] = top_rated
        return context


# Vista para ver el detalle de un blog
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        promedio = blog.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        context['average_rating'] = round(promedio, 1) if promedio else 0

        user_review_exists = False
        if self.request.user.is_authenticated:
            user_review_exists = blog.reviews.filter(reviewer=self.request.user).exists()
        context['user_review_exists'] = user_review_exists

        return context



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