echo "Starting the project"
sleep 2

echo "Downloading the python dependencies"
sleep 2

pip install --no-cache-dir -r Backend/requirements.txt

sh Backend/StartApp.sh