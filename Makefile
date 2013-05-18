run:
	./website/main.py serve

push:
	touch main.py
	rsync -e ssh -avz --exclude feedback.csv ./ dedi:lemooc.com/

clean:
	rm -f *.pyc */*.pyc */*/*.pyc

