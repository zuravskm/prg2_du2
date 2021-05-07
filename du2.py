import geopandas
import networkx as nx 
from matplotlib import pyplot as plt

def create_graph(streams):
    # create graph
    G = nx.Graph()
    # create edges, nodes
    for idx,r in streams.iterrows():
        stream_length = r.SHAPE_LENG # length of stream
        stream_id = r.TOK_ID # id of stream
        print(stream_length, stream_id)
        #print(",".join(map(str,r.geometry.coords)))

        coords = r.geometry.coords    
        mempoint = r.geometry.coords[0]
        for point in r.geometry.coords[1:]:
            G.add_edge(mempoint,point)
            G.edges[mempoint,point]['index'] = idx
            G.edges[mempoint,point]['stream_len'] = stream_length
            G.edges[mempoint,point]['stream_id'] = stream_id
            mempoint = point
    return G

#################################################################################
# input data and input definition file
data = geopandas.read_file('data/dibavod_test.shp')
input_file = geopandas.read_file("zakl_toky.geojson")
label_edge = True
####################################################################################

streams_graph = create_graph(data)

# přidej atribut RAD_TOKU

# vypiš součet délek toků v daném řádu pro každý řád, který se v datech vyskytuje 

# vypiš součet délek toků, které jsou nedosažitelné ze vstupních povodí 

# print graph info
print(nx.info(streams_graph))
# draw graph
pos = {n:n for n in streams_graph.nodes}
nx.draw(streams_graph, with_labels=False, pos=pos, node_size = 10)
if label_edge == True:
    edge_labels = nx.get_edge_attributes(streams_graph,'stream_id') # edge_labels dictionary
    edge_labels = {(lb[0],lb[1]):edge_labels[lb] for lb in edge_labels}
    nx.draw_networkx_edge_labels(streams_graph,pos,edge_labels=edge_labels,font_color='red')
plt.show()
# BONUS
# Mimo povodí Labe, Odry a Moravy uvažujte ještě alespoň 10 dalších toků, které z ČR odtékají, aniž by byly na území ČR součástí nějakého z výše uvedených povodí. Tyto toky přidejte do vstupního souboru spolu s jejich řádem
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR a z území ČR vytékají (tedy se nevlévají do jiného nedosažitelného toku. Jako poznávací znamení berte, že takový tok na žádném konci nenavazuje na jiný tok
