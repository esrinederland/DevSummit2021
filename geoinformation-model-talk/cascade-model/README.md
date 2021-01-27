# GeoInformation: Cascade model

> Terminology: Symbology = Styling = Symbology = Renderer

**Like in CSS, map properties** in the ArcGIS GeoInformation model **can be defined in multple places**: in the Feature Service, in the Feature Layer item, in the Web Map item and/or in the Web Mapping Application itself.

And also like in CSS, **depending on where the properties are defined, they will be overwritten or not**.

A particularity of the GeoInformation model is that **these properties not only apply to rendering/styling**, but also to other properties as we will see below. Another difference is that **not all properties can be specified at all levels**.

## Properties and priorities

Let's see a table showing some properties that can be stored in the geoinformation model. 

In case the priority is defined in multiple levels, the first row indicates the priority (predominance / weight), Shows which property prevails, in other words, which has higher priority. From lower (feature service = 1) to highest priotity (custom apps = 4):

> **Warning**: the following table is not intended to be a complete list of properties used by the GeoInformation model but to serve as an example to understand how the cascade model works.

|Properties / Spec.|Description|[Feature Service](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer)|[Feature Layer Item type](https://www.arcgis.com/home/item.html?id=195e039565ee42fbbefbcc2708bc7e26#visualize)|[Web Map item type](https://geogeeks.maps.arcgis.com/home/webmap/viewer.html?webmap=2ba230842b164b53acaa05df211c36de)|Custom apps<sup>1</sup>
|---|---|---|---|--|--|
|Priority||1|2|3|4|
|[`drawingInfo`](https://developers.arcgis.com/web-map-specification/objects/drawingInfo/)|Simbology|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26?f=json)|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de?f=json)|Y
|[`extent`](https://developers.arcgis.com/web-map-specification/objects/extent/)|Map extension|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26?f=json)|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de?f=json)|Y
|[`labelingInfo`](https://developers.arcgis.com/web-map-specification/objects/labelingInfo/)|Geometry labels|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26/data?f=json)|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y
|[`minScale`](https://developers.arcgis.com/web-map-specification/objects/layer/) and [`maxScale`](https://developers.arcgis.com/web-map-specification/objects/layer/)|Visibility range|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|N|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y|Y
|[`defaultVisibility`](https://developers.arcgis.com/web-map-specification/objects/layer/) or [`visibility`](https://developers.arcgis.com/web-map-specification/objects/featureLayer/)|True / false|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|N|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y
|`viewLayerDefinition`|View layers filter|Y<sup>2</sup>|N|N|**N**|
|[`layerDefinition`](https://developers.arcgis.com/web-map-specification/objects/layerDefinition/)|Filters|N|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26/data?f=json)|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y
|[`popupInfo`](https://developers.arcgis.com/web-map-specification/objects/popupInfo/)|Popup templates|N|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26/data?f=json)|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y
|[`featureReduction`](https://developers.arcgis.com/web-map-specification/objects/featureReduction_cluster/)|Clusters|N|N|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/8e3fd5a7427b48b3b293c586ff4b2301/data?f=json)|Y
|[`baseMap`](https://developers.arcgis.com/web-map-specification/objects/baseMap/)|Background layers|N|N|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y
|[`opacity`](https://developers.arcgis.com/web-map-specification/objects/featureLayer/)|Transparency|N|N|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y
|[`bookmarks`](https://developers.arcgis.com/web-map-specification/objects/bookmark/)|Map locations|N|N|[Y](https://geogeeks.maps.arcgis.com/sharing/rest/content/items/2ba230842b164b53acaa05df211c36de/data?f=json)|Y
|...|...|...|...|...|...

> (1) **Custom apps**:  [client side API/SDK](#), which includes [Web Mapping Applications type](#) and Configurable Apps.
> (2) **View layer definitions** can only be queried by the owner using the [REST API Admin](https://developers.arcgis.com/rest/services-reference/rest-api-admin.htm). I couldn't find this property in the documentation.


## Demo

### Default properties in the Feature Layer

