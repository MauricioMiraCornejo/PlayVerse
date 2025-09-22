from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que no requieren autenticación
        public_urls = [
            reverse('login'),
            reverse('registro'),
            reverse('inicio'),
            reverse('actividades'),
            reverse('ofertas'),
            reverse('terror'),
            reverse('accion'),
            reverse('carreras'),
            reverse('mundoabierto'),
            reverse('suspenso'),
            # URLs de detalles de juegos
            reverse('resident_evil'),
            reverse('outlast'),
            reverse('alien'),
            reverse('silentHill2'),
            reverse('horizon'),
            reverse('eldenring'),
            reverse('mariokart'),
            reverse('projectcars3'),
            reverse('spiderman'),
            reverse('halo3'),
            # URLs de recuperación de contraseña
            reverse('password_reset_request'),
            reverse('password_reset_done'),
            reverse('password_reset_confirm', args=['token']).replace('/token/', ''),
            reverse('password_reset_complete'),
        ]
        
        # Si el usuario no está autenticado y trata de acceder a una URL privada
        if (not request.user.is_authenticated and 
            not any(request.path == url or request.path.startswith(url.replace('/token/', '')) for url in public_urls) and
            not request.path.startswith('/static/') and  # Excluir archivos estáticos
            not request.path.startswith('/media/')):     # Excluir archivos media
            
            messages.error(request, '🔒 Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        response = self.get_response(request)
        return response


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que requieren ser administrador
        admin_urls = [
            '/administracion/',
            '/admin/juegos/',
            '/juegos/crear/',
            '/juegos/editar/',
            '/juegos/eliminar/',
            # Agrega aquí otras URLs de administración
        ]
        
        # Si el usuario está autenticado pero no es admin y trata de acceder a una URL de admin
        if (request.user.is_authenticated and 
            any(request.path.startswith(url) for url in admin_urls) and 
            request.user.tipo_usuario != 'admin' and
            not request.user.is_superuser):
            
            messages.error(request, '❌ Acceso denegado. Se requieren permisos de administrador.')
            return redirect('inicio')
        
        response = self.get_response(request)
        return response


class ClienteAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que requieren ser cliente
        cliente_urls = [
            '/carrito/',
            '/reservas/lista/',
            '/reservas/crear/',
            '/reservas/cancelar/',
        ]
        
        # Si el usuario está autenticado pero no es cliente y trata de acceder a una URL de cliente
        if (request.user.is_authenticated and 
            any(request.path.startswith(url) for url in cliente_urls) and 
            request.user.tipo_usuario != 'cliente'):
            
            messages.error(request, '⚠️ Esta función está disponible solo para clientes.')
            return redirect('inicio')
        
        response = self.get_response(request)
        return response