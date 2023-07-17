FROM python:3

RUN mkdir -p /opt/src/shop/courier
WORKDIR /opt/src/shop/courier

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/decoraterRole.py ./decoraterRole.py
COPY shop/appCourier.py ./appCourier.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop/courier"

ENTRYPOINT ["python", "./application.py"]
