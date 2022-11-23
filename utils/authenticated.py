from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class AuthenticatedBackend(ModelBackend):
    """
        自定义后端登录校验类，继承自ModelBackend，完成手机号、邮箱、用户名等多账号登录
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
