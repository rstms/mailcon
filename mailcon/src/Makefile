# mailserver administration

config:
	mct config

create:
	mct create

uninstall:
	pip uninstall -y mct

install: uninstall
	$(shell [ -e pyproject.toml ] && mv pyproject.toml .pyproject.toml)
	pip install -U -e .
	$(shell [ -e .pyproject.toml ] && mv .pyproject.toml pyproject.toml)

clean:
	rm -f ~/.cloudsigma.conf
	rm -rf ./build
	find . -type d -name __pycache__ | xargs -r rm -rf
	find . -type d -name \*.egg-info | xargs -r rm -rf
	find . -type f -name \*.pyc | xargs -r rm
