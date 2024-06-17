install:
	#install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	#format code
	black *.py 
lint:
	#flake8 or #pylint
	pylint --disable=R,C *.py 
run:
	#run streamlit
	streamlit run interface.py
all: install format lint run