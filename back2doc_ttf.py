# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import os
import sys
import csv
import logging
from bfLog import log_setup
from bfConfig_ttf import bfVersion
DEBUG = False 


bbox = []
min0 = 0
min1 = 0
max0 = 0
max1 = 0
avg0 = 0
avg1 = 0


def getUnicode(_str):
    try:
        a = chr(int(_str,16)).encode('utf-8')
        return a.decode('utf-8')
    except Exception as  e:
        logging.error("fatal error getUnicode %s input %s",e, _str)
        sys.exit(1)
        

def listGlyphs(font, outfile):
    global bbox, min0, min1, avb0, avg1
    with open(outfile, 'w' , encoding='utf8') as fw:
        cnt = 0
        for glyph in font:
            try:
                if font[glyph].unicode > 57343:
                    #if font[glyph].unicode < 57344:    # incase bad characters
                    #    continue
                
                    unicode = hex(font[glyph].unicode)[2:]
                    logging.info("|%s| %s %s",font[glyph].unicode, font[glyph].glyphname, unicode)
                    
                    if len(unicode) < 4:
                        continue;
                    uic = getUnicode(unicode)
                    fw.write(uic)
                    
                    left, bot, right, top = font[glyph].boundingBox()
                    bbox.append([uic, unicode, int(bot), int(top), int(top-bot), int(right-left)])
                    #bbox.append([int(top-bot), int(right-left)])
                    cnt+=1
                    #if cnt > 5: break
                    
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
        bbmin = 99999
        minword = ''
        minuec = 0
        bbmax = 0
        maxword = ''
        maxec = 0
        with open('Log/glyph.csv', mode='w', newline='') as gf:
            gfw = csv.writer(gf)   #, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            gfw.writerow(['uic','unicode','bot','top','height', 'width'])
            for bb in bbox:
                ##print(bb)
                gfw.writerow(bb)
                if bbmin > bb[2]:
                    bbmin = bb[2]
                    minuec = bb[1]
                    minword = bb[0]
                if bbmax < bb[3]:
                    bbmax = bb[3]
                    maxuec = bb[1]
                    maxword = bb[0]
                    
            gfw.writerow(['stat','word','unicode','bot','top','height'])        
            temp = sum(i[2] for i in bbox), sum(i[3] for i in bbox), sum(i[4] for i in bbox)
            average = ('average','','', int(temp[0]/len(bbox)), int(temp[1]/len(bbox)), int(temp[2]/len(bbox)))
            logging.info(average)
            gfw.writerow(average)
            temp = min(i[2] for i in bbox), min(i[3] for i in bbox), min(i[4] for i in bbox)
            boxmin = ('minimum', minword, minuec, temp[0], temp[1], temp[2])
            logging.info(boxmin)
            gfw.writerow(boxmin)
            temp = max(i[2] for i in bbox), max(i[3] for i in bbox), max(i[3] for i in bbox)
            boxmax = ('maximum', maxword, maxuec, temp[0], temp[1], temp[2])
            logging.info(boxmax)
            gfw.writerow(boxmax)
                
        logging.info("Done!  The backdoc file is in %s", outfile)
    else:
        logging.error('Failed %d',rc)

    return(rc)

if __name__ == "__main__":
    rc = main(sys.argv) 
    sys.exit(rc)