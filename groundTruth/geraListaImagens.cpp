#include <iostream>
using namespace std;

int main(int argc, char const *argv[]){
	int n = 25;
	int m = 3;
	for (int i = 1; i <= n; ++i){
		for (int j = 1; j <= m; ++j){
			cout << i << "_" << j << ".bmp" << endl;
		}
	}
}