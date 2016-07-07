var icon = "M21.25,8.375V28h6.5V8.375H21.25zM12.25,28h6.5V4.125h-6.5V28zM3.25,28h6.5V12.625h-6.5V28z";

AmCharts.makeChart( "mapdiv", {
  /**
   * this tells amCharts it's a map
   */
	"type": "map",
	"theme": "light",
	
	colorSteps: 10,

  /**
   * create data provider object
   * map property is usually the same as the name of the map file.
   * getAreasFromMap indicates that amMap should read all the areas available
   * in the map data and treat them as they are included in your data provider.
   * in case you don't set it to true, all the areas except listed in data
   * provider will be treated as unlisted.
   */
  "dataProvider": {
	"map": "brazilLow",
"getAreasFromMap": true,
	images: [ {
      	"latitude": -22.9035,
      	"longitude": -43.2096,
      	"svgPath": icon,
      	"color": "#CC0000",
     	 	"scale": 0.5,
      	"label": "Rio de Janeiro",
      	"labelShiftY": 2,
   		"zoomLevel": 5,
      	"title": "Rio de Janeiro",
      	"description": "Dilma: X votos <br> Aecio: Y votos <br> Marina: Z votos"
   	 } ]  
	},

  /** 
   * create areas settings
   * autoZoom set to true means that the map will zoom-in when clicked on the area
   * selectedColor indicates color of the clicked area.
   */
	"areasSettings": {
		"autoZoom": true,
		"selectedColor": "#71F67A"
	},

	valueLegend: {
   		 right: 10,
    		minValue: "little",
    		maxValue: "a lot!"
	},

  /**
   * let's say we want a small map to be displayed, so let's create it
   */
	"smallMap": {}
} );