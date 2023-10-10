
# http://fontforge.github.io/scripting.html#Example
# https://stuff.mit.edu/afs/sipb.mit.edu/project/wine/src/fontforge-20070511/fontforge/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# http://designwithfontforge.com/en-US/Importing_Glyphs_from_Other_Programs.html
# https://pelson.github.io/2017/xkcd_font_raster_to_vector_and_basic_font_creation/
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# https://github.com/pteromys/svgs2ttf/blob/master/README.md

import fontforge as ff
import psMat
import os
import sys
import csv
import os.path
import logging

from bfLog import log_setup
from bfConfig_ttf import bfVersion, loadConfig
 
config = loadConfig() 
ffMetrics = {}  # font metrics taken from font

'''    
   Font         ascent  _____
   Metrics      xheight _____   scale = 200/xheight
   scaling      base    _____   height =200  scale = xheight / 200
                descent _____   d = font_descender / scale
                
   wordMax and wordMin are whole word metrics calculated from font for each word
   ff_asc, ff_dsc, ff_height taken from the defult font metrics for all of font
'''

def getWord(word):
    #logging.info(word)
    maxt = 0
    minb = 0
    ww = []
    try:
        for w in word:
            g = ffMetrics["ttfFont"][ord(w)]
            #logging.info(g.glyphname)
            #name = g.glyphname
            left, bot, right, top = g.boundingBox()
            #name = g.glyphname
            ww = [bot, top]
            b = ww[0]
            t = ww[1]
            if b < minb:
                minb = b
            if t > maxt:
                maxt = t

        logging.info('getWord %s \t%s \t%s',word, minb, maxt)
    except Exception as e:
            logging.exception('exception %s name:%s ord:%s word:%s min:%s max:%s',e, w, ord(w), word, minb, maxt)
            #traceback.print_exc()
            return(1)
    return minb, maxt


def scale(glyph):   #, wordMin, wordMax):
    #global desc_scale
    options = config["glyph_options"]
    
    wordMin, wordMax = getWord(glyph.glyphname)
    logging.info(glyph)
    printBound(glyph,'Image Size')
    iL, iB, iR, iT = glyph.boundingBox()

    # scale to word
    iH = iT - iB
    wH = wordMax - wordMin
    wScale = wH/iH
 
    scale_matrix = psMat.scale(wScale)
    glyph.transform(scale_matrix)
    
    s = options["font_scale"]/ffMetrics['xheight']
    #log_info('scale to FF',round(s,2))
    logging.debug('scale to FF %5.2f',s)
    scale_matrix = psMat.scale(s)
    glyph.transform(scale_matrix)
    
    # move image vertically 
    sL, sB, sR, sT = glyph.boundingBox()
    y = options["font_offset"] - sB + (wordMin * s)
    base_matrix = psMat.translate(0, y)
    glyph.transform(base_matrix)
    #log_info('move y: %s bot: %s desc:%s'%(round(y,2), round(sB,2), round((wordMin*s),2)))
    logging.info('move y: %5.2f bot: %5.2f desc:%5.2f', y, sB, (wordMin*s))
    printBound(glyph,'Moved ')
 
def printBound(glyph, comment = ""):
    left, bot, right, top = glyph.boundingBox()
    #log_info(comment,'bound height:', round((top-bot),2), 'bot:',round(bot,2), 'top:',round(top,2), 'width:',round((right-left),2),'lb:',round(glyph.left_side_bearing,2), 'rb:',round(glyph.right_side_bearing,2))
    logging.info('%s bound height: %5.2f bot: %5.2f top:%5.2f width:%5.2f lb:%5.2f rb:%5.2f', comment, (top-bot), bot, top, (right-left), glyph.left_side_bearing, glyph.right_side_bearing)
   
def setBearing(glyph):
    options = config["glyph_options"]
    
    left, bot, right, top = glyph.boundingBox()
    
    glyph.width = int(right) - int(left) + 150
    glyph.left_side_bearing = options["left_side_berring"]      #75
    glyph.right_side_bearing = options["right_side_berring"]     #75
    #log_info('bearing', round(glyph.left_side_bearing,2), round(glyph.right_side_bearing,2), round(right-left, 2))
    logging.info('bearing left:%5.2f right:%5.2f width:%5.2f', glyph.left_side_bearing, glyph.right_side_bearing, (right-left))
    
