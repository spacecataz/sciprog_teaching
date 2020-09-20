# Makefile for a simple LaTeX document.

DOC=gnumake
TEX=pdflatex

# Rule for creating a PDF file:
$(DOC).pdf: $(DOC).tex
	$(TEX) $<
	$(TEX) $<

# Clean up:
clean:
	rm -f *.aux *.blg *.dvi *.log *.bbl *~ *.toc *.html $(DOC).pdf
