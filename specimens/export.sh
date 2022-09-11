#!/bin/bash
set -e

if [ $(flatpak list|grep org.inkscape.Inkscape|wc -l) -gt 0 ]; then
    EXE=$(echo flatpak run org.inkscape.Inkscape)
else
    EXE=$(echo inkscape)
fi

xelatex main
$EXE drawing.svg -Co drawing.png
optipng drawing.png
