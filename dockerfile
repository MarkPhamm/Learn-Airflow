FROM apache/airflow:latest
USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow

# Install provider packages from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy SMTP configuration
COPY airflow/config/smtp.conf /opt/airflow/smtp.conf
ENV AIRFLOW__SMTP__CONFIG_FILE=/opt/airflow/smtp.conf