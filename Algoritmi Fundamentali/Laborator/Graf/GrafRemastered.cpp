#include <iostream>
#include <algorithm>
#include <stack>
#include <vector>
#include <queue>
#include <fstream>
#include <list>
#include <climits>
#include <unordered_set>


//Probleme
//BFS https://www.infoarena.ro/job_detail/2788173?action=view-source
//DFS https://www.infoarena.ro/job_detail/2788178?action=view-source
//Biconex https://www.infoarena.ro/job_detail/2788743?action=view-source
//CTC https://www.infoarena.ro/job_detail/2795579?action=view-source
//sortaret https://www.infoarena.ro/job_detail/2789749?action=view-source
//RJ https://www.infoarena.ro/job_detail/2791322?action=view-source
//Graf https://www.infoarena.ro/job_detail/2791468?action=view-source
//Critical connections in a network https://leetcode.com/submissions/detail/578227255/
//Disjoint https://www.infoarena.ro/job_detail/2799580?action=view-source
//APM (Kruskal) https://www.infoarena.ro/job_detail/2799355?action=view-source
//Dijkstra https://www.infoarena.ro/job_detail/2799949?action=view-source
//Bellman-Ford https://www.infoarena.ro/job_detail/2800728?action=view-source

using namespace std;
 
ifstream fin("biconex.in");
ofstream fout("biconex.out");
 
struct Edge
{
    int source;
    int destination;
    int cost;
 
    Edge(int source = 0,int destination = 0,int cost = 0):
            source(source),
            destination(destination),
            cost(cost) { }
    
    friend ostream& operator<<(ostream& out, const Edge& e);
};

struct compareCost{
    bool operator()(Edge& e1, Edge& e2){ return e1.cost > e2.cost; }
};

ostream& operator<<(ostream& out, const Edge& e)
{
    out<<e.source<<' '<<e.destination<<' '<<e.cost<<'\n';
    return out;
}


class Graph{
 
private:
 
    //private variables
    int vertices, edges;
    bool oriented, weighted;
    vector<vector<Edge>> adjacency_list;
    vector<Edge> edges_list;
 
    //To compute:
    vector<int> distances;
    vector<unordered_set<int>> biconnected_components;
    vector<vector<int>> strongly_connected_components;
    vector<int> topological;
    vector<pair<int,int>> bridges;
    vector<Edge> APM;
 

    //private functions
 
    //homework 1;
    void BFS(int starting_vertex);
 
    void DFS(int vertex, vector<int>& visited);
 
    void BCC(int vertex, vector<int>& parent,stack<int>& vertices_stack,vector<int>& discovery_time, vector<int>& lowest_reachable,int& timer); 
 
    void SCCTJ(int vertex, stack<int>& vertices_stack, vector<int>& discovery_time, vector<int>& lowest_reachable, vector<bool>& has_component,int& timer);
 
    void SCCKJ(int vertex,vector<bool>& visited, vector<int>& component);

    void CCN(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable,vector<bool>& visited,vector<int>& parent, int &timer);
 
    void TOPOLOGICAL_SORT(int vertex, vector<int>& visited);
 
    vector<int> BFSMD(int starting_vertex);

    //homework 2;

    void KRUSKAL(vector<int>& parent, vector<int>& dimension,int& total_cost);

    void DIJKSTRA(int vertex, vector<int>& dist, priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>>& heap);

    void BELLMANFORD(int vertex, vector<int>& dist, queue<int>& que);

public:

    Graph(int vertices = 0,int edges = 0,bool oriented = false,bool weighted = false);
 
    Graph transpose();

    vector<int> get_topological(){return topological;}

    void infoarena_graph();
 
    void show_my_graph();
 
    void solve_distances(int starting_vertex);
 
    void solve_connected_components();
 
    void solve_biconnected();

    void solve_strongly_connected_tarjan();
    void solve_strongly_connected_kosaraju();
 
    void solve_topological();
 
    void solve_critical_connections();
 
    void solve_starting_ending_distance(int starting_vertex,int ending_vertex);

    //homework 2;
    int find(int v,vector<int>& parent);

    bool unite(int v1,int v2,vector<int>& parent, vector<int>& dimension);

    void update(int v1,int v2, int cost, vector<int>& dist);

    void solve_apm();

    void solve_dijkstra();

    void solve_bellman_ford();
};



template <class T>
void printv(vector<T> xs){
    for(T i : xs) cout<<i<<' ';
    cout<<'\n';
}
 
