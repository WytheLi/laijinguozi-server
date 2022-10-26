from django.http import JsonResponse


def success(data=None, msg='success.'):
    if data is None:
        data = {}
    return JsonResponse({'code': 200, 'msg': msg, 'data': data})


def fail(msg):
    return JsonResponse()
