from django import forms
from .models import Blog
from .models import Comment



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded bg-gray-800 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-500',
                'rows': 10,
                'placeholder': 'Escribe tu contenido aquí...'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("El contenido no puede estar vacío")
        return content


    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # El usuario y la review se asignan en la vista

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("El comentario no puede estar vacío.")
        return content   