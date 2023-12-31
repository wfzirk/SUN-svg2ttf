
# http://fontforge.github.io/scripting.html#Example
# https://stuff.mit.edu/afs/sipb.mit.edu/project/wine/src/fontforge-20070511/fontforge/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# http://designwithfontforge.com/en-US/Importing_Glyphs_from_Other_Programs.html
# https://pelson.github.io/2017/xkcd_font_raster_to_vector_and_basic_font_creation/
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# https://github.com/pteromys/svgs2ttf/blob/master/README.md
# https://freetype.org/freetype2/docs/glyphs/glyphs-3.html

import fontforge as ff
import psMat
import os
import sys
import csv
import os.path
import xml.etree.ElementTree as ET
import logging

from bfLog import log_setup
from bfConfig_ttf import bfVersion, loadConfig
 
config = loadConfig() 
ffMetrics = {} 

'''
def getWord(word):
    #logging.info(word)
    maxt = 0
    minb = 0
    ##ww = []
    try:
        for w in word:
            g = ffMetrics["ttfFont"][ord(w)]
            #g.left_side_bearing = 10     #75
            #g.right_side_bearing = 10 
            if g.glyphclass == 'baseglyph':
                left, bot, right, top = g.boundingBox()
                logging.info('getWord %s \t%s \t%s \t%s',w, (right-left), (top-bot))
                minb = min(minb, bot)
                maxt = max(maxt, top) 
            #if g.glyphclass == 'mark':
            #    maxt = max(maxt, top)
        logging.info('getWord %s \t%s \t%s',word, minb, maxt)
        #logging.info('bearings  %s  %s', int(g.left_side_bearing), int(g.right_side_bearing)) 
    except Exception as e:
            logging.exception('exception %s name:%s ord:%s word:%s min:%s max:%s',e, w, ord(w), word, minb, maxt)
            #traceback.print_exc()
            return(1)
    return minb, maxt


def scale(glyph):   #, wordMin, wordMax):
    #global desc_scale
    #options = config["glyph_options"]
    options = config["glyph_options_normal"]
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
'''


def wordMetrics(word):
    # get dimensions of ttfFont word
    ymin = 0
    height = 0
    width = 0
    for w in word:
        g = ffMetrics["ttfFont"][ord(w)]
        left, bot, right, top = g.boundingBox()
        if g.glyphclass == 'baseglyph':
            ymin = min(bot, ymin)
            height = max((top-bot),height)
            width = width + (right - left)
        
    #print('wordMetrics', word, ymin, height, width)
    return(ymin, height, width)

def svgMeta(svgFile):
    #print('svgm',filename)
    tree = ET.parse(svgFile)
        
    width, height = tree.getroot().attrib["width"], tree.getroot().attrib["height"]
    width = int(float(width.replace('pt','')))
    height = int(float(height.replace('pt','')))
    #print(f"{os.path.basename(svgFile)}: Width: {width} Height: {height}")
    return(width, height)  

unicodeList = []        # check for duplicates
glyphOptions = config["glyph_options_normal"]
def addFont(font, itype, word, unicode, language):
    logging.info('addfont- %s %s', unicode, word)
    
    try:
        if unicode in unicodeList:
            logging.info('duplicate unicode  %s', unicode)
        
        else:
            unicodeList.append(unicode)

            imgFile = "Svg\\"+unicode+"-"+itype+"-"+language+".svg"
            exists = os.path.isfile(imgFile)
            if exists:
                # get dimensions of word from original font
                wMin, wHeight, wWidth = wordMetrics(word)
                # get dimensions of image - for information only
                svgWidth, svgHeight = svgMeta(imgFile)
                
                # create a new glyph with the code point unicode
                glyph = font.createChar(int(unicode, 16), 'u'+unicode)
                # import svg file into it
                glyph.importOutlines(imgFile) 
                
                # get dimensions of glyph
                gbbox = glyph.boundingBox()
                gWidth = int(gbbox[2] - gbbox[0])
                gHeight = int(gbbox[3] - gbbox[1])
                gMin = int(gbbox[1])
                
                logging.info('widths %s %s svg:%s, word:%s glyph:%s ' % (unicode, word, svgWidth, wWidth, gWidth))
                logging.info('heights  svg:%s, word:%s glyph:%s wMin:%s  gMin:%s' % (svgHeight, wHeight, gHeight, wMin, gMin))

                # scale glyph to fit word
                wScale = wWidth/gWidth
                scale_matrix = psMat.scale(wScale)
                logging.info('scale %s %s',wScale, scale_matrix)
                glyph.transform(scale_matrix)
                
                # make the glyph rest on the baseline
                ymin = glyph.boundingBox()[1]
                y = ymin - wMin
                glyph.transform([1, 0, 0, 1, 0, -y])
                
                # scale to xheight
                s = glyphOptions["font_scale"]/ffMetrics['xheight']
                scale_matrix = psMat.scale(s)
                glyph.transform(scale_matrix)
                
                # set glyph side bearings, can be any value or even 0
                glyph.left_side_bearing = glyphOptions["left_side_bearing"]
                glyph.right_side_bearing = glyphOptions["right_side_bearing"]

            else:
                logging.warning("file %s does not exist", imgFile)
                return(2)
    except Exception as e:
        logging.exception('exception %s file:%s  unicode:%s',imgFile,e, unicode)
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
    ixt = langColumns["index_type"]
    ixu = langColumns["index_unicode"]
    ixn = langColumns["index_name"]
    
    try:
        with open(csvFile, encoding='utf8') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"') 

            for line in csvReader:
                # incase csv file has leading and trailing double quotes
                if len(line) == 1:
                    row = str(line).strip().strip('"')
                    row = row.split(',')
                else:
                    row = line
                if (len(row) < 3) or (len(row[ixu])) != 4: 
                    logging.info('wrong length row len %s  unicode len %s', len(row),len(row[ixu]))
                    continue
                iType = row[ixt]
                if iType.upper() != 'PRI':
                    # only primary words to make font
                    continue
                unicode = row[ixu].lower()
 
                word = row[ixn].strip()
                rc = addFont(font, iType, word, unicode, language)
                if rc:
                    return rc
    except Exception as  e:
        logging.exception("fatal error read_list %s",e)
        return(1)
        
    return 0
    
def getMetrics(ttfFile, ttfFont):
    global ffMetrics
    ffMetrics['ttfFile'] = ttfFile
    ffMetrics['ttfFont'] = ttfFont
    ffMetrics['xheight'] = float(ttfFont.xHeight)
    ffMetrics['ascender'] = float(ttfFont.os2_typoascent)
    ffMetrics['descender'] = float(ttfFont.os2_typodescent)
    logging.info('ffmetrics ascent= %s descent= %s xHeight= %s'%(ffMetrics['ascender'], ffMetrics['descender'], ffMetrics['xheight']))

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