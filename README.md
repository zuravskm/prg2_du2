# Řády vodních toků
## Uživatelská dokumentace
Aplikace umožňuje uživateli spočítat řády jednotlivých toků a součet délek toků pro každý řád. Vstupem jsou zdrojová data vodních toků ve formátu .shp, které je ožné stáhnout např. z dat DIBAVOD, a soubor geojson, ve kterém jsou uvedeny řády toků, od kterých se v aplikaci další toky odvozují. Výstupem je soubor ve formátu geojson, který obsahuje všechny prvky se všemi atributy jako ve vstupním souboru a navíc přidaný atribut RAD_TOKU obsahující informaci o řádu daného toku.

Aplikace také vypíše na výstup součet délek toků v daném řádu pro každý řád, který se v datech vyskytuje a součet délek toků, které jsou nedosažitelné ze vstupních povodí.

## Vývojářská dokumentace
### Vstupy
Jako testová data byla použita datová sada A02 z databáze DIBAVOD...


### Přiřazování řádu toků


