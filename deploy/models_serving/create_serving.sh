#docker run -p 8501:8501 -v "$(pwd)/models/model_animals:/models/model_animals" -v "$(pwd)/models/model_body:/models/model_body" -v "$(pwd)/models/model_arts & sciences:/models/model_arts & sciences" -v "$(pwd)/models/model_death:/models/model_death" -v "$(pwd)/models/model_family:/models/model_family" -v "$(pwd)/models/model_heartache:/models/model_heartache" -v "$(pwd)/models/model_love:/models/model_love" -v "$(pwd)/models/model_nature:/models/model_nature" -v "$(pwd)/models/model_religion:/models/model_religion" -v "$(pwd)/models/model_war:/models/model_war" -v "$(pwd)/models/models.config:/models/models.config" -t tensorflow/serving --model_config_file_poll_wait_seconds=60 --model_config_file=/models/model_animals/models.config

#docker pull tensorflow/serving

docker run -p 8501:8501 \
--name models_served \
-v "$(pwd)/models/model_animals:/models/model_animals" \
-v "$(pwd)/models/model_body:/models/model_body" \
-v "$(pwd)/models/model_arts & sciences:/models/model_arts & sciences" \
-v "$(pwd)/models/model_death:/models/model_death" \
-v "$(pwd)/models/model_family:/models/model_family" \
-v "$(pwd)/models/model_heartache:/models/model_heartache" \
-v "$(pwd)/models/model_love:/models/model_love" \
-v "$(pwd)/models/model_nature:/models/model_nature" \
-v "$(pwd)/models/model_religion:/models/model_religion" \
-v "$(pwd)/models/model_war:/models/model_war" \
-v "$(pwd)/models/year_model:/models/year_model" \
-v "$(pwd)/models.config:/models/models.config" \
-t tensorflow/serving \
--model_config_file_poll_wait_seconds=60 \
--model_config_file=/models/models.config \

 
