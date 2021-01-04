#!/bin/sh

if [ -z "${HTTP_PORT}" ]
then
    HTTP_PORT=8080
fi

python -m http.server "${HTTP_PORT}"