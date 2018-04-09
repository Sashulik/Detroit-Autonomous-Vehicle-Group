#!/bin/bash

# command for converting png to jpeg files in the current directory 
# (at least on macOS with the sips command)

for i in *.png; do j="${i%.*}.jpg"; sips -s format jpeg $i --out $j; done