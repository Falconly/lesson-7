FROM python:3.11.2

COPY bd/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY . /opt/app

WORKDIR /opt/app

LABEL authors="falconly"

CMD ["python", "manage.py", "runserver", "0:8000"]