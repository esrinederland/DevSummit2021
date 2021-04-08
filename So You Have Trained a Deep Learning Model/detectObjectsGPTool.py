import arcpy
import arcgis
import json

## Connect to your GIS Portal
portalUrl = "https://pada.ad.local/" + "portal"
gis = arcgis.gis.GIS(url=portalUrl, profile="portalAdmin", verify_cert=False)

## Get geometry from input parameter
inputFC = arcpy.GetParameterAsText(0)

with arcpy.da.SearchCursor(inputFC, ["SHAPE@JSON"]) as sCursor:
    for row in sCursor:
        inputGeometry = row[0]

## Get input raster and clip to geometry
inputRaster = arcgis.raster.ImageryLayer("https://pada.ad.local/server/rest/services/Hosted/Imagery_Heerenveen/ImageServer", gis=gis)
rasterClip = arcgis.raster.functions.clip(inputRaster, json.loads(inputGeometry))
rasterClip.save()

## Get Deep Learning Model
modelObject = gis.content.get("054c037f7c1c47a99561410d5efe7b65")
model = arcgis.learn.Model(modelObject)
model.install()

## Set Model arguments
modelArguments = {
    "padding": 100,
    "batch_size": 4,
    "threshold": 0.9,
    "return_bboxes": False
}
context = {
    "cellSize": 0.3,
    "processorType" : "CPU"
}

## Inferencing
outputFL = arcgis.learn.detect_objects(
    rasterClip, 
    model, 
    model_arguments=modelArguments, 
    run_nms=True, 
    confidence_score_field="Confidence", 
    class_value_field="Class", 
    max_overlap_ratio=0.3, 
    context=context, 
    gis=gis)

## Append new features to existing Feature Service
featureService = arcgis.features.FeatureLayer("https://pada.ad.local/server/rest/services/Hosted/DetectObjects_test2/FeatureServer/0", gis=gis)
result = featureService.edit_features(adds=outputFL.layers[0].query(where="1=1"))

## Delete temp Feature Service
outputFL.delete()


## Set output parameter
stringResult = json.dumps(result)
arcpy.SetParameterAsText(1, stringResult)