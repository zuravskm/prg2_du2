# Řády vodních toků
## Uživatelská dokumentace
Aplikace umožňuje uživateli spočítat řády jednotlivých toků a součet délek toků pro každý řád. Vstupem jsou zdrojová data vodních toků ve formátu SHP, které je ožné stáhnout např. z dat DIBAVOD, a soubor GeoJSON, ve kterém jsou uvedeny řády toků, od kterých se v aplikaci další toky odvozují. Výstupem je soubor ve formátu GeoJSON, který obsahuje všechny prvky se všemi atributy jako ve vstupním souboru, a navíc přidaný atribut RAD_TOKU obsahující informaci o řádu daného toku.

Aplikace také vypíše do terminálu součet délek toků v daném řádu pro každý řád, který se v datech vyskytuje, a součet délek toků, které jsou nedosažitelné ze vstupních povodí.

Mimo povodí Labe, Odry a Moravy, je v aplikaci uvažováno dalších 10 vodních toků, které z ČR odtékají, aniž by byly na území ČR součástí nějakého ze třech výše uvedených povodí.

Jména toků, které jsou nedosažitelné z uvažovaných povodí (nebyl jim určen řád), jsou vypsána do terminálu. 

## Vývojářská dokumentace
### Vstupy
Jako testová data byla použita datová sada A02 z databáze DIBAVOD...


### Přiřazování řádu toků


