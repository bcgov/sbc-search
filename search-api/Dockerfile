FROM python:3.7
USER root


# Create working directory
RUN mkdir /opt/app && chmod 755 /opt/app && mkdir /opt/app/tmp && chmod 755 /opt/app/tmp
WORKDIR /opt/app

# Install the requirements
COPY ./requirements/repo-libraries.txt .

RUN pip install --no-cache-dir -r repo-libraries.txt

# This may be used to lock things down but breaks alembic during dev work.
#USER 1001

# Run the server
EXPOSE 5000

#CMD ["flask", "run","--host", "0.0.0.0"]
CMD ["python", "app.py"]

