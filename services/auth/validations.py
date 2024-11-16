from validator import Validator

class RegisterValidator(Validator):
    username = 'required|username|max_length:255'
    email = 'required|email|max_length:255'
    password = 'required|password:high|max_length:255'
    ## custom messages if you want
    message = {
        'password': {
            'password': "Password length must longer than 7 and it sould contains lower , upper latin characters and digits, and special",
            'max_length': "Password length must be less than 255"
        },
        'username': {
            'username': "Username not proper format",
            'max_length': "Username length must be less than 255"
        },
        'email': {
            'email': "Email is not an email address",
            'max_length': "Email length must be less than 255"
        }
    }

class LoginValidator(Validator):
    email_or_username = 'required|max_length:255'
    password = 'required|max_length:255'

    message = { 
        'email_or_username': {
            'max_length': "Email or Username length must be less than 255"
        },
        'password': {
            'max_length': "Password length must be less than 255" 
        }
    }

class UpdateUserValidator(Validator):
    
    email = 'email|max_length:255'
    username = 'username|max_length:255'
    message = {
        'email': {
            'email': "Email is not an email address",
            'max_length': "Email or Username length must be less than 255"
        },
        'username': {
            'username': "Username not proper format",
            'max_length': "Username length must be less than 255"
        },
    }


class PasswordResetValidator(Validator):
    password = 'required|password:high|max_length:255'
    message = {
        'password': {
            'password': "Password length must longer than 7 and it sould contains lower , upper latin characters and digits, and special",
            'max_length': "Email length must be less than 255"
        }
    }

class PasswordForgotValidator(Validator):
    email_or_username = 'required|max_length:255'
    message = {
        'email_or_username': {
            'max_length': "Email length must be less than 255"
        }
    }