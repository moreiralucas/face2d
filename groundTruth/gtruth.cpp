// Comando para compilar (é necessário utilizar o c++11)
//g++ -std=c++11 -g gtruth.cpp -o GroundTruth.out `pkg-config --libs opencv --cflags opencv`

#include <iostream>
#include <fstream>
#include <sstream>
#include <opencv2/opencv.hpp>
#include <vector>

using namespace cv;
using namespace std;

#define SCALE 2

FILE *arqi, *arq2;
Mat image, vis;

typedef struct pontos{
	int X;
	int Y;
//	char tipo; //olhoEsq || olhoDir || nariz
}Ponto;
vector<Ponto> ponto;
void draw() {
	for(int i=0; i < vis.rows; i++)
		for(int j=0; j < vis.cols; j++){
			vis.at<Vec3b>(i,j)[2] = image.at<Vec3b>(i/SCALE,j/SCALE)[2];
			vis.at<Vec3b>(i,j)[1] = image.at<Vec3b>(i/SCALE,j/SCALE)[1];
			vis.at<Vec3b>(i,j)[0] = image.at<Vec3b>(i/SCALE,j/SCALE)[0];
		}
	for(int i=0; i < ponto.size(); i++)
		circle(vis, Point(ponto[i].Y,ponto[i].X), 3, Scalar(255,0,0), -1);
	imshow("gtruth", vis);
}
void mousefunc(int event, int x, int y, int flags, void* userdata) {
	if(event == EVENT_LBUTTONDOWN) {
		ponto.push_back({y,x});
		draw();
	}
}
void marker(string nome){
	fstream fp;

	ponto.clear();
	arqi= fopen(("groundTruthTMP/"+ nome + ".txt").c_str(),"w");
	// Create visualizer
	vis.create(image.rows*SCALE, image.cols*SCALE, CV_8UC3);
	cout << "--------------------------------\n" <<
		"Imagem: " + nome + ".bmp\n" <<
		"--------------------------------\n" <<
		"Pressione 'S' para Salvar\nPressione 'Esc' pra ir para a próxima" << endl;
	// Application loop
	draw();

	//namedWindow("gtruth", 1); //Trocar o valor 1 por WINDOW_AUTOSIZE

	namedWindow("gtruth", WINDOW_NORMAL);

	setMouseCallback("gtruth", mousefunc, NULL);
	char c;
	while((c = waitKey(10)) != 27) {
		switch(c) {
			case 's':
				for(int i=0; i < ponto.size(); i++){
					fprintf(arqi, "%d %d\n", ponto[i].Y/SCALE,ponto[i].X/SCALE);
				}
				cout << "Save file: " << nome << endl;
				break;
			case '\b':
				if (!ponto.empty())
					ponto.pop_back();
				draw();
		}
		imshow("gtruth", vis);
	}
	fclose(arqi);
}
int main(int argc, char const *argv[]){
	if(argc > 1){
		cout << "Nao preceisa passar argumentos\nUse apenas " << argv[0] << endl;
		return 0;
	}
	string line, caminho = "imagens.txt";
	std::ifstream file(caminho.c_str(), ifstream::in);
	system("clear");
	//input images	
	while(getline(file,line)){
		stringstream lines(line);
		//cout << "caminho: " + caminho << endl;
		getline(lines,caminho,';');
		
		if (!caminho.empty()){
			// Load image
			image = imread(caminho, 1);
			
			int p = caminho.rfind('/')+1;
			int x = caminho.rfind('.');
			string nomes = caminho.substr(p,x-p);

			// Marca as minúcias
			marker(nomes);
		}
		cout << "PRÓXIMA!\n\n\n" << endl;
		system("clear");
	}
	//fclose(arqi);
}

//nome.erase(nome.end() - 7, nome.end());