int main()
{

	
	return 0;
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
 
        Edge e(x,y,c);
        
        adjacency_list[x].push_back(e);
        edges_list.push_back(e);
 
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

void Graph::BCC(int vertex, vector<int>& parent,stack<int>& vertices_stack,vector<int>& discovery_time, vector<int>& lowest_reachable,int& timer)
{
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;

    for(auto path : adjacency_list[vertex])
    {
        vertices_stack.push(vertex);

        if(parent[path.destination] == -1){
            parent[path.destination] = vertex;
            BCC(path.destination,parent,vertices_stack,discovery_time,lowest_reachable,timer);

            lowest_reachable[vertex] = min(lowest_reachable[vertex],lowest_reachable[path.destination]);

            if(discovery_time[vertex] <= lowest_reachable[path.destination])
            {
                int aux;
                biconnected_components.push_back(unordered_set<int>());
                int n = biconnected_components.size();
                aux = vertices_stack.top();
                while(aux!=vertex)
                {
                    if(biconnected_components[n-1].find(aux) == biconnected_components[n-1].end()){
                        biconnected_components[n-1].insert(aux);
                    }
                    aux = vertices_stack.top();
                    vertices_stack.pop();
                }
                biconnected_components[n-1].insert(aux);
            }
        }
        else{
            lowest_reachable[vertex] = min(lowest_reachable[vertex],discovery_time[path.destination]);
        }
    }
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

#pragma region Homework1_solutions
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
 
void Graph::solve_biconnected(){
    	
    stack<int> vertices_stack;
    vector<int> parent(vertices+1,-1);
    vector<int> discovery_time(vertices+1,0);
    vector<int> lowest_reachable(vertices+1,0);

    int timer = 0;

    BCC(1,parent,vertices_stack,discovery_time,lowest_reachable,timer);

    fout<<biconnected_components.size()<<'\n';
    for(auto components : biconnected_components){
        for(auto i : components){
            fout<<i<<' ';
        }
        fout<<'\n';
    }

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
    int v1_parent = find(v1,parent);
    int v2_parent = find(v2,parent);

    if(v1_parent == v2_parent) return false;

    if(dimension[v1_parent] <= dimension[v2_parent])
    {
        parent[v1_parent] = v2_parent;
        dimension[v2_parent] += dimension[v1_parent];
    }
    else
    {
        parent[v2_parent] = v1_parent;
        dimension[v1_parent] += dimension[v2_parent];
    }
    return true;
}

void Graph::KRUSKAL(vector<int>& parent, vector<int>& dimension,int& total_cost)
{

    sort(edges_list.begin(),edges_list.end(),[](Edge e1,Edge e2){ return e1.cost < e2.cost;});

    for(auto e : edges_list)
        if(unite(e.source,e.destination,parent,dimension))
        {
            total_cost+=e.cost;
            APM.push_back(e);
        }
    
}

void Graph::DIJKSTRA(int vertex, vector<int>& dist, priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>>& heap)
{
    dist[vertex] = 0;
    heap.push({0,vertex});
    vector<int> vis(vertices+1,0);

    while(!heap.empty())
    {
        int node = heap.top().second;
        heap.pop();

        if(!vis[node])
            for(auto path : adjacency_list[node])
            {
                if(!vis[path.destination])
                    if(dist[path.destination] == -1 || dist[path.destination] > path.cost + dist[node]){
                        dist[path.destination] = path.cost + dist[node];
                        heap.push({dist[path.destination],path.destination});
                    }
            }
        vis[node] = 1;
    }
}


void Graph::BELLMANFORD(int vertex,vector<int>& dist,queue<int>& que)
{
    que.push(vertex);
    dist[vertex] = 0;

    vector<int> cont(vertices+1,0);

    while(!que.empty())
    {
        int node = que.front();
        que.pop();
        cont[node] += 1;
        if(cont[node] > vertices) return;

        for(auto path : adjacency_list[node])
        {
            int v2 = path.destination;
            int cost = path.cost;
            if(dist[v2] > dist[node] + cost)
            {
                dist[v2] = dist[node] + cost;
                que.push(v2);
            }
        }

    }
}

void Graph::solve_apm()
{
    vector<int> parent(vertices+1);
    vector<int> dimension(vertices+1,1);

    for(int i = 1;i<vertices+1;i++)
        parent[i] = i;
    
    int total_cost = 0;

    KRUSKAL(parent,dimension,total_cost);

    fout<<total_cost<<'\n';
    fout<<APM.size()<<'\n';
    for(auto e : APM)
        fout<<e.source<<' '<<e.destination<<'\n';
}

void Graph::solve_dijkstra()
{
    vector<int> dist(vertices+1,-1);
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> heap;

    DIJKSTRA(1,dist,heap);

    for(int i = 2;i<vertices+1;i++)
    {
        if(dist[i] == -1)
            fout<<0<<' ';
        else fout<<dist[i]<<' ';
    }
}

void Graph::solve_bellman_ford()
{
    vector<int> dist(vertices+1,INT_MAX);
    queue<int> que;

    BELLMANFORD(1,dist,que);

    for(int i = 0;i<edges;i++)
    {
        int v1 = edges_list[i].source;
        int v2 = edges_list[i].destination;
        int cost = edges_list[i].cost;
        if(dist[v1] != INT_MAX && dist[v1] + cost < dist[v2])
            {
                fout<<"Ciclu negativ!";
                return;
            }
    }
    for(int i = 2;i<vertices+1;i++)
        fout<<dist[i]<<' ';
}
