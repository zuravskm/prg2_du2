import geopandas
import pandas as pd
import networkx as nx 
from matplotlib import pyplot as plt


def create_graph(streams_data, streams_dict):
    """creates graph where edges are water streams and nodes are defined by geographical coordinates"""
    """returns created graph and dictionary ID_dict of TOK_ID as keys and '-1' as values"""
    ID_dict = {}
    # explode multipart featurest singlepart features
    streams_data = geopandas.GeoDataFrame.explode(streams_data)
    # create graph
    G = nx.Graph()
    # create edges, nodes
    for idx,r in streams_data.iterrows():
        stream_id = r.TOK_ID
        coords = r.geometry.coords
        mempoint = coords[0]
        # add start point of Labe, Morava, Odra to dictionary
        if stream_id in streams_dict and len(streams_dict[stream_id]) == 1:
            streams_dict[stream_id].append(mempoint)
        for point in coords[1:]:
            G.add_edge(mempoint, point)
            G.edges[mempoint, point]['stream_id'] = stream_id
            mempoint = point
        ID_dict[stream_id] = -1
    return G, ID_dict

def BFS_basin(graph_river, dic_stream): 
    river_dictionary = {}
    for i in dic_stream:
        first_point = dic_stream[i][1]
        graph_river.nodes[first_point]["stream_id"] = i
        graph_river.nodes[first_point]["basin"] = dic_stream[i][0]
        for afrom, ato in nx.bfs_edges(graph_river,dic_stream[i][1]): # stream[i][1] is start point of Labe, Odra, Morava...
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
    """loads data form input definition file"""
    """returns dictionary of TOK_ID as keys and RAD_TOKU as values"""
    streams = geopandas.read_file(data_path)
    streams_dict = {}
    for idx,r in streams.iterrows():
        stream_id = r.TOK_ID
        stream_rank = r.RAD_TOKU
        streams_dict[stream_id] = [stream_rank] 
    return streams_dict

def save_data(input_data, output_path, dict_basin, all_IDs):  
    """assigns an attribute RAD_TOKU to output data and saves them to the output file"""
    for id in all_IDs:
        if id not in dict_basin:
            dict_basin[id] = all_IDs[id]
    TOK_ID = list(dict_basin.keys())
    RAD_TOKU = list(dict_basin.values())
    dataframe = {"TOK_ID": TOK_ID,"RAD_TOKU": RAD_TOKU}
    df = pd.DataFrame(dataframe)
    # joining RAD_TOKU to input data
    output_data = input_data.merge(df, on = 'TOK_ID')
    output_data.to_file(output_path, driver = 'ESRI Shapefile', encoding = 'utf-8') # , driver='GeoJSON')

def count_length(data_path):
    """counts the sum of length of each rank that exists in output data and the sum of length of reachless streams"""
    streams = geopandas.read_file(data_path)
    stream_rank_list = []
    reachable_streams = {}
    reachless_streams = {}
    # create list of all ranks that exists in output data
    for idx,r in streams.iterrows():
        stream_rank = r.RAD_TOKU
        stream_length = r.SHAPE_LENG
        # list of all flow rank numbers
        if stream_rank in stream_rank_list:
            pass
        else:
            stream_rank_list.append(stream_rank)
    stream_rank_list = sorted(stream_rank_list)
    
    # counts flow length
    for rank in stream_rank_list:
        # reachable streams
        if rank != -1:
            final_length = 0
            for idx,r in streams.iterrows():
                stream_rank = r.RAD_TOKU
                stream_length = r.SHAPE_LENG
                if rank == stream_rank:
                    final_length = final_length + stream_length
                    reachable_streams[stream_rank] = final_length 
                else:
                    pass  
        # reachless streams
        else:
            final_length = 0
            for idx,r in streams.iterrows():
                stream_rank = r.RAD_TOKU
                stream_length = r.SHAPE_LENG
                if rank == stream_rank:
                    final_length = final_length + stream_length
                    reachless_streams[stream_rank] = final_length 
                else:
                    pass
    
    # print the lenghts of reachable and reachless streams
    for key, value in reachable_streams.items():
        print('Délka toků {k}. řádu je {v} metrů'.format(k=key,v=round(value)))
    for key, value in reachless_streams.items():
        print('Délka nedosažitelných toků je {v} metrů'.format(v=round(value)))


def print_reachless_stream_names(output_path):
    """prints all names of reachless streams"""
    stream_names = []
    streams = geopandas.read_file(output_path)
    for idx,r in streams.iterrows():
        stream_name = r.NAZ_TOK
        stream_rank = r.RAD_TOKU
        if stream_rank == -1 and stream_name != None and stream_name not in stream_names:
            stream_names.append(stream_name)
    print(stream_names)


# input data
data = geopandas.read_file('data/A03_Vodni_tok_HU.shp', driver = 'ESRI Shapefile', encoding = 'utf-8')
# input definition file
stream_list = load_streams("zakl_toky.geojson")
# output file
out_path = "data/output.shp"

# create graph
streams_graph, list_ID = create_graph(data, stream_list)
# set basin level
dictionary_streams = BFS_basin(streams_graph, stream_list)
# flow ranks assignment and data saving
save_data(data,out_path,dictionary_streams, list_ID)
# print the sum of length of individual ranks and of reachless streams
count_length(out_path)
# print all names od reachless streams
print_reachless_stream_names(out_path)

# draw graph
"""IMPORTANT: drawing is not suitable for large datasets (whole DIBAVOD data)!"""
draw_plot = False
label_edge = True
label_edge_atribute = 'basin' # display basin level on edges
label_node = True
label_node_atribute = "basin"

if draw_plot == True:
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
