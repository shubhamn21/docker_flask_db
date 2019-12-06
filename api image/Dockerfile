FROM python:2.7

RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends apt-utils\
    netcat \
  && apt-get -q clean

RUN mkdir /app

COPY . /app

WORKDIR /app/datalist

RUN chmod +x start_postgres.sh

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["./start_postgres.sh"]
