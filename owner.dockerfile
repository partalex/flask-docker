FROM python:3

RUN mkdir -p /opt/src/shop
WORKDIR /opt/src/shop

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/appOwner.py ./appOwner.py
COPY shop/decoraterRole.py ./decoraterRole.py
COPY shop/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop"

ENTRYPOINT ["python", "./appOwner.py"]
