#!/bin/bash

locall=../Documentos/FACE2D/
for i in $(ls ../Documentos/FACE2D);
do
	tmp=`echo $i`
	#echo $locall$tmp
	./a.out --cascade="haarcascade_frontalface_alt.xml" --nested-cascade="haarcascade_eye_tree_eyeglasses.xml" $locall$tmp
done
