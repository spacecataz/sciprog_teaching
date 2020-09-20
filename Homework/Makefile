# Makefile for a simple LaTeX document.

TEX=pdflatex
BIB=dtw_bib.bib

SOURCE=$(wildcard *.tex)
PDFS=$(patsubst %.tex,%.pdf, $(SOURCE))

help:
	@echo "Compile homework tex files into PDFs."
	@echo "Just specify the final pdf that you want to see:"
	@echo "    make hw_01.pdf   "
	@echo " ...will compile hw_01.tex into a pdf.  Easy."

all: $(PDFS)

# Rule for creating a PDF file:
%.pdf: %.tex %.bbl
	$(TEX) $<
	$(TEX) $<
	$(TEX) $<

# Rule for creating the bbl file:
# If there is a bibliography in the tex file, call bibtex.
# If not, just touch the bbl file and move on.
%.bbl: $(BIB) %.tex
	if grep -q 'dtw_bib' $*.tex;		\
	then $(TEX) $*.tex; bibtex $*;		\
	else touch  $*.bbl; fi			\

# Clean up:
clean:
	rm -f *.out *.aux *.blg *.dvi *.log *.bbl *~ *.toc hw*.pdf
