if [ -z "${MY_SERVICE_HTTP_PORT}" ]
then
    MY_SERVICE_HTTP_PORT=3000
fi
pipenv run uvicorn main:app --host=0.0.0.0 --port=${MY_SERVICE_HTTP_PORT}