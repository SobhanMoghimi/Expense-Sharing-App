FROM python:3.11-buster
LABEL authors="Sobhan Moghimi"
#RUN apt -y update && apt -y install net-tools vim telnet curl

ENV PYTHONUNBUFFERED 1
RUN pip3 install --upgrade pip
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r ./requirements.txt

COPY esa ./esa

EXPOSE 8100
EXPOSE 8200

# use this command to debug
#ENTRYPOINT ["tail", "-f", "/dev/null"]


