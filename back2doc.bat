Build the backfont documents
@echo on

set ver=x.x
set ttffont=Input/times.ttf
set language=ENG
set infile=dist/example%ver%_%language%.sfd
set outfile=dist/example%ver%_%language%.txt

cmd /c fontforge -quiet -script back2doc_ttf.py %infile% %outfile% 
