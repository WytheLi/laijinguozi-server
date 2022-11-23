import jwt
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, jwt_decode_handler


class JwtTokenAuthentication(JSONWebTokenAuthentication):
    """
        由于微信登录，不仅要判断请求头中token有效，而且要有open_id。这里对原先的认证类进行重写
    """
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            return False

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)
