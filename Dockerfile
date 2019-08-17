FROM registry.git.zoodroom.com/basket/fertilizer:latest

LABEL MAINTAINER="Sayyed Alireza Hoseini <alireza.hosseini@zoodroom.com>"

RUN apk add --update --no-cache netcat-openbsd linux-headers

COPY requirements.txt /src/requirements.txt

RUN set -ex \
    && apk add --no-cache --update --virtual .build-deps \
        g++ \
        make \
        git \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /src/requirements.txt \
    && apk del .build-deps \
    && apk add --no-cache libstdc++

COPY . /src
WORKDIR /src

EXPOSE 3031

#ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uwsgi", "--ini", "/src/fig/uwsgi_fig.ini"]