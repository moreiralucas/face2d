// Comando para compilar (é necessário utilizar o c++11)
//g++ -std=c++11 -g `pkg-config --cflags opencv` gtruth.cpp -o GroundTruth `pkg-config --libs opencv`
#include <iostream>
#include <fstream>
#include <sstream>
#include <opencv2/opencv.hpp>
#include <vector>

using namespace cv;
using namespace std;

#define SCALE 1

FILE *arqi;
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
		//switch(ponto[i].tipo){
			//case 'e':
				circle(vis, Point(ponto[i].Y,ponto[i].X), 3, Scalar(255,0,0), -1);
			//	break;
			//case 'd':
			//	circle(vis, Point(ponto[i].Y,ponto[i].X), 3, Scalar(0,255,0), -1);
			//	break;
			//case 'n':
			//	circle(vis, Point(ponto[i].Y,ponto[i].X), 3, Scalar(0,0,255), -1);
			//	break;
		//}
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
	nome.erase(nome.end() - 4, nome.end());
	arqi= fopen((nome + ".txt").c_str(),"w");
	// Create visualizer
	vis.create(image.rows*SCALE, image.cols*SCALE, CV_8UC3);
	cout << "Ordem das marcações:" << "\n" <<
		"Olho esquerdo e depois olho direito" << "\n" <<
		"Em seguuida o nariz" << "\n" << 
		"--------------------------------" << "\n" <<
		"Pressione 'S' para Salvar" << endl;
	// Application loop
	draw();
	namedWindow("gtruth", 1);
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
				ponto.pop_back();
				draw();
		}
		imshow("gtruth", vis);
	}
	fclose(arqi);
}

void viewMinutiae(string caminho){
	int x,y, j=0;
	string line, letra, xiz, ipicilon;
	ifstream file(caminho, ifstream::in);
	ponto.clear();
	vis.create(image.rows*SCALE, image.cols*SCALE, CV_8UC3);
	
	while(getline(file,line)){
		stringstream lines(line);
		getline(lines,letra,' ');
		getline(lines,ipicilon, ' ');
		getline(lines,xiz);
		x=atoi(xiz.c_str());
		y=atoi(ipicilon.c_str());
		cout << letra << " " << y << " " << x << endl;
		ponto.push_back({y*SCALE,x*SCALE,letra[0]});
	}
	draw();
	namedWindow("gtruth", 1);
	char c;
	
	while((c = waitKey(10)) != 27)
		imshow("gtruth", vis);
}
int main(int argc, char **argv) {
	//Altere o valor de "decision" para visualizar ou para marcar a imagem
	bool decision = true; //'true' para plotar || "false" para exibir imagem plotada
	// Load image
	image = imread(argv[1], 1);
	if(decision){
		// Marca as minúcias
		marker(argv[1]);
	}else{
		//Visualiza as minúcias marcadas
		viewMinutiae(argv[2]);
	}
}