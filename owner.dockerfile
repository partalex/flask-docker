FROM python:3

RUN mkdir -p /opt/src/shop/owner
WORKDIR /opt/src/shop/owner

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/appOwner.py ./appOwner.py
COPY shop/decoraterRole.py ./decoraterRole.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop/owner"

ENTRYPOINT ["python", "./application.py"]
