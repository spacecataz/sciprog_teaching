# Makefile for creating HTML files of source code.
# Requires Pygments.

SOURCE  = $(wildcard *.py)
ALLHTML = $(patsubst %.py, %.html, $(SOURCE))
ALLPDF  = $(patsubst %.py, %.pdf,  $(SOURCE))

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

