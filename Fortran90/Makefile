# Makefile for all FORTRAN90 Material

DOCSOURCE = $(wildcard *.tex)
F90SOURCE = $(wildcard *.f90)
DOCPDF = $(patsubst %.tex, %.pdf, $(DOCSOURCE))
F90PDF = $(patsubst %.f90, %.pdf, $(F90SOURCE))
F90HTML= $(patsubst %.f90, %.html,$(F90SOURCE))

default: pdf f90pdf

# Create docs, PDFs of source code:
pdf: $(DOCPDF)

# Create HTML and PDFs of all F90 source code:
f90pdf: $(F90HTML)

# Create HTML of source code:
html: $(F90HTML)

# Rule for creating a PDF file:
%.pdf: %.tex
	pdflatex $<
	pdflatex $<

# Create HTML of source code:
%.html : %.f90
	pygmentize -f html \
	-O full,style=emacs,linenos='inline',title="Source Code: $<" \
	-o $*.html $< 

	wkhtmltopdf $*.html $*.pdf

# Clean up:
clean:
	rm -f *.aux *.blg *.dvi *.log *.bbl *~ *.toc *.html $(DOCPDF)
