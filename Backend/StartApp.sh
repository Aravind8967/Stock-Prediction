echo "Starting the python app in nohup"
sleep 2

echo "Downloading the python dependencies"
sleep 2

pip install --no-cache-dir -r requirements.txt

echo "python requirments are installed"

nohup python app.py > app.log 2>&1 &

sleep 2 

echo "Backend API running on localhost:8080"