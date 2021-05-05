import geopandas
import networkx as nx 
from matplotlib import pyplot as plt

# soubor se vstupními daty
data = geopandas.read_file('du2/A02_Vodni_tok_JU_selection.shp')
# soubor, ve kterém jsou uvedeny řády toků, od kterých se budou další toky odvozovat
vzor = geopandas.read_file("du2/zakl_toky.geojson")

# vytvoř graf
G = nx.Graph()

# vytvoř hrany, resp. nody
for idx,r in data.iterrows():
    coords = r.geometry.coords    
    mempoint = r.geometry.coords[0]
    for point in r.geometry.coords[1:]:
        G.add_edge(mempoint,point)
        G.edges[mempoint,point]['index'] = idx
        mempoint = point

# přidej atribut RAD_TOKU


# vypiš součet délek toků v daném řádu pro každý řád, který se v datech vyskytuje 


# vypiš součet délek toků, které jsou nedosažitelné ze vstupních povodí 







# vypiš info o grafu
print(nx.info(G))
# vykresli graf
pos = {n:n for n in G.nodes}
nx.draw(G, pos=pos, node_size = 1)
plt.show()

# BONUS
# Mimo povodí Labe, Odry a Moravy uvažujte ještě alespoň 10 dalších toků, které z ČR odtékají, aniž by byly na území ČR součástí nějakého z výše uvedených povodí. Tyto toky přidejte do vstupního souboru spolu s jejich řádem
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR
# Vypište jména všech pojmenovaných toků, jimž nebyl určen řád, protože jsou z daných vstupních povodí nedosažitelné na území ČR a z území ČR vytékají (tedy se nevlévají do jiného nedosažitelného toku. Jako poznávací znamení berte, že takový tok na žádném konci nenavazuje na jiný tok
