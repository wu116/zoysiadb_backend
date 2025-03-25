# 建立 python 3.9环境
FROM python:3.9

COPY sources.list sources.list

# 安装netcat
RUN bash sources.list \
&& apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 3B4FE6ACC0B21F32 \
&& apt-get update \
&& apt install -y netcat \
&& apt-get install -y cron \
&& apt-get install -y nano \
&& apt-get install -y ncbi-blast+

# 作者
MAINTAINER wu116

# 设置 python 环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 可选：设置镜像源为国内
COPY pip.conf /root/.pip/pip.conf

# 容器内创建 myproject 文件夹
ENV APP_HOME=/var/www/html/zoysiadb_project
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# 将当前目录加入到工作目录中（. 表示当前目录）
ADD . $APP_HOME

# 更新pip版本
RUN /usr/local/bin/python -m pip install --upgrade pip

# 安装项目依赖 移除\r in windows 给start.sh可执行权限
RUN pip install -r requirements.txt && sed -i 's/\r//' ./start.sh && chmod +x ./start.sh

# 数据迁移，并使用uwsgi启动服务
ENTRYPOINT /bin/bash ./start.sh
