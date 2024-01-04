Develop Guide on Ubuntu
1. map .env file
```
source export_env.sh
```
2. run redis service
```
sudo docker-compose up -d
```
3. init environment 
```
pip install -r requirements.txt   
```
4. start a local webserver
```
uvicorn main:app --reload
```
5. run test SSEHub
```
python tests/run_test.py
```
