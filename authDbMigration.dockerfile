FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY authentication/appAuthentication.py ./appAuthentication.py
COPY authentication/configuration.py ./configuration.py
COPY authentication/decoraterRole.py ./decoraterRole.py
COPY authentication/models.py ./models.py
COPY authentication/manage.py ./manage.py
COPY authentication/migrate.py ./migrate.py
COPY authentication/models.py ./models.py
COPY authentication/requirements.txt ./requirements.txt


RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/authentication"

ENTRYPOINT ["python", "./migrate.py"]