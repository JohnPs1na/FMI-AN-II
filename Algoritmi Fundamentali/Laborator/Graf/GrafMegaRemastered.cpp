#include <iostream>
#include <algorithm>
#include <stack>
#include <vector>
#include <queue>
#include <fstream>
#include <list>
#include <climits>
#include <unordered_set>
 
#define INF INT_MAX/2
 
 
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
//APM (Kruskall) https://www.infoarena.ro/job_detail/2799355?action=view-source
//Dijkstra https://www.infoarena.ro/job_detail/2799949?action=view-source
//Bellman-Ford https://www.infoarena.ro/job_detail/2800728?action=view-source
 
using namespace std;
 
ifstream fin("maxflow.in");
ofstream fout("maxflow.out");
 
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
 


    //private functions
    //homework 1;
    void BFS(int starting_vertex,vector<int>& distances);
 
    void DFS(int vertex, vector<int>& visited);
 
    void BCC(int vertex, vector<int>& parent,stack<int>& vertices_stack,vector<int>& discovery_time, vector<int>& lowest_reachable,vector<unordered_set<int>>& biconnected_components,int& timer); 
 
    void SCCTJ(int vertex, stack<int>& vertices_stack, vector<int>& discovery_time, vector<int>& lowest_reachable, vector<bool>& has_component,vector<vector<int>>& strongly_connected_components,int& timer);
 
    void SCCKJ(int vertex,vector<bool>& visited, vector<int>& component);
 
    void CCN(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable,vector<bool>& visited,vector<int>& parent,vector<pair<int,int>>& bridges, int &timer);
 
    void TOPOLOGICAL_SORT(int vertex, vector<int>& visited,vector<int>& topological);
 
    vector<int> BFSMD(int starting_vertex);
 
 
    //homework 2;
 
    void KRUSKAL(vector<int>& parent, vector<int>& dimension,int& total_cost, vector<Edge>& mst);
 
    void DIJKSTRA(int vertex, vector<int>& dist, priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>>& heap);
 
    void BELLMANFORD(int vertex, vector<int>& dist, queue<int>& que);
 
    //homework 3;
    
    void ROYFLOYD(vector<vector<int>>& matrix_of_weights);
 
    bool MAXFLOW(int source, int destination, vector<vector<int>>& capacity, vector<vector<int>>& flow, vector<int>& parent);
 
public:
 
    Graph(int vertices = 0,int edges = 0,bool oriented = false,bool weighted = false);
 
    Graph transpose();
 
    void add_edge(int v1,int v2,int c = 0);
 
    void infoarena_graph();
 
    void show_my_graph();
 
    //homework 1
    vector<int> solve_distances(int starting_vertex);
 
    int solve_connected_components();
 
    vector<unordered_set<int>> solve_biconnected();
 
    vector<vector<int>> solve_strongly_connected_tarjan();
    vector<vector<int>> solve_strongly_connected_kosaraju();
 
    vector<int> solve_topological();
 
    vector<pair<int,int>> solve_critical_connections();
 
    vector<int> solve_starting_ending_distance(int starting_vertex,int ending_vertex);
 
    //homework 2;
    int find(int v,vector<int>& parent);
 
    bool unite(int v1,int v2,vector<int>& parent, vector<int>& dimension);
 
    void update(int v1,int v2, int cost, vector<int>& dist);
 
    pair<vector<Edge>,int> solve_apm();
 
    vector<int> solve_dijkstra();
 
    vector<int> solve_bellman_ford();
 
    //homework 3;
    int solve_tree_diameter();
 
    vector<vector<int>> solve_roy_floyd(vector<vector<int>>& matrix_of_weights);
 
    int solve_max_flow(vector<vector<int>>& capacity);
};
 
 
 
template <class T>
void printv(vector<T> xs){
    for(T i : xs) cout<<i<<' ';
    cout<<'\n';
}
 
int main()
{

}
 
 
 
#pragma region Utility
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
 