def addFont(font, unicode, language, imagename):  #, mn, mx) :

    try:
        file = "svg\\"+language+"_"+unicode+".svg"
        exists = os.path.isfile(file)
        if exists:
            logging.info('addFont file %s %s %s', file, unicode, imagename)
            '''
            if unicode == -1:
                glyph = font.createChar(-1, imagename)
            else:
                glyph = font.createChar(int(unicode, 16))
            '''    
            glyph = font.createChar(int(unicode, 16), imagename)
            glyph.importOutlines(file)  
            scale(glyph)    #, mn, mx)
            setBearing(glyph) 
            glyph.glyphname = language+"_"+unicode #change glyphname after scaling to get consistent size of glyph words               
        else:
            logging.warning("file %s does not exist", file)
            return(2)
    except Exception as e:
        logging.exception('exception %s file:%s  unicode:%s',file,e, unicode)
        #traceback.print_exc()
        return(1)
   
def createFont(backfont):  
    props = config['props']

    fontname = os.path.basename(backfont)
    logging.info('fontname %s', fontname)
    '''
    ascent = 1000
    descent = 800
    em = 1000
    encoding = "Custom"
    weight = "Regular"
    #font = fontforge.font()
    '''
    ffont = ff.font()
    ffont.fontname = fontname
    ffont.familyname = fontname
    ffont.fullname = fontname
    ffont.ascent = props["ascent"]
    ffont.descent = props["descent"]
    ffont.em = props["em"]
    ffont.encoding = props["encoding"]
    ffont.weight = props["weight"]
    ffont.save(backfont+'.sfd')

    return ffont

def read_list(font, csvFile, language): 
    logging.info('readlist %s',csvFile)
    langColumns = config["lang_columns"]
    ixu = langColumns["index_unicode"]
    ixn = langColumns["index_langName"]
           
    try:
        with open(csvFile, encoding='utf8') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"') 
            cnt = 0
            for row in csvReader:
  
                if (len(row) < 3) or (len(row[ixu])) != 4: 
                    logging.info('row %d wrong length row len %s  unicode len %s', cnt,len(row),len(row[ixu]))
                    cnt+=1
                    continue
                ncol = len(row)
                unicode = row[ixu].lower()
                name = row[ixn]
                unicode = row[ixu].lower()
                name = row[ixn].strip()
                addFont(font, unicode, language, name)
                cnt+=1
                
    except Exception as  e:
        logging.exception("fatal error read_list %s",e)
        return(1)
        
    return 0
    
def getMetrics(ttfFile, ttfFont):
    global ffMetrics
    v = {}
    v['ttfFile'] = ttfFile
    v['ttfFont'] = ttfFont
    v['xheight'] = float(ttfFont.xHeight)
    v['ascender'] = float(ttfFont.os2_typoascent)
    v['descender'] = float(ttfFont.os2_typodescent)
    ffMetrics = v
    logging.info('ffmetrics ascent= %s descent= %s xHeight= %s'%(v['ascender'], v['descender'], v['xheight']))

def main(*ffargs):
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    logging.info('version %s', bfVersion)
    
    args = []
    for a in ffargs[0]:
        logging.info(a)
        args.append(a)
    rc = 0

    if len(args) > 4: 
        try:
            csvFile = args[1]
            ttfFile = args[2]
            language = args[3].upper()
            backFont = args[4]
            logging.info('arg4 %s',backFont)
            ttfFont = ff.open(ttfFile)
            getMetrics(ttfFile, ttfFont)
            font = createFont(backFont)  

            rc = read_list(font, csvFile, language)  
            if rc == 0:
                logging.info('Saving %s.sfd %d',backFont, rc)
                status = font.save(backFont+".sfd")
                logging.info('status = %s',status)

                logging.info('Generating %s.ttf',backFont)
                #if not namelist:
                status = font.generate(backFont+".ttf")
                logging.info('status = %s',status)
                
                logging.info('Generating %s.woff',backFont)
                #if not namelist:
                status = font.generate(backFont+".woff")
                logging.info('status = %s', status)

        except Exception as e:
            logging.exception('exception %s',e)
            rc = 1
       
    else:
        logging.warning("SYNTAX Error")
        logging.warning("syntax: fontforge -quiet -script svg2Font_ttf.py %infile% %ttffont% %language% %outfile%")
        logging.warning("   Creates a back font from the svg files in /Svg directory")
        logging.warning("   using the names in the csv file for font characteristics")
        logging.warning("   The csv file is expected to have:")
        logging.warning("      Symbol, English Name, Language Name, Unicode(string), Reference")
        rc = 1
        
    if rc == 0:
        logging.info('Done saved font files in %s .ttf |.woff |.sfd', backFont)
    else:
        logging.error('Failed %d',rc)
    
    return rc

if __name__ == "__main__":
   
    logging.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)