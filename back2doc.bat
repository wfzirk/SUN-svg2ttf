Build the backfont documents
@echo on

set ver=x.x
set ttffont=Input/times.ttf
set language=ENG
set infile=dist/SUNBFx.x_ENG.sfd
set outfile=dist/SUNBFx.x_ENG.txt

cmd /c fontforge -quiet -script back2doc_ttf.py %infile% %outfile% 
