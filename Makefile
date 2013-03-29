run:
	./main.py serve

push:
	rsync -e ssh -avz --exclude feedback.csv ./ dedi:lemooc.com/

