#!/bin/bash

superset db upgrade

superset fab create-admin --username "$ADMIN_USERNAME" --firstname Superset --lastname Admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"

superset init

/bin/sh -c /usr/bin/run-server.sh