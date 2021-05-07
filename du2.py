import geopandas
import networkx as nx 
from matplotlib import pyplot as plt

def create_graph(streams_data, streams_dic):
    # create graph
    G = nx.Graph()
    # create edges, nodes
    for idx,r in streams_data.iterrows():
        stream_id = r.TOK_ID # id of stream
        coords = r.geometry.coords    
        mempoint = coords[0]

        if stream_id in streams_dic and len(streams_dic[stream_id]) == 1: # add start point of Labe, Morava, Odra to dictionary 
                streams_dic[stream_id].append(mempoint)

        for point in coords[1:]:
            G.add_edge(mempoint,point)
            G.edges[mempoint,point]['stream_id'] = stream_id
            mempoint = point
    return G

def BFS_basin(graph_river, dic_stream): 
    river_dictionary = {}
    for i in dic_stream:
        first_point = dic_stream[i][1]
        graph_river.nodes[first_point]["stream_id"] = i
        graph_river.nodes[first_point]["basin"] = dic_stream[i][0]
        for afrom, ato in nx.bfs_edges(graph_river,dic_stream[i][1]): # stream[i][1] is start point of Labe, Odra, Morava...
            #print(f"{afrom} -> {ato}", graph_river.nodes[afrom]["basin"])
            graph_river.nodes[ato]["stream_id"] = streams_graph.edges[afrom,ato]["stream_id"]
            if graph_river.nodes[afrom]["stream_id"] == graph_river.nodes[ato]["stream_id"]:
                graph_river.nodes[ato]["basin"] = graph_river.nodes[afrom]["basin"]

            else:
                graph_river.nodes[ato]["basin"] = graph_river.nodes[afrom]["basin"] + 1
 
            basin_level = max(graph_river.nodes[afrom]["basin"],graph_river.nodes[ato]["basin"])
            graph_river.edges[afrom,ato]["basin"] = basin_level
            river_dictionary[graph_river.edges[afrom,ato]["stream_id"]] = basin_level
    return river_dictionary

def load_streams(data_path):
    streams = geopandas.read_file(data_path)
    streams_dict = {}
    for idx,r in streams.iterrows():
        stream_id = r.TOK_ID
        stream_rad = r.RAD_TOKU

        streams_dict[stream_id] = [stream_rad] 
    return streams_dict
    
#################################################################################
# input data and input definition file
data = geopandas.read_file('data/dibavod_test.shp')
input_file = geopandas.read_file("zakl_toky.geojson")
stream_list = {123.0:[1], 333.0:[1]} # 123 je Labe ktery ma rad toku 1, 333 je odra s radek toku 1
# IMPORTANT: not suitable for large datasets!
label_edge = True
label_edge_atribute = 'basin' # display basin level on edges
label_node = True
label_node_atribute = "basin"

####################################################################################

streams_graph = create_graph(data, stream_list)
dictionary_streams = BFS_basin(streams_graph, stream_list) # set basin level
print(dictionary_streams) # dictionary with streams ID and basin level

################## ----> zde najoinovat povodi k puvodnim datum a data ulozit :D ve slovniku dictionary_streams jsou ulozeny ID toku a k nim vzdy rad toku
# přidej atribut RAD_TOKU

# vypiš součet délek toků v daném řádu pro každý řád, který se v datech vyskytuje 

# vypiš součet délek toků, které jsou nedosažitelné ze vstupních povodí 

# print graph info
print(nx.info(streams_graph))
# draw graph
pos = {n:n for n in streams_graph.nodes}
labels_node = {}
if label_node== True:
    for v in streams_graph.nodes:
        if label_node_atribute in streams_graph.nodes[v]:
            labels_node[v] = streams_graph.nodes[v][label_node_atribute]
        else:
            labels_node[v] = 'inf'

nx.draw(streams_graph, with_labels=label_node, pos=pos,labels=labels_node, node_size = 5, font_color='green',font_size=25)
if label_edge == True:
    edge_labels = nx.get_edge_attributes(streams_graph,label_edge_atribute) # edge_labels dictionary
    nx.draw_networkx_edge_labels(streams_graph,pos,edge_labels=edge_labels,font_color='red')

plt.show()
# BONUS
# Mimo povodí Labe, Odry a Moravy uvažujte ještě alespoň 10 dalších toků, které z ČR odtékají, aniž by byly na území ČR součástí nějakého z výše uvedených povodí. Tyto toky přidejte do vstupního souboru spolu s jejich řádem
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR a z území ČR vytékají (tedy se nevlévají do jiného nedosažitelného toku. Jako poznávací znamení berte, že takový tok na žádném konci nenavazuje na jiný tok
