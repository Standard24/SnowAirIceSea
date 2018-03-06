pdflatex MainPart.tex -shell-escape
bibtex MainPart1.aux
bibtex MainPart2.aux
bibtex MainPart3.aux
pdflatex MainPart.tex -shell-escape
pdflatex MainPart.tex -shell-escape

