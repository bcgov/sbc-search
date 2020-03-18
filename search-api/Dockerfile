FROM python:3.7
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
WORKDIR /opt/app

RUN apt-get update && \
    apt-get install -y python-dev build-essential libaio1

# Install the requirements
COPY ./requirements/prod.txt .
COPY ./requirements/dev.txt .
COPY ./requirements/repo-libraries.txt .

RUN pip install --no-cache-dir -r prod.txt
RUN pip install --no-cache-dir -r dev.txt
RUN pip install --no-cache-dir -r repo-libraries.txt

# This may be used to lock things down but breaks alembic during dev work.
# TODO: add this for production only.
#USER 1001

# We don't run `pip install .` in order to have live updates
# TODO: switch to installation for prod only.
# pip install .

# Add the src dir to our pythonpath for live updates.
# TDOO: disable for prod.
#ENV FLASK_APP search_api/__init__.py

# Run the server
EXPOSE 5000

CMD ./command.sh
