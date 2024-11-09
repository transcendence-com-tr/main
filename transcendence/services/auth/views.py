from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from transcendence.services.models.user import User
from rest_framework.permissions import AllowAny
from .validations import RegisterValidator , LoginValidator , UpdateUserValidator , PasswordResetValidator , PasswordForgotValidator
from .checkers import check_register_user, check_login_user, check_auth_user
from transcendence.services.responses import error_response, success_response
import jwt
from django.conf import settings
from django.core.mail import send_mail
import requests
import random
import time
from django.utils.crypto import get_random_string
import datetime
import os

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    errors = {}
    validator = RegisterValidator({'username': username, 'email': email, 'password': password})
    status = validator.validate()
    user_errors = check_register_user(email, username)
    if user_errors:
            errors.update(user_errors)
    if status and not errors:
        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password
        )
        user.save()
        token = jwt.encode({
            "user_id": user.id,
        }, settings.SECRET_KEY, algorithm='HS256')
        return success_response("Register Succeed", "Successfully registered", "success", 200, {
            "token": token
        }, None, True, "#/home")
    else:
        errors.update(validator.get_message())
        return error_response("Register Error", "An error was encountered while registering", "error", 400, None,
                              errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    email_or_username = data.get('email_or_username').strip()
    password = data.get('password')
    validator = LoginValidator({'email_or_username': email_or_username, 'password': password})
    status = validator.validate()
    if status:  
        errors = check_login_user(email_or_username, password)
        if errors:
            return error_response("Login Error", "An error was encountered while logging in", "error", 400, None,
                                  errors)
        else:
            try:
                user = User.objects.get(email=email_or_username)
            except User.DoesNotExist:
                user = User.objects.get(username=email_or_username)
            token = jwt.encode({
                "user_id": user.id,
            }, settings.SECRET_KEY, algorithm='HS256')
            return success_response("Login Succeed", "Successfully logged in", "success", 200, {
                "token": token
            }, None, True, "#/2fa")
    else:
        errors = validator.get_message()
        return error_response("Login Error", "An error was encountered while logging in",
                              "error", 400, None, errors)


@api_view(['GET'])
@permission_classes([AllowAny])
def me(request):
    return success_response("User Info", "User information is successfully fetched", "success", 200, {
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "username_42": request.user.username_42,
            "email_42": request.user.email_42,
        }}, None, None)

@api_view(['GET'])
@permission_classes([AllowAny])
def login_42(request):
    return success_response("42 Login redirection", "You are redirecting to 42 login page", "success",
                            200, None, None, True,
                            settings.CONNECT_LINK42)

