:: generate images based on wordlist in csv file
@echo on
set ver=x.x
set ttffont=Input/times.ttf
set language=ENG
set infile=input/pw_Sun22_07_08_BF-ENG.csv
set outfile=

fontforge -script csv2svg_ttf.py %infile%  %ttffont% %language%

