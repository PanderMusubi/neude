#!/usr/bin/env python

from os import listdir, path
from fontforge import activeFont, nameFromUnicode
from psMat import translate
import sys  

# Following is needed for Unicode characters in file names
reload(sys)  
sys.setdefaultencoding('utf8')

__author__ = "Stichting z25.org <info@z25.org>"
__license__ = "MIT"



font = activeFont()
glyphDir = r'/home/sander/workspace/neude/src/glyphs/11-ExtraBlack'
svgfiles = [fname for fname in listdir(glyphDir) if fname[-4:].lower()=='.svg']

src_unis = []#TODO base all on unicode codepoints
for svgfile in svgfiles:
    if '_alt' in svgfile or '_hor' in svgfile or '_ver' in svgfile:
#        print('DEBUG: skipping %s'%svgfile)  #FIXME
        continue
#    print('DEBUG: svg', svgfile)
    try:
        src = svgfile.split('_')[0]
        uni = int(src, 16)
    except:
        print('ERROR: Invalid glyph unicode value in file name: %s'%(svgfile.split('_')[0]))
        exit(1)
    else:
        if uni in src_unis: # one design per glyph
            print('ERROR: Duplicate glyph name %s\t%06d\t%s'%(svgfile, uni, str(gname)))
            exit(1)
        else:
            src_unis.append(uni)
        gname = nameFromUnicode(uni)
        if font:
            glyph = font.createChar(uni, gname)
            glyph.clear()
            if src != '0020':#TODO test
                glyph.importOutlines(path.join(glyphDir, svgfile))
            glyph.width = 725 #TODO how to set this globally?
        else:
            # Test run from outside of Fontforge
            print('INFO: found %s\t%06d\t%s'%(svgfile, uni, str(gname)))

dst_unis = []
with open('/home/sander/workspace/neude/src/fonts/refs.tsv', 'r') as refs:
    for line in refs:
        line = line.strip()
        if '\t' in line and line[0] != '#':
            dst, dc, ref, rc, op = line.split('\t')
#            print('DEBUG: dst', dc, 'ref', rc)
            if dst == ref:
                print('ERROR: Reference destination %s is itself'%dst)
            elif ref in ('0', '00', '000', ):
                print('ERROR: Reference is 0 for destination %s'%dst)
            try:
                dst_uni = int(dst, 16)
            except:
                print('ERROR: Invalid destination glyph unicode value in reference %s ~ %s'%(dst, ref))
                continue
            try:
                ref_uni = int(ref, 16)
            except:
                print('ERROR: Invalid reference glyph unicode value in reference %s ~ %s'%(dst, ref))
                continue
            else:
                dst_gname = nameFromUnicode(dst_uni)
                ref_gname = nameFromUnicode(ref_uni)
                if dst_uni in src_unis:
                    print('ERROR: Reference destination %s (U%s) exists as source glyph'%(dst_uni, dst))
                    continue
                else:
                    if ref_uni in src_unis or ref_uni in dst_unis:
                        if font:
                            glyph = font.createChar(dst_uni, dst_gname)
                            if dst_uni not in dst_unis: # support multiple references
                                dst_unis.append(dst_uni)
                                glyph.clear()
                            if op == 'n':
                                glyph.addReference(ref_gname)
                            elif op == 'V': # vertical flip between descender and ascender
                                glyph.addReference(ref_gname, (1.0, 0.0, 0.0, -1.0, 0.0, 500.0))
                            elif op == 'v': # vertical flip between baseline and cap line
                                glyph.addReference(ref_gname, (1.0, 0.0, 0.0, -1.0, 0.0, 500.0 + 80.0))
                            elif op == 'h': # horizontal between glyph width
                                glyph.addReference(ref_gname, (-1.0, 0.0, 0.0, 1.0, 725.0, 0.0))
                            elif op == 'hv' or op == 'vh':
                                glyph.addReference(ref_gname, (-1.0, 0.0, 0.0, -1.0, 725.0, 500.0 + 80.0))
                            else:
                                print('ERROR: Unknown operation')
                            glyph.width = 725 #TODO how to set this globally?
                    else:
                        print('WARNING: Destination %s (U%s) %s has unavailable reference %s (U%s) %s, skipping, please reorder reference file or add SVG sources'%(dst_uni, dst, dst_gname, ref_uni, ref, ref_gname))