@api_view(['GET'])
@permission_classes([AllowAny])
def login_42_callback(request):
    code = request.GET.get('code')
    response = requests.post('https://api.intra.42.fr/oauth/token', data={
        'grant_type': 'authorization_code',
        'client_id': settings.CLIENT_ID42,
        'client_secret': settings.CLIENT_SECRET42,
        'code': code,
        'redirect_uri': 'http://localhost/'
    })
    data = response.json()
    access_token = data.get('access_token')
    user_42 = requests.get('https://api.intra.42.fr/v2/me', headers={
        'Authorization': f'Bearer {access_token}'
    }).json()
    if (user_42.get('login') == None):
        return error_response("42 Login Error", "42 login failed", "error", 400, None, None, True, "#/login")
    
    ## ikinci kez giridiğinde ve username ataması yapılmışsa direkt girecek
    if (User.objects.filter(username_42=user_42.get('login'), username__isnull=False).exists()):
        user_id = User.objects.get(username_42=user_42.get('login')).id
        token = jwt.encode({
                "user_id": user_id,
            }, settings.SECRET_KEY, algorithm='HS256')
        return success_response("42 Login Succeed", "Successfully logged in with 42", "success", 200, {'token': token}, None, True, "#/2fa")
    ## username ve email ataması yapılmamışsa
    else:
        ## ilk kez giriyorsa ve çakışma yok ise kayıt yapacak ve 2fa'e yönlendirelecek
        if (not User.objects.filter(username=user_42.get('login')).exists() and not User.objects.filter(email=user_42.get('email')).exists()):
            image = user_42.get('image').get('link')
            response = requests.get(image)

            if response.status_code == 200:
                save_directory = os.path.join(settings.IMAGE_ROOT, 'users')
                os.makedirs(save_directory, exist_ok=True)

                file_name = get_random_string(length=32) + '.jpg'
                image = "/assets/images/users/" + file_name
                file_name = os.path.join(save_directory, file_name)
                with open(file_name, 'wb') as file:
                    file.write(response.content)
            else:
                image = "/assets/images/users/default-profile.png"
            user = User.objects.create(
                username_42=user_42.get('login'),
                email_42=user_42.get('email'),
                username=user_42.get('login'),
                email=user_42.get('email'),
                image=image,
                password=make_password(get_random_string(length=32))
            )
            token = jwt.encode({
                "user_id": user.id,
            }, settings.SECRET_KEY, algorithm='HS256')
            user.save()
            return success_response("42 Login Succeed", "Successfully logged in with 42", "success", 200, {'token': token}, None, True, "#/2fa")
        ## ilk kez giriyorsa ve çakışma var ise;
        elif (User.objects.filter(username=user_42.get('login')).exists() or User.objects.filter(email=user_42.get('email')).exists()):
            image = user_42.get('image').get('link')
            response = requests.get(image)
            if response.status_code == 200:
                save_directory = os.path.join(settings.IMAGE_ROOT, 'users')
                os.makedirs(save_directory, exist_ok=True)

                file_name = get_random_string(length=32) + '.jpg'
                image = "/assets/images/users/" + file_name
                file_name = os.path.join(save_directory, file_name)
                with open(file_name, 'wb') as file:
                    file.write(response.content)
            else:
                image = "/assets/images/users/default-profile.png"
            ## ilk kez giriyorsa ve çakışma var ise(kayıt yapılmalı) ve kayıdı yapılmamışsa 42-register'a yönlendirecek
            if (not User.objects.filter(username_42=user_42.get('login')).exists()):
                user = User.objects.create(
                    username_42=user_42.get('login'),
                    email_42=user_42.get('email'),
                    image=image,
                    password=make_password(get_random_string(length=32)),
                )
                user.save()
                token = jwt.encode({
                    "user_id": user.id,
                }, settings.SECRET_KEY, algorithm='HS256')
                return success_response("42 Login Succeed", "Successfully logged in with 42", "success", 200, {'token': token}, None, True, "#/42-register")
            ## ilk kez giriyorsa ve çakışma var ve kayıdı yapılmışsa(tekrar kayıt yapılmamalı) gene 2fa'ye yönlendirecek
            else:
                user_id = User.objects.get(username_42=user_42.get('login')).id
                token = jwt.encode({
                    "user_id": user_id,
                }, settings.SECRET_KEY, algorithm='HS256')
                return success_response("42 Login Succeed", "Successfully logged in with 42", "success", 200, {'token': token}, None, True, "#/42-register")


@api_view(['PUT'])
def auth(request):
    data = request.data
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    image = request.FILES.get('image')

    if not request.user.email and not request.user.username:
        errors = {}
        validator = RegisterValidator({'username': username, 'email': email, 'password': password})
        if email or username:
            user_errors = check_register_user(email, username)
            if user_errors:
                errors.update(user_errors)
        status = validator.validate()
        if status and not errors:
            hashed_password = make_password(password)
            User.objects.filter(id=request.user.id).update(email=email, password=hashed_password, username=username)
            return success_response("Update Succeed", "User successfully updated", "success", 200, None, None, True, "#/home")
        elif not status or errors:
            errors.update(validator.get_message())
            return error_response("Update Error", "An error was encountered while updating", "error", 400, None, errors, False)
    else:
        if not email and not username and not image:
            return error_response("Update Error", "At least one field required", "error", 400, None, None, True, None)
        errors = {}
        if (request.user.email != email or request.user.username != username):
            user_errors = check_auth_user(email, username , request.user.id) ## changed
            if user_errors:
                errors.update(user_errors)
        validator = UpdateUserValidator({'email': email, 'username': username})
        status = validator.validate()
        if status and not errors:
            # changed
            if email:
                User.objects.filter(id=request.user.id).update(email=email)  
            if username:
                User.objects.filter(id=request.user.id).update(username=username)
            if image:
                save_directory = os.path.join(settings.IMAGE_ROOT, 'users')
                os.makedirs(save_directory, exist_ok=True)
                file_name = get_random_string(length=32) + '.jpg'
                new_image = "/assets/images/users/" + file_name
                file_name = os.path.join(save_directory, file_name)
                with open(file_name, 'wb') as file:
                    for chunk in image.chunks():
                        file.write(chunk)
                User.objects.filter(id=request.user.id).update(image=new_image)
                old_image_path = os.path.join(settings.BASE_DIR, 'transcendence/frontend' + request.user.image)
                if (request.user.image 
                    and request.user.image != "/assets/images/default-profile.png" ## changed
                    and os.path.exists(old_image_path)):
                    os.remove(old_image_path)
            return success_response("Update Succeed", "User successfully updated", "success", 200, None, None, True, "#/home")
        else:
            errors.update(validator.get_message())
            return error_response("Update Error", "An error was encountered while updating", "error", 400, None, errors, False)

