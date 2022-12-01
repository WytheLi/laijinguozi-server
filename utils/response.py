from rest_framework.response import Response


def success(data=None, msg='success.'):
    if data is None:
        data = {}
    return Response({'code': 0, 'msg': msg, 'data': data})


def fail(msg, code=1000):
    return Response({'code': code, 'msg': msg})
