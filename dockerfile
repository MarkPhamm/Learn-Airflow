# Start of Selection
FROM apache/airflow:latest

USER root
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow
# End of Selection