import arcgis
import datetime

## Connect to your GIS Portal
gis = arcgis.gis.GIS(url="https://pada.ad.local/portal", profile="portalAdmin", verify_cert=False)

## Get input raster
inputRaster = arcgis.raster.ImageryLayer("https://pada.ad.local/server/rest/services/Hosted/Imagery_Heerenveen/ImageServer", gis=gis)

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

## Get parcel from parcel layer
parcelLayer = arcgis.features.FeatureLayer("https://basisregistraties.arcgisonline.nl/arcgis/rest/services/DKK/DKKv4/FeatureServer/2")

## Create query to select parcel
lastHour = datetime.datetime.now() - datetime.timedelta(hours=1)
query = f"last_edited_date > TIMESTAMP '{lastHour.strftime('%Y-%m-%d %H:%M:%S')}'"
features = parcelLayer.query(where=query, out_sr=3857).features

for feature in features:
    inputGeometry = feature.geometry

    ## Clip raster to geometry
    rasterClip = arcgis.raster.functions.clip(inputRaster, inputGeometry)
    
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
    print(result)

    ## Delete temp Feature Service
    outputFL.delete()