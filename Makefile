.PHONY: all clean test

all: output.html
clean:
	@rm -f output.html

test: output.html lorem-ipsum.html
	diff $^ | less

output.html: render.py renderer/*.py lorem-ipsum.xml
	python3 render.py lorem-ipsum.xml > $@
