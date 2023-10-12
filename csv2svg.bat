:: generate images based on wordlist in csv file
@echo on
set ver=x.x
set ttffont=Input/times.ttf
set language=ENG
set infile=input/example-ENG.csv
set outfile=

fontforge -quiet -script csv2svg_ttf.py %infile%  %ttffont% %language%

