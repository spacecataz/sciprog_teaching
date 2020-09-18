# Makefile for a simple LaTeX document.

DOC=example
TEX=pdflatex
BIB=sample_bib.bib

# Rule for creating a PDF file:
$(DOC).pdf: $(DOC).tex $(DOC).bbl
	$(TEX) $<
	$(TEX) $<

# Rule for creating the bbl file:
$(DOC).bbl: $(BIB) $(DOC).tex
	$(TEX) $(DOC).tex
	bibtex $(DOC)

# Create HTML of source code:
$(DOC).html : $(DOC).tex
	pygmentize -l tex -f html -O full,style=emacs,linenos=1 \
	$(DOC).tex > $(DOC).html 

# Clean up:
clean:
	rm -f *.aux *.blg *.dvi *.log *.bbl *~ *.toc *.html $(DOC).pdf
