import os
import sys
import time
from pathlib import Path

import django
from django_redis import get_redis_connection

base_path = Path(__file__).resolve().parent.parent

sys.path.insert(0, base_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laijinguozi.settings")     # 加载django的环境变量
django.setup()  # 将django环境生效

from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def get_invalid_token(token):
    redis_conn = get_redis_connection('token_blacklist')
    payload = jwt_decode_handler(token)
    invalid_time = redis_conn.get(token)

    return {
        "user_info": payload,
        "expiry_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(payload['exp']))),
        "invalid_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(invalid_time)))
    }


if __name__ == '__main__':
    res = get_invalid_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjY3ODk2NTAyLCJlbWFpbCI6ImFkbWluQGl0ZmlyZS5jb20ifQ.5yTZ7cC2dXiXVVjRr7pQHlKgeopjdboeQgMkluxWz6Y')
    print(res)
