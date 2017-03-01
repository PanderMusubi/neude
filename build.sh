cp -f src/fonts/Neude_beta.?tf .

ttx -o specimens/Neude_beta-otf.ttx Neude_beta.otf
ttx -o specimens/Neude_beta-ttf.ttx Neude_beta.ttf

#OTF_MODIFIED <modified value="
#TTF_MODIFIED <modified value="

TTF_VERSION=`grep '      <version value="' specimens/Neude_beta-ttf.ttx|awk -F '"' '{print $2}'`
OTF_VERSION=`grep '      <version value="' specimens/Neude_beta-otf.ttx|awk -F '"' '{print $2}'`

OTF_GLYPHS=`grep '<GlyphID id="' specimens/Neude_beta-otf.ttx|grep -v '.null'|grep -v '.notdef'|grep -v 'nonmarkingreturn'|wc -l`
TTF_GLYPHS=`grep '<GlyphID id="' specimens/Neude_beta-ttf.ttx|grep -v '.null'|grep -v '.notdef'|grep -v 'nonmarkingreturn'|wc -l`

fntsample -f Neude_beta.otf -o specimens/Neude_beta-otf-fntsample.pdf
fntsample -f Neude_beta.ttf -o specimens/Neude_beta-ttf-fntsample.pdf

fntsample -g -i 0x0000-0x007F -f Neude_beta.otf -o specimens/Neude_beta-otf-fntsample-basic-latin.svg
fntsample -g -i 0x0000-0x007F -f Neude_beta.ttf -o specimens/Neude_beta-ttf-fntsample-basic-latin.svg

inkscape -z -e specimens/Neude_beta-otf-fntsample-basic-latin.png specimens/Neude_beta-otf-fntsample-basic-latin.svg
inkscape -z -e specimens/Neude_beta-ttf-fntsample-basic-latin.png specimens/Neude_beta-ttf-fntsample-basic-latin.svg

convert -flatten specimens/Neude_beta-otf-fntsample-basic-latin.png specimens/Neude_beta-otf-fntsample-basic-latin.png
convert -flatten specimens/Neude_beta-ttf-fntsample-basic-latin.png specimens/Neude_beta-ttf-fntsample-basic-latin.png

fontimage --pixelsize 64 --text NEUDE_BETA --pixelsize 42 --text 0123456789 --text ABCDEFGHIJKLMNOPQRSTUVWXYĲZ --pixelsize 32 --text BLOWZY\ NIGHT-FRUMPS\ VEX\'D\ JACK\ Q. --text LYNX\ C.Q.\ VOS\ PRIKT\ BH\:\ DAG\ ZWEMJUF\! --text $OTF_GLYPHS\ GLYPHS\ V.\ $OTF_VERSION -o specimens/Neude_beta-otf-fontimage.png Neude_beta.otf
fontimage --pixelsize 64 --text NEUDE_BETA --pixelsize 42 --text 0123456789 --text ABCDEFGHIJKLMNOPQRSTUVWXYĲZ --pixelsize 32 --text BLOWZY\ NIGHT-FRUMPS\ VEX\'D\ JACK\ Q. --text LYNX\ C.Q.\ VOS\ PRIKT\ BH\:\ DAG\ ZWEMJUF\! --text $TTF_GLYPHS\ GLYPHS\ V.\ $TTF_VERSION -o specimens/Neude_beta-ttf-fontimage.png Neude_beta.ttf


