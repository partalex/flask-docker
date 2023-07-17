FROM python:3

RUN mkdir -p /opt/src/shop/customer
WORKDIR /opt/src/shop/customer

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/decoraterRole.py ./decoraterRole.py
COPY shop/appCustumer.py ./appCustumer.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop/customer"

ENTRYPOINT ["python", "./application.py"]


