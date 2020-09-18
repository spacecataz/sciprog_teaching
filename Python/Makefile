# Makefile for creating HTML files of source code.
# Requires Pygments.


# Create HTML of source code:
%.html : %
	pygmentize -f html -O full,style=emacs \
	$< > $*.html

# Clean up:
clean:
	rm -f *.html *.blg *.dvi *.log *.bbl *~ *.toc
