#!/usr/bin/env fontforge -lang=py
# http://www.typophile.com/node/81351
# http://fontforge.github.io/scripting.html#Example
# https://fontforge.github.io/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# https://www.php.net/manual/en/imagick.queryfontmetrics.php

import sys
import os
import csv
import subprocess
import time
import glob
import logging
from bfLog import log_setup
from bfConfig_ttf import bfVersion, loadConfig

config = loadConfig() 

def mkdirp(path):
    if not os.path.exists(path):
        os.makedirs(path) 

def makeSVG(fontName, itype, name, unicode, language):
    svgopt = config["svg_options"]
    svgFile = "Svg\\"+unicode+"-"+itype+"-"+language+".svg"
    pngFile = "Png\\"+unicode+"-"+itype+"-"+language+".png"
    pnmFile = "tmp.pnm"

    if glob.glob(svgFile):
        logging.warning('***duplicate file %s',svgFile) 
        return 'duplicate'
    if glob.glob(pngFile):
        logging.warning('***duplicate file %s',pngFile)  
        return 'duplicate'
        

    #cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+name+'"'+" "+pnmFile
    cmd = "magick convert" + " -font "+fontName \
        +" -pointsize "+str(svgopt["pointsize"]) \
        +" -interword-spacing "+ str(svgopt["interword-spacing"]) \
        +" label:"+'"'+name+'"'+" -trim "+pnmFile
    logging.info(cmd)
    try:
        status = subprocess.call(cmd, shell=True)   
        cmd = "potrace" +" --svg "+pnmFile+" -o "+'"'+svgFile+'"'
        logging.info('   status %s %s ',status, cmd)
        if status == 0:
            status = subprocess.call(cmd, shell=True)
        if status != 0:    
            logging.error('Error processing  %s %s',status, cmd)
            return(status)

        cmd = "magick convert" + " -font "+fontName \
            +" -pointsize "+str(svgopt["pointsize"]) \
            +" -interword-spacing "+ str(svgopt["interword-spacing"]) \
            +" label:"+'"'+name+'"'+" -trim "+pngFile
        logging.info(cmd)
        status = subprocess.call(cmd, shell=True)
        if status != 0:    
            logging.error('Error processing  %s %s',status, cmd)
            return(status)
            
    except Exception as  e:
        logging.exception("fatal error makePNG file  %s %s", pngFile, e)
        return(2)  
            
    return(0)

def read_list(fontName, csvFile, language):
    langColumns = config["lang_columns"]
    ixt = langColumns["index_type"]
    ixu = langColumns["index_unicode"]
    ixn = langColumns["index_name"]
    status = 0
    try:
        logging.info('readlist %s %s %s',fontName, csvFile, language)
        logging.info('dict columns ixu %s  ixn  %s',ixu,ixn)
        with open('Dist/duplicates.txt', 'w') as dup:
                with open(csvFile, encoding='utf8') as csvDataFile:
                    csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"')
                    for line in csvReader:
                        #print(type(line),len(line), line)
                        #print(str(line))
                        # incase csv file has leading and trailing double quotes
                        if len(line) == 1:
                            row = str(line).strip().strip('"')
                            row = row.split(',')
                        else:
                            row = line

                        name = row[ixn].strip()  #.replace(" ","_")
                        unicode = row[ixu].strip().lower()
                        if len(name) == 0:
                            continue
                        
                        if (len(row) < 3) or (len(row[ixu])) != 4: 
                            logging.info('row wrong length row len %s  unicode len %s',len(row),len(row[ixu]))
                            continue

                        if len(unicode) == 4:
                            status = makeSVG(fontName, row[ixt], name, unicode, language)

                        if status != 0:
                            if status == 'duplicate':
                                status = 'Duplicate Entry '+unicode+':'+name
                                dup.write(status+'\n')
                            else:    
                                return status

    except Exception as e:
        logging.exception("fatal error read_list %s",e)   # file=sys.stderr)
        return(3)
        
    return status


def main(*ffargs):   
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    logging.info('version %s', bfVersion)
    args = []
    rc = 0
    for a in ffargs[0]:
        logging.info('%s',a)
        args.append(a)
        

    if len(args) > 2:
        csvFile = args[1]
        fname, lExt = csvFile.split(".")
        ttfFont = args[2].lower()
        language = args[3].upper()
        status = read_list(ttfFont, csvFile, language)
        logging.info('read_list status %s',status)
        rc = status
    else:
        logging.warning("SYNTAX Error")
        logging.warning("syntax: fontforge -script csv2svg_ttf.py  %csv_infile%  %ttf_file%  %language%")
        logging.warning("Creates svg files in the /svg directory using")
        logging.warning("   The csv file is expected to have:")
        logging.warning("      Symbol, English Name, Language Name, Unicode(string), Reference")
        rc = 1

    if rc == 0:
        logging.info('Done SVG files are in Svg directory')
    else:
        if 'Duplicate' in rc:
            logging.warning('Duplicates found %s',rc)
        else:
            logging.error('Failed %s',rc)

    return(rc)

if __name__ == "__main__":
    mkdirp('Log')
    mkdirp('Svg')
    mkdirp('Png')
    mkdirp('Dist')
    rc = main(sys.argv) 
    sys.exit(rc)