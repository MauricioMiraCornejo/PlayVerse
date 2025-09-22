from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db import IntegrityError
from .forms import RegistroForm, LoginForm, JuegoForm, ReservaForm, ItemCarritoForm, PasswordResetRequestForm, PasswordResetConfirmForm
from .models import Juego, Reserva, Carrito, ItemCarrito, Usuario, PasswordResetToken

def es_administrador(user):
    # MODIFICACIÓN: Usar is_superuser (campo nativo de Django) Y mantener compatibilidad con tipo_usuario
    #return user.is_superuser or user.tipo_usuario == 'admin'
    return user.is_superuser  == True

def inicio(request):    
    return render(request, "index.html")

def actividades(request):    
    return render(request, "informacion/actividades.html")  

@login_required
def reservas(request):     
    return render(request, "gestion/reservas.html")  

def ofertas(request):      
    return render(request, "gestion/ofertas.html") 

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
    else:
        form = LoginForm()
    return render(request, "acceso/login.html", {'form': form})  

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registro exitoso. ¡Bienvenido a PlayVerse!')
                return redirect('inicio')
            except IntegrityError:
                messages.error(request, 'Error al crear el usuario. El email o nombre de usuario ya existe.')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroForm()
    
    return render(request, "acceso/registro.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')

@login_required
def perfil(request):
    return render(request, "acceso/perfil.html")

# Decorador personalizado para verificar administrador
def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(
        es_administrador, 
        login_url='inicio'
    )(view_func))
    return decorated_view_func

# Vista solo para administradores
@admin_required
def administracion(request):
    return render(request, "gestion/administracion.html")

# VISTAS PARA RECUPERACIÓN DE CONTRASEÑA
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            usuario = Usuario.objects.get(email=email)
            
            # Eliminar tokens previos no utilizados
            PasswordResetToken.objects.filter(usuario=usuario, utilizado=False).delete()
            
            # Crear nuevo token
            token_obj = PasswordResetToken(usuario=usuario)
            token = token_obj.generar_token()
            token_obj.save()
            
            # Enviar correo electrónico (en consola para desarrollo)
            subject = 'Recuperación de contraseña - PlayVerse'
            html_message = render_to_string('acceso/password_reset_email.html', {
                'usuario': usuario,
                'token': token,
                'dominio': request.get_host(),
            })
            plain_message = strip_tags(html_message)
            
            # Para desarrollo, mostramos el token en consola
            print(f"Token de recuperación para {email}: {token}")
            print(f"URL de recuperación: http://{request.get_host()}/password-reset/confirm/{token}/")
            
            # En producción, descomenta esto para enviar emails reales:
            # send_mail(
            #     subject,
            #     plain_message,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [email],
            #     html_message=html_message,
            #     fail_silently=False,
            # )
            
            messages.success(request, 'Se ha enviado un correo con instrucciones para restablecer tu contraseña.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'acceso/password_reset_request.html', {'form': form})

def password_reset_done(request):
    return render(request, 'acceso/password_reset_done.html')

def password_reset_confirm(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token, utilizado=False)
        if not token_obj.es_valido():
            messages.error(request, 'El enlace de recuperación ha expirado o es inválido.')
            return redirect('password_reset_request')
        
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                # Actualizar contraseña
                usuario = token_obj.usuario
                new_password = form.cleaned_data['new_password1']
                usuario.set_password(new_password)
                usuario.save()
                
                # Marcar token como utilizado
                token_obj.utilizado = True
                token_obj.save()
                
                messages.success(request, 'Tu contraseña ha sido restablecida correctamente. Ahora puedes iniciar sesión.')
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
        
        return render(request, 'acceso/password_reset_confirm.html', {'form': form, 'token': token})
    
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'El enlace de recuperación es inválido.')
        return redirect('password_reset_request')

def password_reset_complete(request):
    return render(request, 'acceso/password_reset_complete.html')

# VISTAS PARA JUEGOS (CRUD)
@admin_required
def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, 'gestion/lista_juegos.html', {'juegos': juegos})

