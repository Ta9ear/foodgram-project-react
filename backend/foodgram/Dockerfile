FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN python3 -m pip install -U pip

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]