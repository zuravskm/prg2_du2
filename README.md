# Řády vodních toků
## Uživatelská dokumentace
Aplikace umožňuje uživateli spočítat řády jednotlivých toků a součet délek toků pro každý řád. Vstupem jsou zdrojová data vodních toků ve formátu SHP, které je ožné stáhnout např. z dat DIBAVOD, a soubor GeoJSON, ve kterém jsou uvedeny řády toků, od kterých se v aplikaci další toky odvozují. Výstupem je soubor ve formátu GeoJSON, který obsahuje všechny prvky se všemi atributy jako ve vstupním souboru, a navíc přidaný atribut RAD_TOKU obsahující informaci o řádu daného toku.

Aplikace také vypíše do terminálu součet délek toků v daném řádu pro každý řád, který se v datech vyskytuje, a součet délek toků, které jsou nedosažitelné ze vstupních povodí.

Mimo povodí Labe, Odry a Moravy, je v aplikaci uvažováno dalších 10 vodních toků, které z ČR odtékají, aniž by byly na území ČR součástí nějakého ze třech výše uvedených povodí.

Jména toků, které jsou nedosažitelné z uvažovaných povodí (nebyl jim určen řád), jsou vypsána do terminálu. 

## Vývojářská dokumentace
### Vstupy
Jako testová data byla použita datová sada A02 z databáze DIBAVOD ve formátu SHP. Druhým vstupem je soubor ve formátu GeoJSON, ve kterém jsou definovány IDs a řády toků vybraných 13 řek vytékajících z ČR.

### Přístup k datům
Vstupní data jsou převedena do struktury grafu s využitím knihovny NetworkX ve funkci create_graph. Graf je vytvořen z hran, které reprezentují jednotlivé toky. Koncové nody hran jsou zeměpisné souřadnice vstupních dat. Výstupem této funkce je vlastní graf a slovník, jehož klíčem jsou ID vodních toků a hodnotou je řád toku nastavený na hodnotu -1.

Řády toků jsou načteny ze vstupního GeoJSONu pomocí funkce load_streams. Výstupem funkce je slovník 13 vstupních vodních toků, kde klíčem jsou ID vodních toků a hodnotou je jejich řád.

### Přiřazování řádu toků
Vytvořený graf je procházen pomocí algoritmu BFS (tzn. procházení grafu do šířky). ...

### Přiřazení atributu RAD_TOKU a výstup dat
Přiřazení atributu RAD_TOKU a výstup dat a výstup dat provádí funkce save_data, jejíž parametry jsou vstupní data, cesta k výstupnímu souboru, slovník vodních toků (dict_basin), které mají přiřazený řád, a slovník všech vodních toků s nastaveným řádem -1. 

Slovník dict_basin je rozšířen o nedosažitelné toky, které mají řád -1 a nejsou součástí původního slovníku dict_basin. Výsledný slovník je zapsán do výstupního souboru ve formátu GeoJSON. 

### Výpočet délky toku dle řádu
Nejprve je vytvořen seznam všech řádů, které se ve vstupních datech vyskytují. Pomocí tohoto seznamu jsou procházena výstupní data a pro každý řád je sčítána délka toků. Délka nedosažitelných toků (toky s řádem -1) je počítána v samostatném cyklu na rozdíl od délky toků s přiřazeným řádem. Výsledné součty délek toků podle řádů a součet délky nedosažitelných toků jsou vypsány do terminálu. 

### Výpis názvů nedosažitelných toků






