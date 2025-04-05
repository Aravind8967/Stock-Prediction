FROM python:3.9.13

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get upgrade -y; apt-get install -y sudo vim nano

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD [ "python", "app.py" ]