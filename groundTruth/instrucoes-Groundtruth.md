*As marcações serão feitas da esquerda para a direita, começando com o olho esquerdo, depois direito e por fim o nariz (marcar o ponto mais baixo do nariz).*

Após as marcações, será feito a média dos pontos de cada olho e posteriormente, será salvo em um arquivo de texto, em diretórios separados, com as seguinte especificações:

Diretório:
```
<groundTruth/nomeDeQuemMarcou_groundTruth/n_m.bmp>
```
**n**: 1 <= n >= 25

**m**: 1 <= m >= 5

Arquivo referente à imagem marcada:

```
<nome da imagem.jpeg> <olhoEsq> <olhoDir> <nariz>
```


# Como compilar e executar o código...


Compile com:
```
make
```

Execute com:
```
./GroundTruth.out
```

OBS: Não é necessário passar parâmetro na execução do algoritmo

