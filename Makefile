.PHONEY: all
all:
	# Targets are:
	#	clean
	#	build - build the zip file
	#	docs - build the user documentation

.PHONEY: clean
clean:
	find _build -mindepth 1 -delete

.PHONEY: build
build:
	true

.PHONEY: docs
docs:
	true
