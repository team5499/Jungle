.PHONY: clean
clean:
	rm -rf virtualenv_run
	rm -rf .tox

.PHONY: install-hooks
install-hooks: virtualenv_run
	virtualenv_run/bin/pre-commit install -f --install-hooks

.PHONY: test
test: virtualenv_run
	virtualenv_run/bin/tox

.PHONY: upgrade-requirements
upgrade-requirements: virtualenv_run
	virtualenv_run/bin/upgrade-requirements

virtualenv_run:
	virtualenv -p python3.6 virtualenv_run
	virtualenv_run/bin/pip install -r requirements-dev.txt
