import json

from django.http import JsonResponse

def error_response(title, message, state,  status, payload=None, error=None, message_view=True, redirect=None):
    return JsonResponse({
        'title': title,
        'message': message,
        'state': state,
        'status': status,
        'message_view': message_view,
        'redirect': redirect,
        'payload': payload,
        'error': error
    }, status=status)

def success_response(title, message, state,  status, payload=None, error=None, message_view=True, redirect=None):
    return JsonResponse({
        'title': title,
        'message': message,
        'state': state,
        'status': status,
        'message_view': message_view,
        'redirect': redirect,
        'payload': payload,
        'error': error
    }, status=status)

def socket_response(event, payload):
    return str(json.dumps({
        'event': event,
        'payload': payload,
    }))




