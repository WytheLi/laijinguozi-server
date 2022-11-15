import requests

from .utils import RequestType


class WechatBase:

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def _request(self, url, method=RequestType.GET, params=None, data=None):
        if method == RequestType.GET:
            response = requests.get(url, params=params)
        elif method == RequestType.POST:
            response = requests.post(url, params=params, data=data)

        # 待补充
        return response.status_code, response.text if 'application/json' in response.headers.get('Content-Type') else response.content


class WechatLogin(WechatBase):

    def __init__(self, *args, **kwargs):
        super(WechatLogin, self).__init__(*args, **kwargs)
        self.base_url = 'https://api.weixin.qq.com'

    def get_access_token(self):
        """
            https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getAccessToken.html
        :return: {
            "access_token":"ACCESS_TOKEN",
            "expires_in":7200
        }
        """
        url = self.base_url + '/cgi-bin/token'
        params = dict()
        params.setdefault('appid', self.app_id)
        params.setdefault('secret', self.app_secret)
        params.setdefault('grant_type', 'client_credential')
        return self._request(url, RequestType.GET, params=params)

    def get_phone_number(self, code):
        """
            https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html
        :param code:
        :return: {
            "errcode":0,
            "errmsg":"ok",
            "phone_info": {
                "phoneNumber":"xxxxxx",
                "purePhoneNumber": "xxxxxx",
                "countryCode": 86,
                "watermark": {
                    "timestamp": 1637744274,
                    "appid": "xxxx"
                }
            }
        }
        """
        url = self.base_url + '/wxa/business/getuserphonenumber'
        params = dict()
        params.setdefault('access_token', self.get_access_token()['access_token'])
        return self._request(url, RequestType.POST, params=params, data={'code': code})

    def code2session(self, js_code):
        """
            https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
        :param js_code:
        :return: {
            "openid":"123456",
            "session_key":"xxxxx",
            "unionid":"xxxxx",
            "errcode":0,
            "errmsg":"xxxxx"
        }
        """
        url = self.base_url + '/sns/jscode2session'
        params = dict()
        params.setdefault('appid', self.app_id)
        params.setdefault('secret', self.app_secret)
        params.setdefault('js_code', js_code)
        params.setdefault('grant_type', 'authorization_code')
        return self._request(url, RequestType.GET, params=params)
