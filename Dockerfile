FROM python:3
ENV PYTHONDEBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn cinema.wsgi:application --bind 0.0.0.0:$PORT
