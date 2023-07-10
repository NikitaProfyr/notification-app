FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /notification_app/

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app .

CMD ["python", "manage.py", "runserver"]