#include <bits/stdc++.h>

using namespace std;
FILE *arq2;
int main(int argc, char **argv){
/*	fstream fp;
	char nome[100];
	arq2 = fopen(("imagens.txt"),"r");
	//for (int i = 0; i < 3; ++i){
	int i=1;
	while(fscanf(arq2, "%s", nome) != EOF){
		cout << i++ << ": ";
		cout << nome << endl;
	}
*/	int i =0;
	string line, caminho = "imagens.txt";
	ifstream file(caminho, ifstream::in);
	while(getline(file,line)){
		line.erase(line.begin(), line.begin()+10);
		cout << line << endl;
	}
}


queue<int> q;

q.push(10); // adiciona 10 no fundo da fila
q.push(5);
q.front();  // retorna 10 da frente da fila
q.pop();    // remove 10 da frente da fila