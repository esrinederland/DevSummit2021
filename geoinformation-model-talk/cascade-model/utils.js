let goToLayerExtent = function(){
    featureLayer.queryExtent().then(function (response) {
        console.log(response.extent.toJSON())
        view.goTo(response.extent).catch(function (error) {
        if (error.name != "AbortError") {
            console.error(error);
        }
        });
    })
};
