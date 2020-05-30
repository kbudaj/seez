FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ADD . /app/seez

WORKDIR /app/seez
RUN pip3 install -r requirements.txt

ADD . /app/seez
