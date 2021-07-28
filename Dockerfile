# FROM ubuntu:18.04
FROM rasa/rasa:2.6.0
ENTRYPOINT []
USER root
ADD ./models /app/models/
ADD . /app/

ADD ./certs/chatbot.indiadataportal.com  /app/certs/

RUN chmod +x /app/scripts/*
CMD /app/scripts/start_services.sh
