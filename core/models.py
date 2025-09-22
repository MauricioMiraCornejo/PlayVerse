from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
import secrets
import string
from django.utils import timezone
from datetime import timedelta

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    ]
    
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='cliente')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Juego(models.Model):
    CATEGORIA_CHOICES = [
        ('terror', 'Terror'),
        ('accion', 'Acción'),
        ('carreras', 'Carreras'),
        ('mundoabierto', 'Mundo Abierto'),
        ('suspenso', 'Suspenso'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    imagen = models.CharField(max_length=200)  # URL de la imagen
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    actividad = models.CharField(max_length=100)
    fecha = models.DateField()
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')

class PasswordResetToken(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    utilizado = models.BooleanField(default=False)
    
    def es_valido(self):
        # El token es válido por 24 horas
        return not self.utilizado and (timezone.now() - self.fecha_creacion) < timedelta(hours=24)
    
    def generar_token(self):
        alphabet = string.ascii_letters + string.digits
        self.token = ''.join(secrets.choice(alphabet) for i in range(50))
        return self.token
    
    def __str__(self):
        return f"Token para {self.usuario.email}"