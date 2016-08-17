#include <bits/stdc++.h>

using namespace std;

typedef struct ponto{
	int x;
	int y;
}Point;
FILE *arqi;
vector<Point> A, B, C, vetor;
void imprimeVetor(vector<Point> pontos){
	//Point A;
	//while(!pontos.empty()){
	//	cout << A.x << " " << A.y << endl;
	//}
}
Point media2Pontos(Point um, Point dois){
	Point result;
	result.x = (um.x+dois.x)/2;
	result.y = (um.y+dois.y)/2;
	return result;
}
Point media3pontos(Point um, Point dois, Point tres){
	Point result;
	result.x = (um.x+dois.x+tres.x)/3;
	result.y = (um.y+dois.y+tres.y)/3;
	return result;
}
void calcMedIndividual(string caminho){
    int x, y;
	vector<Point> pontos;
    ifstream data(caminho);
    
    if (!data.is_open()){
        exit(EXIT_FAILURE);
    }
    string str;
    while (getline(data, str)){
        istringstream iss(str);
        string token;
        bool a = true;
        while (getline(iss, token, ' ')){
            // process each token
            //cout << token << " " ;
            if(a) x = atoi(token.c_str());
            else y = atoi(token.c_str());
            a=false;
        }
        pontos.push_back(Point({x,y}));
    }
    int tam = pontos.size();
    Point tmp, tmp2;
    reverse(pontos.begin(),pontos.end());
    for (int i = 1; i <= tam; ++i){
    	if((i%2) == 0){
    		tmp2 = pontos.back();
    		C.push_back(media2Pontos(tmp,tmp2));
    		cout << "É par: ";
    	}
    	tmp = pontos.back();
    	pontos.pop_back();
    	cout <<"i:"<< i <<" "<< tmp.x <<" "<< tmp.y << endl;
    }
    C.push_back(tmp);
    //imprimeVetor(pontos);
}
void calcMediaGeral(){
	Point a, b, c;
	for (int i = 0; i < 3; ++i)	{
		a = A.back(); A.pop_back();
		b = B.back(); B.pop_back();
		c = C.back(); C.pop_back();

		vetor.push_back(media3pontos(a,b,c));
	}
}
void writeFile(string nome){
	arqi= fopen(("coordenadas_groundTruth/"+ nome + ".txt").c_str(),"w");
	Point tmp;
	for (int i = 0; i < 3; ++i){
		tmp = vetor.back();
		vetor.pop_back();
		fprintf(arqi, "%d %d", tmp.x, tmp.y);
	}
	cout << "Save file: " << nome << endl;
	fclose(arqi);
}
int main(int argc, char const *argv[]){

	if(argc < 2){
		cout << "error!\nImage not found!" << endl;
		return 0;
	}
	calcMedIndividual(argv[1]);
	swap(C,A);
	calcMedIndividual(argv[2]);
	swap(C,B);
	calcMedIndividual(argv[3]);
	
	calcMediaGeral();
	
	string nome = argv[1];
	writeFile(nome);
	
}