FROM python:3.8.5-buster
USER root

# # Installing Oracle instant client
WORKDIR    /opt/oracle
RUN        apt-get update && apt-get install -y libaio1 wget unzip \
  && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
  && unzip instantclient-basiclite-linuxx64.zip \
  && rm -f instantclient-basiclite-linuxx64.zip \
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
COPY ./requirements/dev.txt .
COPY ./requirements/repo-libraries.txt .

RUN pip install --no-cache-dir -r prod.txt
RUN pip install --no-cache-dir -r repo-libraries.txt

COPY . .

RUN pip install .

USER 1001

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000",  "--config", "/opt/app/gunicorn_config.py", "wsgi:application"]
