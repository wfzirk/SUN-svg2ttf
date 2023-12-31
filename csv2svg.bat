
:: generate images based on wordlist in csv file

@echo on
Setlocal EnableDelayedExpansion

if not exist Dist mkdir Dist
if not exist Log mkdir Log
if not exist Svg mkdir Svg
if not exist Png mkdir Png

del /Q Svg\*
del /Q Png\*

call doEnv_ttf.bat

fontforge -quiet -script csv2svg_ttf.py %infile%  %ttffont% %language%
::python csv2svg_ttf.py csv2svg_ttf.py %infile%  %ttffont% %language%

