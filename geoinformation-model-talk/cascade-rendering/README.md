# GeoInformation: Cascade model

> Terminology: Symbology = Styling = Symbology = Renderer

Like in CSS, map properties in the ArcGIS GeoInformation model can be defined in multple places: in the Feature Service, in the Feature Layer item, in the Web Map item and/or in the Web Mapping Application itself.

And also like in CSS, depending on where the styles are defined, they will be overwritten or not.

A particularity of the GeoInformation model is that these values not only apply to rendering, but also to other properties as we will see below. Another difference is that not all properties can be specified at all levels.

## Properties and priorities

Let's see a table showing from less priority (predominance / weigh) to max. priority how it applies:

|Prio.|Level|Rendering properties|Other properties|Examples|
|---|---|---|---|---|
|1|[Feature Service](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer)|**Per layer**:  `drawingInfo` (symbology), `minScale` & `maxScale` (visibility range), `extent`, `defaultVisibility`, `templates`, `geometryType`, ...|`hasViews`, `serviceItemId`, supported operations, ... |[Feature layer properties](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)
|2|[Feature Layer Item type](https://www.arcgis.com/home/item.html?id=195e039565ee42fbbefbcc2708bc7e26#visualize)| `drawingInfo`, `defaultVisibility`, `popupInfo` (popups), `labelingInfo` (labels), `definitionExpression` (filters).<br> `layerDefinition` on Layer Views. It also have it owns definition expressions.|n.a.|[Feature Layer Item Data](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26/data?f=json)
|3|[Web Map item type](https://geogeeks.maps.arcgis.com/home/webmap/viewer.html?webmap=2ba230842b164b53acaa05df211c36de)|Symbology, popups, labels, definition expression, basemap, extent, layers visibility range, transparency, filters, bookmarks, clustering ...|n.a.|[Item data](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json) (`drawingInfo`, `popupInfo`, `labelingInfo`, `definitionExpression`, `baseMapLayers`, `opacity`, `bookmarks`, `minScale`, `maxScale`, ... )
|4|[Web Mapping Applications item type](#) and [Client side API/SDK](#)|n.a.|Anything|Anything|

## Demo

### Default properties in the Feature Layer

