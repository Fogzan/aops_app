FROM python:3.12-slim

EXPOSE 5000
WORKDIR /usr/app
ENV ENV production

COPY requirements.txt /usr/app/
RUN pip install --only-binary :all: greenlet \
    && pip install -r requirements.txt \
    && pip install waitress

RUN dnf install -y pip
RUN dnf install -y mariadb105-devel gcc python3-devel
RUN pip install mysqlclient


COPY /app /usr/app/
CMD waitress-serve --host 0.0.0.0 --port 5000 app:app
