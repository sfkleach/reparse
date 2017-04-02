.PHONEY: all
all:
	# Targets are:
	#	clean
	#	build - build the zip file
	#	docs - build the user documentation

.PHONEY: clean
clean:
	find _build -mindepth 1 -delete
	rm docs/vision.html

.PHONEY: build
build: docs
	mkdir -p _build
	mkdir -p _build/docs
	cp docs/vision.html _build/docs

.PHONEY: docs
docs: docs/vision.html
	true

docs/vision.html:
	asciidoctor docs/vision.txt
