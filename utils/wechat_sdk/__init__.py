import os

from .login import WechatLogin

appid = os.getenv('APPID')
app_secret = os.getenv('APP_SECRET')

wechat_login = WechatLogin(appid, app_secret)
