all: clean dt_ice.py

run:
	python3 ./limits_update.py
	
dt_ice.py:
	slice2py ../slice/dt.ice
 
clean:
	rm dt_ice.py
	rm -r digitaltwin
	-sudo rm -r __pycache__
