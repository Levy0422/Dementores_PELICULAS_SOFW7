from django import forms
from .models import Blog
from .models import Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.HiddenInput()
        self.fields['content'].required = True
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '<p><br></p>':
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