.PHONY: run test push clan

test:
	py.test

run:
	./manage.py serve

push:
	touch main.py
	rsync -e ssh -avz --exclude feedback.csv ./ dedi:lemooc.com/

clean:
	rm -f *.pyc */*.pyc */*/*.pyc
	rm -rf *.egg *.egg-info
	rm -rf dist

