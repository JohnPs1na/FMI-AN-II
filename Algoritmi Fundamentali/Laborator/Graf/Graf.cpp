#include <bits/stdc++.h>

using namespace std;

ifstream fin("graf.in");
ofstream fout("graf.out");

class Graph {

private:

    //Variabile private

    int vertices;
    int edges;
    bool oriented;
    vector<int> *adjacency_list;

    //To compute:
    vector<list<int>> biconnected_components;
    vector<vector<int>> strongly_connected_components;
    vector<int> topological;
    vector<pair<int,int>> bridges;

    //Functii private

    void BFS(int starting_vertex, int *distances); //Breadth-first search

    void DFS(int vertex, int *visited); //Depth-first search

    void BCC(int vertex, vector<int> &parent, stack<int> &vertices_stack, vector<int> &discovery_time,
             vector<int> &lowest_reachable, int &timer);  //Biconnected Components

    void SCC(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable, stack<int> &vertices_stack,
             vector<bool> &on_stack, int &timer);   //Strongly connected components

    void CCN(int vertex,vector<int>& discovery_time, vector<int>& lowest_reachable,vector<bool>& visited, vector<int>& parent, int& timer); //Critical Connections

    void TOPOLOGICAL_SORT(int vertex, vector<bool> &visited);

    vector<int> BFSMD(int starting_vertex);

public:

    Graph(int vertices = 0, int edges = 0, bool oriented = false);

    ~Graph();

    void infoarena_graph();

    void show_my_graph();

    void solve_distances(int starting_vertex);

    void solve_connected_components();

    void solve_biconnected();

    void solve_strongly_connected();

    void solve_topological();

    void solve_critical_connections();

    void solve_starting_ending_distance(int starting_vertex, int ending_vertex);

};

bool solve_havel_hakimi(vector<int> degrees);

void printv(vector<int> xs){
    for(int i : xs) cout<<i<<' ';
    cout<<'\n';
}


int main() {

    int n,m,s,e;
    fin>>n>>m>>s>>e;
    Graph g(n,m,false);
    g.infoarena_graph();
    g.solve_starting_ending_distance(s,e);

}

#pragma region Initialization

Graph::Graph(int vertices, int edges, bool oriented) : vertices(vertices), edges(edges), oriented(oriented) {
    adjacency_list = new vector<int>[vertices + 1];
}

Graph::~Graph() {
    delete[] adjacency_list;
}

void Graph::infoarena_graph() {
    int x, y;
    if (oriented) {
        for (int i = 1; i <= edges; i++) {
            fin >> x >> y;
            adjacency_list[x].push_back(y);
        }
    } else {
        for (int i = 1; i <= edges; i++) {
            fin >> x >> y;
            adjacency_list[x].push_back(y);
            adjacency_list[y].push_back(x);
        }
    }
}

void Graph::show_my_graph() {
    for (int i = 1; i < vertices + 1; i++) {
        cout << i << "=>";

        for (int j : adjacency_list[i]) {
            cout << j << ' ';
        }
        cout << '\n';
    }
}

#pragma endregion

//Algorithm implementations
#pragma region Algorithms

void Graph::BFS(int starting_vertex, int *distances) {

    int *visited = (int *) calloc(vertices + 1, sizeof(int));
    queue<int> que;
    que.push(starting_vertex);

    distances[starting_vertex] = 1;
    visited[starting_vertex] = 1;

    while (!que.empty()) {
        int current_node = que.front();
        que.pop();

        for (auto neighbor : adjacency_list[current_node]) {
            if (!visited[neighbor]) {
                que.push(neighbor);
                visited[neighbor] = 1;
                distances[neighbor] = distances[current_node] + 1;
            }
        }
    }

    free(visited);
}

void Graph::DFS(int vertex, int *visited) {

    visited[vertex] = 1;

    for (auto neighbor : adjacency_list[vertex])
        if (!visited[neighbor])
            DFS(neighbor, visited);
}

vector<int> Graph::BFSMD(int starting_vertex){

    int *visited = (int *) calloc(vertices + 1, sizeof(int));
    queue<int> que;
    que.push(starting_vertex);

    vector<int> distances(vertices+1,0);
    distances[starting_vertex] = 0;
    visited[starting_vertex] = 1;

    while (!que.empty()) {
        int current_node = que.front();
        que.pop();

        for (auto neighbor : adjacency_list[current_node]) {
            if (!visited[neighbor]) {
                que.push(neighbor);
                visited[neighbor] = 1;
                distances[neighbor] = distances[current_node] + 1;
            }
        }
    }

    free(visited);

    return distances;
}

//Used Tarjan Algorithm for biconnected components, strongly connected components, and bridges (critical connections) implementation
//The following implementations are similar, because you need to keep track of the some things that are happening during the dfs

