import arcgis

## Connect to your GIS Portal
portalUrl = "https://pada.ad.local/" + "portal"
gis = arcgis.gis.GIS(url=portalUrl, profile="xxx", verify_cert=False, username="xxx", password="xxx")
