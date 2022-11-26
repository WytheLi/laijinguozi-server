import requests

url = 'http://150.158.25.50:8085/group1/upload'
files = {'file': open('../utils/wechat_sdk/img/mini-wechat-login.png', 'rb')}
options = {'output': 'json', 'path': '', 'scene': ''}  # 参阅浏览器上传的选项
r = requests.post(url, data=options, files=files)
print(r.text)
