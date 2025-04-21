FROM python:3.9.13

WORKDIR /app

COPY . /app

RUN apt-get update ; apt-get install -y sudo vim nano 

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 755 StartApp.sh

EXPOSE 8080

CMD [ "sh", "StartApp.sh" ]
