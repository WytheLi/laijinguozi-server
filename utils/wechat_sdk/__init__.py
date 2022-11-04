import os

from .login import WechatLogin

appid = os.getenv('appid')
app_secret = os.getenv('app_secret')

wechat_login = WechatLogin(appid, app_secret)
