# GeoInformation: Cascade model

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents** 

- [Introduction](#introduction)
- [Properties and priorities](#properties-and-priorities)
- [Examples using the ArcGIS JavaScript API](#examples-using-the-arcgis-javascript-api)
  - [Load a layer with it default properties](#load-a-layer-with-it-default-properties)
  - [Overwrite previous layer properties with Portal Item properties](#overwrite-previous-layer-properties-with-portal-item-properties)
  - [Overwrite previous Portal Item with web map properties](#overwrite-previous-portal-item-with-web-map-properties)
  - [Overwrite previous web map properties with custom code](#overwrite-previous-web-map-properties-with-custom-code)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

> Terminology: Symbology = Styling = Symbology = Renderer

## Introduction

**Like in CSS, map properties** in the ArcGIS GeoInformation model **can be defined in multple places**: in the Feature Service, in the Feature Layer item, in the Web Map item and/or in the Web Mapping Application itself.

And also like in CSS, **depending on where the properties are defined, they will be overwritten or not**.

Particularities of the GeoInformation model:

* Not all properties are directly related to styling (e.g. `bookmarks`)
* Not all properties can be specified at all levels

## Properties and priorities

Let's see a table showing some properties that can be stored in the geoinformation model. 

In case the priority is defined in multiple levels, the first row indicates the priority (predominance / weight), Shows which property prevails, in other words, which has higher priority. From lower (feature service = 1) to highest priotity (custom apps = 4):

> **Warning**: the following table is not intended to be a complete list of properties used by the GeoInformation model but to serve as an example to understand how the cascade model works.

|Properties / Spec.|Description|[Feature Service](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer)|[Feature Layer Item type](https://www.arcgis.com/home/item.html?id=195e039565ee42fbbefbcc2708bc7e26#visualize)<sup>1</sup>|[Web Map item type](https://www.arcgis.com/home/webmap/viewer.html?webmap=c1354b360f3d4d709220f134f10b744a)|Custom apps<sup>2</sup>
|---|---|---|---|--|--|
|Priority||1|2|3|4|
|[`drawingInfo`](https://developers.arcgis.com/web-map-specification/objects/drawingInfo/)|Simbology|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|[`extent`](https://developers.arcgis.com/web-map-specification/objects/extent/)|Map extension|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)<sup>3</sup>|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26?f=json)<sup>4</sup>|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a?f=json)|Y
|[`labelingInfo`](https://developers.arcgis.com/web-map-specification/objects/labelingInfo/)|Geometry labels|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26/data?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|[`minScale`](https://developers.arcgis.com/web-map-specification/objects/layer/) and [`maxScale`](https://developers.arcgis.com/web-map-specification/objects/layer/)|Visibility range|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|N|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y|Y
|[`defaultVisibility`](https://developers.arcgis.com/web-map-specification/objects/layer/) or [`visibility`](https://developers.arcgis.com/web-map-specification/objects/featureLayer/)|True / false|[Y](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json)|N|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|`viewLayerDefinition`|View layers filter|Y<sup>5</sup>|N|N|**N**|
|[`layerDefinition`](https://developers.arcgis.com/web-map-specification/objects/layerDefinition/)|Filters|N|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26/data?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|[`popupInfo`](https://developers.arcgis.com/web-map-specification/objects/popupInfo/)|Popup templates|N|[Y](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26/data?f=json)|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|[`featureReduction`](https://developers.arcgis.com/web-map-specification/objects/featureReduction_cluster/)|Clusters|N|N|[Y](https://www.arcgis.com/sharing/rest/content/items/8e3fd5a7427b48b3b293c586ff4b2301/data?f=json)|Y
|[`baseMap`](https://developers.arcgis.com/web-map-specification/objects/baseMap/)|Background layers|N|N|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|[`opacity`](https://developers.arcgis.com/web-map-specification/objects/featureLayer/)|Transparency|N|N|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|[`bookmarks`](https://developers.arcgis.com/web-map-specification/objects/bookmark/)|Map locations|N|N|[Y](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json)|Y
|...|...|...|...|...|...

**Notes:**

> 1.- On this table we are using a Feature Layer Item type as an example of Layer Item type because is is one of the layers that support more properties, but each layer supports different properties.<br>
> 2.- When we say custom apps we mean:  [client side API/SDK](#), which includes [Web Mapping Applications type](#) and Configurable Apps.<br>
> 3.- Although the extension is included in the service definition, it is not used by default when loading the layer, as we would have an unexpected behavior when loading multiple layers.<br>
> 4.- The extent saved in the item metadata is used to make the item searchable by location, not to focus the map view on this as an initial extent.<br>
> 5.- **View layer definitions** can only be queried by the owner using the [REST API Admin](https://developers.arcgis.com/rest/services-reference/rest-api-admin.htm). I couldn't find this property in the documentation.

**Important**: 


## Examples using the ArcGIS JavaScript API

### Load a layer with it default properties

[The load layer demo](.feature-layer.html) shows how to load layer properties using the JavaScript API we just need to add the URL of the layer on the `FeatureLayer` class. 

```js
const featureLayer = new FeatureLayer({
    url: 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0'
});

map.add(featureLayer);
```

As mention in the notes under the table, the extent defined in the layer expecification is not used by default, so if we want to set the extent we have to do it manually:

```js
const gotoExtent = async function(){
    // Recover layer extent from the expect
    const getExtent = featureLayer
                        .queryExtent()
                        .then(response => response.extent);

    const mapReady = view.when();

    // Wait until mapview is ready and we have the expect
    Promise.all([getExtent, mapReady]).then(values =>{
        view.goTo(values[0]).catch(function (error) {
            if (error.name != "AbortError") {
                console.error(error);
            }
        });
    })
}
gotoExtent();
```

### Overwrite previous layer properties with Portal Item properties

[The load feature layer item demo](.feature-layer-item.html) shows how [the item properties](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26?f=json) of [a Portal Item](https://www.arcgis.com/home/item.html?id=195e039565ee42fbbefbcc2708bc7e26) which references/point the [previous feature service](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer) will overwrite the properties **on each layer** in the spec of feature service ([0](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/0?f=json), [1](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/1?f=json), [2](https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Poverty_by_Age_Boundaries/FeatureServer/3?f=json)).

The code looks like this:

```js
const layer = Layer.fromPortalItem({
    portalItem: {
        id: "195e039565ee42fbbefbcc2708bc7e26"
    }
})
.then(layer => {
    map.add(layer);
})
.catch(error => {
    console.log("Layer failed to load: ", error);
});
 ```

 The extent saved in the item metadata is used to make the item searchable by location, not as an initial extent, but we could also use it:

 ```js
new PortalItem({
    id: itemID
})
.load()
.then(function(item){
    view.goTo(item.extent);
});
```

### Overwrite previous Portal Item with web map properties

[The load web maps item demo](.webmap-item.html) shows how the [web map item properties](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json) which references the previous [Portal Item](https://www.arcgis.com/home/item.html?id=195e039565ee42fbbefbcc2708bc7e26) will overwrite [its properties](https://www.arcgis.com/sharing/rest/content/items/195e039565ee42fbbefbcc2708bc7e26?f=json).

```js
const webmap = new WebMap({
    portalItem: {
        id: "c1354b360f3d4d709220f134f10b744a"
    }
});

const view = new MapView({
    map: webmap,
    container: "viewDiv"
});
```

### Overwrite previous web map properties with custom code

[The custom app starting from a webmap demo](.custom-app.html) shows how to overwrite the [web map properties](https://www.arcgis.com/sharing/rest/content/items/c1354b360f3d4d709220f134f10b744a/data?f=json) using the properties and methods available in the JavaScript API.

The following sample code shows how to overwrite the extent of the view using the [`extent` property](https://developers.arcgis.com/javascript/latest/api-reference/esri-views-MapView.html#properties-summary) in the [`MapView` class](https://developers.arcgis.com/javascript/latest/api-reference/esri-views-MapView.html):

```js
const webmap = new WebMap({
    portalItem: {
        id: "c1354b360f3d4d709220f134f10b744a"
    }
});

const view = new MapView({
    map: webmap,
    container: "viewDiv",
    extent: {
        "spatialReference": {
            "latestWkid": 3857,
            "wkid": 102100
        },
        "xmin": -8244513.280543869,
        "ymin": 4976904.837374379,
        "xmax": -8224945.401302891,
        "ymax": 4980736.243417169
    }
});
```
