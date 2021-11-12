#include <iostream>
#include <algorithm>
#include <stack>
#include <vector>
#include <queue>
#include <fstream>
#include <list>

//DE REZOLVAT BICONEX!
//DE REZOLVAT BICONEX!
//DE REZOLVAT BICONEX!
//DE REZOLVAT BICONEX!
//DE REZOLVAT BICONEX!
//DE REZOLVAT BICONEX!
//DE REZOLVAT BICONEX!

using namespace std;
 
ifstream fin("ctc.in");
ofstream fout("ctc.out");
 
struct Edge
{
    int source;
    int destination;
    int cost;
 
    Edge(int source = 0,int destination = 0,int cost = 0):
            source(source),
            destination(destination),
            cost(cost) { }
};
 
 
class Graph{
 
private:
 
    //private variables
    int vertices, edges;
    bool oriented, weighted;
    vector<vector<Edge>> adjacency_list;
 
    //To compute:
    vector<int> distances;
    vector<list<int>> biconnected_components;
    vector<vector<int>> strongly_connected_components;
    vector<int> topological;
    vector<pair<int,int>> bridges;
 

    //private functions
 
    //homework 1;
    void BFS(int starting_vertex);
 
    void DFS(int vertex, vector<int>& visited);
 
    void BCCTJ(); //Tarjan Algorithm
 
    void BCCKJ(); //Kosaraju Algorithm
 
    void SCCTJ(int vertex, stack<int>& vertices_stack, vector<int>& discovery_time, vector<int>& lowest_reachable, vector<bool>& has_component,int& timer);
 
    void SCCKJ(int vertex,vector<bool>& visited, vector<int>& component);

    void CCN(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable,vector<bool>& visited,vector<int>& parent, int &timer);
 
    void TOPOLOGICAL_SORT(int vertex, vector<int>& visited);
 
    vector<int> BFSMD(int starting_vertex);

    //homework 2;

    void KRUSKAL();

public:

    Graph(int vertices = 0,int edges = 0,bool oriented = false,bool weighted = false);
 
    Graph transpose();

    vector<int> get_topological(){return topological;}

    void infoarena_graph();
 
    void show_my_graph();
 
    void solve_distances(int starting_vertex);
 
    void solve_connected_components();
 
    void solve_biconnected_tarjan();
    void solve_biconnected_kosaraju();

    void solve_strongly_connected_tarjan();
    void solve_strongly_connected_kosaraju();
 
    void solve_topological();
 
    void solve_critical_connections();
 
    void solve_starting_ending_distance(int starting_vertex,int ending_vertex);

    //homework 2;
    int find(int v,vector<int>& parent);

    bool unite(int v1,int v2,vector<int>& parent, vector<int>& dimension);

    void solve_apm();
};
 
void printv(vector<int> xs){
    for(int i : xs) cout<<i<<' ';
    cout<<'\n';
}
 
int main()
{
    int n, m;
    fin>>n>>m;
    Graph g(n,m,true);
    g.infoarena_graph();
    g.solve_strongly_connected_kosaraju();

}

#pragma region utilities
Graph::Graph(int vertices, int edges, bool oriented, bool weighted) :
        vertices(vertices),
        edges(edges),
        oriented(oriented),
        weighted(weighted)
{
    adjacency_list.resize(vertices + 1);
}

Graph Graph::transpose()
{
    Graph gt(vertices,edges,oriented,weighted);
    for(int i = 1;i<vertices+1;i++)
        for(auto path : adjacency_list[i])
            gt.adjacency_list[path.destination].push_back(Edge(path.destination,i,path.cost));
    return gt;
}
 
void Graph::infoarena_graph() {
    int x,y;
    int c = 0;
    for(int i = 1;i<=edges;i++)
    {
        fin>>x>>y;
 
        if(weighted)
            fin>>c;
 
        adjacency_list[x].push_back(Edge(x,y,c));
 
        if(!oriented)
            adjacency_list[y].push_back(Edge(y,x,c));
    }
}
 
void Graph::show_my_graph() {
    for(int i = 1;i<=vertices;i++){
        cout<<i<<"=>";
        for(auto path : adjacency_list[i])
            cout<<path.destination<<' ';
        cout<<'\n';
    }
}
#pragma endregion

//homework 1;
#pragma region Homework1_private
void Graph::BFS(int starting_vertex)
{
 
    distances.resize(vertices+1,-1);
    queue<int> que;
    que.push(starting_vertex);
    distances[starting_vertex] = 0;
    while(!que.empty()){
        int vert = que.front();
        que.pop();
        for(auto path : adjacency_list[vert])
            if(distances[path.destination] == -1){
                que.push(path.destination);
                distances[path.destination] = distances[vert] + 1;
            }
    }
}
 
void Graph::DFS(int vertex, vector<int>& visited)
{
    visited[vertex] = 1;
    for(auto path : adjacency_list[vertex])
        if(!visited[path.destination])
            DFS(path.destination,visited);
}

