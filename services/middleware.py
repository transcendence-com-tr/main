import jwt
from django.conf import settings
from django.urls import reverse
from .responses import error_response
from django.urls import resolve, Resolver404
from django.http import JsonResponse
from transcendence.services.models.user import User

class DisableCSRFMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.path.startswith('/api')):
            return self.get_response(request)
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response

class URLPathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if (not request.path.startswith('/api')):
            return self.get_response(request)
        if not request.path.endswith('/'):
            request.path_info = request.path = f"{request.path}/"
        try:
            resolve(request.path_info)
        except Resolver404:
            return error_response("URL Error", "URL not found", "error",
                                   404, None, {'url': {'required': 'URL not found or in invalid format'}})
        return self.get_response(request)


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.path.startswith('/api')):
            return self.get_response(request)
        excluded_paths = [
            reverse('auth:register'),
            reverse('auth:login'),
            reverse('auth:login_42'),
            reverse('auth:login_42_callback'),
            reverse('auth:forgot_password'),
            reverse('frontend:register'),
            reverse('frontend:login'),
            reverse('frontend:help')
        ]
        if any(request.path == path for path in excluded_paths):
            return self.get_response(request)
        token = request.headers.get('Authorization')
        if token is None or not token.startswith('Bearer '):
            return error_response(
                "Unauthorized Token",
                "Token not provided or invalid",
                "error",
                401,
                None,
                None,
                False
            )
        token = token.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            request.user = User.objects.get(id=user_id)
            request.user.verify_code = payload.get('verify_code')
            request.user.password_code = payload.get('password_code')
            request.user.is_verified = payload.get('is_verified')
            if ((request.user.is_verified == False or request.user.is_verified == None)):
                paths = [
                    reverse('auth:two_factor'),
                    reverse('auth:two_factor_verify'),
                    reverse('frontend:two_factor_auth'),
                    reverse('auth:me'),
                    reverse('frontend:logout'),
                    reverse('auth:reset_password'),
                    reverse("auth:connect_42"),
                    reverse("frontend:connect_42"),
                    reverse("frontend:register_42"),
                    reverse('auth:auth'),
                ]
                if not any(request.path == path for path in paths):
                    if (request.user.username == None or request.user.email == None):
                        return error_response(
                            "Unauthorized Token",
                            "User not verified",
                            "error",
                            401,
                            None,
                            None,
                            True, "#/42-register")
                    return error_response(
                        "Unauthorized Token",
                        "User not verified",
                        "error",
                        401,
                        None,
                        None,
                        True, "#/2fa")
                else:
                    return self.get_response(request)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return error_response(
                "Unauthorized Token",
                "Token expired or invalid",
                "error",
                401,
                None,
                None,
                False
            )

        response = self.get_response(request)
        return response
