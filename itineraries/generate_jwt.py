import jwt
import datetime

# Replace with your secret key
SECRET_KEY = 'django-insecure-u$d4l-(2-*1i#ni6s2-1%6fz(n0xl*^+kt2ft)w0m01o8q^cku'

def generate_token(username, is_admin):
    payload = {
        
        'sub': username,
        'isAdmin': is_admin,
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=10)  # Token valid for 10 hours
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

if __name__ == "__main__":
    token = generate_token('testuser', True)
    print(f"Generated JWT Token: {token}")
