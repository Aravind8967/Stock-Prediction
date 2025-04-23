DB_IMAGE="stockpred:database"
DB_CONT="pred_database"

AI_IMAGE="stockpred:genai"
AI_CONT="pred_genai"

FE_IMAGE="stockpred:frontend"
FE_CONT="pred_frontend"

NETWORK="pred_network"

echo "Starting the project"
sleep 2

echo "Downloading the python dependencies"
sleep 2

pip install --no-cache-dir -r Backend/requirements.txt

echo "python requirments are installed"

cd Backend

nohup python app.py > app.log 2>&1 &

cd ..

sleep 2

echo "Backend API running on localhost:8080"

sleep 4

echo "creating the Projecct network"

docker network create "$NETWORK"
sleep 2

echo "$NETWORK network created"

echo "Building the database image"
sleep 2

DB_STATUS=$(docker ps -a --filter "name=$DB_CONT" --format "{{.Names}}")
AI_STATUS=$(docker ps -a --filter "name=$AI_CONT" --format "{{.Names}}")
FE_STATUS=$(docker ps -a --filter "name=$FE_CONT" --format "{{.Names}}")

# ========================= Database creating process =================================

if [ "$DB_STATUS" == "$DB_CONT" ]; then
  echo "$DB_STATUS container found starting the container"
  docker start "$DB_CONT"
  sleep 3
  echo "$DB_CONT container started"
else 
  echo "$DB_CONT container not found Checking for image $DB_IMAGE"
  sleep 2

  if [[ -z $(docker images -q "$DB_IMAGE") ]]; then
    echo "Image not found locally → building..."
    cd Database/
    docker build -t "$DB_IMAGE" .
    sleep 2
    echo " $DB_IMAGE Database Image built "
    sleep 2
    docker run -dit --name "$DB_CONT" --network "$NETWORK" -p 82:3306 "$DB_IMAGE"
    sleep 2
    cd ..
    echo "$DB_CONT container running..."
  else
    echo "Image $DB_IMAGE already exists. Skipping build."
    sleep 2
    docker run -dit --name "$DB_CONT" --network "$NETWORK" -p 82:3306 "$DB_IMAGE"
    sleep 2
    echo "$DB_CONT container running..."
  fi
fi

sleep 5

# ============================ GenAI creating process =====================================

if [ "$AI_STATUS" == "$AI_CONT" ]; then
  echo "$AI_STATUS container found starting the container"
  docker start "$AI_CONT"
  sleep 3
  echo "$AI_CONT container started"
else 
  echo "$AI_CONT container not found Checking for image $DB_IMAGE"
  sleep 2
  if [[ -z $(docker images -q "$AI_IMAGE") ]]; then
    echo "Image not found locally → building..."
    cd GenAI/
    docker build -t "$AI_IMAGE" .
    sleep 2
    echo " $AI_IMAGE GenAI Image built "
    sleep 2
    docker run -dit --name "$AI_CONT" --network "$NETWORK" -p 83:80 "$AI_IMAGE"
    sleep 2
    cd ..
    echo "$AI_CONT container running..."
  else
    echo "Image $AI_IMAGE already exists. Skipping build."
    sleep 2
    docker run -dit --name "$AI_CONT" --network "$NETWORK" -p 83:80 "$AI_IMAGE"
    sleep 2
    echo "$AI_CONT container running"
  fi
fi


sleep 5
# =============================== Frontend creating process =================================

if [ "$FE_STATUS" == "$FE_CONT" ]; then
  echo "$FE_STATUS container found starting the container"
  docker start "$FE_CONT"
  sleep 3
  echo "$FE_CONT container started"
else 
  echo "$FE_CONT container not found Checking for image $FE_IMAGE"
  sleep 2
  if [[ -z $(docker images -q "$FE_IMAGE") ]]; then
    echo "Image not found locally → building..."
    cd Frontend/
    docker build -t "$FE_IMAGE" .
    sleep 2
    echo " $FE_IMAGE GenAI Image built "
    sleep 2
    docker run -dit --name "$FE_CONT" --network "$NETWORK" -p 80:80 "$FE_IMAGE"
    sleep 2
    cd ..
    echo "$FE_CONT container running"
  else
    echo "Image $FE_IMAGE already exists. Skipping build."
    sleep 2
    docker run -dit --name "$FE_CONT" --network "$NETWORK" -p 80:80 "$FE_IMAGE"
    sleep 2
    echo "$FE_CONT container running"
  fi
fi

sleep 4

echo "All Project Cotainers running in $NETWORK "