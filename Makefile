.PHONY: run clean requirements env config install pylint jslint lint shell db deploy log test

root_path="/opt/eyebrowse"
env_path=$(root_path)/env
debug_path=$(root_path)/debug
log_path="/var/opt/eyebrowse/logs"

ifndef env
	env=dev
endif

ifndef debug
	debug=true
endif

shell:
	python manage.py shell

run:
	python manage.py runserver

clean:
	find . -type f -name '*.py[cod]' -delete
	find . -type f -name '*.*~' -delete

requirements:
	pip install -r requirements.txt

log:
	sudo mkdir -p $(log_path)
	sudo touch $(log_path)/eyebrowse.log

env:
	sudo mkdir -p $(root_path)
	echo $(env) | sudo tee $(env_path) > /dev/null
	echo $(debug) | sudo tee $(debug_path) > /dev/null

config:
	if [ -s config.py ]; then \
		cp config.py config.py-backup; \
	else \
		touch config.py && cp config_template.py config.py; \
	fi;
	git checkout config_template.py # reset the template

db:
	python manage.py syncdb
	python manage.py migrate

install: clean requirements env log config db

pylint:
	-flake8 .

jslint:
	-jshint -c .jshintrc --exclude-path .jshintignore .

lint: clean pylint jslint

deploy: lint
	fab prod deploy restart_apache
