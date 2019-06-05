# Minimal Docker container for Python applications
# https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3

# FROM python:3-onbuild
# FAT image
#FROM python:3.7 --> image size is 943MB

# A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size!
FROM python:3.7-alpine # --> image size is 101MB

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

ADD paho_mqtt_to_gsheet.py /
ADD configuration.py /
ADD GoogleSheetsHandler.py /
ADD MqttNodeHandler.py /
ADD token.pickle /

CMD [ "python3", "./paho_mqtt_to_gsheet.py" ]
