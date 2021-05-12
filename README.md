# INDIAN DATA PORTAL Chatbot

#### To train model locally
> rasa train --domain domain-grp/
#### To talk to bot in shell
> rasa shell

#### To see bot working locally with UI
> rasa run -m models --enable-api --cors "*"
#### To run Docker image of chatbot

> **you can replace sahib-bot-idp with your bot name**
 '''
> docker build -t sahib-bot-idp . 

> docker run -it  -p 5005:5005 sahib-bot-idp:latest
 '''
#### To run chatbot in shell using docker container
> docker run  -it --workdir /app sahib-bot-idp bash ./scripts/start_shell.sh
#### To stop Docker container
> docker stop <container-id>
> docker image rm -f sahib-bot-idp:latest
## To do
1. Have to solve the issue of chatbot giving False Positives ( Menas correct answer for wrong answer)
2. Have to work on Deployment phase
3. Permission error ( How to save model after training from docker image itself --if possible )