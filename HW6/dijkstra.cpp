#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#define MAX 200
#define MAX_LEN 1000000
using namespace std;

struct node {
	int number;
	bool known;
	int previous;
	int dist;
};

int matrix[MAX + 1][MAX + 1];
node graph[MAX + 1];
vector<int> X;
int ten[10] = {7,37,59,82,99,115,133,165,188,197 };

void readData(char * path) {
	ifstream fin(path);
	if(fin.fail()) {
		cout<<"File Open Error!"<<endl;
		return;
	}
	int from, to, len;
	string line;

	while(!fin.eof()) {
		getline(fin, line);

		stringstream st(line);
		st>>from;
		while(st>>to) {
			char c;
			st>>c;
			if(c !=',') {
				cout<<"File Format Error!"<<endl;
				return;
			}
			//The above sentence to judge the comma can be replaced by one sentence
			//st.ignore();//The writable parameter in brackets represents the number of skip elements, the default is 1
			st>>len;
			matrix[from][to] = len;
		}
	}
}

void initGraph() {
	for(int i = 0; i <MAX + 1; i++) {
		graph[i].known = false;
		graph[i].number = i;
		graph[i].previous = 0;
		graph[i].dist = MAX_LEN;
	}
}

void dijkstra(int s) {
	graph[s].dist = 0;
	int curr, next, shortest;

	while(X.size() <MAX) {
		shortest = MAX_LEN;
		//find vertex in Q with smallest distance in maxtrix[]
		for(int i = 1; i <= MAX; i++) {
			if( !graph[i].known && graph[i].dist <shortest) {
				shortest = graph[i].dist;
				next = i;
			}
		}
		curr = next;
		//If the shortest side is not reachable, exit the loop
		if(shortest == MAX_LEN) break;
		//curr is the current vertex, mark it as known and store it in X
		X.push_back(curr);
		graph[curr].known = true;

		//Process all neighbors of curr
		for(int j = 1; j <= MAX; j++) {
			if(matrix[curr][j]> 0 && graph[curr].dist + matrix[curr][j] <graph[j].dist) {
				graph[j].dist = graph[curr].dist + matrix[curr][j];
				graph[j].previous = curr;
			}
		}
	}
}

int main() {
	readData("dijkstraData.txt");
	initGraph();
	dijkstra(1);

	ofstream fout("out.txt");
	for(int i = 0; i <10; i++) {
		fout<<graph[ ten[i] ].dist<<',';
	}
	fout.close();

	return 0;
}