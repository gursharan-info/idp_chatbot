# cd /app/
# Start rasa server with nlu model

rasa run -m models --credentials credentials.yml  --enable-api --cors "*"   

# SAMIK 's VERSION'
# # Start rasa server with nlu model
# rasa run -m /app/models --enable-api \
#         --endpoints /app/endpoints.yml \
#         --credentials /app/credentials.yml \
#         -p $PORT


#Original version
# rasa run --model models — enable-api — cors “*” — debug \
# -p $PORT4