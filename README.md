create virtual envaranment 

cd app 
uvicorn main:app --reload

for start app you should make next steps:

1. create virtual environment
2. activate virtual environment
3. install requirements with command 'pip install -r requirements.txt'
4. install Redis server (if not using Docker):
   - For Ubuntu/Debian: `sudo apt-get install redis-server`
   - Start Redis: `sudo service redis-server start`
5. start app with command 'uvicorn main:app --reload'

If using Docker:
1. Build the image: `docker build -t fastapi-redis-app .`
2. Run the container: `docker run -p 8000:8000 -p 6379:6379 fastapi-redis-app`

