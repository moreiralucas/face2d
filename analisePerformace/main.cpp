#include <bits/stdc++.h>

using namespace std;

struct Point{
	int x, y;
};
vector<Point> ground, lucas, kalyf, alvaro, pontos;


void lerDados(string caminho, bool flag){
	//flag = 0 := arquivo com três linhas
	//flag = 1 := arquivo com cinco linhas
	ifstream data(caminho);
	if(!data.is_open())
		exit(EXIT_FAILURE);
	pontos.clear();
	string str, xiz, ypicilon;
	//getline(data, str);
	int i = 1;
	while(getline(data, str)){
		int x, y;
		stringstream lines(str);
		getline(lines, xiz, ' ');
		getline(lines, ypicilon);
		x = atoi(xiz.c_str()); //cout << "Valor de x: " << x << endl;
		y = atoi(ypicilon.c_str()); //cout << "Valor de y: " << y << endl;
		if(flag && ((i % 2) == 0)){ //entra nesse if na segunda linha do arquivo lido
			Point tmp = pontos.back();
			pontos.pop_back();
			x = (x + tmp.x)/2;
			y = (y + tmp.y)/2;
		}
		pontos.push_back({x, y});
		i++;
		//cout << "pontos.size(): " << pontos.size() << endl;
	}
	for (int i = 0; i < pontos.size(); ++i){
		//cout << "pontos[i].x: " << pontos[i].x;
		//cout << " pontos[i].y: " << pontos[i].y << endl;
	}
}

double mediaImagem(){
	double media, dist = 0;
	dist += abs(ground[0].x - alvaro[0].x);
	dist += abs(ground[0].y - alvaro[0].y);
	dist += abs(ground[1].x - alvaro[1].x);
	dist += abs(ground[1].y - alvaro[1].y);

	dist += abs(ground[0].x - kalyf[0].x);
	dist += abs(ground[0].y - kalyf[0].y);
	dist += abs(ground[1].x - kalyf[1].x);
	dist += abs(ground[1].y - kalyf[1].y);

	dist += abs(ground[0].x - lucas[0].x);
	dist += abs(ground[0].y - lucas[0].y);
	dist += abs(ground[1].x - lucas[1].x);
	dist += abs(ground[1].y - lucas[1].y);

	media = dist / 12;
	//cout << "media: " << dist << "/12: " << media << endl;
	return media;
}

double variancia(double media){
	double var = 0;
	var += pow((abs(ground[0].x - alvaro[0].x) - media), 2);
	var += pow((abs(ground[0].y - alvaro[0].y) - media), 2);
	var += pow((abs(ground[1].x - alvaro[1].x) - media), 2);
	var += pow((abs(ground[1].y - alvaro[1].y) - media), 2);
	
	var += pow((abs(ground[0].x - kalyf[0].x) - media), 2);
	var += pow((abs(ground[0].y - kalyf[0].y) - media), 2);
	var += pow((abs(ground[1].x - kalyf[1].x) - media), 2);
	var += pow((abs(ground[1].y - kalyf[1].y) - media), 2);
	
	var += pow((abs(ground[0].x - lucas[0].x) - media), 2);
	var += pow((abs(ground[0].y - lucas[0].y) - media), 2);
	var += pow((abs(ground[1].x - lucas[1].x) - media), 2);
	var += pow((abs(ground[1].y - lucas[1].y) - media), 2);
	
	return (var / 11); //var / 12 -1
}

double desvioPadrao(double var){
	return sqrt(var);
}

int main(int argc, char const *argv[]){
	if(argc < 5){
		cout << "Argc: " << argc << endl;
		cout << "Use: " << argv[0] << " <media.txt> <alvaro.txt> <kalyf.txt> <lucas.txt>" << endl;
		return 0;
	}
	//cout << argv[1] << " " << argv[2] << " " << argv[3] << " " << argv[4] << endl;
	//return 0;
	cout << argv[5] << " ";//identificador da imagem

	lerDados(argv[1], 0); //cout << "Leu ground\n\n";
	swap(pontos, ground);

	lerDados(argv[2], 1); //cout << "Leu alvaro\n\n";
	swap(pontos, alvaro);

	lerDados(argv[3], 1); //cout << "Leu kalyf\n\n";
	swap(pontos, kalyf);

	lerDados(argv[4], 1); //cout << "Leu lucas\n\n";
	swap(pontos, lucas);

	double M = mediaImagem(); //cout << "M: " << M << endl;

	double var = variancia(M); //cout << var << " ";// << endl;//cout << "var: " << var << endl;

	double dp = desvioPadrao(var); cout << dp << endl;//cout << "dp: " << dp << endl;
	return 0;
}