#whatever version that suits you
FROM rasa/rasa-sdk:2.6.0

#define the working directory of Docker container
WORKDIR /app 
#copy the requirements txt file with your dependencies in actions directory
COPY ./requirements-actions.txt ./ 
#copy everything in ./actions directory (your custom actions code) to /app/actions in container
COPY ./ /app/actions

#install dependencies inside Docker container
USER root 
RUN pip install -r requirements-actions.txt 
USER 1001 