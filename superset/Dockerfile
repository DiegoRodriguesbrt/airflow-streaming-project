FROM apache/superset:latest

USER root

# Instale as dependências do sistema para o mysqlclient
RUN apt-get update && \
    apt-get install -y pkg-config libmariadb-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install mysqlclient
RUN pip install pinotdb

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY ./superset-init.sh /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]