### test'i yapılacak
@api_view(['PUT'])
@permission_classes([AllowAny])
def connect_42(request):
    data = request.data
    email_or_username = data.get('email_or_username').strip()
    password = data.get('password')
    validator = LoginValidator({'email_or_username': email_or_username, 'password': password})
    status = validator.validate()
    if status:
        errors = check_login_user(email_or_username, password)
        if errors:
            return error_response("Login Error", "An error was encountered while logging in", "error", 400, None,
                                  errors)
        else:
            try:
                user = User.objects.get(email=email_or_username)
            except User.DoesNotExist:
                user = User.objects.get(username=email_or_username)
            User.objects.filter(id=request.user.id).delete()
            User.objects.filter(id=user.id).update(username_42=request.user.username_42, email_42=request.user.email_42)
            token = jwt.encode({
                "user_id": user.id,
            }, settings.SECRET_KEY, algorithm='HS256')
            return success_response("42 Connect Succeed", "Successfully connected to 42", "success", 200, {'token':token}, None, True, "#/2fa")
    else:
        errors = validator.get_message()
        return error_response("Login Error", "An error was encountered while logging in",
                              "error", 400, None, errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def two_factor(request):
    #random code 6 digit
    verify_code = random.randint(100000, 999999)

    token = jwt.encode({
        "user_id": request.user.id,
        'verify_code': str(verify_code),
        "exp":  datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
    }, settings.SECRET_KEY, algorithm='HS256')
    email = request.user.email

    try: 
        print(email)
        ## changed
        if (email != None):
            send_mail(
            'Activate Your Account',
            'Activate your account with this code: ' + str(verify_code),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,)
    except:
        return error_response("Email Verification Error", "Email could not be sent", "error", 400, None, None, True, None)

    return success_response("Email Verification Succeed", "Email verification sent successfully", "success", 200, {
        "token": token
    }, None, True)


@api_view(['POST'])
@permission_classes([AllowAny])
def two_factor_verify(request):
    verify_code = request.data.get('verify_code')
    if (verify_code == request.user.verify_code):
        token = jwt.encode({
            "user_id": request.user.id,
            "is_verified": True,
            "exp":  datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
        }, settings.SECRET_KEY, algorithm='HS256')
        return success_response("Verification Succeed", "Verification succeed", "success", 200, {
            "token": token
        }, None, True, "#/home")
    else:
        return error_response("Verification Error", "Verification failed", "error", 400, None, None, True, None)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email_or_username = request.data.get('email_or_username')

    validator = PasswordForgotValidator({'email_or_username': email_or_username})
    status = validator.validate()

    if status:
        if ('@' in email_or_username):
            email = email_or_username
        else:
            username = email_or_username
            if (User.objects.filter(username=username).exists()):
                email = User.objects.get(username=username).email
            else:
                return error_response("Email Verification Error", "Username didn't find", "error", 400, None, None, True, "#/reload")

        if email and (User.objects.filter(email=email).exists()):
            password_code = random.randint(100000, 999999)
            user = User.objects.get(email=email)
            token = jwt.encode({
                "user_id": user.id,
                'password_code': str(password_code),
                "exp":  datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
            }, settings.SECRET_KEY, algorithm='HS256')
            send_mail(
                'Reset Password',
                'Reset your password with this code: ' + str(password_code),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return success_response("Email Verification Succeed", "Email verification sent successfully", "success", 200, {
                "token": token
            }, None, True)
    
        else:
            return error_response("Email Verification Error", "Email not found", "error", 400, None, None, True, "#/reload")
        
    else:
        errors = validator.get_message()
        return error_response("Email Verification Error", "An error was encountered while sending email", "error", 400, None, errors, "true", "#/reload")

    

@api_view(['PUT'])
@permission_classes([AllowAny])
def reset_password(request):
    password_code = request.data.get('password_code')
    password = request.data.get('password')

    validator = PasswordResetValidator({'password': password})
    status = validator.validate()
    if status:
        if (password_code == request.user.password_code):
            hashed_password = make_password(password)
            User.objects.filter(id=request.user.id).update(password=hashed_password)
            token = jwt.encode({
                "user_id": request.user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
            }, settings.SECRET_KEY, algorithm='HS256')
            return success_response("Password Reset Succeed", "Password reset succeed", "success", 200, {
                "token": token}, None, True, "#/home")
        else:
            return error_response("Password Reset Error", "Password code is invalid", "error", 400, None, None, True, None)
        
    else:
        errors = validator.get_message()
        return error_response("Password Reset Error", "An error was encountered while resetting password", "error", 400, None, errors)