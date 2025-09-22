from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que no requieren autenticación
        public_urls = [
            reverse('login'),
            reverse('registro'),
            reverse('inicio'),
        ]
        
        # Si el usuario no está autenticado y trata de acceder a una URL privada
        if not request.user.is_authenticated and request.path not in public_urls:
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
            # Agrega aquí otras URLs de administración
        ]
        
        # Si el usuario está autenticado pero no es admin y trata de acceder a una URL de admin
        if (request.user.is_authenticated and 
            request.path in admin_urls and 
            request.user.tipo_usuario != 'admin'):
            return redirect('inicio')
        
        response = self.get_response(request)
        return response