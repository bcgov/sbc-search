FROM python:3.7
USER root


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
ENV ORACLE_HOME /opt/ora/instantclient
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:$ORACLE_HOME

# Run the server
EXPOSE 5000

CMD ./command.sh
