#include <iostream>
using namespace std;

int main(int argc, char const *argv[]){
	int n = 50;
	int m = 5;
	for (int i = 26; i <= n; ++i){
		for (int j = 1; j <= m; ++j){
			cout << "../FACE2D/" << i << "_" << j << ".bmp" << endl;
		}
	}
}