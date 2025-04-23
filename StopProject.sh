DB_CONT="pred_database"
AI_CONT="pred_genai"
FE_CONT="pred_frontend"


DB_STATUS=$(docker ps --filter "name=$DB_CONT" --format "{{.Names}}")
AI_STATUS=$(docker ps --filter "name=$AI_CONT" --format "{{.Names}}")
FE_STATUS=$(docker ps --filter "name=$FE_CONT" --format "{{.Names}}")
PY_PID=$(ps -ef | grep python | awk '{print $2}')


if [ "$DB_STATUS" == "$DB_CONT" ]; then
    docker stop "$DB_CONT"
    sleep 3
    echo "$DB_CONT container stoppend"
fi
sleep 2
if [ "$AI_STATUS" == "$AI_CONT" ]; then
    docker stop "$AI_CONT"
    sleep 3
    echo "$AI_CONT container stoppend"
fi
sleep 2
if [ "$FE_STATUS" == "$FE_CONT" ]; then
    docker stop "$FE_CONT"
    sleep 3
    echo "$FE_CONT container stoppend"
fi
sleep 2

if [ "$PY_PID" ]; then
    echo "Python is running"
    kill -9 "$PY_PID"
    sleep 2
    echo "Python process stopped"
fi
sleep 5

echo "Project stopped"