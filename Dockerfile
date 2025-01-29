FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
ENV PYTHONPATH=/app

EXPOSE 5000


CMD ["flask", "--app", "app/server.py", "run", "-h", "0.0.0.0", "-p", "8080"]
