.PHONEY: all
all:
	# Targets are:
	#	clean
	#	build - build the zip file
	#	docs - build the user documentation
	# 	check - run unit tests
	#	ubuntu-sdk - install the SDK on linux, excludes IDE tools.

.PHONEY: build
build: docs
	mkdir -p _build
	mkdir -p _build/docs
	cp docs/vision.html _build/docs

.PHONEY: check
check:
	nose2

DOCS=docs/vision.html docs/syntax.html docs/commands.html docs/grammar.html

.PHONEY: docs
docs: $(DOCS)
	true

docs/%.html: docs/%.txt
	asciidoctor -a stylesheet=readthedocs.css $<

.PHONEY: clean
clean:
	mkdir -p _build
	find _build -mindepth 1 -delete
	rm -f $(DOCS)

# Will require admin password.

.PHONEY: sdk-ubuntu
sdk-ubuntu:
	apt-get install -y python3 python3-pip rubygems git
	gem install asciidoctor
	pip3 install --upgrade pip
	pip3 install nose2

.PHONEY: sdk-ubuntu-check
sdk-ubuntu-check:
	docker run --rm -v `pwd`:/tmp/reparse:ro ubuntu /bin/bash -c "apt-get update && apt-get upgrade -y && apt-get install -y git; git -C /tmp/reparse show HEAD:scripts/sdk-ubuntu-check.sh | /bin/bash"
