from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField

# MODELO DE BLOG
class Blog(models.Model):
    GENRE_CHOICES = [
        ('accion', 'Acción'),
        ('aventura', 'Aventura'),
        ('comedia', 'Comedia'),
        ('drama', 'Drama'),
        ('terror', 'Terror'),
        ('romance', 'Romance'),
        ('documental', 'Documental'),
        ('animacion', 'Animación'),
        ('fantasia', 'Fantasía'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    content = RichTextField()
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        blank=False,  
        null=False    
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# MODELO DE RESEÑAS
class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} - {self.blog.title}"

# MODELO DE COMENTARIOS A RESEÑAS
class Comment(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_comments')
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username}"


