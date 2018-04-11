#!/bin/sh

pdflatex -output-directory=./bin Compile.tex


# ok, this is stupid: bibtex has to be executed in ./bin now.
# so, go there, take some bibliography files with you and delete them after you used it
cp AGFstyle.bst literature.bib ./bin
cd  ./bin
bibtex Compile.aux
rm AGFstyle.bst literature.bib
cd ../

pdflatex -output-directory=./bin Compile.tex
pdflatex -output-directory=./bin Compile.tex
