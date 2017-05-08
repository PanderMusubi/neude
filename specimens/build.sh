
cp -f ../src/fonts/Neude.?tf ..

rm -f Neude-otf.ttx
rm -f Neude-ttf.ttx

ttx -o Neude-otf.ttx ../Neude.otf
ttx -o Neude-ttf.ttx ../Neude.ttf

#OTF_MODIFIED <modified value="
#TTF_MODIFIED <modified value="

OTF_VERSION=`grep '      <version value="' Neude-otf.ttx|awk -F '"' '{print $2}'`
#TTF_VERSION=`grep '      <version value="' Neude-ttf.ttx|awk -F '"' '{print $2}'`
TTF_VERSION=$OTF_VERSION

OTF_GLYPHS=`grep '<GlyphID id="' Neude-otf.ttx|grep -v '.null'|grep -v '.notdef'|grep -v 'nonmarkingreturn'|wc -l`
TTF_GLYPHS=`grep '<GlyphID id="' Neude-ttf.ttx|grep -v '.null'|grep -v '.notdef'|grep -v 'nonmarkingreturn'|wc -l`

fntsample -f ../Neude.otf -o Neude-otf-fntsample.pdf
fntsample -f ../Neude.ttf -o Neude-ttf-fntsample.pdf

fntsample -g -i 0x0000-0x007F -f ../Neude.otf -o Neude-otf-fntsample-basic-latin.svg
fntsample -g -i 0x0000-0x007F -f ../Neude.ttf -o Neude-ttf-fntsample-basic-latin.svg

inkscape -z -e Neude-otf-fntsample-basic-latin.png Neude-otf-fntsample-basic-latin.svg
inkscape -z -e Neude-ttf-fntsample-basic-latin.png Neude-ttf-fntsample-basic-latin.svg

convert -flatten Neude-otf-fntsample-basic-latin.png Neude-otf-fntsample-basic-latin.png
convert -flatten Neude-ttf-fntsample-basic-latin.png Neude-ttf-fntsample-basic-latin.png

fontimage --pixelsize 64 --text NEUDE --pixelsize 42 --text 0123456789\ \"\'+=^\`\| --text ABCDEFGHIJKLMNOPQRSTUVWXYĲZ --pixelsize 32 --text BLOWZY\ NIGHT-FRUMPS\ VEX\'D\ JACK\ Q. --text LYNX\ C.Q.\ VOS\ PRIKT\ BH\:\ DAG\ ZWEMJUF\! --text $OTF_GLYPHS\ GLYPHS\ V.\ $OTF_VERSION -o Neude-otf-fontimage.png ../Neude.otf
fontimage --pixelsize 64 --text NEUDE --pixelsize 42 --text 0123456789\ \"\'+=^\`\| --text ABCDEFGHIJKLMNOPQRSTUVWXYĲZ --pixelsize 32 --text BLOWZY\ NIGHT-FRUMPS\ VEX\'D\ JACK\ Q. --text LYNX\ C.Q.\ VOS\ PRIKT\ BH\:\ DAG\ ZWEMJUF\! --text $TTF_GLYPHS\ GLYPHS\ V.\ $TTF_VERSION -o Neude-ttf-fontimage.png ../Neude.ttf

echo
echo 'TTF version: '$TTF_VERSION
echo 'OTF version: '$OTF_VERSION

echo
echo 'TTF glyphs: '$TTF_GLYPHS
echo 'OTF glyphs: '$OTF_GLYPHS
