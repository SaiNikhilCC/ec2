from rest_framework.authentication import BasicAuthentication
import jwt
from ecommerce.settings import SECRET_KEY
from rest_framework.exceptions import AuthenticationFailed

class CustomAuthentication(BasicAuthentication):
     
    def authenticate(self,request):
        try:
            # print(request.headers)
            authorization_data = request.headers.get('Authorization')
            # print(authorization_data)
            if 'Authorization' in request.headers.keys():            
                data = authorization_data.split(" ")
                token = data[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                return (payload,None)
            else:
                raise  AuthenticationFailed('No token found!')
        except jwt.exceptions.ExpiredSignatureError as e:
            raise AuthenticationFailed('Token expired')
        except jwt.exceptions.DecodeError as e:
            raise AuthenticationFailed('Decode error')
        except jwt.exceptions.InvalidAlgorithmError as e:
            raise AuthenticationFailed('Invalid algorithm')
        except Exception as e:
            raise e


