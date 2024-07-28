FROM python:3.11.6-alpine3.18

WORKDIR /app

# 将当前目录内容添加到工作目录
ADD . /app

# 更新包列表并安装必要的系统依赖，包括 C 编译器和其他依赖项
RUN apk update && \
    apk add --no-cache build-base linux-headers pcre-dev

# 升级 pip 并安装 requirements.txt 中的依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 安装 uwsgi
RUN pip install uwsgi

# 暴露端口 8080
EXPOSE 8080

# 启动 uwsgi
CMD ["uwsgi", "uwsgi.ini"]