@admin_required
def crear_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Juego creado exitosamente.')
                return redirect('lista_juegos')
            except IntegrityError:
                messages.error(request, 'Error al crear el juego. Verifique los datos.')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = JuegoForm()
    
    return render(request, 'gestion/form_juego.html', {'form': form, 'titulo': 'Crear Juego'})

@admin_required
def editar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    if request.method == 'POST':
        form = JuegoForm(request.POST, instance=juego)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Juego actualizado exitosamente.')
                return redirect('lista_juegos')
            except IntegrityError:
                messages.error(request, 'Error al actualizar el juego.')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = JuegoForm(instance=juego)
    
    return render(request, 'gestion/form_juego.html', {'form': form, 'titulo': 'Editar Juego'})

@admin_required
def eliminar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    if request.method == 'POST':
        try:
            juego.delete()
            messages.success(request, 'Juego eliminado exitosamente.')
            return redirect('lista_juegos')
        except Exception as e:
            messages.error(request, f'Error al eliminar el juego: {str(e)}')
            return redirect('lista_juegos')
    
    return render(request, 'gestion/confirmar_eliminacion.html', {'objeto': juego})

# VISTAS PARA CARRITO
@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.itemcarrito_set.all()
    total = items.aggregate(total=Sum('precio'))['total'] or 0
    
    return render(request, 'gestion/carrito.html', {
        'items': items,
        'total': total
    })

@login_required
def agregar_al_carrito(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        juego=juego,
        defaults={'precio': juego.precio, 'cantidad': 1}
    )
    
    if not created:
        item.cantidad += 1
        item.precio = juego.precio * item.cantidad
        item.save()
    
    messages.success(request, f'{juego.nombre} agregado al carrito.')
    return redirect('ver_carrito')

@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    
    if request.method == 'POST':
        form = ItemCarritoForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.precio = item.juego.precio * item.cantidad
            item.save()
            messages.success(request, 'Carrito actualizado.')
    
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Item eliminado del carrito.')
    return redirect('ver_carrito')

# VISTAS PARA RESERVAS
@login_required
def lista_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'gestion/lista_reservas.html', {'reservas': reservas})

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user  # Asignar usuario automáticamente
            reserva.estado = 'pendiente'    # Estado por defecto
            reserva.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('lista_reservas')
    else:
        # Si viene de ofertas con actividad predefinida
        actividad = request.GET.get('actividad', '')
        form = ReservaForm(initial={'actividad': actividad} if actividad else None)
    
    return render(request, 'gestion/reservas.html', {'form': form})

@login_required
def cancelar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id, usuario=request.user)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva cancelada exitosamente.')
        return redirect('lista_reservas')
    return render(request, 'gestion/confirmar_cancelacion.html', {'reserva': reserva})

# CATEGORIAS
def terror(request):     
    return render(request, "categorias/terror.html")  

def accion(request):     
    return render(request, "categorias/accion.html")  

def carreras(request):     
    return render(request, "categorias/carreras.html")  

def mundoabierto(request):     
    return render(request, "categorias/mundoabierto.html")  

def suspenso(request):     
    return render(request, "categorias/suspenso.html")  

# JUEGOS - Vistas de detalle
def alien(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Alien")
    return render(request, "juegos/alien.html", {'juego': juego})  

def eldenring(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Elden Ring")
    return render(request, "juegos/eldenring.html", {'juego': juego})

def halo3(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Halo 3")
    return render(request, "juegos/halo3.html", {'juego': juego})

def horizon(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Horizon")
    return render(request, "juegos/horizon.html", {'juego': juego})

def mariokart(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Mario Kart")
    return render(request, "juegos/mariokart.html", {'juego': juego})

def outlast(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Outlast")
    return render(request, "juegos/outlast.html", {'juego': juego})

def projectcars3(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Project CARS 3")
    return render(request, "juegos/projectcars3.html", {'juego': juego})

def resident_evil(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Resident Evil")
    return render(request, "juegos/resident_evil.html", {'juego': juego})

def silentHill2(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Silent Hill 2")
    return render(request, "juegos/SilentHill2.html", {'juego': juego})

def spiderman(request):     
    juego = get_object_or_404(Juego, nombre__icontains="Spiderman")
    return render(request, "juegos/spiderman.html", {'juego': juego})