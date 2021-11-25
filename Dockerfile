FROM python:3
ENV PYTHONUNBUFFERED=1
ADD mqtt.py /
RUN pip install influxdb paho-mqtt
CMD ["python", "-u", "mqtt.py"]
