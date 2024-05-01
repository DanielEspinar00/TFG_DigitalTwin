all: clean dt_ice.py

run:
	sudo python3 ./gw.py --Ice.Config=gw.config
	
dt_ice.py:
	slice2py ../slice/dt.ice
 
clean:
	rm dt_ice.py
	rm -r digitaltwin
	-sudo rm -r __pycache__
