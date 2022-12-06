FROM python:3.7
MAINTAINER li <wytheli168@163.com>
# 替换debian镜像地址改成阿里云地址解决update更新慢的问题
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install vim
RUN apt-get -y install lrzsz
RUN pip install --upgrade pip --index-url https://pypi.douban.com/simple
# 创建work目录
WORKDIR /code
ADD . /code
# 安装依赖包
RUN pip install -r requirements.txt --index-url https://pypi.douban.com/simple
# 同步数据库
RUN python manage.py makemigrations
RUN python manage.py migrate
# 给sh文件执行权限
RUN chmod u+x ./start.sh
RUN chmod u+x ./shutdown.sh
# 开放端口
EXPOSE 8080
# 执行启动服务命令
ENTRYPOINT ["sh"]
CMD ["./start.sh"]