void Graph::add_edge(int v1,int v2,int c)
{
    adjacency_list[v1].push_back(Edge(v1,v2,c));
    edges++;
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
void Graph::BFS(int starting_vertex,vector<int>& distances)
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
 
void Graph::BCC(int vertex, vector<int>& parent,stack<int>& vertices_stack,vector<int>& discovery_time, vector<int>& lowest_reachable,vector<unordered_set<int>>& biconnected_components,int& timer)
{
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;
 
    for(auto& path : adjacency_list[vertex])
    {
        vertices_stack.push(vertex);
 
        if(parent[path.destination] == -1){
            parent[path.destination] = vertex;
            
            //will DFS till it reaches a leaf in dfs tree pushing nodes into the stack
            BCC(path.destination,parent,vertices_stack,discovery_time,lowest_reachable,biconnected_components,timer);
 
            //will recurr till it meet an articulation point 
            //updating lowest reachable value to the min of all its neighbors
            lowest_reachable[vertex] = min(lowest_reachable[vertex],lowest_reachable[path.destination]);
 
            //articulation point is found when its discovery time is less than or equal to the lowest_reachable value of the neighbor
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
 
        //the leaf will check all cross edges of the dfs tree and update lowest_reachable to the first discovered
        else{
            lowest_reachable[vertex] = min(lowest_reachable[vertex],discovery_time[path.destination]);
        }
    }
}
 
 
void Graph::SCCTJ(int vertex,stack<int>& vertices_stack, vector<int>& discovery_time,vector<int>& lowest_reachable, vector<bool>& has_component,vector<vector<int>>& strongly_connected_components, int& timer)
{
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;
 
    vertices_stack.push(vertex);
 
    for(auto path : adjacency_list[vertex])
    {
        if(discovery_time[path.destination]==-1)
        {
            //will DFS till it reaches a leaf
            SCCTJ(path.destination,vertices_stack,discovery_time,lowest_reachable,has_component,strongly_connected_components,timer);
 
            //continue updating values of lowest reachable ancestor till we found an articulation point
            lowest_reachable[vertex] = min(lowest_reachable[vertex],lowest_reachable[path.destination]);
        }
        //if the leaf is not a part(because we need a max component) of a connected component, update value of its lowest reachable ancestor
        else if (!has_component[path.destination])
            lowest_reachable[vertex] = min(lowest_reachable[vertex],discovery_time[path.destination]);
    }
    
    // oriented !!
    // neither descendants nor vertex itself has no cross edges to vertex ancestors, means it is an articulation point
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
 
 
void Graph::CCN(int vertex, vector<int> &discovery_time, vector<int> &lowest_reachable,vector<bool>& visited,vector<int>& parent,vector<pair<int,int>>& bridges, int &timer)
{
    discovery_time[vertex] = lowest_reachable[vertex] = ++timer;
    visited[vertex] = true;
    
    for(auto path : adjacency_list[vertex])
    {
        if(!visited[path.destination])
        {
            parent[path.destination] = vertex;
            CCN(path.destination,discovery_time,lowest_reachable,visited,parent,bridges,timer);
            lowest_reachable[vertex] = min(lowest_reachable[vertex],lowest_reachable[path.destination]);
 
            if(discovery_time[vertex] < lowest_reachable[path.destination])
                bridges.push_back({vertex,path.destination});
        }
        else if(parent[vertex] != path.destination)
            lowest_reachable[vertex] = min(lowest_reachable[vertex],discovery_time[path.destination]);
    }
}
 
//topological sort (helps solving scc based on kosaraju algorithm)
void Graph::TOPOLOGICAL_SORT(int vertex, vector<int>& visited,vector<int>& topological){
    visited[vertex] = 1;
    for(auto path : adjacency_list[vertex])
        if(!visited[path.destination])
            TOPOLOGICAL_SORT(path.destination,visited,topological);
    topological.push_back(vertex);
}
 
#pragma endregion 
 
#pragma region Homework1_solutions
vector<int> Graph::solve_distances(int starting_vertex) 
{
    vector<int> distances;
    BFS(starting_vertex,distances);
    return distances;
}
 
 
int Graph::solve_connected_components()
{
    vector<int> visited(vertices+1,0);
    int cnt = 0;
    for(int i = 1;i<=vertices;i++)
        if(!visited[i])
            DFS(i,visited),cnt++;
    return cnt;
}
 
vector<unordered_set<int>> Graph::solve_biconnected(){
    	
    stack<int> vertices_stack;
    vector<int> parent(vertices+1,-1);
    vector<int> discovery_time(vertices+1,0);
    vector<int> lowest_reachable(vertices+1,0);
    vector<unordered_set<int>> biconnected_components;
    int timer = 0;
 
    BCC(1,parent,vertices_stack,discovery_time,lowest_reachable,biconnected_components,timer);
 
    return biconnected_components;
}
 
vector<vector<int>> Graph::solve_strongly_connected_tarjan()
{
    stack<int> vertices_stack;
    vector<int> discovery_time(vertices+1,-1);
    vector<int> lowest_reachable(vertices+1,-1);
    vector<bool> has_component(vertices+1,false);
    vector<vector<int>> strongly_connected_components;
    int timer = 0;
 
    for(int i = 1;i<vertices+1;i++)
        if(discovery_time[i] == -1)
            SCCTJ(i,vertices_stack,discovery_time,lowest_reachable,has_component,strongly_connected_components,timer);
    
    return strongly_connected_components;
}   
 
vector<vector<int>> Graph::solve_strongly_connected_kosaraju()
{
    vector<bool> visited(vertices+1,false);
    vector<vector<int>> strongly_connected_components;

    vector<int> topological = solve_topological();
  
    Graph gt = transpose();
 
    //will iterate through topologically sorted vector and will do dfs from all unvisited vertices
    //all the dfs will form strongly conected components
    for(int i = topological.size()-1;i>=0;i--)
    {
        if(!visited[topological[i]])
        {
            vector<int> component;
            gt.SCCKJ(topological[i],visited,component);
            strongly_connected_components.push_back(component);
        }
    }
 
    return strongly_connected_components;
}
 
vector<int> Graph::solve_topological()
{
    vector<int> visited(vertices+1,0);
    vector<int> topological;
    for(int i = 1;i<=vertices;i++)
        if(!visited[i])
            TOPOLOGICAL_SORT(i,visited,topological);
    
    return topological;
}

vector<pair<int,int>> Graph::solve_critical_connections(){
 
    vector<bool> visited(vertices+1,false);
    vector<int> discovery_time(vertices + 1, -1);
    vector<int> lowest_reachable(vertices + 1, -1);
    vector<int> parent(vertices + 1,-1);
    vector<pair<int,int>> bridges;
    int timer = 0;
 
    parent[1] = 1;
    for(int i = 1;i<=vertices+1;i++){
        if(!visited[i])
            CCN(i,discovery_time,lowest_reachable,visited,parent,bridges,timer);
    }
 
    return bridges;
}

vector<int> Graph::solve_starting_ending_distance(int starting_vertex, int ending_vertex){
 
    vector<int> start_min_dist = solve_distances(starting_vertex);
    vector<int> end_min_dist = solve_distances(ending_vertex);
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
 
    return min_dist_vertices;
}



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
 
 
//homework 2;
#pragma region Homework2
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
 
 
void Graph::KRUSKAL(vector<int>& parent, vector<int>& dimension,int& total_cost,vector<Edge>& mst)
{
    //sort edges by cost 
    sort(edges_list.begin(),edges_list.end(),[](Edge e1,Edge e2){ return e1.cost < e2.cost;});
 
    //select each optimal edge
    for(auto e : edges_list)
        if(unite(e.source,e.destination,parent,dimension))
        {
            total_cost+=e.cost;
            mst.push_back(e);
        }
    
}
 
 
void Graph::DIJKSTRA(int vertex, vector<int>& dist, priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>>& heap)
{
    dist[vertex] = 0;
    heap.push({0,vertex});
    vector<int> vis(vertices+1,0);
 
    //basically a BFS
    //we always select to add a edge from a vertex with minimal distance
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
 
    vector<int> check_count(vertices+1,0); //will check if a node has been checked n times
                                           //if so quit 
 
    while(!que.empty())
    {
        int node = que.front();
        que.pop();
        check_count[node] += 1; 
 
        if(check_count[node] > vertices){
            return; 
        }
 
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
#pragma endregion
 
#pragma region Homework2_solve
 
pair<vector<Edge>, int> Graph::solve_apm()
{
    vector<int> parent(vertices+1);
    vector<int> dimension(vertices+1,1);
    vector<Edge> mst;
 
    for(int i = 1;i<vertices+1;i++)
        parent[i] = i;
    
    int total_cost = 0;
 
    KRUSKAL(parent,dimension,total_cost,mst);
 
    return make_pair(mst,total_cost);
}
 
vector<int> Graph::solve_dijkstra()
{
    vector<int> dist(vertices+1,-1);
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> heap;
 
    DIJKSTRA(1,dist,heap);
 
    return dist;
}
 
vector<int> Graph::solve_bellman_ford()
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
                cout<<"Ciclu negativ!";
                vector<int> fs(1,0);
                return fs;
            }
    }
    
    return dist;
}
#pragma endregion
 
//homework 3;
int Graph::solve_tree_diameter()
{
    vector<int> distances1;
    BFS(1,distances1);
 
 
    pair<int,int> id_val = {0,distances1[0]};
 
    for(int i = 0;i<distances1.size();i++)
        if(id_val.second < distances1[i])
            id_val = {i,distances1[i]};
        
    vector<int> distances2;
    BFS(id_val.first,distances2);
 
 
    for(int i = 0;i<distances2.size();i++)
        if(id_val.second < distances2[i])
            id_val = {i,distances2[i]};
 
    return id_val.second;
}
 
void Graph::ROYFLOYD(vector<vector<int>>& matrix_of_weights)
{
 
    for(int k = 1;k<=vertices;k++)
        for(int i = 1;i<=vertices;i++)
            for(int j = 1;j<=vertices;j++)
                matrix_of_weights[i][j] = min(matrix_of_weights[i][j],matrix_of_weights[i][k]+matrix_of_weights[k][j]);
    
}
 
bool Graph::MAXFLOW(int source, int destination,vector<vector<int>>& capacity,vector<vector<int>>& flow, vector<int>& parent)
{
 
    vector<bool> visited(vertices+1,false);
    queue<int> que;
    que.push(source);
    parent[source]=-1;
 
    while(!que.empty())
    {
        int node = que.front();
        que.pop();
        visited[node] = true;
 
        if (node!=destination)
        {
            for(auto path : adjacency_list[node])
            {
                
                if(capacity[node][path.destination] == flow[node][path.destination])
                    continue;
                if(visited[path.destination])
                    continue;
                
                parent[path.destination] = node;
                que.push(path.destination);
            }
        }
    }
    return visited[destination];
}
 
vector<vector<int>> Graph::solve_roy_floyd(vector<vector<int>>& matrix_of_weights)
{
    ROYFLOYD(matrix_of_weights);
    return matrix_of_weights;
}
 
int Graph::solve_max_flow(vector<vector<int>>& capacity)
{
    vector<vector<int>> flow(vertices+1,vector<int>(vertices+1,0));
    vector<int> parent(vertices+1,0);
 
 
    int source = 1;
    int destination = vertices;
    int max_flow = 0;
 
    while(MAXFLOW(source,destination,capacity,flow,parent))
    {
        for(auto& path : adjacency_list[destination])
        {
            int node = path.destination;
            
            if(flow[node][destination] == capacity[node][destination]) continue;
 
            parent[destination] = node;
 
            int minflow = INF;
            for(int vert = destination; vert!=source; vert = parent[vert])
                minflow = min(minflow,capacity[parent[vert]][vert] - flow[parent[vert]][vert]);
            
            if(minflow == 0) continue;
 
            for(int vert = destination;vert!=source;vert = parent[vert])
            {
                flow[parent[vert]][vert] += minflow;
                flow[vert][parent[vert]] -= minflow;
            }
            max_flow += minflow;
        }
    }
    return max_flow;
}
