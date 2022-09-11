#!/usr/bin/env python3
'''Imports glyphs into FontForge'''

__author__ = "Stichting z25.org <info@z25.org>"
__license__ = "MIT"

from os import listdir, path
import sys
from fontforge import activeFont, nameFromUnicode
#from psMat import translate

WIDTH = 725

def get_src_unis(cwd, font):
    '''get TODO'''
    src_unis = set()#TODO base all on unicode codepoints
    glyph_dir = path.join(cwd, '..', 'glyphs', '11-ExtraBlack')
    svgfiles = [fname for fname in listdir(glyph_dir) if fname[-4:].lower() == '.svg']
    for svgfile in svgfiles:
        if '_alt' in svgfile or '_hor' in svgfile or '_ver' in svgfile:
            print(f'DEBUG: skipping {svgfile}')  #FIXME
            continue
        print(f'DEBUG: svg {svgfile}')
        uni = None
        try:
            src = svgfile.split('_')[0]
            uni = int(src, 16)
        except ValueError as verr:
            print(f'ERROR: Invalid glyph unicode value in file name {svgfile}, {verr}')
            sys.exit(1)
        gname = nameFromUnicode(uni)
        if uni in src_unis: # one design per glyph
            print(f'ERROR: Duplicate glyph name %{svgfile}\t%06d\t{gname}'%uni)
            sys.exit(1)
        else:
            src_unis.add(uni)
        if font:
            glyph = font.createChar(uni, gname)
            glyph.clear()
            if src != '0020':#TODO test
                glyph.importOutlines(path.join(glyph_dir, svgfile))
            glyph.width = WIDTH
        else:
            # Test run from outside of Fontforge
            print(f'INFO: found {svgfile}\t%06d\t{gname}'%uni)

    return src_unis

def main():
    '''Imports glyphs into FontForge'''

    # Following is needed for Unicode characters in file names
#    reload(sys)
#    sys.setdefaultencoding('utf8')

    cwd = path.dirname(path.realpath(__file__))
    font = activeFont()

    src_unis = get_src_unis(cwd, font)

    dst_unis = set()
    for line in open(path.join(cwd, 'refs.tsv')):
        line = line.strip()
        if '\t' in line and line[0] != '#':
            dst, dstc, ref, refc, oper = line.split('\t')
            print(f'DEBUG: dst {dstc} ref {refc}')
            if dst == ref:
                print(f'ERROR: Reference destination {dst} is itself')
            elif ref in ('0', '00', '000', ):
                print(f'ERROR: Reference is 0 for destination {dst}')
            try:
                dst_uni = int(dst, 16)
            except ValueError as verr:
                print('ERROR: Invalid destination glyph unicode value' \
                      f'in reference {dst} ~ {ref}, {verr}')
                continue
            try:
                ref_uni = int(ref, 16)
            except ValueError as verr:
                print('ERROR: Invalid reference glyph unicode value' \
                      f' in reference {dst} ~ {ref}, {verr}')
                continue
            dst_gname = nameFromUnicode(dst_uni)
            ref_gname = nameFromUnicode(ref_uni)
            if dst_uni in src_unis:
                print(f'ERROR: Reference destination {dst_uni} (U{dst})' \
                      ' exists as source glyph')
                continue
            else:
                if ref_uni in src_unis or ref_uni in dst_unis:
                    if font:
                        glyph = font.createChar(dst_uni, dst_gname)
                        # support multiple references
                        if dst_uni not in dst_unis:
                            dst_unis.add(dst_uni)
                            glyph.clear()
                        if oper == 'n':
                            glyph.addReference(ref_gname)
                        # vertical flip between descender and ascender
                        elif oper == 'V':
                            glyph.addReference(ref_gname,
                                               (1.0, 0.0, 0.0, -1.0,
                                                0.0, 500.0))
                        # vertical flip between baseline and cap line
                        elif oper == 'v':
                            glyph.addReference(ref_gname,
                                               (1.0, 0.0, 0.0, -1.0,
                                                0.0, 500.0 + 80.0))
                        # horizontal between glyph width
                        elif oper == 'h':
                            glyph.addReference(ref_gname,
                                               (-1.0, 0.0, 0.0, 1.0,
                                                725.0, 0.0))
                        elif oper == 'hv' or oper == 'vh':
                            glyph.addReference(ref_gname,
                                               (-1.0, 0.0, 0.0, -1.0,
                                                725.0, 500.0 + 80.0))
                        else:
                            print('ERROR: Unknown operation')
                        glyph.width = WIDTH
                else:
                    print(f'WARNING: Destination {dst_uni} (U%s)' \
                          f' {dst_gname} has unavailable reference ' \
                          f'{ref_uni} (U%s) {ref_gname},' \
                          ' skipping, please reorder reference' \
                          ' file or add SVG sources'%(dst, ref))

if __name__ == "__main__":
    main()
