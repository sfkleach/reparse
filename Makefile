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
	find _build -mindepth 1 -delete
	rm -f $(DOCS)

# Will require admin password.
.PHONEY: ubuntu-sdk
ubuntu-sdk:
	sudo apt-get install -y python3 rubygems
	gem install asciidoctor

