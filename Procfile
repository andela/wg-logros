release: invoke create_settings --settings-path ./settings.py --database-path ./database.sqlite 
release: invoke bootstrap_wger --settings-path ./settings.py --no-start-server
web:gunicorn wger.wsgi 