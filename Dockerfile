FROM ubuntu:18.04
FROM rasa/rasa:2.6.0
ENTRYPOINT []
USER root
# RUN apt-get update && apt-get install -y python3.6 python3-pip &&\
#      python3 -m pip install — no-cache — upgrade pip && pip3 install — no-cache rasa==2.6.0

ADD . /app/
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh
