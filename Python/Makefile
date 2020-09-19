# Makefile for creating HTML files of source code.
# Requires Pygments.

ALLHTML=sciprog.html test_sciprog.html
ALLPDF =sciprog.pdf test_sciprog.pdf

# Convert all source files into PDF:
pdf: $(ALLPDF)

# Convert all source files into HTML.
html: $(ALLHTML)

%.pdf: %.html
	wkhtmltopdf $< $*.pdf

# Create HTML of source code:
%.html : %.py
	pygmentize -f html \
	-O full,style=emacs,linenos='inline',title="Source Code: $<" \
	-o $*.html $< 

# Clean up:
clean:
	rm -f *.html *.blg *.dvi *.log *.bbl *~ *.toc *.pdf

