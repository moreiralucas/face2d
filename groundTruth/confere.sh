#!/bin/bash

# O algoritmo verifica a quantidade de arquivos nos três diretórios (lucas, Alvaro e Kaly)
# E verifica se cada arquivo tem 5 linhas de informações

names=(lucas alvaro kalyf)
for name in ${names[@]}; do
	echo $name
	ls $name\_groundTruth/ | wc -l
	ok=0
	for file in $name\_groundTruth/*; do
		nlines=`wc -l $file`
		nlines=`awk -v RS=[0-9]+ '{print RT+0;exit}' <<< "$nlines"`
		if [[ nlines -ne 5 ]]; then
			ok=1
			problematico=$file
		fi
	done
	if [[ ok -ne 0 ]]; then
		echo "$name tem pelo menos um arquivo com numero diferente de linhas do q 5:"
		echo $problematico
	fi
	echo
done