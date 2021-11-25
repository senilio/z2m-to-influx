FROM python:3
ENV PYTHONUNBUFFERED=1
RUN pip install influxdb paho-mqtt
ADD mqtt.py /
CMD ["python", "-u", "mqtt.py"]