void Graph::BCC(int vertex, vector<int> &parent, stack<int> &vertices_stack, vector<int> &discovery_time,
                vector<int> &lowest_reachable, int &timer) {

    // consider lowest reachable value as being a better path from a node to another
    // for example if we want to reach a certain point and we have 2 neighbors with different discovery time we will chose
    // the one with the less value because we want to reach faster that certain point

    // increment the discovery time of the vertex you are visiting
    // this is the only information you posses at the moment
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;
    vertices_stack.push(vertex);

    for (int neighbor : adjacency_list[vertex]) {

        if (neighbor != parent[vertex]) {

            //now for each neighbor you are checking in adjacency list you are pushing on stack the vertex you are currently visiting
            //assuming it is an articulation point

            //if the neighbor you are checking has not been visited yet you will visit him next via DFS
            if (parent[neighbor] == -1) {

                parent[neighbor] = vertex; //set the parent of neighbor to be te current node
                BCC(neighbor, parent, vertices_stack, discovery_time, lowest_reachable, timer); //DFS

                cout<<vertices_stack.top()<<' ';

                //After you reach a point when DFS cant visit unvisited nodes you get back and update the values of your vertex lowest_reachable point
                //with the values of the neighbor you currently visited and set it to the min value between both of them
                lowest_reachable[vertex] = min(lowest_reachable[neighbor],
                                               lowest_reachable[vertex]);
                //You do this operation until you are in a vertex which has its discovery time less than or equal to the lowest reachable
                //value of the neighbor you currently visited


                //if you manage to find such a vertex, that means it is an articulation point, and all the vertices
                //you pushed into the stack by now are part of a biconnected component

                if (discovery_time[vertex] <= lowest_reachable[neighbor]) {
                    list<int> component;
                    vector<bool> pushed(vertices + 1, false);
                    component.push_back(vertex);
                    pushed[vertex] = true;
                    int temp = vertices_stack.top();

                    while (temp != vertex) {
                        if (!pushed[temp]) {
                            component.push_back(temp);
                            pushed[temp] = true;
                        }
                        vertices_stack.pop();
                        temp = vertices_stack.top();
                    }
                    biconnected_components.push_back(component);
                }
            }

                //if the neighbor you are visiting has been actually visited, we need to check if it's discovery time is less then our lowest reachable value
                //if so, that means you have a path to that node that is better than the path you are on right now, so when you
                //get back by recursion it will tell the other vertices that he found a better path and will set all other vertices' lowest_reachable value to the minimal one
                //so it will form a biconnected component
            else {
                lowest_reachable[vertex] = min(discovery_time[neighbor],
                                               lowest_reachable[vertex]);
            }
        }
    }
}


void Graph::SCC(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable, stack<int> &vertices_stack,
                vector<bool> &on_stack, int &timer) {

    //set the discovery time and lowest_reachable value at the time you discover this node
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;

    //save your node intro the stack assuming it could be an articulation point
    vertices_stack.push(vertex);
    on_stack[vertex] = true;

    for (auto neighbor : adjacency_list[vertex]) {

        //for every neighbor if it has't been visited recursively do dfs and update the lowest_reachable vertex;
        if (discovery_time[neighbor] == -1) {
            SCC(neighbor, discovery_time, lowest_reachable, vertices_stack, on_stack, timer);
            lowest_reachable[vertex] = min(lowest_reachable[vertex], lowest_reachable[neighbor]);
        }

            //if the vertex is already on the stack, just update the lowest_reachable value
        else if (on_stack[neighbor]) {
            lowest_reachable[vertex] = min(lowest_reachable[vertex], discovery_time[neighbor]);
        }
    }

    //A strongly connected component will have all its vertices' lowest_reachable values equal

    if (lowest_reachable[vertex] == discovery_time[vertex]) {
        vector<int> component;

        int temp;
        do {
            temp = vertices_stack.top();
            vertices_stack.pop();
            on_stack[temp] = false;
            component.push_back(temp);
        } while (temp != vertex);

        strongly_connected_components.push_back(component);
    }
}


//similar to articulation points for an edge to be a bridge the condition is that the vertex X should have
//the lowest_reachable value greater than his parent's discovery time
// ( NO PATH TO X or one of its ancestors )
//Explanations similar to the previous algorithms.
void Graph::CCN(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable,vector<bool>& visited,vector<int>& parent, int &timer) {

    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;
    visited[vertex] = true;

    for(int neighbor : adjacency_list[vertex]){
        if(!visited[neighbor]){
            parent[neighbor] = vertex;
            CCN(neighbor,discovery_time,lowest_reachable,visited,parent,timer);
            lowest_reachable[vertex] = min(lowest_reachable[vertex],lowest_reachable[neighbor]);

            if(discovery_time[vertex] < lowest_reachable[neighbor])
                bridges.push_back({vertex,neighbor});
        }
        else if(parent[vertex] != neighbor){
            lowest_reachable[vertex] = min(lowest_reachable[vertex],discovery_time[vertex]);
        }
    }
}

