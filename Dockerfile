FROM ubuntu:22.04
ENV APP_DIR=/cassava_sos

ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}

RUN apt-get update && \
  apt-get install -y python3-pip software-properties-common python3-cairocffi

# install GDAL dependencies for the Python Fiona package
RUN add-apt-repository ppa:ubuntugis/ppa && \
  apt-get update && \
  apt-get install -y gdal-bin libgdal-dev

COPY requirements.txt ${APP_DIR}
RUN pip3 install -r ${APP_DIR}/requirements.txt

COPY code/*.py ${APP_DIR}
COPY input ${APP_DIR}

RUN mkdir ${APP_DIR}/odk_temp_download

ENTRYPOINT ["./main.py"]