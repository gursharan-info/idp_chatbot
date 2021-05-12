# FROM ubuntu:18.04
FROM rasa/rasa:2.6.0
ENTRYPOINT []
USER root

ADD . /app/
RUN chmod +x /app/scripts/*
CMD /app/scripts/start_services.sh
