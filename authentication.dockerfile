FROM python:3

#RUN rm -r /opt/src/authentication
RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY authentication/ ./

RUN pip install -r ./requirements.txt

#ENV PYTHONPATH="/opt/src/authentication"

ENTRYPOINT ["python", "./application.py"]
