
:: generate font from images in svg files

@echo on
Setlocal EnableDelayedExpansion

call doEnv_ttf.bat

fontforge -quiet -script svg2Font_ttf.py %infile% %ttffont% %language% %sfdfile%
	
