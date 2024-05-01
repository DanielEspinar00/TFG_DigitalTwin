DATABASE:=tfg_history

all: dt_ice.py

run:
	sudo -u postgres python3 dt.py
dt_ice.py:
	slice2py ../slice/dt.ice
	
createDB:
	sudo -u postgres createdb $(DATABASE)
openDB:
	sudo -u postgres psql -d $(DATABASE)

build:
	sudo docker build --rm -f dockerfiles/Dockerfile.dt --tag dt-server .
	sudo docker build --rm -f dockerfiles/Dockerfile.db --tag dt-database .

db-container:
	sudo docker run --rm -ti --name db --hostname db -p 5432:5432 dt-database

server-container:
	sudo docker run --rm -ti --name server --hostname server -p 10000:10000 dt-server


remove:
	-sudo docker stop server db
	-sudo docker rm server db

clean:
	-rm dt_ice.py
	-rm -r digitaltwin
	-sudo rm -r __pycache__
