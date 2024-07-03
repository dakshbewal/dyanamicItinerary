import jwt
from django.conf import settings
from django.http import JsonResponse

SECRET_KEY = settings.SECRET_KEY

def token_required(f):
    def wrap(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'message': 'Token is missing!'}, status=403)
        
        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_data = data  # Attach the token data to the request object
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token has expired!'}, status=403)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid Token!'}, status=403)
        
        return f(request, *args, **kwargs)
    
    return wrap
