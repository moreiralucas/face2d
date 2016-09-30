#!/bin/bash
#echo "contando linhas..."
#sleep 2
#LINHAS=`cat imagens.txt | wc -l`
#echo "existem $LINHAS no arquivo!"

#var=coordenadas.txt


for i in $(cat imagens.txt);
do
	template=`echo $i | cut -c10- | cut -d "." -f 1`
	um=alvaro_groundTruth$template".txt"
	dois=kalyf_groundTruth$template".txt"
	tres=lucas_groundTruth$template".txt"
	#echo $um $dois $tres
	#echo $var
	#echo "$i"
	./CalculaMedia.out $um $dois $tres
	#./RNsID $i $var #imagens/groundtruth/$template.txt imagens/resultados/$template`echo _result`.txt 
	#mv coordenadas.txt resultados/$template`echo _minucias`.txt
done


#echo "Contando as linhas ..."
#sleep 5
#LINHAS=`cat ~/relatorio/processos.txt | wc -l`
#echo "Existem $LINHAS no arquivo."