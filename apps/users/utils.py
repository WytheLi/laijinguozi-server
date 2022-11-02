import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class AuthBackend(ModelBackend):
    """
        自定义认证后端ModelBackend，完成手机号、邮箱、用户名等多账号登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UsersModel = get_user_model()
        try:
            user = UsersModel.objects.get(
                # username=<account_number> or mobile=<account_number> or email=<account_number>
                Q(username=username) | Q(mobile=username) | Q(email=username)
            )
        except UsersModel.DoesNotExist:
            return None

        # 校验密码
        if user.check_password(password):
            return user


def wx_login(user_code):
    """
        微信登录
    """
    # TODO
    api_url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'
    r = requests.get(api_url)
    return r.json()
