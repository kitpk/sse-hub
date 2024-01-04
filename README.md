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
Diagram, Sequence Diagram and Test Case Scenario
- https://lucid.app/lucidspark/3caa2c18-cb97-4983-9e38-651862b6a040/edit?invitationId=inv_054d7ef7-83d7-4613-9701-3d1adcd172a3
