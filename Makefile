.PHONY: run test demo

run:
	python3 src/main.py

test:
	python3 -m unittest discover -s tests -v

demo:
	python3 src/main.py --vfs tests/vfs/deep --no-interactive \
		--script tests/startup/stage5.emu