void Graph::TOPOLOGICAL_SORT(int vertex, vector<bool> &visited) {
    visited[vertex] = true;
    for (int neighbor : adjacency_list[vertex]) {
        if (!visited[neighbor])
            TOPOLOGICAL_SORT(neighbor, visited);
    }
    topological.push_back(vertex);
}

#pragma endregion


//infoarena solutions
#pragma region Solutions

//Minimal distances BFS problem
void Graph::solve_distances(int starting_vertex) {
    int *distances = (int *) calloc(vertices + 1, sizeof(int));

    BFS(starting_vertex, distances);

    for (int i = 1; i < vertices + 1; i++)
        fout << distances[i] - 1 << ' ';

    free(distances);
}

//Connected compontents DFS problem
void Graph::solve_connected_components() {

    int counter = 0;
    int *visited = (int *) calloc(vertices + 1, sizeof(int));

    for (int i = 1; i < vertices + 1; i++)
        if (!visited[i]) {
            DFS(i, visited);
            counter++;
        }

    fout << counter;
    free(visited);
}



void Graph::solve_biconnected() {

    //initialize the stuff you will work with
    stack<int> vertices_stack;
    vector<int> parent(vertices + 1, -1);
    vector<int> discovery_time(vertices + 1, -1);
    vector<int> lowest_reachable(vertices + 1, -1);

    //global timer for discovery time and lowest reachable value
    int timer = 0;

    parent[1] = 1;
    BCC(1, parent, vertices_stack, discovery_time, lowest_reachable, timer);

    list<int>::iterator it;
    fout << biconnected_components.size() << '\n';
    for (auto components : biconnected_components) {
        for (it = components.begin(); it != components.end(); it++)
            fout << *it << ' ';
        fout << '\n';
    }
}

void Graph::solve_strongly_connected() {

    vector<int> discovery_time(vertices + 1, -1);
    vector<int> lowest_reachable(vertices + 1, -1);
    vector<bool> on_stack(vertices + 1, false);
    stack<int> vertices_stack;

    int timer = 0;

    for (int i = 1; i < vertices + 1; i++) {
        if (discovery_time[i] == -1)
            SCC(i, discovery_time, lowest_reachable, vertices_stack, on_stack, timer);
    }

    fout << strongly_connected_components.size() << '\n';

    for (auto component : strongly_connected_components) {
        for (int i : component)
            fout << i << ' ';
        fout << '\n';
    }
}

void Graph::solve_topological() {

    vector<bool> visited(vertices + 1, false);

    for (int i = 1; i < vertices + 1; i++) {
        if (!visited[i])
            TOPOLOGICAL_SORT(i, visited);
    }

    for (int i = topological.size() - 1; i >= 0; i--) {
        fout << topological[i] << ' ';
    }
}

void Graph::solve_critical_connections(){

    vector<bool> visited(vertices+1,false);
    vector<int> discovery_time(vertices + 1, -1);
    vector<int> lowest_reachable(vertices + 1, -1);
    vector<int> parent(vertices + 1,-1);
    int timer = 0;

    parent[1] = 1;
    for(int i = 1;i<=vertices+1;i++){
        if(!visited[i])
            CCN(i,discovery_time,lowest_reachable,visited,parent,timer);
    }

    for(auto br : bridges){
        cout<<br.first<<"--"<<br.second;
        cout<<'\n';
    }
}


void Graph::solve_starting_ending_distance(int starting_vertex, int ending_vertex){

    vector<int> start_min_dist = BFSMD(starting_vertex);
    vector<int> end_min_dist = BFSMD(ending_vertex);
    vector<int> frequency(vertices+1,0);

    int min_dist = start_min_dist[ending_vertex];


    for(int i = 1;i<=vertices;i++){
        if(start_min_dist[i] + end_min_dist[i] == min_dist)
            frequency[start_min_dist[i]]++;
    }

    vector<int> min_dist_vertices;

    for(int i = 0;i<=vertices;i++){
        if(frequency[start_min_dist[i]] == 1 && start_min_dist[i] + end_min_dist[i] == min_dist)
            min_dist_vertices.push_back(i);
    }

    fout<<min_dist_vertices.size()<<'\n';

    for(auto i : min_dist_vertices){
        fout<<i<<' ';
    }
}



//Havel Hakimi - given a vector of vertices' degree
//say if there is a graph which coresponds to the given data
bool solve_havel_hakimi(vector<int> degrees){

    sort(degrees.begin(),degrees.end(),greater<int>());

    while(!degrees.empty()){

        printv(degrees);
        int current = degrees[0];
        if(current > degrees.size())
            return false;
        else if (current == 0)
            return true;
        for(int i = 0;i<=current;i++)
            if(degrees[i] - 1 < 0)
                return false;
            else
                degrees[i]--;
        degrees.erase(degrees.begin());
        sort(degrees.begin(),degrees.end(),greater<int>());
    }

    return true;
}
#pragma endregion
