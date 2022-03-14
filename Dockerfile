FROM python:3.8.5-slim-buster

COPY ./dist/mkaddis-1.0.0-py3-none-any.whl .

RUN pip install ./mkaddis-1.0.0-py3-none-any.whl