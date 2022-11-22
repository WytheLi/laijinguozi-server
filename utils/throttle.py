from rest_framework.throttling import SimpleRateThrottle


class SmsRateThrottle(SimpleRateThrottle):
    scope = 'sms_code'  # 限流的配置文件key

    def get_cache_key(self, request, view):

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }
