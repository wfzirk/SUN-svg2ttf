# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import os
import sys
import csv
import logging
from bfLog import log_setup
from bfConfig_ttf import bfVersion
DEBUG = False 


def getUnicode(_str):
    try:
        a = chr(int(_str,16)).encode('utf-8')
        return a.decode('utf-8')
    except Exception as  e:
        logging.error("fatal error getUnicode %s input %s",e, _str)
        sys.exit(1)
        

def listGlyphs(font, outfile):

    with open(outfile, 'w' , encoding='utf8') as fw:
        for glyph in font:
            try:
                if font[glyph].unicode > 57343:
                    #if font[glyph].unicode < 57344:    # incase bad characters
                    #    continue
                
                    unicode = hex(font[glyph].unicode)[2:]
                    logging.info("|%s| %s %s %s",font[glyph].unicode, font[glyph].glyphname, unicode, len(unicode))
                    
                    if len(unicode) < 4:
                        continue;
                    uic = getUnicode(unicode)
                    fw.write(uic)
         
            except Exception as e:
                logging.exception("fatal error listGlyph %s",e)
                return 1,""
                
            if DEBUG:
                cnt = cnt+1
                if cnt>10:
                    break
    return 0

def main(*ffargs):  
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    
    logging.info('version %s', bfVersion)
    args = []
    for a in ffargs[0]:
        logging.info(a)
        args.append(a)

    if len(args) == 3: 
        font = fontforge.open(args[1])
        outfile = args[2]
        
    else:
        logging.warning("SYNTAX Error")
        logging.warning("syntax: fontforge -quiet -script back2doc_ttf.py %sfd_infile% %outfile%")
        logging.warning("Creates a backfont text file for verification of word alignment")
        return 1

    rc = listGlyphs(font, outfile)
    if rc == 0:
        logging.info("Done!  The backdoc file is in %s", outfile)
    else:
        logging.error('Failed %d',rc)

    return(rc)

if __name__ == "__main__":
    rc = main(sys.argv) 
    sys.exit(rc)