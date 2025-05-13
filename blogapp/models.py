from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# MODELOS

class Blog(models.Model):
    title = models.CharField(max_length=200)  # Nota: 'title' no 'titulo'
    content = models.TextField()  # Nota: 'content' no 'contenido'
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} - {self.blog.title}"



from django.contrib.auth.models import User

class Comment(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_comments')
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username}"
    
    class Review(models.Model):
     blog = models.ForeignKey(Blog, related_name='reviews', on_delete=models.CASCADE)
     reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     rating = models.IntegerField()
     comment = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reviewer.username} - {self.rating} stars'