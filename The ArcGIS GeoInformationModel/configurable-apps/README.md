# Configurable Apps

Configurable apps is a mechanism based on the ArcGIS GeoInformation model that allows users of an organization to create and configure web applications without having to write any code.

As we will see, apps can be [created from maps](https://doc.arcgis.com/en/arcgis-online/create-maps/create-map-apps.htm), [from scenes](https://doc.arcgis.com/en/arcgis-online/create-maps/create-scene-apps.htm) and also [from groups](https://doc.arcgis.com/en/arcgis-online/create-maps/create-gallery-apps.htm).

Although Esri provides more than [80 templates](https://www.arcgis.com/home/search.html?q=tags%3AArcGIS%20web%20application%20template%20owner%3Aesri_en&t=content&sortField=modified&sortOrder=desc), any developer [can create its own configurable app](https://doc.arcgis.com/en/arcgis-online/create-maps/create-app-templates.htm) (using **any web technology**), [register it within and organization](https://doc.arcgis.com/en/arcgis-online/create-maps/create-app-templates.htm#ESRI_SECTION1_FBEEDC333D2A4765BA3F807B50AD558A) and enable it so any other member can create application from is them same way as Esri does.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents** 

- [How it works](#how-it-works)
  - [For maps](#for-maps)
  - [For groups](#for-groups)
  - [Internals](#internals)
- [Configurable Apps types](#configurable-apps-types)
  - [Configurables apps](#configurables-apps)
  - [Self configured apps](#self-configured-apps)
- [Utils to develop your own configurable app](#utils-to-develop-your-own-configurable-app)
- [Build and share configurable app templates](#build-and-share-configurable-app-templates)
- [Related sites and talks](#related-sites-and-talks)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## How it works

First we are going to learn how it works from and user/admin point of view.

### For maps

In the following animation (video linked) you can see how to to add a custom template (that consume a web map), configure an organization and create an instance of that template in 12 steps:

[![How to Setup a custom configurable app in ArcGIS](imgs/How-to-Setup-a-custom-configurable-app-in-ArcGIS.gif)](https://youtu.be/k-fRKWWG2I8)

Steps described above:

1. Find or develop a configurable app template
2. Make it accesible from the Internet
3. Login to your account
4. Create the template in our organization
5. Add the configuration parameters
6. Create a group that we will use afterwards
7. Add the new template (item) to this group
8. Configure the organization the use the new group
9. Create the webmap to be used in the intance's template
10. Create the instance of the configurable app
11. Configure de app
12. Save and launch

### For groups

App templates can also be used to display items to build a custom layout, for example to display the items of a group. 

You do this by the group details page of a group you own and then clicking "Create a web app" from the right panel:

![Create configurable app](imgs/create-configurable-app-from-group.png)

**IMPORTANT:** Have in consideration the templates listed when click will read from a different settings located at: [Organization > Settings > **Groups**](https://www.arcgis.com/home/organization.html?tab=groups#settings) (*not Map!*)


![Configure Organization Configurable apps for groups](imgs/configure-organization-configurable-apps-for-groups.png)

Check the [Esri templates for groups](https://www.arcgis.com/home/search.html?q=typekeywords%3A%22Configurable%22%20owner%3Aesri_en%20gallery%20typekeywords%3A%22gallery%22&t=content&sortField=modified&sortOrder=desc)

### Internals

Ok, it is now time to talk about the internals. 

Check these to examples of items and it's data:

|Item|Typekeywords|Data|
|---|---|---|
|[Template](https://www.arcgis.com/home/item.html?id=4d1c59bb91fa4db78c34b1069d35cc3f)|`Web Map`, `Map`, `Online Map`, `Mapping Site`, `JavaScript`, `Configurable`|[configurationSettings](https://hhkaos.maps.arcgis.com/sharing/rest/content/items/4d1c59bb91fa4db78c34b1069d35cc3f/data?f=json)
|[Instance](https://www.arcgis.com/home/item.html?id=dfd3d90e66ed4aa9812cdf8729bf1404)|`Web Map`, `Map`, `Online Map`, `Mapping Site`, `JavaScript`|[instace configurations](https://hhkaos.maps.arcgis.com/sharing/rest/content/items/dfd3d90e66ed4aa9812cdf8729bf1404/data?f=json)

So there are two things:

* The template: where the definition of the configuration parameters and the URL whereo the template is located
* The instance: which is actually the final application that a user has built from the template. With the value of each configuration parameter.

This is simple, right?. 

We have seen an example of one of the two types of configurable apps. Next we will see there is another type called "selfConfigured".

ArcGIS add typekeywords based on the characteristics of a template:

|Template type|Some of the typekeywords included|
|---|---|
|Configurable App for Maps|`Mapping Site`, `JavaScript`, `Configurable`|
|Configurable App for groups|`Mapping Site`, `JavaScript`, `Configurable`, `gallery`|
|Self Configurable App|`Mapping Site`, `JavaScript`, `Configurable`,`selfConfigured`


## Configurable Apps types

From the [Content page](https://www.arcgis.com/home/content.html) in your organization you can click: "Add Item" > "An application" and this will allow you to create two types of configurable apps:

<img src="imgs/configurable-app-types.png" style="width:350px" alt="Configurable apps">

### Configurables apps

This type of configurable apps requires a [configuration file](https://doc.arcgis.com/en/arcgis-online/create-maps/create-app-templates.htm#ESRI_SECTION2_242BA51358AB45879C77C17EE9B1473A) that will be used to define the interface of the [default configuration panel](https://www.arcgis.com/home/webmap/configureApp.html). 

Configuration file (entered throught the template: [item settings](https://hhkaos.maps.arcgis.com/home/item.html?id=4d1c59bb91fa4db78c34b1069d35cc3f#settings) and stored in the [data item](https://hhkaos.maps.arcgis.com/sharing/rest/content/items/4d1c59bb91fa4db78c34b1069d35cc3f/data?f=json)):

![Configuration parameters](imgs/configuration-parameters.png)

Default configuration panel (data is stored in the [data item](https://hhkaos.maps.arcgis.com/sharing/rest/content/items/dfd3d90e66ed4aa9812cdf8729bf1404/data?f=json)):

[![Default configuration panel](imgs/default-configuration-panel.png)](https://hhkaos2.maps.arcgis.com/home/webmap/configureApp.html?appid=dfd3d90e66ed4aa9812cdf8729bf1404)

Example of these type of configurable apps are: Minimalist, Nearby, Interactive Legend, Attachment Viewer, Map Styles, ... [see all](https://www.arcgis.com/home/search.html?q=tags%3AArcGIS%20web%20application%20template%20owner%3Aesri_en%20-typekeywords%3AselfConfigured&t=content&sortField=modified&sortOrder=desc)

### Self configured apps

This type will use a custom configuration panel implemented in the template itself and displayed when the URL contains a parameter `edit=true`:

![Custom configurable panel](imgs/custom-configurable-panel.png)

Example of these type of configurable apps are: Storymaps, GeoForm, Impact Summary, ... ([see all](https://www.arcgis.com/home/search.html?q=tags%3AArcGIS%20web%20application%20template%20owner%3Aesri_en%20typekeywords%3AselfConfigured&t=content&sortField=modified&sortOrder=desc))

## Utils to develop your own configurable app

You can develope a template from scratch of use the project 
[configurable-app-examples-4x-js](https://github.com/Esri/configurable-app-examples-4x-js). It includes configurable application examples using [ApplicationBase](https://github.com/Esri/application-base-js) (a core class for creating a configurable application using JavaScript/TypeScript).


## Build and share configurable app templates

> [Youtube video tour](https://github.com/Geo-Developers/youtube-video-tour): This is an applitacion template for ArcGIS Online which displays a map route and a video at the same time. You can click over the route and the video will synchronize.


## Related sites and talks

* [Awesome list - ArcGIS Configurable Apps](https://esri-es.github.io/awesome-arcgis/arcgis/products/configurable-apps/#apps-developed-by-esri)
* Talks in spanish: 
    * How To: Youtube Video Tour: [Video](https://www.youtube.com/watch?v=l-NJHZlviqE) | [Slides](https://docs.google.com/presentation/d/10TeSrRbQ0wTi4AlRLjxxndxnneAwvHUyVozc53sP4jk/edit#slide=id.g34dccead2_019) (2014)
    * [Aplicaciones Configurables Personalizadas](https://www.youtube.com/watch?v=DIsA6DFf5N0) (2016) 
    * [Desmitificando la personalización de storymaps (extended)](https://www.youtube.com/watch?v=yAWl9ccSbOg) (2017)