void Graph::SCCTJ(int vertex,stack<int>& vertices_stack, vector<int>& discovery_time,vector<int>& lowest_reachable, vector<bool>& has_component, int& timer)
{
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;

    vertices_stack.push(vertex);

    for(auto path : adjacency_list[vertex])
    {
        if(discovery_time[path.destination]==-1)
        {
            SCCTJ(path.destination,vertices_stack,discovery_time,lowest_reachable,has_component,timer);
            lowest_reachable[vertex] = min(lowest_reachable[vertex],lowest_reachable[path.destination]);
        }

        else if (!has_component[path.destination])
            lowest_reachable[vertex] = min(lowest_reachable[vertex],discovery_time[path.destination]);
    }
    
    if(lowest_reachable[vertex] == discovery_time[vertex])
    {
        vector<int> component;

        int temp;
        do{
            temp = vertices_stack.top();
            vertices_stack.pop();
            has_component[temp] = true;
            component.push_back(temp);
        }while(temp!=vertex);

        strongly_connected_components.push_back(component);
    }
}

//Kosaraju util strongly_connected;
void Graph::SCCKJ(int vertex,vector<bool>& visited, vector<int>& component)
{
    visited[vertex] = true;
    component.push_back(vertex);

    for(auto path : adjacency_list[vertex])
        if(!visited[path.destination])
            SCCKJ(path.destination,visited,component);
}


void Graph::CCN(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable,vector<bool>& visited,vector<int>& parent, int &timer)
{
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;
    visited[vertex] = true;
    
    for(auto path : adjacency_list[vertex])
    {
        if(!visited[path.destination])
        {
            parent[path.destination] = vertex;
            CCN(path.destination,discovery_time,lowest_reachable,visited,parent,timer);
            lowest_reachable[vertex] = min(lowest_reachable[vertex],lowest_reachable[path.destination]);

            if(discovery_time[vertex] < lowest_reachable[path.destination])
                bridges.push_back({vertex,path.destination});
        }
        else if(parent[vertex] != path.destination)
            lowest_reachable[vertex] = min(lowest_reachable[vertex],discovery_time[path.destination]);
    }
}

//topological sort (helps solving scc based on kosaraju algorithm)
void Graph::TOPOLOGICAL_SORT(int vertex, vector<int>& visited){
    visited[vertex] = 1;
    for(auto path : adjacency_list[vertex])
        if(!visited[path.destination])
            TOPOLOGICAL_SORT(path.destination,visited);
    topological.push_back(vertex);
}
#pragma endregion 

#pragma region Homework2_solutions
void Graph::solve_distances(int starting_vertex) 
{
    BFS(starting_vertex);
    for(int i = 1;i<vertices+1;i++)
        fout<<distances[i]<<' ';
}
 
 
void Graph::solve_connected_components()
{
    vector<int> visited(vertices+1,0);
    int cnt = 0;
    for(int i = 1;i<=vertices;i++)
        if(!visited[i])
            DFS(i,visited),cnt++;
    fout<<cnt;
}
 
void Graph::solve_strongly_connected_tarjan()
{
    stack<int> vertices_stack;
    vector<int> discovery_time(vertices+1,-1);
    vector<int> lowest_reachable(vertices+1,-1);
    vector<bool> has_component(vertices+1,false);

    int timer = 0;

    for(int i = 1;i<vertices+1;i++)
        if(discovery_time[i] == -1)
            SCCTJ(i,vertices_stack,discovery_time,lowest_reachable,has_component,timer);
    
    fout<<strongly_connected_components.size()<<'\n';

    for(auto component : strongly_connected_components){
        for(auto i : component) fout<<i<<' ';
        fout<<'\n';
    }
}   

void Graph::solve_strongly_connected_kosaraju()
{
    vector<bool> visited(vertices+1,false);

    solve_topological();

    Graph gt = transpose();

    for(int i = topological.size()-1;i>=0;i--)
    {
        if(!visited[topological[i]])
        {
            vector<int> component;
            gt.SCCKJ(topological[i],visited,component);
            strongly_connected_components.push_back(component);
        }
    }

    fout<<strongly_connected_components.size()<<'\n';

    for(auto component : strongly_connected_components)
    {
        for(auto i : component)
            fout<<i<<' ';
        fout<<'\n';
    }
}

void Graph::solve_topological()
{
    vector<int> visited(vertices+1,0);
 
    for(int i = 1;i<=vertices;i++)
        if(!visited[i])
            TOPOLOGICAL_SORT(i,visited);
}
#pragma endregion


//homework 2;
int Graph::find(int v,vector<int>& parent)
{
    while(v!=parent[v])
        v = parent[v];
    return v;
}

bool Graph::unite(int v1, int v2,vector<int>& parent, vector<int>& dimension)
{

}
void Graph::KRUSKAL()
{

}

void Graph::solve_apm()
{

}
