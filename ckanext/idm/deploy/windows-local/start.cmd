docker stop ckan
taskkill /F /IM python.exe /T
START paster serve development.ini
timeout 10
explorer http://localhost:5000/
