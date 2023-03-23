FROM python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY templates templates
COPY core core
COPY account account
COPY task task
COPY static static
COPY manage.py manage.py
RUN mkdir db

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]