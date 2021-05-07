import geopandas
import networkx as nx 
from matplotlib import pyplot as plt

def create_graph(streams_data, streams_dic):
    # create graph
    G = nx.Graph()
    # create edges, nodes
    for idx,r in streams_data.iterrows():
        stream_length = r.SHAPE_LENG # length of stream
        stream_id = r.TOK_ID # id of stream
        stream_name = r.NAZ_TOK
        #print(stream_length, stream_id)
        #print(",".join(map(str,r.geometry.coords)))
        coords = r.geometry.coords    
        mempoint = coords[0]

        set_basin = False
        if stream_id in streams_dic: # add start point of Labe, Morava, Odra to dictionary 
            #print(streams_dic[stream_id], type(streams_dic[stream_id]))
            set_basin = True
            if len(streams_dic[stream_id]) == 1:
                streams_dic[stream_id].append(mempoint)
                G.add_node(mempoint)
                G.nodes[mempoint]['basin'] = streams_dic[stream_id][0]

        for point in coords[1:]:
            G.add_edge(mempoint,point)
            G.edges[mempoint,point]['index'] = idx
            G.edges[mempoint,point]['stream_len'] = stream_length
            G.edges[mempoint,point]['stream_id'] = stream_id

            if set_basin == True:
                G.edges[mempoint,point]['basin'] = streams_dic[stream_id][0] # set basin level for Labe, Morava, Odrava
            else:
                G.edges[mempoint,point]['basin'] = -1 # set basin level for other streams
            mempoint = point
            G.nodes[mempoint]['basin'] = "inf"
        set_basin = False
    return G

def BFS_basin(graph_river, dic_stream): 
    river_dictionary = {}  
    for i in dic_stream:
        afrom_previous = dic_stream[i][1]
        ato_previous = dic_stream[i][1]
        for afrom, ato in nx.bfs_edges(graph_river,dic_stream[i][1]): # stream[i][1] is start point of Labe, Odra, Morava...
            print(f"{afrom} -> {ato}", graph_river.nodes[afrom]["basin"])
            river_dictionary[graph_river.edges[afrom,ato]["stream_id"]] = 1
            
            """if streams_graph.nodes[afrom] == streams_graph.nodes[ato_previous]:
                streams_graph.nodes[afrom]['basin'] = streams_graph.nodes[ato_previous]['basin']+1"""

            """if streams_graph.nodes[afrom]['basin'] != "inf":
                streams_graph.nodes[ato]['basin'] = streams_graph.nodes[afrom]['basin'] + 1"""
            afrom_previous = afrom
            ato_previous = ato
            """if streams_graph.edges[(afrom,ato)]['basin'] != -1:
                streams_graph.nodes[ato]['basin'] = streams_graph.edges[(afrom,ato)]['basin']
                streams_graph.nodes[afrom]['basin'] = streams_graph.edges[(afrom,ato)]['basin']"""
            #streams_graph[edge]['basin'] = 
            """if streams_graph[edge]['basin'] != -1:
                pass
            else:
                streams_graph[edge]['basin'] = streams_graph.nodes[edge]['basin'] + 1"""
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
label_edge = True
label_edge_atribute = 'basin' # display basin level on edges
label_node = True
label_node_atribute = "basin"
stream_list = {123.0:[1], 333.0:[1]} # 123 je Labe ktery ma rad toku 1, 333 je odra s radek toku 1
####################################################################################

streams_graph = create_graph(data, stream_list)
dictionary_streams = BFS_basin(streams_graph, stream_list) # set basin level
print(dictionary_streams) # dictionary with streams ID and basin level

################## ----> zde najoinovat povodi k puvodnim datum a data ulozit :D
# přidej atribut RAD_TOKU

# vypiš součet délek toků v daném řádu pro každý řád, který se v datech vyskytuje 

# vypiš součet délek toků, které jsou nedosažitelné ze vstupních povodí 

# print graph info
print(nx.info(streams_graph))
# draw graph
pos = {n:n for n in streams_graph.nodes}

if label_node== True:
    labels_node = {}
    for v in streams_graph.nodes:
        if "basin" in streams_graph.nodes[v]:
            labels_node[v] = streams_graph.nodes[v]['basin']
        else:
            labels_node[v] = 'inf'

nx.draw(streams_graph, with_labels=True, pos=pos,labels=labels_node, node_size = 10)
if label_edge == True:
    edge_labels = nx.get_edge_attributes(streams_graph,label_edge_atribute) # edge_labels dictionary
    nx.draw_networkx_edge_labels(streams_graph,pos,edge_labels=edge_labels,font_color='red')


plt.show()
# BONUS
# Mimo povodí Labe, Odry a Moravy uvažujte ještě alespoň 10 dalších toků, které z ČR odtékají, aniž by byly na území ČR součástí nějakého z výše uvedených povodí. Tyto toky přidejte do vstupního souboru spolu s jejich řádem
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR a z území ČR vytékají (tedy se nevlévají do jiného nedosažitelného toku. Jako poznávací znamení berte, že takový tok na žádném konci nenavazuje na jiný tok
