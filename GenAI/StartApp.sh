echo "Starting the AI interface APP in nohup"
sleep 2

nohup ollama serve > ollama.log 2>&1 &
echo "ollama is running"
sleep 4

nohup python3 aiApp.py > aiApp.log 2>&1 &

sleep 2

tail -f aiApp.log
