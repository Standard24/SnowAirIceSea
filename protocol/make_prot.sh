#!/bin/sh

pdflatex MainPart.tex
#bibtex Mainpart.aux
pdflatex MainPart.tex
#pdflatex MainPart.tex