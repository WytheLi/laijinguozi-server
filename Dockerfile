FROM python:3.7

# 替换debian镜像地址改成阿里云地址解决update更新慢的问题
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install vim

ENV PIP_MIRROR=http://mirrors.aliyun.com/pypi/simple/
ENV PIP_TRUST_HOST=mirrors.aliyun.com

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user
USER user

# # 安装依赖包
ADD requirements.txt requirements.txt
RUN pip install --upgrade pip  -i $PIP_MIRROR --trusted-host $PIP_TRUST_HOST
RUN pip install  setuptools
RUN pip install -i $PIP_MIRROR --trusted-host $PIP_TRUST_HOST -r requirements.txt --no-warn-script-location
