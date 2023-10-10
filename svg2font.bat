:: generate font from images in svg files
@echo on

set ver=x.x
set ttffont=Input/times.ttf
set language=ENG
set infile=input/pw_Sun22_07_08_BF-ENG.csv
set outfile=dist/SUNBF%ver%_%language%

fontforge -quiet -script svg2Font_ttf.py %infile% %ttffont% %language% %outfile%
	
