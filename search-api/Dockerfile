FROM python:3.8.5-buster
USER root

ARG VCS_REF="missing"
ARG BUILD_DATE="missing"

ENV VCS_REF=${VCS_REF}
ENV BUILD_DATE=${BUILD_DATE}

LABEL org.label-schema.vcs-ref=${VCS_REF} \
  org.label-schema.build-date=${BUILD_DATE}

# install ssh services in disabled mode
RUN apt-get update && apt-get install -y apt-utils openssh-server openssh-client sudo \
  # && systemctl disable ssh \
  && systemctl enable ssh \
  && sed -i 's/#GatewayPorts no/GatewayPorts clientspecified/g' /etc/ssh/sshd_config \
  && sed -i -e '$ame:x:1001:65534::/:/usr/sbin/nologin' /etc/passwd

# Installing Oracle instant client
WORKDIR    /opt/oracle
RUN        apt-get update && apt-get install -y apt-utils libaio1 wget unzip \
  && wget https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basiclite-linux.x64-21.1.0.0.0.zip \
  && wget https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sqlplus-linux.x64-21.1.0.0.0.zip \
  && unzip instantclient-basiclite-linux.x64-21.1.0.0.0.zip \
  && rm -f instantclient-basiclite-linux.x64-21.1.0.0.0.zip \
  && unzip instantclient-sqlplus-linux.x64-21.1.0.0.0.zip \
  && rm -f instantclient-sqlplus-linux.x64-21.1.0.0.0.zip \
  && cd /opt/oracle/instantclient* \
  && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
  && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
  && ldconfig

# Create working directory
RUN mkdir /opt/app && chmod 755 /opt/app

RUN apt-get update && \
  apt-get install -y python-dev build-essential libaio1

WORKDIR /opt/app

# Install the requirements
COPY ./requirements/prod.txt .
COPY ./requirements/repo-libraries.txt .

RUN pip install --no-cache-dir -r prod.txt
RUN pip install --no-cache-dir -r repo-libraries.txt

COPY . .

RUN pip install .

USER 1001

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080",  "--config", "/opt/app/gunicorn_config.py", "wsgi:application"]
