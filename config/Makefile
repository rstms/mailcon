# mailserver administration

config:
	./configure

install:
	pip3 install -U -e .

clean:
	rm -f ~/.cloudsigma.conf
	find . -type d -name __pycache__ | xargs -r rm -rf
	find . -type d -name \*.egg-info | xargs -r rm -rf
	find . -type f -name \*.pyc | xargs -r rm
