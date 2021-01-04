if [ -z "${MYSERVICE_HTTP_PORT}" ]
then
    MYSERVICE_HTTP_PORT=3000
fi
pipenv run uvicorn main:app --host=0.0.0.0 --port=${MYSERVICE_HTTP_PORT}