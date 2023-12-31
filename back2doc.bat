
::  Build the backfont documents

@echo on
Setlocal EnableDelayedExpansion

call doEnv_ttf.bat

cmd /c fontforge -quiet -script back2doc_ttf.py %sfdfile% %txtfile% 
