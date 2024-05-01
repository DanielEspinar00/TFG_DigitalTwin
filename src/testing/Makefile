all: clean dt_ice.py

run:
	python3 ./gw_sim.py
	
dt_ice.py:
	slice2py ../slice/dt.ice

server_tests:
	python3 ./server_test.py
 
clean:
	rm dt_ice.py
	rm -r digitaltwin
	-sudo rm -r __pycache__
