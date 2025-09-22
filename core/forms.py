from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Juego, Reserva, Carrito, ItemCarrito, PasswordResetToken

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'fecha_nacimiento', 'password1', 'password2', 'direccion', 'telefono']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Correo electrónico')
    
    def clean_username(self):
        return self.cleaned_data['username']

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen', 'stock', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descripción detallada del juego...',
                'class': 'form-control'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del juego'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL de la imagen (ej: img/juego.jpg)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo')
        return stock

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['actividad', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class ItemCarritoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrito
        fields = ['juego', 'cantidad']

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su correo electrónico'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Usuario.objects.filter(email=email).exists():
            raise ValidationError('No existe una cuenta con este correo electrónico.')
        return email

class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña'
        }),
        min_length=6,
        max_length=18
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su nueva contraseña'
        }),
        min_length=6,
        max_length=18
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError('Las contraseñas no coinciden.')
        
        # Validaciones adicionales de contraseña
        if new_password1:
            if not any(char.isupper() for char in new_password1):
                raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
            if not any(char.isdigit() for char in new_password1):
                raise ValidationError('La contraseña debe contener al menos un número.')
        
        return cleaned_data