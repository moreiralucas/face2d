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
typedef struct minucias{
	int X;
	int Y;
	char tipo;
}Minucia;
vector<Minucia> minucia;
void draw() {
	for(int i=0; i < vis.rows; i++)
		for(int j=0; j < vis.cols; j++){
			vis.at<Vec3b>(i,j)[2] = image.at<Vec3b>(i/SCALE,j/SCALE)[2];
			vis.at<Vec3b>(i,j)[1] = image.at<Vec3b>(i/SCALE,j/SCALE)[1];
			vis.at<Vec3b>(i,j)[0] = image.at<Vec3b>(i/SCALE,j/SCALE)[0];
		}
	for(int i=0; i < minucia.size(); i++)
		switch(minucia[i].tipo){
			case 'e':
				circle(vis, Point(minucia[i].Y,minucia[i].X), 3, Scalar(255,0,0), -1);
				break;
			case 'd':
				circle(vis, Point(minucia[i].Y,minucia[i].X), 3, Scalar(0,255,0), -1);
				break;
			case 'n':
				circle(vis, Point(minucia[i].Y,minucia[i].X), 3, Scalar(0,0,255), -1);
				break;
		}
	//for(int i=0; i < minucia.size(); i++)
	//	circle(vis, Point(minucia[i].X,minucia[i].Y), 3, CV_RGB(255,0,0), -1);
	imshow("gtruth", vis);
}
void mousefunc(int event, int x, int y, int flags, void* userdata) {
	if(event == EVENT_LBUTTONDOWN) {
		minucia.push_back({y,x,'e'});
		draw();
	}
	if(event == EVENT_RBUTTONDOWN){
		minucia.push_back({y,x,'d'});
		draw();
	}
	if(event == EVENT_MBUTTONDOWN){
		minucia.push_back({y,x,'n'});
		draw();
	}
}
void marker(string nome){
	fstream fp;

	minucia.clear();
	nome.erase(nome.end() - 4, nome.end());
	arqi= fopen((nome + ".txt").c_str(),"w");
	// Create visualizer
	vis.create(image.rows*SCALE, image.cols*SCALE, CV_8UC3);
	cout << "Botão esquerdo do mouse: Olho esquerdo." << "\n" <<
		"Botão direto do mouse: Olho direito." << "\n" <<
		"Botão do meio do mouse: Nariz" << "\n" << 
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
				for(int i=0; i < minucia.size(); i++){
					fprintf(arqi, "%c %d %d\n",minucia[i].tipo, minucia[i].Y/SCALE,minucia[i].X/SCALE);
				}
				cout << "Save file: " << nome << endl;
				break;
			case '\b':
				minucia.pop_back();
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
	minucia.clear();
	vis.create(image.rows*SCALE, image.cols*SCALE, CV_8UC3);
	
	while(getline(file,line)){
		stringstream lines(line);
		getline(lines,letra,' ');
		getline(lines,ipicilon, ' ');
		getline(lines,xiz);
		x=atoi(xiz.c_str());
		y=atoi(ipicilon.c_str());
		cout << letra << " " << y << " " << x << endl;
		minucia.push_back({y*SCALE,x*SCALE,letra[0]});
	}
	draw();
	namedWindow("gtruth", 1);
	char c;
	
	while((c = waitKey(10)) != 27)
		imshow("gtruth", vis);
	//caminho.erase(caminho.end() - 4, caminho.end());
	//caminho += "_plotado.png";
	//imwrite(caminho,vis);
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