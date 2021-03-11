SHELL := bash 
TARGET ?= origin
# pypy.org static page and blog makefile
# type `make help` to see all options 

all: build

.PHONY: clean build help

venv_nikola/bin/nikola:  ## create a virtualenv to build the website
	@python3 -mvenv ./venv_nikola
	@venv_nikola/bin/python -mpip install wheel
	@venv_nikola/bin/python -mpip install -r requirements.txt
	@venv_nikola/bin/nikola plugin -i localsearch

build: venv_nikola/bin/nikola  ## build the website if needed, the result is in ./public
	venv_nikola/bin/nikola build

auto: venv_nikola/bin/nikola ## build and serve the website, autoupdate on changes
	venv_nikola/bin/nikola auto -a 0.0.0.0

clean:  venv_nikola/bin/nikola  ## clean the website, usually not needed at all
	venv_nikola/bin/nikola clean

# Add help text after each target name starting with '\#\#'
help:   ## Show this help.
	@echo "\nHelp for building the website, based on nikola"
	@echo "Possible commands are:"
	@grep -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\(.*\):.*##\(.*\)/    \1: \2/'
