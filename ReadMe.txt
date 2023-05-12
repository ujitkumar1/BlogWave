Useage:

To Run Flask Serve
	Go to backend directory and run the app.py file or in cmd write python app.py

To Run VueJs(npm) server:
	Go to ui directory and and in the cmd run the following commands:
		npm install
		npm run serve
		
For Celery and Redis
	Go to backend directory and run the below commands in WSL(Ubuntu):
		redis-server
		celery -A app.celery worker -l info
		celery -A app.celery beat --max-interval 1 -l info