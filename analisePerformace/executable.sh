#!/bin/bash

#locall=../Documentos/FACE2D/
#for i in $(ls ../groundTruth/lucas_groundTruth/);
#do
#	tmp=`echo $i`
#	echo $tmp
#	#echo $locall$tmp
#	
#done



for i in $(cat ../groundTruth/imagens.txt);
do
	template=`echo $i | cut -d "." -f 1`
	um=../groundTruth/alvaro_groundTruth/$template".txt"
	dois=../groundTruth/kalyf_groundTruth/$template".txt"
	tres=../groundTruth/lucas_groundTruth/$template".txt"
	#echo $um $dois $tres
	#echo $var
	#echo $i
	#echo $template
	echo $um $dois $tres
	#cat $tres
	#./RNsID $i $var #imagens/groundtruth/$template.txt imagens/resultados/$template`echo _result`.txt 
	#mv coordenadas.txt resultados/$template`echo _minucias`.txt
done

