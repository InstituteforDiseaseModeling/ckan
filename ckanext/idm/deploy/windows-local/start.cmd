docker stop ckan
START paster serve development.ini
timeout 10
explorer http://localhost:5000/
