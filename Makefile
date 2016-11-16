clean:
	-@rm -f screencapture-full.png
	-@pkill -9 -f jekyll

deploy: clean
	bundle exec jekyll serve --detach
	webkit2png --width 1200 --fullsize --filename screencapture http://127.0.0.1:4000/staccato/
	python scripts/onoffmix.py screencapture-full.png
	make clean
