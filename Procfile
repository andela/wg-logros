release: invoke create-settings --settings-path ./settings.py --database-path ./database.sqlite 
release: invoke bootstrap-wger --settings-path ./settings.py --no-start-server
web: gunicorn wger.wsgi --log-file -