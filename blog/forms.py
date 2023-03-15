from django import forms
from django.contrib.auth.models import User
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class NewUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput()) #Esto es para que se oculte mientras la escribis.

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return confirm_password
    
    def save(self, commit=True): #primero guarda el usuario ingresado (pero no en la base de datos todavía), encripta contraseña y lo guarda.
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user