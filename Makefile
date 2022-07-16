
venv/bin/activate: requirements.txt
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

server: venv/bin/activate
	./venv/bin/python -m http.server --directory ./src/html

start: venv/bin/activate
	./venv/bin/python -m http.server --directory ./build

build: venv/bin/activate
	rm -rf build
	./venv/bin/python build.py

clean:
	rm -rf __pycache__
	rm -rf venv

.PHONY: clean server build
