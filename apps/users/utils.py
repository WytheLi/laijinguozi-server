from .serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
        负责控制登录或刷新jwt token后响应返回的数据结构
        默认: rest_framework_jwt.utils.jwt_response_payload_handler
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
