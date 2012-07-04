publish:
	cp -R doc/build/html/_static doc/build/html/_modules .
	cp doc/build/html/index.html doc.html
	cp doc/build/html/genindex.html .
	rm -rf doc/build
