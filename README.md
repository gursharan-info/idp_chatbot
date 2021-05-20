# INDIAN DATA PORTAL Chatbot

#### To train model locally
```
rasa train --domain domain-grp/

```
#### To talk to bot in shell
```
rasa shell

```

#### To see bot working locally with UI


``` 
rasa run -m models --enable-api --cors "*" 
```

if if gives error port 5005 already in use 
check with

```
docker ps

```
> if your conatiner is running if yes stop it 
> and if no container is running and it is still saying the same
 
```
rasa run -m models --enable-api --cors "*" -p [ port-number ]
```
> and also make sure that this port number is also present in IDP.html in **socketUrl** : [ ip-address ]: [ port-number ]


#### To run Docker image of chatbot

> **you can replace sahib-bot-idp with your bot name**
```
docker build -t sahib-bot-idp . 

docker run -it  -p 5005:5005 sahib-bot-idp:latest
```
#### To run chatbot in shell using docker container
```
docker run  -it --workdir /app sahib-bot-idp bash ./scripts/start_shell.sh

```
#### To stop Docker container
```
docker stop <container-id>
```

#### To remove docker image

```
docker image rm -f sahib-bot-idp:latest
```


## Problem we faced while connecting RASA X with Github

To connect rasa x to Github via UI RASA X expects files to be of same structure as we get after
```
rasa init
```

Prerequisites for making **build-domain.py** file 
```
pip3 install HiYaPyCo

```
Means it does not support multiple domain files 
But What we have done is we have written a script **build-domain.py** and gave it path of all domain files so what it does is it takes all domain files combines them to make **domain.yml** 
so that we can connect RASA X to github via UI.

Now whenever we make multiple domain files before every re training
run

```
python3 build-domain.py

rasa train

```

### No need of below command now

```
rasa train --domain domain-grp/

```

## To do
1. Have to solve the issue of chatbot giving False Positives ( Menas correct answer for wrong answer)
2. Have to work on Deployment phase
3. Permission error ( How to save model after training from docker image itself --if possible )
4. Have to see why docker-compose is creating error with ` --cors "*" ` command in rasa 
5. How to test RASA for multiple Domain and NLU files