echo "Starting the python app in nohup"
sleep 2

nohup python app.py > app.log 2>&1 &

sleep 2 

tail -f app.log
