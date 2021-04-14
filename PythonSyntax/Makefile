# Makefile for converting the Jupyter notebooks into PDFs.
CONVERTER=jupyter-nbconvert
SOURCE  = $(wildcard *.ipynb)

pdf: $(SOURCE)
	jupyter-nbconvert --to pdf $(SOURCE)

# Clean up:
clean:
	rm -f *.html *.blg *.dvi *.log *.bbl *~ *.toc *.pdf
